import json
from flask_sqlalchemy import SQLAlchemy
from db import Datapoints, db
from flask import Flask, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

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
def home_page():
    return json.dumps({"Test"}), 200

#expect to use this route for the home screen. If new day then a blank
#datapoint record is created. If not new day, then we get datapoint record
@app.route('/api/get_data/', methods=['POST'])
def get_user_data():
    post_body = json.loads(request.data)
    username = post_body['username']
    date = post_body['date']
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        #this means that it's a new day so we will create a new datapoint record
        datapoint = create_new_blank_datapoint_record(username, date)
    return json.dumps({'success':True, 'data':datapoint.serialize()}), 200

def create_new_blank_datapoint_record(username, date):
    datapoint = Datapoints(username=username, date=date)
    db.session.add(datapoint)
    db.session.commit()
    return datapoint

#expect to use this route when the user clicks on the water button
@app.route('/api/get_data/water', methods=['GET'])
def get_user_water_data():
    username = request.args.get('username', default = '', type = str)
    date = request.args.get('date', default = '', type = str)
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    data = datapoint.serialize()
    del data['mood_data']
    del data['sleep_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

#expect to use this route when the user clicks on the mood button
@app.route('/api/get_data/mood', methods=['GET'])
def get_user_mood_data():
    username = request.args.get('username', default = '', type = str)
    date = request.args.get('date', default = '', type = str)
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    data = datapoint.serialize()
    del data['water_data']
    del data['sleep_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

#expect to use this route when the user clicks on the sleep button
@app.route('/api/get_data/sleep', methods=['GET'])
def get_user_sleep_data():
    username = request.args.get('username', default = '', type = str)
    date = request.args.get('date', default = '', type = str)
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    data = datapoint.serialize()
    del data['water_data']
    del data['mood_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

#expect to use this route when the user clicks on the fitness button
@app.route('/api/get_data/fitness', methods=['GET'])
def get_user_fitness_data():
    username = request.args.get('username', default = '', type = str)
    date = request.args.get('date', default = '', type = str)
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    data = datapoint.serialize()
    del data['water_data']
    del data['mood_data']
    del data['sleep_data']
    return json.dumps({'success':True, 'data':data}), 200

@app.route('/api/update_mood/', methods=['POST'])
def update_user_mood():
    post_body = json.loads(request.data)
    username = post_body['username']
    date = post_body['date']
    update_to = post_body['update_to']
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    datapoint.mood_data = update_to
    db.session.commit()
    data = datapoint.serialize()
    del data['water_data']
    del data['sleep_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

@app.route('/api/update_sleep/', methods=['POST'])
def update_user_sleep():
    post_body = json.loads(request.data)
    username = post_body['username']
    date = post_body['date']
    update_to = post_body['update_to']
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    datapoint.sleep_data = update_to
    db.session.commit()
    data = datapoint.serialize()
    del data['water_data']
    del data['mood_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

@app.route('/api/update_fitness/', methods=['POST'])
def update_user_fitness():
    post_body = json.loads(request.data)
    username = post_body['username']
    date = post_body['date']
    update_to_intensity = post_body['update_to_intensity']
    update_to_duration = post_body['update_to_duration']
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    datapoint.fitness_intensity_data = update_to_intensity
    datapoint.fitness_duration_data = update_to_duration
    db.session.commit()
    data = datapoint.serialize()
    del data['water_data']
    del data['mood_data']
    del data['sleep_data']
    return json.dumps({'success':True, 'data':data}), 200


#Note: we should have an undo button for adding water in the IOS side
@app.route('/api/update_water/', methods=['POST'])
def update_user_water():
    post_body = json.loads(request.data)
    username = post_body['username']
    date = post_body['date']
    update_by = post_body['update_by']
    datapoint = Datapoints.query.filter_by(username=username, date=date).first()
    if not datapoint:
        return json.dumps({'success':False,'error':'invalid username or date'}), 404
    datapoint.water_data = update_by + datapoint.water_data
    db.session.commit()
    data = datapoint.serialize()
    del data['mood_data']
    del data['sleep_data']
    del data['fitness_data_intensity']
    del data['fitness_data_duration']
    return json.dumps({'success':True, 'data':data}), 200

#processing
def corelation_processing(var1, var2, username):
    datapoint = Datapoints.query.filter_by(username=username)
    data = {'Date':[record.date for record in datapoint],
    'Water':[record.water_data for record in datapoint],
    'Mood':[record.mood_data for record in datapoint],
    'Sleep':[record.sleep_data for record in datapoint],
    'Fitness':[(record.fitness_duration_data*(0.5*record.fitness_intensity_data + 0.5)) for record in datapoint]}
    #the complex looking expression for fitness basically multiplies duration
    # with 1 for light, 1.5 for medium and 2 for heavy intensity
    nparray = pd.DataFrame(data)
    print(nparray)
    X = nparray[var1].values.reshape(-1,1)
    y = nparray[var2].values.reshape(-1,1)
    regressor = LinearRegression()
    regressor.fit(X, y) #training the algorithm
    #To retrieve the intercept:
    print(regressor.intercept_[0])
    intercept = regressor.intercept_[0]
    #For retrieving the slope:
    print(regressor.coef_[0][0])
    coef = regressor.coef_[0][0]
    y_pred = regressor.predict(X)
    df = pd.DataFrame({'Actual': y.flatten(), 'Predicted': y_pred.flatten()})
    print(df)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, y_pred)))
    MAE = metrics.mean_absolute_error(y, y_pred)
    MSE = metrics.mean_squared_error(y, y_pred)
    RMS = np.sqrt(metrics.mean_squared_error(y, y_pred))
    return {"var1":var1, "var2": var2,"intercept":intercept, "coef":coef, "MAE":MAE, "MSE":MSE, "RMS":RMS}

@app.route('/api/corelation', methods=['GET'])
def corelation_specific():
    var1 = request.args.get('var1', default = '', type = str)
    var2 = request.args.get('var2', default = '', type = str)
    data = corelation_processing(var1, var2, "kj228")
    print(data)
    return json.dumps({'success':True, 'data':data}), 200

#(As we have to inclde a delete function). When the user deactivates his/her
#account we wiull remove their login credentials from the auth table
#and delete all data relating to that user.
def delete_user_by_username(username):
        Datapoints.query.filter_by(username=username).delete()
        db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
