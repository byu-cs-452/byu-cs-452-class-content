"""Every few seconds, find abandoned jobs and put them back on the queue.   python restorer.py"""
import time

import reliable_queue as rq

r = rq.connect()
print(f"restorer: checking {rq.PROCESSING} every 2s (lease {rq.LEASE_SECONDS}s, max {rq.MAX_ATTEMPTS} attempts)")
while True:
    for jid, what in rq.restore(r):
        print(f"restorer: {jid[:8]} {what}")
    print("restorer:", rq.counts(r))
    time.sleep(2)
