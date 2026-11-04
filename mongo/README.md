# Mongo Learning Plan

> **Background reading:** [MongoDB in the Real World](RealWorldUses.md) — five companies using MongoDB in production, what for, and why.

## Mongo Activity (in class): Steps 1–3

Hand in one PDF with your code and results for Step 2 and Step 3. AI use: [Level 2 (Reviewer)](https://cs.byu.edu/department/ai-policy).

- [Step 1](Step1.ipynb)  (CRUD) (In Class - Together 15 min)

  - Using a sandbox environment create, read, update, delete documents. Query documents that other students are creating at the same time.

- [Step 2](Step2.ipynb) (Simple Query Operators) (In Class - In groups or alone (10 min), turn-in)

  - Using a provided connection to MongoDb query a movies dataset. Practice your skills with simple query operators.

- [Step 3](Step3.ipynb) (Aggregations on Data) (In Class - together, then the exercises, turn-in)

  - Using the same movies dataset learn to do simple group by operations and projections (unwind, named columns, and math).

## Mongo Project (optional extra credit): Steps 4–5

Learning objectives:

- **Understand the data** before you query it: what one row means, which numbers are running totals and which are
  daily, where the state totals hide in the county data.
- **Get fluent with aggregation pipelines:** chain `$match`, `$group`, `$project`, `$sort`, `$lookup` and `$out` to
  build an answer one stage at a time.
- **See how real data is messy:** the three datasets don't list states the same way, so the join by state isn't
  clean. Find out why and decide what to do about it.

Steps:

- [Step 4](Step4.md) (Create your own Atlas MongoDB Deployment)

  - Create a free account on Atlas and connect to it!

- [Step 5](Step5.ipynb) (Answer questions using data by performing queries, aggregations, and joins)

  - Redo Covid information SparkSQL/Kusto lab using MongoDB. Answer new questions by including vaccination and population data.

Hand in a .pdf or .ipynb with your code and results, labeled by question. Keep your Atlas password out of what you
hand in (an environment variable or Colab secret works).
