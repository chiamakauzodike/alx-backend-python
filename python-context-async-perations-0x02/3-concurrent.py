import asyncio
import aiosqlite
import os


DB_NAME = os.environ.get("DB_NAME")

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

# Run and get results
all_users, older_users = asyncio.run(fetch_concurrently())

print("[All Users]")
for user in all_users:
    print(user)

print("\n[Users older than 40]")
for user in older_users:
    print(user)