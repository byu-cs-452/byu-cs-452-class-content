"""Every few seconds, find abandoned jobs and put them back on the queue.   python reaper.py"""
import time

import reliable_queue as rq

r = rq.connect()
print(f"reaper: checking {rq.PROCESSING} every 2s (lease {rq.LEASE_SECONDS}s, max {rq.MAX_ATTEMPTS} attempts)")
while True:
    for jid, what in rq.reap(r):
        print(f"reaper: {jid[:8]} {what}")
    print("reaper:", rq.counts(r))
    time.sleep(2)
