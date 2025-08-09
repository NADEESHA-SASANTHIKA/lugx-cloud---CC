import psycopg2
from clickhouse_driver import Client

# ClickHouse client (assumes port-forward to localhost:9000 is active)
ch_client = Client(host='localhost')

# Connect to PostgreSQL (via port-forward to localhost:5432)
pg_conn = psycopg2.connect(
    host='analyticsdb.cpco8iag0bag.ap-southeast-2.rds.amazonaws.comq',
    port=5432,
    user='postgres',
    password='mypassword',
    database='analyticsdb'
)

# Export ClickHouse events
rows = ch_client.execute("SELECT event, page, timestamp FROM analytics.events")

# Insert into PostgreSQL
cur = pg_conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS analyticsdb_events (
        event TEXT,
        page TEXT,
        timestamp TIMESTAMP
    );
""")

for row in rows:
    cur.execute("INSERT INTO analyticsdb_events (event, page, timestamp) VALUES (%s, %s, %s)", row)

pg_conn.commit()
cur.close()
pg_conn.close()
print("✅ Export complete.")

