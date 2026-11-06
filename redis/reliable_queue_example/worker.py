"""A worker that sometimes dies in the middle of a job, on purpose.

python worker.py --name w1 --crash-chance 0.3
"""
import argparse
import json
import os
import random
import time

import reliable_queue as rq

ap = argparse.ArgumentParser()
ap.add_argument("--name", default=f"worker-{os.getpid()}")
ap.add_argument("--crash-chance", type=float, default=0.25, help="chance of dying mid-job (0 to 1)")
ap.add_argument("--work-seconds", type=float, default=2.0)
a = ap.parse_args()

r = rq.connect()
print(f"{a.name}: waiting for jobs")
while True:
    job = rq.claim(r, a.name)
    if job is None:
        continue
    j = json.loads(job)
    print(f"{a.name}: claimed {j['id'][:8]} ({j['payload']['image']})")

    # The "model": in the real project this is model.predict(batch).
    for _ in range(int(a.work_seconds * 2)):
        time.sleep(0.5)
        if random.random() < a.crash_chance / (a.work_seconds * 2):
            print(f"{a.name}: CRASH while working on {j['id'][:8]}. The job is still in {rq.PROCESSING}.")
            os._exit(1)   # die without cleaning up, like a killed process or a lost machine
        rq.heartbeat(r, job, a.name)

    r.set(f"result:{j['id']}", json.dumps({"label": "castle", "by": a.name}))   # save the result first...
    rq.ack(r, job)                                                               # ...then acknowledge
    print(f"{a.name}: done {j['id'][:8]}")
