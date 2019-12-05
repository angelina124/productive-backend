from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

<<<<<<< HEAD

class User(db.Model):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String, nullable=False)
    password_encrypted= db.Column(db.Integer, nullable=False)

=======
#Notes: for now we're internally storing the fitness data as a single int that will indicate
#intensity and length. Appropriate processing will be done on the backend before
#returning this data in order to return it as two separate values.
#Need to ask Conner how to change this to an object containg two properties.

class Datapoints(db.Model):
    __tablename__='datapoints'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, nullable=False)
    date =db.Column(db.String, nullable=False)
    water_data=db.Column(db.Integer, nullable=False)
    mood_data=db.Column(db.Integer, nullable=False)
    sleep_data=db.Column(db.Integer, nullable=False)
    fitness_intensity_data=db.Column(db.Integer, nullable=False)
    fitness_duration_data=db.Column(db.Integer, nullable=False)

#In reality we will never create a Datapoint object with all the values
#already filled in. It will always be a blank datapoint object with
#only the username and date
>>>>>>> dc9a4757f91e42c060f6253bb0d99c13d64052d4
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.date = kwargs.get('date')
        self.water_data= kwargs.get('water_data',0)
        self.mood_data= kwargs.get('mood_data',0)
        self.sleep_data= kwargs.get('sleep_data',0)
        self.fitness_intensity_data= kwargs.get('fitness_intensity_data',0)
        self.fitness_duration_data= kwargs.get('fitness_duration_data',0)

    def serialize(self):
        return {
            'date': self.date,
            'username': self.username,
            'water_data': self.water_data,
            'mood_data': self.mood_data,
            'sleep_data': self.sleep_data,
            'fitness_data_intensity': self.fitness_intensity_data,
            'fitness_data_duration': self.fitness_duration_data
        }
