from flask import Flask, request, jsonify
from flask_cors import CORS
from clickhouse_driver import Client
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

MAX_RETRIES = 10
RETRY_DELAY = 3

# Ensure table exists by connecting once at startup
def setup_clickhouse():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = Client(host='clickhouse', port=9000)
            client.execute('CREATE DATABASE IF NOT EXISTS analyticsdb')
            client.execute('''
                CREATE TABLE IF NOT EXISTS analyticsdb.events (
                    event String,
                    page String,
                    timestamp DateTime
                ) ENGINE = MergeTree()
                ORDER BY timestamp
            ''')
            print("✅ ClickHouse is ready.")
            return
        except Exception as e:
            print(f"❌ ClickHouse not ready, retrying in {RETRY_DELAY} seconds... ({attempt}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    raise Exception("❌ ClickHouse connection failed after retries.")

setup_clickhouse()

# Use a fresh connection on every request
def get_client():
    return Client(host='clickhouse', port=9000)

@app.route('/track', methods=['POST'])
def track():
    try:
        data = request.get_json()
        event = data.get('event')
        page = data.get('page')
        timestamp = datetime.now()

        client = get_client()
        client.execute('INSERT INTO analyticsdb.events (event, page, timestamp) VALUES', [(event, page, timestamp)])
        return jsonify({'message': 'Event recorded'}), 200

    except Exception as e:
        print(f"Error inserting event: {e}")
        return jsonify({'error': 'Failed to store event'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
