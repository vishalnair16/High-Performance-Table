# MongoDB Atlas Setup Guide

## Understanding Your MongoDB URI

Your MongoDB Atlas connection string looks like this:
```
mongodb+srv://vishalnair16:<db_password>@cluster0.84iovxr.mongodb.net/?appName=Cluster0
```

## Two Ways to Specify Database Name

### Option 1: Database Name in URI (Recommended for MongoDB Atlas)

Add the database name directly in the connection string:
```
mongodb+srv://vishalnair16:YOUR_PASSWORD@cluster0.84iovxr.mongodb.net/high_performance_db?appName=Cluster0
                                                                      ^^^^^^^^^^^^^^^^^^^^
                                                                      Database name here
```

**In your `.env` file:**
```env
MONGO_URI=mongodb+srv://vishalnair16:YOUR_PASSWORD@cluster0.84iovxr.mongodb.net/high_performance_db?appName=Cluster0
```

### Option 2: Database Name Separately (Current Implementation)

Keep the URI as-is and specify the database name separately:
```
mongodb+srv://vishalnair16:YOUR_PASSWORD@cluster0.84iovxr.mongodb.net/?appName=Cluster0
```

**In your `.env` file:**
```env
MONGO_URI=mongodb+srv://vishalnair16:YOUR_PASSWORD@cluster0.84iovxr.mongodb.net/?appName=Cluster0
DB_NAME=high_performance_db
```

## Step-by-Step Setup

1. **Get Your Password**
   - Replace `<db_password>` with your actual MongoDB Atlas password
   - If you don't remember it, reset it in MongoDB Atlas dashboard

2. **Create `.env` File**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` File**
   - Open `.env` in a text editor
   - Replace `YOUR_PASSWORD` with your actual password
   - Choose one of the options above for database name

4. **Example `.env` File:**
   ```env
   # Using Option 2 (separate DB_NAME)
   MONGO_URI=mongodb+srv://vishalnair16:MyPassword123@cluster0.84iovxr.mongodb.net/?appName=Cluster0
   DB_NAME=high_performance_db
   
   REDIS_HOST=redis
   REDIS_PORT=6379
   ENABLE_CACHE=true
   ```

5. **Test Connection**
   ```bash
   # Start services
   docker-compose up -d
   
   # Check health
   curl http://localhost:8000/health
   ```

## Important Notes

- **Database Name**: MongoDB will create the database automatically when you first insert data
- **Password**: Make sure to URL-encode special characters in your password (e.g., `@` becomes `%40`)
- **Network Access**: Ensure your IP is whitelisted in MongoDB Atlas (or use `0.0.0.0/0` for development)
- **Connection String**: The current code uses `DB_NAME` separately, so Option 2 is already implemented

## Troubleshooting

**Connection Failed:**
- Check your password is correct
- Verify IP whitelist in MongoDB Atlas
- Check network connectivity

**Database Not Found:**
- The database will be created automatically on first insert
- Verify `DB_NAME` is set correctly
- Check MongoDB Atlas dashboard for database creation

**Authentication Failed:**
- Verify username and password
- Check if user has proper permissions
- Ensure database user exists in MongoDB Atlas

## Current Implementation

The code currently uses **Option 2** - it connects to the cluster and then selects the database specified in `DB_NAME`. This is the recommended approach as it's more flexible.

```python
# In app/core/database.py
db.database = db.client[settings.DB_NAME]  # Database name from config
```

So you just need to:
1. Set `MONGO_URI` with your password
2. Set `DB_NAME` to whatever you want (default: `high_performance_db`)

The database will be created automatically when you seed data!

