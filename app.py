import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/profil", methods=["POST"])
def profil_post():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    message_receive = request.form['message_give']
    count = db.profil.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'name': name_receive,
        'email': email_receive,
        'message': message_receive,
        'done': 0
    }
    db.profil.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/profil/done", methods=["POST"])
def profil_done():
    num_receive = request.form['num_give']
    db.profil.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update Done!'})

@app.route("/profil/delete", methods=["POST"])
def profil_delete():
    num_receive = request.form['num_give']
    db.profil.delete_one(
        { 'num': int(num_receive)},
    )
    return jsonify({'msg': 'Delete Success!'})

@app.route("/profil", methods=["GET"])
def profil_get():
    profils_list = list(db.profil.find({}, {'_id': False}))
    return jsonify({'profils': profils_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True) 