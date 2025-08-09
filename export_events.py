import psycopg2
from clickhouse_driver import Client
from datetime import datetime

# Connect to ClickHouse
ch_client = Client(host='localhost', port=9000, user='default', password='')

# Connect to RDS Postgres
pg_conn = psycopg2.connect(
    host='analyticsdb.cpco8iag0bag.ap-southeast-2.rds.amazonaws.com',
    port=5432,
    user='postgres',
    password='mypassword',
    database='analyticsdb'
)

try:
    cur = pg_conn.cursor()

    # Get latest timestamp from RDS
    cur.execute("SELECT MAX(timestamp) FROM analyticsdb_events")
    last_timestamp = cur.fetchone()[0]
    if last_timestamp is None:
        last_timestamp = datetime(1970, 1, 1)
    print(f"Last timestamp: {last_timestamp}")

    # Format timestamp for ClickHouse (avoid parameter binding)
    last_ts_str = last_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # Same style as test_clickhouse.py
    query = f"""
        SELECT event, page, timestamp
        FROM analytics.events
        WHERE timestamp > '{last_ts_str}'
        ORDER BY timestamp ASC
    """
    rows = ch_client.execute(query)

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyticsdb_events (
            event TEXT,
            page TEXT,
            timestamp TIMESTAMP
        );
    """)

    # Insert data
    inserted_rows = 0
    for row in rows:
        cur.execute("INSERT INTO analyticsdb_events (event, page, timestamp) VALUES (%s, %s, %s)", row)
        inserted_rows += 1

    pg_conn.commit()
    print(f"✅ {inserted_rows} new rows exported to RDS at {datetime.now()}.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    cur.close()
    pg_conn.close()
