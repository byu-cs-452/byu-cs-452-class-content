"""A reliable work queue on Redis lists: claim -> process -> acknowledge, plus a reaper.

Keys:
  jobs:queue       list   jobs waiting for a worker
  jobs:processing  list   jobs a worker has claimed but not finished
  jobs:claims      hash   job id -> {"worker": name, "at": unix time of the claim or last heartbeat}
  jobs:attempts    hash   job id -> how many times it has been handed to a worker
  jobs:dead        list   jobs that failed MAX_ATTEMPTS times (a "dead letter" list for a human to look at)
"""
import json
import os
import time
import uuid

import redis

QUEUE = "jobs:queue"
PROCESSING = "jobs:processing"
CLAIMS = "jobs:claims"
ATTEMPTS = "jobs:attempts"
DEAD = "jobs:dead"

LEASE_SECONDS = 10   # a claim older than this (with no heartbeat) is treated as abandoned
MAX_ATTEMPTS = 3     # after this many tries, stop retrying and move the job to jobs:dead


def connect():
    # e.g. set REDIS_URL=redis://default:<password>@<host>:<port>/0 for a redis.io database
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(url, decode_responses=True)


def job_id(job):
    return json.loads(job)["id"]


def enqueue(r, payload):
    job = json.dumps({"id": str(uuid.uuid4()), "payload": payload})
    r.rpush(QUEUE, job)
    return job


def claim(r, worker, timeout=5):
    """Move one job from the queue to the processing list in ONE atomic step.

    BLMOVE (LMOVE that waits) is the key idea: the job is never "in the air." It is always in
    exactly one of the two lists, so if this worker dies, the job is still sitting in jobs:processing.
    """
    job = r.blmove(QUEUE, PROCESSING, timeout, "LEFT", "RIGHT")
    if job is None:
        return None
    jid = job_id(job)
    # If the worker dies between BLMOVE and this HSET, the reaper still finds the job (see reap()).
    r.hset(CLAIMS, jid, json.dumps({"worker": worker, "at": time.time()}))
    r.hincrby(ATTEMPTS, jid, 1)
    return job


def heartbeat(r, job, worker):
    """Call during long work so the reaper knows this worker is still alive."""
    r.hset(CLAIMS, job_id(job), json.dumps({"worker": worker, "at": time.time()}))


def ack(r, job):
    """The work is done and its result is saved: forget the job."""
    jid = job_id(job)
    with r.pipeline() as p:   # MULTI ... EXEC, so all three happen together
        p.lrem(PROCESSING, 1, job)
        p.hdel(CLAIMS, jid)
        p.hdel(ATTEMPTS, jid)
        p.execute()


# Runs inside Redis, so nothing can happen between the check and the requeue.
# If LREM removes nothing, the worker acked the job a moment ago: leave it alone.
REQUEUE_LUA = """
if redis.call('LREM', KEYS[1], 1, ARGV[1]) == 0 then return 0 end
redis.call('HDEL', KEYS[3], ARGV[2])
local tries = tonumber(redis.call('HGET', KEYS[5], ARGV[2]) or '0')
if tries >= tonumber(ARGV[3]) then
  redis.call('RPUSH', KEYS[4], ARGV[1])
  redis.call('HDEL', KEYS[5], ARGV[2])
  return 2
end
redis.call('LPUSH', KEYS[2], ARGV[1])
return 1
"""


def reap(r, now=None):
    """Find abandoned jobs in the processing list and put them back at the front of the queue.

    Returns a list of (job id, what happened) for printing.
    """
    now = now or time.time()
    requeue = r.register_script(REQUEUE_LUA)
    actions = []
    for job in r.lrange(PROCESSING, 0, -1):
        jid = job_id(job)
        c = r.hget(CLAIMS, jid)
        if c is None:
            # Claimed, but the worker died before it wrote its claim. Start the clock now.
            r.hsetnx(CLAIMS, jid, json.dumps({"worker": "?", "at": now}))
            continue
        c = json.loads(c)
        if now - c["at"] < LEASE_SECONDS:
            continue
        result = requeue(keys=[PROCESSING, QUEUE, CLAIMS, DEAD, ATTEMPTS], args=[job, jid, MAX_ATTEMPTS])
        if result == 1:
            actions.append((jid, f"requeued (worker {c['worker']} went quiet {now - c['at']:.0f}s ago)"))
        elif result == 2:
            actions.append((jid, f"moved to {DEAD} after {MAX_ATTEMPTS} attempts"))
    return actions


def counts(r):
    return {"queue": r.llen(QUEUE), "processing": r.llen(PROCESSING), "dead": r.llen(DEAD),
            "results": len(r.keys("result:*"))}
