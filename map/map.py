
from flask import Flask, request, jsonify
from pymongo import MongoClient
from app import app

client = MongoClient('mongodb://test:test@localhost',27017)
# db 연결
db = client.dbjungle


@app.route('/feed', methods=['POST'])
def save_feed():
    # 피드 제목
    title_receive = request.form['title_give']
    # 피드 내용(후기)
    contents_receive = request.form['contents_give']
    # 좌표값을 가져온다.
    coordinate_receive = request.form['coordinate_give']
    # 메모 아이디를 가져온다.
    id_receive = request.form['id_give']

    # 피드 생성
    feed = {'title': title_receive, 'contents': contents_receive, 'script_randomid': id_receive}

    # mongdoDB 저장
    db.feed.insert_one(feed)

    # 자바스크립트에서 생성한 script_randomid로 검색하여 Object ID 추출후 str형태로 형변환후 피드백
    temp4id = db.feeds.find_one({'script_randomid': id_receive})

    return jsonify({'result': 'success'})

@app.route('/feed', methods=['GET'])
def read_feed():
    result = list(db.feeds.find({}, {'_id':0}))
    return jsonify({'result': 'success', 'feeds': result})


@app.route('/api/delete', methods=['POST'])
def delete_feed():
    id_receive = request.form['id_give']
    db.feeds.delete_one({'id_copy': id_receive})
    return jsonify({'result': 'success'})


@app.route('/api/edit', methods=['POST'])
def update_feeds():
    id_receive = request.form['id_give']
    new_title = request.form['title_edit']
    new_contents = request.form['contents_edit']

    db.feeds.update_one({'id_copy': id_receive}, {'$set': {'title': new_title}})
    db.feeds.update_one({'id_copy': id_receive}, {'$set': {'contents': new_contents}})
