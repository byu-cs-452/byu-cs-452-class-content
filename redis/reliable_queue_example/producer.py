"""Put N jobs on the queue.   python producer.py 20"""
import sys

import reliable_queue as rq

r = rq.connect()
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for i in range(n):
    rq.enqueue(r, {"image": f"photo_{i:03}.jpg"})
print(f"queued {n} jobs ->", rq.counts(r))
