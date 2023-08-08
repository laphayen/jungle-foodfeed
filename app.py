from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
client = MongoClient('mongodb://seungtae:jeon8175@13.125.153.232', 27017)
dblog = client.jungle_food_feed #db명

app.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "b'\xf6e\xa5S\xef\xd4g\xdbT\xeb\x9d\xc8\x9e\xc6\xab\xcd'"
		)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    id = request.form['id']
    checkId = list(dblog.login.find({'id':id}))
    if len(checkId) != 0 :
        return jsonify({'result': 'fail', 'msg':'이미 아이디가 존재합니다.'})
    pw = request.form['pw']
    name = request.form['name']

    pw_hash = bcrypt.generate_password_hash(pw)
    dblog.login.insert_one({'id':id,'pw':pw_hash,'name':name})
    return jsonify({'result': 'success', 'msg':'회원 가입에 성공했습니다!'})

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['pw']
    checkUser = list(dblog.login.find({'id':id}))
    if len(checkUser) == 0:
        return jsonify({'result': 'fail', 'msg':'아이디가 존재하지 않습니다.'})
    elif not bcrypt.check_password_hash(checkUser[0]['pw'],pw):
        return jsonify({'result': 'fail', 'msg':'비밀번호가 틀렸습니다.'})
    else :
        return jsonify({'result': 'success', 'id':id,'msg':'로그인 되었습니다!', 'access_token' : create_access_token(identity = id,
											expires_delta = False)})
    
@app.route('/logout')
def logOut():
   token_blacklist = set()  # 토큰 블랙리스트
   data = request.get_json()
   token = data.get('token')

   if token:
    token_blacklist.add(token)
    return jsonify({'message': 'Logged out successfully'}), 200
   else:
    return jsonify({'message': 'Token is missing'}),

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)