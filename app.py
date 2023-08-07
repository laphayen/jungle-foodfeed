from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://poqop721:crafter10@52.78.157.63', 27017)
db = client.jungle_food_feed #db명

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('login.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)