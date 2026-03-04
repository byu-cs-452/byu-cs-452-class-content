# AI + SQL Natural Language Interface Project

In this project you will design a database and create a natural language interface to it using AI.  
This should take about 6 hours if you want to code from scratch. (As a TA doing this project for the first time, it took me a little longer than this to complete by myself from scratch, but in groups you can definitely finish in that time)   
Below are some instructions and you can check the examples folder to get some ideas on where you might start. There is also sample_post.md in this directory that you could look at to see what your final submission should look like.

## Some Questions to Ask Yourself Throughout This Project:

* How good is GPT at generating SQL?
* What are the limitations and capabilities?
* Can you use GPT capabilities as a software engineer?
* Do you know the costs of using GPT?

---

# Research and Setup

* **Read a Published Paper** : Read this paper! Learn about the three prompting strategies presented - https://arxiv.org/abs/2305.11853

* **OpenAI Setup**: Create a new OpenAI Account or pay the $5. This should be enough to complete the assignment. (Cost me 29 cents in including all my debugging)

* **Developer Setup**: Setup a developer API KEY, find your "ORGID". Learn how to interface with OpenAI. Learn about different models and their costs (GPT 3.5, davinci, GPT 4, etc). Search Google to find more information.

---

# Design and Build

* **Design a database!** If you have a hard time coming up with an idea of what to model, maybe try one of these (restaurant, university, hair salon, system for tracking pianos on campus, vending machines, etc..). You can reuse your "Your Choice" design as well. You'll also need to put data into your database. (You can reuse the one from the build your own database assignment)

* **Build an app** that users can use plain words to ask questions and get answers in plain words using data from your database!

* **App Logic**: Your app will take questions, send them to GPT with your schema, get a SQL syntax, use the SQL to query your database, send the resulting data back to GPT, get a natural language answer and provide it back to the user.

* **Create a picture:**

  * Consider using https://drawsql.app to make your schema.

  * As another option, https://supabase.com will give you a nice postgres option and schema visualizer.

* **Example Code**: I recommend you write your own code, work brings learning that you cannot get in any other way! Feel free to look at my code and Dr Jenkins code as well.

  * Professor Reynolds' example code: https://github.com/byu-cs-452/byu-cs-452-class-content/tree/main/aisql/examples

  * Dr Jenkins Fall 2023 project example: https://github.com/porterjenkins/byu-cs452-labs/tree/main/python_sql_lite

---

# Individual and Group Responsibilities

* You can work in groups of 1-5 people. However, regardless of how many people there are in your group, each person must at least:

  * Read the paper: https://arxiv.org/abs/2305.11853

  * Create a schema picture (either from the schema or manually)

  * Contribute to the database design (maybe a table, foreign key, attribute, something!)

  * Execute the program with an API key that they individually generated in OpenAI.

  * Experiment with a question that they personally came up with!

  * Self report in Canvas.

---

# Posting and Submission

* **What you will post on our class channel (as a group of 1-5 people):**

  * Working code files (and DB if using SQLite). Remember, never share your Open AI API key or OrgID. Preferably in the form of a github link!

  * One+ sentence description or purpose of your database

  * Picture of Schema

  * Sample question, SQL query, response that worked (if you have one)

  * Sample question, SQL query, response that did not work (if you have one)

  * A file outlining at least 6 other examples.

  * Describe somewhere which prompting strategies you tried and if you noticed a difference between them. (Note my post only does two of three - which is fine!).

  * Remember, this assignment is meant to be creative and fun. Feel free to experiment and try new things!

  * Here is a sample post of what you might submit of the results from this project.:
    https://github.com/byu-cs-452/byu-cs-452-class-content/blob/main/aisql/sample_post.md

* **Review**: Please take a look at other's posts. Please read, then react with a reply or emoji to at least 3 posts of others! Please start by reviewing those posts with less reactions so everyone's projects can be read/reviewed. I'm not asking you to criticize other's work, but please do share feedback or ask questions if something is unclear!

---

Going further.... Could you imagine what it would take to make a system that could enable users to talk in natural language to any database?
