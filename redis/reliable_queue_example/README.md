# Reliable queue example: claim, work, acknowledge, reap

A tiny version of the work queue that survives worker crashes. No TensorFlow needed: the "model" is a sleep,
and the worker crashes on purpose. Animated walkthrough:
[Reliable Redis Queue](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/reliable_queue.html).

| File | What it does |
|---|---|
| `reliable_queue.py` | `enqueue`, `claim` (BLMOVE queue → processing + a claim), `heartbeat`, `ack`, `reap` |
| `producer.py` | Queues N jobs |
| `worker.py` | Claims jobs and sometimes dies mid-job (`--crash-chance`) |
| `reaper.py` | Every 2 s, requeues jobs whose claim is older than the lease; after 3 tries, moves them to `jobs:dead` |

## Run it

```
pip install redis
set REDIS_URL=redis://default:<password>@<host>:<port>/0      (Windows; on macOS/Linux use export)
python reaper.py                      # terminal 1
python worker.py --name w1            # terminal 2 (restart it when it crashes)
python worker.py --name w2            # terminal 3
python producer.py 20                 # terminal 4
```

Watch the reaper's counts: every job ends up in `result:<id>` or, after crashing workers 3 times, in `jobs:dead`.
Nothing gets stuck in `jobs:processing`.

## The ideas

- **Never let a job be "in the air."** `BLMOVE` moves it from the queue to the processing list in one atomic step.
- **Save, then acknowledge.** The worker writes the result, then removes the job from the processing list.
- **A lease.** A claim records who took the job and when. A claim older than `LEASE_SECONDS` (with no heartbeat)
  means the worker is probably dead.
- **The reaper** requeues abandoned jobs with a Lua script, so the check and the move happen atomically.
- **At-least-once.** A slow worker can lose its lease and the job runs twice, so the work must be safe to repeat
  (`SET result:<id>` is).
- **Dead letters.** A job that keeps crashing workers stops being retried and waits for a human.

Redis Streams (`XREADGROUP`, `XACK`, `XPENDING`, `XAUTOCLAIM`) build the same thing into Redis.
