import asyncio
import aiosqlite
import os


DB_NAME = os.environ.get("DB_NAME")


async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("[All Users]")
        for row in rows:
            print(row)
        await cursor.close()

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        print("[Users older than 40]")
        for row in rows:
            print(row)
        await cursor.close()

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
