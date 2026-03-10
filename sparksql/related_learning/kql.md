# KQL (Kusto Query Language) — Quick Start

> **Why is this in the SparkSQL folder?** KQL and SparkSQL solve the same problem — querying big data — but with different syntax and ecosystems. SparkSQL uses SQL on Hadoop/Spark clusters; KQL uses a pipe-forward syntax on Azure Data Explorer (ADX). Seeing both helps you recognize that the *concepts* (filter → aggregate → project) are universal even when the language changes.

---

## 1 — Get Started (≈ 2 minutes)

1. Open **[Azure Data Explorer](https://dataexplorer.azure.com/)** — sign in with your **byu.edu** Microsoft account.
2. Click **"My Cluster" → Create free cluster** (no credit card needed, lasts 1 year).
3. On the home page click **"Explore sample data with KQL"** — this adds the `help` cluster with a **Samples** database containing ready-made tables like `StormEvents`.

> **Can I save my queries?** Yes — ADX now supports **Saved Queries** in the web UI. You can also download any query as a `.kql` file or share a link. That said, all the queries you need for class are right here.

---

## 2 — KQL Basics (the pipe model)

KQL reads left-to-right, top-to-bottom. Each line pipes (`|`) the previous result into the next operator.

```kql
StormEvents                        // start with a table
| where State == "TEXAS"           // filter rows
| summarize Count = count() by EventType   // group & aggregate
| order by Count desc              // sort
| take 10                          // limit rows
```

That's the whole pattern: **Table → filter → aggregate → sort → limit**.

---

## 3 — Storm Events 🌪️

All queries below run against `StormEvents` in the `help` cluster → `Samples` database (already connected if you did step 1.3).

### Deadliest event types
```kql
StormEvents
| summarize Deaths = sum(DeathsDirect + DeathsIndirect) by EventType
| order by Deaths desc
| take 10
```

### Property damage by state
```kql
StormEvents
| summarize Damage = sum(DamageProperty) by State
| order by Damage desc
| take 10
```

### Storm events on a map 🗺️
```kql
StormEvents
| where BeginLat != 0 and BeginLon != 0
| project BeginLon, BeginLat, EventType, State
| take 500
| render scatterchart with (kind=map)
```
> **Try it:** Run this and click the map icon. You'll see storm locations plotted geographically.

### Events over time (timechart)
```kql
StormEvents
| summarize Count = count() by bin(StartTime, 7d)
| render timechart
```

---

## 4 — NYC Taxi Data 🚕

The `help` cluster also has a `nyc_taxi` database. Connect to it:

**Cluster:** `help.kusto.windows.net` → **Database:** `nyc_taxi`

### Biggest tip ever
```kql
Trips
| order by tip_amount desc
| take 1
| project vendor_id, pickup_datetime, trip_distance, fare_amount, tip_amount, total_amount
```

### Average fare by passenger count
```kql
Trips
| where passenger_count between (1 .. 6)
| summarize AvgFare = avg(fare_amount), AvgTip = avg(tip_amount), Rides = count()
        by passenger_count
| order by passenger_count asc
```

### Rides per hour of day
```kql
Trips
| extend Hour = hourofday(pickup_datetime)
| summarize Rides = count() by Hour
| order by Hour asc
| render columnchart
```

---

## 5 — Book of Mormon & Bible Word Analysis 📖

These queries use `externaldata` to pull texts directly from the internet — no ingestion needed.

### Load the texts
```kql
let BookOfMormon =
    externaldata (Line: string)
    ["https://ia601205.us.archive.org/18/items/thebookofmormon00017gut/mormon13.txt"]
    with (format="txt");
let Bible =
    externaldata (Line: string)
    ["https://www.gutenberg.org/cache/epub/10/pg10.txt"]
    with (format="txt");
```

### Top words in the Book of Mormon
```kql
let BookOfMormon =
    externaldata (Line: string)
    ["https://ia601205.us.archive.org/18/items/thebookofmormon00017gut/mormon13.txt"]
    with (format="txt");
BookOfMormon
| extend Words = extract_all(@"([a-zA-Z]+)", Line)
| mv-expand Word = Words to typeof(string)
| extend Word = tolower(Word)
| where strlen(Word) > 2
| summarize Count = count() by Word
| order by Count desc
| take 25
```

### Words unique to the Book of Mormon (not in the Bible)
```kql
let BookOfMormon =
    externaldata (Line: string)
    ["https://ia601205.us.archive.org/18/items/thebookofmormon00017gut/mormon13.txt"]
    with (format="txt");
let Bible =
    externaldata (Line: string)
    ["https://www.gutenberg.org/cache/epub/10/pg10.txt"]
    with (format="txt");
let BomWords =
    BookOfMormon
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
let BibleWords =
    Bible
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
BomWords
| join kind=leftanti BibleWords on Word
| take 50
```

### Words unique to the Bible (not in the Book of Mormon)
```kql
let BookOfMormon =
    externaldata (Line: string)
    ["https://ia601205.us.archive.org/18/items/thebookofmormon00017gut/mormon13.txt"]
    with (format="txt");
let Bible =
    externaldata (Line: string)
    ["https://www.gutenberg.org/cache/epub/10/pg10.txt"]
    with (format="txt");
let BomWords =
    BookOfMormon
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
let BibleWords =
    Bible
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
BibleWords
| join kind=leftanti BomWords on Word
| take 50
```

### Words shared by BOTH books
```kql
let BookOfMormon =
    externaldata (Line: string)
    ["https://ia601205.us.archive.org/18/items/thebookofmormon00017gut/mormon13.txt"]
    with (format="txt");
let Bible =
    externaldata (Line: string)
    ["https://www.gutenberg.org/cache/epub/10/pg10.txt"]
    with (format="txt");
let BomWords =
    BookOfMormon
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
let BibleWords =
    Bible
    | extend Words = extract_all(@"([a-zA-Z]+)", Line)
    | mv-expand Word = Words to typeof(string)
    | extend Word = tolower(Word)
    | where strlen(Word) > 2
    | distinct Word;
BomWords
| join kind=inner BibleWords on Word
| project Word
| take 50
```

---

## 6 — COVID Data (NY Times) 🦠

Same dataset from the SparkSQL COVID notebook, queried with KQL via `externaldata`.

### Load the data
```kql
let Covid =
    externaldata (['date']: datetime, county: string, state: string, fips: string, cases: long, deaths: long)
    ["https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"]
    with (format="csv", ignoreFirstRecord=true);
```

### County with the most deaths
```kql
let Covid =
    externaldata (['date']: datetime, county: string, state: string, fips: string, cases: long, deaths: long)
    ["https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"]
    with (format="csv", ignoreFirstRecord=true);
Covid
| order by deaths desc
| take 1
| project county, state, deaths
```

### Total deaths by state
```kql
let Covid =
    externaldata (['date']: datetime, county: string, state: string, fips: string, cases: long, deaths: long)
    ["https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"]
    with (format="csv", ignoreFirstRecord=true);
Covid
| summarize MaxDeaths = max(deaths) by county, state
| summarize TotalDeaths = sum(MaxDeaths) by state
| order by TotalDeaths desc
| take 10
```

### Death rate by state
```kql
let Covid =
    externaldata (['date']: datetime, county: string, state: string, fips: string, cases: long, deaths: long)
    ["https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"]
    with (format="csv", ignoreFirstRecord=true);
Covid
| summarize MaxCases = max(cases), MaxDeaths = max(deaths) by county, state
| summarize Cases = sum(MaxCases), Deaths = sum(MaxDeaths) by state
| extend DeathRate = round(100.0 * Deaths / Cases, 2)
| order by DeathRate desc
| take 10
```

---

## KQL vs SparkSQL Cheat Sheet

| Concept | SparkSQL | KQL |
|---|---|---|
| Select columns | `SELECT col1, col2` | `\| project col1, col2` |
| Filter rows | `WHERE x > 5` | `\| where x > 5` |
| Aggregate | `GROUP BY x` | `\| summarize ... by x` |
| Sort | `ORDER BY x DESC` | `\| order by x desc` |
| Limit | `LIMIT 10` | `\| take 10` |
| Count | `COUNT(*)` | `count()` |
| Distinct | `SELECT DISTINCT` | `\| distinct` |
| Set difference | `EXCEPT` | `\| join kind=leftanti` |
| Read external file | `spark.read.csv(url)` | `externaldata (...) [url]` |
