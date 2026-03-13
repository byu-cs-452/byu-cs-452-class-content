# Step 4 — Create Your Own Atlas MongoDB Deployment

## 1. Create a Free Atlas Account

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com/) and sign up (Google sign-in works).
2. Choose the **Free / M0** tier when prompted to create your first cluster.
3. Pick any cloud provider and region — the closest to you will have the lowest latency.

## 2. Create a Database User

1. In the left sidebar, go to **Security → Database Access**.
2. Click **Add New Database User**.
3. Choose **Password** authentication.
4. Set a username and password — **save these**, you'll need them for your connection string.
5. Set privileges to **Read and write to any database**.

## 3. Allow Network Access

1. Go to **Security → Network Access**.
2. Click **Add IP Address**.
3. For class purposes, click **Allow Access from Anywhere** (`0.0.0.0/0`).
   - ⚠️ This is fine for a free sandbox. For production, restrict to specific IPs of the datacenter that would access it. 

## 4. Get Your Connection String

1. Go to **Deployment → Database** and click **Connect** on your cluster.
2. Choose **Drivers** (Python).
3. Copy the connection string — it will look like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
   ```
4. Replace `<username>` and `<password>` with the credentials from step 2.

## 5. Test the Connection

```python
from pymongo import MongoClient

uri = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/"
client = MongoClient(uri)

# Quick test
print(client.list_database_names())
```

If you see a list of databases (at least `admin`, `local`), you're connected! 🎉
