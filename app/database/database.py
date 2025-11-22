import sqlite3
import time

with sqlite3.connect('server_metrics.db') as connection:
    cursor = connection.cursor()

    create_query = '''
    CREATE TABLE IF NOT EXISTS Metrics (
        timestamp INTEGER PRIMARY KEY,
        cpu REAL,
        ram REAL,
        temp REAL
    );
    '''
    cursor.execute(create_query)

    ts = int(time.time())
    metrics = (ts, '23.5', '45.7', '43.2')

    insert_query = '''
    INSERT INTO Metrics (timestamp, cpu, ram, temp)
    VALUES (?, ?, ?, ?);
    '''
    cursor.execute(insert_query, metrics)
    connection.commit()

print("Success")
