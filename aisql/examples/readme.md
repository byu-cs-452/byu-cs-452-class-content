# Example AI SQL Database

## Description
This example represents the mock data to manage an upcoming dogshow. 

## Overview of the Files
* **db_bot.py**: This is the main script that initializes the database, manages the prompting strategies and sends the questions to OpenAI.
* **setup.sql**: Contains the information to setup the tables and structure of the database.
* **setupData.sql**: Contains the mock information that fills the tables in the database.
* **config.json**: Contains the OpenAI API Key. **Note: Don't share or commit yours.**
* **responses_\<strategy>_\<time>.json**: The output logs that record the provided prompts and questions, as well as the generated SQL queries and natural language responses.

## Prompting Strategies Used
This project attempts to try out the three strategies “zero-shot, single-domain, and cross-domain” as outlined in this paper: https://arxiv.org/abs/2305.11853 <- read it 😊
