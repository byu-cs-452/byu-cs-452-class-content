# MongoDB in the Real World

Five documented examples of organizations running MongoDB in production. Most details come from MongoDB's own customer stories or partner blogs, so treat performance numbers as vendor-reported.

| Organization | What they use it for | Why MongoDB |
|---|---|---|
| **Toyota Connected North America** | Telemetry platform behind Toyota's Safety Connect service in 9+ million Toyota and Lexus vehicles. When sensors detect a crash or the driver presses SOS, the car sends telemetry and location data to a safety agent. | After reliability problems with a legacy database, they moved to AWS and MongoDB Atlas. The platform runs on 20+ Atlas databases behind microservices and reports 99.99% availability, with maintenance and upgrades done without downtime. |
| **Coinbase** (crypto exchange) | Built on MongoDB since launching in 2012; it backs core parts of the trading platform. | Crypto traffic is extremely spiky. Coinbase built a machine learning model that predicts traffic surges and triggers parallel cluster scaling in Atlas, reporting a 60% reduction in scaling time. |
| **Bosch** (IoT) | The Bosch IoT Suite covers 250+ IoT projects and 10+ million connected devices. In Bosch IoT Insights, raw input sits in object storage and processed data is stored in MongoDB. | Stores, manages, and analyzes varied, high-volume device data in real time, which suits a flexible document model. |
| **Forbes** (media) | Content management system and digital products; a MongoDB customer since 2011. | Moved from self-managed MongoDB to Atlas on Google Cloud so the team could stop managing databases. Reported release cycles 2x–10x faster and 25% lower total cost of ownership. |
| **Novo Nordisk** (pharma) | Generative AI pipeline for regulatory documents, cutting Clinical Study Report production from 12 weeks to 10 minutes. | Atlas keeps source data and vector embeddings together for retrieval-augmented generation (RAG). |

## Patterns to notice

These map onto MongoDB's most common use cases:

- **High-volume telemetry / IoT** — Toyota, Bosch
- **Scaling under unpredictable load** — Coinbase
- **Flexible content** — Forbes
- **AI and vector search** — Novo Nordisk

Large companies rarely use only one database. Coinbase's own job postings list MongoDB alongside Postgres, Aurora, DynamoDB, and Redis. Knowing when to pick a document database versus a relational one is the valuable skill.

## Sources

- [MongoDB Atlas transforms Toyota Safety Connect (KMWorld)](https://www.kmworld.com/Articles/News/KM-In-Practice/MongoDB-Atlas-transforms-Toyota-Safety-Connect-165968.aspx)
- [Toyota Connected case study (MongoDB)](https://www.mongodb.com/solutions/customer-case-studies/toyota-connected)
- [Coinbase case study (MongoDB)](https://www.mongodb.com/solutions/customer-case-studies/coinbase)
- [Coinbase powered by MongoDB (Percona)](https://www.percona.com/blog/2018/08/10/this-week-in-data-with-colin-charles-48-coinbase-powered-by-mongodb-and-prometheus-graduates-in-the-cncf/)
- [Coinbase datastores job posting (Built In)](https://builtin.com/job/senior-software-engineer-infrastructure-platform-datastores/6952477)
- [Three major IoT data challenges (MongoDB blog)](https://mongodb.com/blog/post/three-major-iot-data-related-challenges-how-address-them)
- [Bosch IoT Insights: data storage](https://atms.trelleborg-tires.com/static-contents/docu/html/Data-storage.html)
- [Forbes migrates to MongoDB Atlas (Google Cloud blog)](https://cloud.google.com/blog/products/databases/forbes-migrates-to-mongodb-atlas-on-google-cloud)
- [Forbes customer story (MongoDB)](https://mongodb.com/customers/forbes)
- [Customer successes, March 2025 (MongoDB blog)](https://mongodb.com/blog/post/innovating-with-mongodb-customer-successes-march-2025)
