# Work Queue Project (polling, notifications, logging, concurrency, redis)

This sample was taken from a machine learning blog. Feel free to read it and understand the intent of the provided code:  
https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/

![alt text](system_design.png)

## 1. Python Environment

- Recommended to use Python 3.11.3 (Download it here: https://www.python.org/ftp/python/3.11.3/)
- VSCode is recommended. You can launch VSCode from this directory. Then use the command palette (`Ctrl+Shift+P`) → `"Python: Create Environment"`. Choose Python 3.11.3 and check the box for including `requirements.txt`.

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
- Run `simple_request.py` with [castle_image.jpg](castle_image.jpg).  
- Report the results and the detected objects with their confidence scores.  

### 4. Concurrency and Scaling
- Identify and Describe the main issues that occur when multiple web servers (`run_web_server.py`) and/or multiple model servers (`run_model_server.py`) are running at the same time.    
- Update the code to fix one issue, test that it works, and explain the solution using words and diagrams.  

### 5. Reducing Polling Overhead
- Polling is reliable but it is the most expensive way to interact with a system.  
- Instead of having the web server poll REDIS waiting for a key to show up, research and implement a way that instead uses notifications and only uses polling as a backup.
- Test your implementation and explain how it reduces overhead using code, words, and diagrams.  

<details>
<summary>How to Enable Redis Notifications</summary>
To use Redis notifications it is not that difficult. Though you do need to open the redis CLI (you can access from the cloud redis insight tool) and enable notifications:  
	
```
CONFIG SET notify-keyspace-events KEA
```

The Code then to enable this would be:  

```py
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)
# Define a handle to the pubsub
p = db.pubsub()

#....

# generate an ID for the classification then add the
# classification ID + image to the queue
k = str(uuid.uuid4())
image = helpers.base64_encode_image(image)
d = {"id": k, "image": image}

# Subscribe to key-space events for our specific key (subscribe before queueing work so we don't miss it!)
p.psubscribe(f"__keyspace@0__:{k}")

# Push work into queue
db.rpush(settings.IMAGE_QUEUE, json.dumps(d))

#....

print(f"waiting for message...")
result = p.get_message(timeout=24.0)
print (result)
output = db.get(k)
print (output)
```
</details>

### 6. Stress Test Fix
- The provided stress_test.py doesn't work because it starts threads but exits before they finish.
- Update the code so threads are properly joined before the program terminates.
- Explain how and what you did to fix it.

### 7. Unified Logging
- Write a simple logging function callable from any file.
- Each log entry should be in a consitent format and include:
	- Server name
	- Main running Python script name
	- Timestamp
	- Action
