from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cnyi5.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    name_receive = request.form['post_give']
    post_receive = request.form['post_give']

    doc = {
        'name':name_receive,
        'post':post_receive,
        'image':url_receive
    }
    db.posting.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    posting = list(db.posting.find({}, {'_id': False}))
    #print(movie_list)
    return jsonify({'posting': posting})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
