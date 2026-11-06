# Data Pipelines: Ideas and Technologies to Explore

A long list to spark ideas. Skim it, borrow from it, or go your own way. The project itself is
[Build a Pipeline](build_a_pipeline.md).

## Pipeline ideas

**From the Data Pipeline project** (each has years of history and a live feed):

- EIA hourly electric grid: US electricity demand and generation by fuel type
- USGS earthquakes: worldwide quakes, a live feed that updates every minute (the [demo](https://github.com/byu-cs-452/cs452-pipeline-reference))
- Open-Meteo weather: hourly weather back to 1940 for any city
- NOAA tides and water levels: observed vs. predicted tides every 6 minutes
- Bike share (Citi Bike, Divvy, Capital Bikeshare): trip history plus live station status (challenge)
- Wikimedia: pageview history plus the live edit stream (challenge)

**More ideas** (some would need instructor approval for the project):

- Website or app clickstream: what users do, from server and client logs (how much of industry's data arrives)
- Scrape articles or blog posts, compute embeddings, and load them into a vector database (like the Podcast and RAG projects)
- Public transit in real time: bus and train positions (GTFS-realtime, e.g. UTA)
- Flights overhead: live aircraft positions (OpenSky Network)
- Air quality: EPA AirNow or PurpleAir sensors (Wasatch Front inversions!)
- Snowpack and ski conditions: NRCS SNOTEL stations
- River and stream flows: USGS Water Services
- Stock or crypto prices, sports scores and stats
- Hacker News, Reddit or GitHub activity: posts, comments, events
- Space weather: NASA and NOAA solar flare and geomagnetic data
- Game player counts (Steam) or your own smart-home and fitness devices

## Technologies, by stage

- **Schedule and orchestrate:** Cloud Scheduler + Cloud Run, Azure Functions or Logic Apps, GitHub Actions, cron or
  Task Scheduler, Apache Airflow (AWS runs it for you as Amazon MWAA), Dagster, Prefect, Databricks Lakeflow jobs
- **Process and transform:** Apache Beam (autoscales on Google Dataflow), Apache Spark, dbt, pandas, Polars
- **Buffer and stream:** Google Pub/Sub, Azure Event Hubs, Apache Kafka (or Redpanda)
- **Store and analyze:** BigQuery, Azure Data Explorer (Kusto), ClickHouse, PostgreSQL or TimescaleDB, DuckDB or
  MotherDuck, Databricks Delta tables, Snowflake, pgvector for embeddings
- **File and table formats:** Parquet (columnar files that DuckDB, BigQuery, Spark and pandas all read), Apache
  Iceberg, Delta Lake, Apache Hudi
- **Version your data:** DVC, lakeFS, Iceberg/Delta/Hudi time travel, S3 object versioning
- **Check data quality:** Great Expectations, Soda, dbt tests, AWS Glue Data Quality
- **Data for AI:** feature stores (Feast, SageMaker Feature Store, Databricks), vector stores (pgvector, Pinecone,
  Weaviate)
- **Show it's alive:** Looker Studio (Data Studio), ADX dashboards, Power BI, Grafana, Databricks AI/BI dashboards
- **Tools companies buy:** Matillion, Informatica, AWS Glue, Fivetran, Talend, dbt Cloud

**A bigger idea:** a Beam pipeline that reads raw text from cloud storage, processes the documents, gets embeddings
from an ML model and writes them to Postgres. Because Beam is parallel (MapReduce style), it can autoscale on
Google Dataflow.

## Architecture ideas worth knowing

- OLTP vs. OLAP: the operational database that runs the app vs. the analytical store that answers questions
- Data warehouse, data lake, data lakehouse, and when to choose each over querying an operational database
- Medallion architecture: bronze (raw, as it arrived), silver (cleaned), gold (ready for analysis or ML)
- Data mesh, data fabric, data virtualization
- Change data capture (CDC)
- Feature stores (for machine learning)
- Microservices and event-driven design
- Batch vs. online vs. streaming architectures
- ETL vs. ELT: transform before loading, or load raw data first and transform inside the store (ELT is the usual
  approach for AI systems)
- Data engineering for AI: training and evaluation data, feature stores, vector stores
- Data as a product, DataOps, data contracts (a producer's promise about schema, meaning and quality)
- Data quality: what to check, and whether a failed check stops the pipeline, quarantines the bad rows or just
  alerts
- Data versioning and reproducibility: knowing exactly which data a report or model was built from

*Thanks to Scott Toborg (Engineering the AI Enterprise) for suggestions on this list.*
