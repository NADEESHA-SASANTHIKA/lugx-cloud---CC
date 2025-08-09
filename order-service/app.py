from flask import Flask, request, jsonify
import psycopg2
import os
import json

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (cart_items, total_price) VALUES (%s, %s)", 
                (str(data['cart_items']), data['total_price']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Order saved'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
