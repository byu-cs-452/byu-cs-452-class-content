# Work Queue Project (polling, notifications, logging, concurrency, redis)

This sample was taken from a machine learning blog. Feel free to read it and understand the intent of the provided code:  
https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/

![alt text](system_design.png)

## 1. Python Environment

- **Use Python 3.11 or 3.12.** TensorFlow does not currently support Python 3.13 or 3.14. If you're using Colab, verify its Python version with `!python --version` — if it's 3.13+, you may need to create a custom runtime or use a local environment instead.
- VSCode is recommended. You can launch VSCode from this directory. Then use the command palette (`Ctrl+Shift+P`) → `"Python: Create Environment"`. Choose Python 3.11 or 3.12 and check the box for including `requirements.txt`.

If you didn't check the box to include `requirements.txt`, you can install the dependencies from your terminal like this:

```
pip install -r requirements.txt
```

Or like this:  

```
pip install tensorflow
pip install flask
pip install pillow
pip install redis
pip install requests
```

## 2. Setup settings.py

You will need to put your own redis connection information in [settings.py](settings.py). 
- Option 1: You can get a free 30mb REDIS account on redis.io
- Option 2: you could install REDIS locally

If you haven't already, you can set up REDIS following these instructions:  
https://github.com/byu-cs-452/byu-cs-452-class-content/blob/main/redis/01%20-%20Create%20Redis%20Cluster.md  

### Finding Redis Connection Info
1. In redis.io, open your database and go to the Configuration tab.
2. Under Public Endpoint, copy the text before the `:` — that’s your `REDIS_HOST`.
3. The number after the `:` is your `REDIS_PORT`.
4. Scroll down to Security, then find and set your password, and copy it as `REDIS_PASSWORD`.

## 3. Running the Project

The tutorial from the blog talks a lot about apache web server, but you can just run the necessary commands in three separate shells (or threads in colab).  

Note: you may have to use the `python3` command instead of `python` if on MacOS or Linux.

First shell:
```
python run_web_server.py 
```

Second shell:
```
python run_model_server.py
```

Third shell:
```
python simple_request.py 
```

(Make sure you run these in order, because simple_requst.py needs the servers to be up and running)

---

## Deliverables (Include code, diagrams, and brief explanations in your PDF)

### 1. Redis Key Structure
- Identify the "key" in the REDIS database where the web server stores the user's image.  
- State the data type and describe the structure of the stored value.  

### 2. Web Server to Model Server Communication
- Explain how the web server communicates with the model (worker) server to hand off work and receive back results.  
- Describe how it works for the web server to respond to web requests. 

### 3. Model Output
- Run `simple_request.py` with [castle_image.jpg](castle_image.jpg) (which is the default).  
- Report the results and the detected objects with their confidence scores.  

### 4. Concurrency and Scaling
- Running multiple worker (model) servers simultaneously causes a bug. Identify it, fix it, and explain your solution with code and diagrams.  
- Are multiple web servers safe to run? Why or why not? Will they ever generate conflicting UUIDs? Will subscribing to notifications scale or conflict between multiple web server instances? (Research and explain your answer.)  
- What happens if a worker crashes after claiming an item from the queue but before writing the result? That work is lost. Describe — you don't need to implement — a strategy to handle this.  

### 5. Reducing Polling Overhead
- Polling is reliable but it is the most expensive way to interact with a system.  
- Instead of having the web server poll REDIS waiting for a key to show up, research and implement a way that instead uses Redis notifications.
- Test your implementation and explain how it reduces overhead using code, words, and diagrams.  
- What happens if the notification is missed or the worker crashes before writing the result? Describe a strategy you could use to ensure no work is lost.  

<details>
<summary>How to Enable Redis Notifications</summary>
To use Redis notifications it is not that difficult. Though you do need to open the redis CLI (you can access from the cloud redis insight tool) and enable notifications:  
	
```
CONFIG SET notify-keyspace-events KEA
```

> **⚠️ Important:** You must subscribe to the keyspace event **before** pushing work onto the queue. If you subscribe after, the notification may fire before your subscription is active, and you'll miss it.

The code to use notifications would look like this:  

```py
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)

# Create a pubsub handle for listening to Redis notifications
p = db.pubsub()

# Generate a unique ID for this classification request
k = str(uuid.uuid4())
image = helpers.base64_encode_image(image)
d = {"id": k, "image": image}

# IMPORTANT: Subscribe BEFORE pushing work so we don't miss the notification
# This listens for any keyspace event on our specific result key
p.psubscribe(f"__keyspace@0__:{k}")

# Now push the work into the queue
db.rpush(settings.IMAGE_QUEUE, json.dumps(d))

# Wait for the notification that our result key was created
while True:
    message = p.get_message(timeout=30.0)
    if message is None:
        # Timeout — something went wrong
        break
    if message["type"] == "pmessage":
        # This is the actual keyspace notification — our result is ready!
        # (The first message from get_message is always a subscribe
        #  confirmation with type "psubscribe" — not the event. That's
        #  why we loop and check for "pmessage" specifically.)
        break

# The notification only tells us the event HAPPENED (a SET occurred on our key).
# We still need to fetch the actual result data from Redis.
output = db.get(k)

# Clean up: unsubscribe and close the pubsub connection
p.punsubscribe()
p.close()
```
</details>

### 6. Stress Test Fix
- The provided `stress_test.py` is broken because it doesn't properly join its threads.
- Fix it so threads are properly joined before the program terminates.
- Explain how and what you did to fix it.

### 7. Unified Logging
- Implement a logging solution callable from any file.
- Each log entry should be in a consistent format and include:
	- Server name
	- Main running Python script name
	- Timestamp
	- Action
- Some implementation options to consider:
	- **Console logger**: A shared Python module that prints formatted log lines to stdout
	- **File logger**: Write logs to a shared file using Python's built-in `logging` module
	- **Redis logger**: Push log entries to a Redis list so you can view the full picture across all servers from one place
	- Come up with your own approach!
- Pick one that is most interesting to you and implement it. Describe how it works and any interesting features it has!

---

## Going Further: Reliable Queues

The `LPOP` fix for Deliverable 4 ensures each item is processed once, but if a worker crashes mid-processing, that item is gone. Redis provides commands for building reliable queues:

- **`BRPOPLPUSH` / `LMOVE`**: Atomically pops an item from one list and pushes it to a "processing" list. If the worker completes successfully, it removes the item from the processing list. If the worker crashes, a monitor process can detect stuck items in the processing list and re-queue them.

This is called a *two-phase commit* pattern: claim → process → acknowledge. It's how production systems like Sidekiq and Celery handle job reliability.
