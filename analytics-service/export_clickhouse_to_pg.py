from clickhouse_driver import Client as ClickHouseClient
import psycopg2

# Connect to ClickHouse
ch_client = ClickHouseClient(host='localhost')

# Connect to PostgreSQL
pg_conn = psycopg2.connect(
    dbname="lugx_gaming",
    user="postgres",
    password="mypassword",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Create table if not exists (without scroll column)
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS analytics_events (
    event TEXT,
    page TEXT,
    timestamp TIMESTAMP
)
""")
pg_conn.commit()

# Fetch from ClickHouse
rows = ch_client.execute("SELECT event, page, timestamp FROM analytics.events")

# Insert into PostgreSQL
for row in rows:
    try:
        pg_cursor.execute("""
        INSERT INTO analytics_events (event, page, timestamp)
        VALUES (%s, %s, %s)
        """, row)
    except Exception as e:
        print("⚠️ Skipping row:", row, "Reason:", e)

pg_conn.commit()
print(f"✅ Exported {len(rows)} rows to PostgreSQL.")

# Close connections
pg_cursor.close()
pg_conn.close()

