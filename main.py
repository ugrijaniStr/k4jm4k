from flask import Flask, render_template
import pymongo
import random

app = Flask(__name__, static_folder = "static/css")
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['users']

class Main(object):
    def randPort() -> int:
        return random.randint(1000,9999)
    
    @app.route('/')
    def index():
        collection = db['users']
        users = []

        for user in collection.find():
            users.append(user)


        address = user["address"]
        status = user["status"]
        date = user["status"]


        return render_template('index.html', items = users, address = address, status = status, date = date)
    
if(__name__ == '__main__'):
    app.run(host = '127.0.0.1', port = Main.randPort())