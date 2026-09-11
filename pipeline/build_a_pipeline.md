# Data Pipeline Project — Stage Options

Build a pipeline that (1) bulk-loads a large historical dataset and (2) automatically ingests new data from the same source on a regular cadence. The cadence is your call — hourly batch pulls are the well-trodden path, but faster, slower-but-justified, or full streaming are all fair game. The only hard rule: the stream can't be dead. Your pipeline must be visibly alive, with new data arriving on its own, no human pushing the button. You'll make a choice at each stage — your demo video is where you explain why.

**Heads up:** a separate follow-up assignment checks whether your pipeline is *still* running one week later. Build like something that has to survive unattended, because it does.

## Stage 1: Data source

Pick one. Each has millions of rows of history *and* a live feed that updates hourly or faster.

**Schema-Consistent Options** (seed and hourly data share a schema — one table, clean append):

- **EIA Hourly Electric Grid Monitor** — hourly US electricity demand, generation by fuel type, and interchange for 66 balancing authorities, back to mid-2015. Free instant API key; same endpoint serves history and the latest hour. Tens of millions of rows if you take multiple regions/series.
- **USGS Earthquakes** — worldwide seismic events, ~3–4M in the full catalog, no API key. Live GeoJSON feed updates every minute; the FDSN API pages through decades of history (20k events/request — you'll write a pagination loop).
- **Open-Meteo Weather** — hourly weather back to 1940 via the historical archive API, live current conditions via the forecast API, no key. Scale your seed by choosing more cities/variables; each team picks its own set.
- **NOAA CO-OPS Tides & Water Levels** — coastal water levels every 6 minutes, decades of hourly history per station, no key. Includes *predicted* tides alongside observed, enabling residual analysis (observed − predicted).

**Challenge Options** 🏗️ (bigger and messier — the historical data and the live feed have *different schemas*, so you'll design a multi-table model and a join strategy):

- **Bike share (Citi Bike / Divvy / Capital Bikeshare)** — history is monthly trip-record CSVs (Citi Bike alone: 100M+ trips since 2013); live is the GBFS station-status JSON updating every minute. Trips and station availability are different entities joined on station — model both.
- **Wikimedia** — history is monthly pageview dumps (hundreds of millions of rows); live is the edit stream. Pageviews and edits are different entities joined on article/page. Note the live side is a continuous firehose (SSE), which a scheduled batch job can't literally consume — acceptable designs: poll the RecentChanges REST API for a recent window each run (simplest), capture a short SSE sample each run, or run a true always-on consumer feeding a buffer (hardest, most impressive — see Stages 2–3).

Choosing a challenge option earns the extra-credit tier. Any other source with real history + an hourly-or-faster feed may be used with instructor approval.

## Stage 2: Ingestion compute (keeps the data flowing)

Pick your cadence first, then the tool. Scheduled batch (e.g., hourly) is the standard, well-documented path. Continuous/streaming ingestion — an always-on consumer rather than a scheduled job — is more challenging and totally fine; it pairs naturally with Stage 3.

- *Azure:* Function with a timer trigger, or Logic Apps
- *Google:* Cloud Scheduler triggering a Cloud Run function or scheduled Cloud Run job
- *Apache/open-source:* Airflow run locally (`airflow standalone` or Docker), or cron/Task Scheduler in a container on your own machine
- *Wildcard:* GitHub Actions scheduled workflow (free for public repos, version-controlled, runs even when your laptop sleeps)
- *Databricks:* a scheduled Lakeflow job in **Databricks Free Edition** (serverless, quota-limited, no credit card). Note: choosing Databricks here effectively chooses it for Stages 4–5 too — see the platform note below.

Note: the historical seed is a separate, one-time bulk load — expect to use a different tool for it (bulk load utility, not your hourly function). Explain both paths in your writeup. **Seeding etiquette:** pull the historical data *once*, save the raw files locally, and bulk-load from your saved copy. These are free public services; a class re-downloading decades of data on repeat is how nice things go away — and your own iteration loop will be 100× faster from disk anyway.

## Stage 3 (optional / production-realism tier): Buffer or streaming layer

- *Azure:* Event Hubs (⚠️ billed hourly, ~$0.50–0.75 for a two-day project — **delete the namespace when done**)
- *Google:* Pub/Sub (free at this volume)
- *Apache:* Kafka via Redpanda or similar in Docker, locally

Direct writes to the database are perfectly acceptable at this volume; this stage exists to practice decoupling ingestion from storage. (If you chose Wikimedia's push-based stream, a buffer stops being optional-flavored and starts making real sense.)

## Stage 4: Analytical store

- *Azure:* ADX free personal cluster — no Azure subscription or credit card required; ~100 GB uncompressed capacity (20 GB compressed); one-year trial that may auto-renew; full KQL. Create it at [dataexplorer.azure.com](https://dataexplorer.azure.com) ("My Cluster"), **not** a paid cluster through the Azure portal.
- *Google:* BigQuery sandbox (10 GB storage, 1 TB queries/month free)
- *Open-source:* ClickHouse or PostgreSQL/TimescaleDB in Docker, locally — or **DuckDB**, a zero-setup single binary that can bulk-load 100M rows on a laptop in minutes and query parquet files directly. DuckDB is the fastest path from download to first query in this entire matrix, and it's rapidly becoming a standard tool in industry. (MotherDuck, its cloud service, has a free tier if you want it hosted.)
- *Databricks:* Delta tables queried through the SQL editor or notebooks in Free Edition — the "lakehouse" pattern, and the same platform can also run your ingestion (Stage 2) and dashboards (Stage 5).

All schema-consistent seeds fit every store. A maximal challenge-option seed (full Citi Bike history, multiple months of pageview dumps) can exceed BigQuery's sandbox cap or ADX's compressed limit — check your math, or trim the seed. That's a real capacity-planning decision; document it.

## Stage 5: Prove it's alive

- *Azure:* ADX dashboards or Power BI
- *Google:* Looker Studio
- *Open:* Grafana (works against everything above)
- *Databricks:* built-in AI/BI dashboards on your Delta tables

Show your data growing on its own: a chart or query demonstrating new data arriving across multiple unattended runs, plus (recommended demo material) a query that joins the live trickle to the historical seed — e.g., "how does today compare to the 10-year average?" How you demonstrate liveness is up to you; just make it convincing.

## Requirements regardless of path

1. **Idempotency** — your job will re-fetch overlapping data (feeds return windows, not deltas). Show your dedup strategy: unique IDs, upserts, `arg_max` materialized views, whatever fits your store.
2. **Gaps and failure handling** — expect a gap between where your seed ends and your trickle begins: most sources publish historical data with a lag (Open-Meteo's archive trails by several days; EIA data arrives hours late). Some runs will fetch nothing new — that's normal, not a bug. Document how you handle the seed/trickle gap and what happens when the API is down at 3 a.m. (skipped run or backfill? why?).
3. **Secrets management** — API keys and connection strings must never appear in your repo. Use your platform's secret store (GitHub Actions secrets, environment variables, Key Vault, etc.). A committed credential costs points even if the repo is private, because it will one day not be.
4. **Cost accounting** — report actual spend from your billing console (expected: $0, or <$1 with Event Hubs) and explain it. Keep billable resources running only as long as the follow-up assignment needs them, then delete them.

## Deliverables

1. **Architecture sketch** — a simple diagram of what you built: boxes, arrows, and the named technology at each stage. Hand-drawn is fine; clarity beats polish.
2. **30-second demo video** — walk through your pipeline and show it alive (fresh data that arrived without you touching anything).

**Follow-up assignment (separate, one week later):** another 30-second video checking on your pipeline. Full credit whether it's still running or has caught fire — you just need to document what happened and why. Dead pipelines with good post-mortems are worth as much as living ones. (This is why Requirement 4 says *keep* your resources up until then.)

## The Databricks path: one platform vs. composed parts

**Databricks** is one of the most widely used data platforms in industry, built on Apache Spark around a "lakehouse" architecture. Its **Free Edition** (which replaced the old Community Edition in 2025) is a durable, no-cost, serverless workspace — no credit card, no expiring trial — that can cover your entire pipeline: scheduled ingestion jobs (Stage 2), Delta table storage and SQL (Stage 4), and dashboards (Stage 5), all in one place.

That integration is exactly what makes it worth reflecting on. If you choose Databricks, your writeup must address the tradeoff: what did the all-in-one platform give you (less glue code, fewer credentials, one UI) and what did it take away (less visibility into the seams, vendor coupling, quota limits you don't control)? Students composing their pipeline from separate parts should be able to point at each seam; Databricks students should be able to explain what's hidden inside theirs. Both are legitimate architectures — knowing when to pick which is the actual lesson.

Practical caveats for Free Edition: it's serverless-only and quota-limited, supports Python and SQL (no Scala), and quotas are enforced — check that your seed size fits before committing.

## A note on Snowflake

**Snowflake** is the other name you'll see constantly in data engineering job postings — a cloud data warehouse in the same family as BigQuery and ADX. We skip it here only because it offers a 30-day trial rather than a durable free tier. Everything transfers: Snowflake will feel familiar after BigQuery, and "I built this same pipeline on BigQuery/ClickHouse" is a credible answer when a recruiter asks.
