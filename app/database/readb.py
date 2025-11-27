import sqlite3
import time
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

DB_PATH = Path(__file__).resolve().parent / 'server_metrics.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_executor = ThreadPoolExecutor(max_workers=1)

CREATE_TABLE_SQL = '''
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

LATEST_ROW_SQL = '''
SELECT timestamp, mem_total, mem_used, mem_prcnt, cpu_prcnt, cpu_freq, cpu_temp
FROM Metrics
ORDER BY timestamp DESC
LIMIT 1;
'''

LATEST_24HR_ROW_SQL = '''
SELECT timestamp, mem_total, mem_used, mem_prcnt, cpu_prcnt, cpu_freq, cpu_temp
FROM Metrics
ORDER BY timestamp DESC
LIMIT 288;
'''

def _read_latest_sync():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        cursor.execute(LATEST_ROW_SQL)
        row = cursor.fetchone()
        return dict(row) if row else None

def _read_latest_sync_24hr():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        cursor.execute(LATEST_24HR_ROW_SQL)
        rows = cursor.fetchall()
        return [dict(row) for row in rows] if rows else None

async def read_latest():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _read_latest_sync)

async def read_latest_24hr():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _read_latest_sync_24hr)
