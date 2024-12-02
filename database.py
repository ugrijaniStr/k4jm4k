from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import threading
import time

app = Flask(__name__)

# Povezivanje na MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client["users"]  # Zamensite sa vašim imenom baze
collection = db["users"]  # Zamensite sa vašim imenom kolekcije

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def get_status():
    data = list(collection.find({"address": "('127.0.0.1', 64958)"}))
    result = []
    for item in data:
        result.append({
            'id': str(item["_id"]),
            'address': item["address"],
            'status': item["status"],
            'date': item["date"]
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)