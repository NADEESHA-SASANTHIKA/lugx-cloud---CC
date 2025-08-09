from flask import Flask, request, jsonify
import os
import json
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO games (name, category, release_date, price) VALUES (%s, %s, %s, %s)", 
                (data['name'], data['category'], data['release_date'], data['price']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Game added'}), 201

@app.route('/games', methods=['GET'])
def get_games():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM games")
    games = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(games)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
