from clickhouse_driver import Client
try:
    ch_client = Client(host='localhost', port=9000, user='default', password='')
    rows = ch_client.execute("SELECT event, page, timestamp FROM analytics.events ORDER BY timestamp DESC LIMIT 5")
    print("✅ Success:", rows)
except Exception as e:
    print(f"❌ Error: {e}")
