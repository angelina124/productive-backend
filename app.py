import json
from flask_sqlalchemy import SQLAlchemy
from db import User, db
from flask import Flask, request

app = Flask(__name__)
db_filename = 'cms.db'

#db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
# Your routes here

@app.route('/api/user/<int:id>/', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if(user is None):
        return json.dumps({'success':False,'error':'No user found for that id'}), 404
    return json.dumps({'success':True, 'data':user.serialize()}), 200

@app.route('/api/user/', methods=['POST'])
def create_user():
    #TODO: check for error
    post_body = json.loads(request.data)
    username = post_body['username']
    password = post_body['password']
    user = User(
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data':user.serialize()}), 200

@app.route('/api/user/<int:id>/', methods=['DELETE'])
def delete_user_by_id(id):
    try:
        user = User.get(id)
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user}), 200
    except:
        return json.dumps({'success': False, 'error': 'Unable to delete user'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
