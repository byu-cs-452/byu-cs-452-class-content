# Redis animations

Open these through GitHub Pages so the animations run:

| Page | What it shows |
|---|---|
| [Polling vs. Notifications](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/polling_vs_notifications.html) | The work queue project step by step: polling, the second-worker bug, notifications + atomic pop, scaling |
| [Pooling Redis Subscribers](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/subscriber_pooling.html) | One subscriber connection per request vs. one per process, how the pool routes answers, Redis and OS connection limits (Linux, Windows, macOS) |
| [Reliable Redis Queue](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/reliable_queue.html) | Claim with LMOVE into a processing list, acknowledge after saving, and a restorer that requeues jobs from crashed workers (code in `../reliable_queue_example`) |
| [Listening and Security](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/listening_and_security.html) | Network, TLS, AUTH, ACLs, limits and validation: which layer stops each kind of bad message, in the class setup vs. production |
| [Stress Testing the Queue](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/stress_testing.html) | What `stress_test.py` really measures, an interactive bottleneck calculator for this pipeline, removing local bottlenecks, and Locust/k6 load tests |
| [How Redis Scales](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/how_redis_scales.html) | Scale up first (and why exact clustering percentages aren't published), a live CRC16 hash-slot calculator with `{tag}` keys, a cluster simulator (add/remove/crash nodes, hot key), MOVED vs. ASK, what Redis does and doesn't balance, slots vs. a consistent-hashing ring |
