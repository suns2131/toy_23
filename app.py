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
    name_receive = request.form['name_give']
    post_receive = request.form['post_give']
    posting_all = list(db.posting.find({}, {'_id': False}))
    count = len(posting_all) + 1
    doc = {
        'num' : count,
        'name':name_receive,
        'post':post_receive,
        'image':url_receive,
        'like': 0
    }
    db.posting.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    posting = list(db.posting.find({}, {'_id': False}))
    #print(movie_list)
    return jsonify({'posting': posting})

@app.route("/movie/like", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    like_receive = request.form['like_give']
    #print(num_receive,like_receive)
    like_msg = ''
    if like_receive != '0':
        like_msg = '좋아요 완료!'
    else:
        like_msg = '좋아요 취소완료!'
    db.posting.update_one({'num': int(num_receive)}, {'$set': {'like': like_receive}})

    return jsonify({'msg': like_msg})

@app.route("/movie/reply", methods=["POST"])
def save_reply():
    reply_receive = request.form['reply_give']
    num_receive = request.form['num_give']
    doc = {
        'reply': reply_receive,
        'num': num_receive
    }
    db.reply.insert_one(doc)

    return jsonify({'msg': '등록되었습니다!'})


@app.route("/movie/reply", methods=["GET"])
def show_reply():
    posting = list(db.reply.find({}, {'_id': False}))
    return jsonify({'posting': posting})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
