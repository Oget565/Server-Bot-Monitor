import sqlite3
import time
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

DB_PATH = Path(__file__).resolve().parent / 'server_metrics.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Thread pool for async database operations
_executor = ThreadPoolExecutor(max_workers=1)

def _save_to_db_sync(data):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        create_query = '''
        CREATE TABLE IF NOT EXISTS Metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            mem_total REAL,
            mem_used REAL,
            mem_prcnt REAL,
            cpu_prcnt REAL,
            cpu_freq REAL,
            cpu_temp REAL
        );
        '''
        cursor.execute(create_query)

        ts = int(time.time())

        insert_query = '''
        INSERT INTO Metrics (timestamp, mem_total, mem_used, mem_prcnt, cpu_prcnt, cpu_freq, cpu_temp)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        params = (ts, data['mem_total'], data['mem_used'], data['mem_prcnt'],
                  data['cpu_prcnt'], data['cpu_freq'], data['cpu_temp'])
        cursor.execute(insert_query, params)
        connection.commit()

    print("Database updated")

async def save_to_db(data):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_executor, _save_to_db_sync, data)
    print("Database saved")

