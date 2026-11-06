# Redis animations

Open these through GitHub Pages so the animations run:

| Page | What it shows |
|---|---|
| [Polling vs. Notifications](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/polling_vs_notifications.html) | The work queue project step by step: polling, the second-worker bug, notifications + atomic pop, scaling |
| [Pooling Redis Subscribers](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/subscriber_pooling.html) | One subscriber connection per request vs. one per process, how the pool routes answers, Redis and OS connection limits (Linux, Windows, macOS) |
| [Reliable Redis Queue](https://byu-cs-452.github.io/byu-cs-452-class-content/redis/media/reliable_queue.html) | Claim with LMOVE into a processing list, acknowledge after saving, and a reaper that requeues jobs from crashed workers (code in `../reliable_queue_example`) |
