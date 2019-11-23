from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

user_water_association_table = Table('user_water_association', db.Model.metadata,
    Column('user_id', db.Integer, ForeignKey('users.id')),
    Column('water_id', db.Integer, ForeignKey('water.id'))
)
user_fitness_association_table = Table('user_fitness_association', db.Model.metadata,
    Column('user_id', db.Integer, ForeignKey('users.id')),
    Column('fitness_id', db.Integer, ForeignKey('fitness.id'))
)
user_sleep_association_table = Table('user_sleep_association', db.Model.metadata,
    Column('user_id', db.Integer, ForeignKey('users.id')),
    Column('sleep_id', db.Integer, ForeignKey('sleep.id'))
)
user_mood_association_table = Table('user_mood_association', db.Model.metadata,
    Column('user_id', db.Integer, ForeignKey('users.id')),
    Column('mood_id', db.Integer, ForeignKey('mood.id'))
)


class User(db.Model):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String, nullable=False)
    password_encrypted= db.Column(db.Integer, nullable=False)
    water = relationship("Water", secondary=user_water_association_table, back_populates="user")
    fitness = relationship("Fitness", secondary=user_fitness_association_table, back_populates="user")
    sleep = relationship("Sleep", secondary=user_sleep_association_table, back_populates="user")
    mood = relationship("Mood", secondary=user_mood_association_table, back_populates="user")

    def __init__(self, **kwargs):
        self.username = kwargs.get('username','')
        #TODO: figure out how we should encrypt passwords
        self.password_encrypted = kwargs.get('password','')


    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Datapoint(db.Model):
    __tablename__='water'
    id= db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Integer, nullable=False)  #Unix time
    amount=db.Column(db.Integer, default=0)
    user = relationship("User", secondary=user_water_association_table, back_populates="water")

    def __init__(self, **kwargs):
        self.date = kwargs.get('date','')
        self.user =  [kwargs.get('user', '')]



# MODEL POLYMORPHISM: MERGE ALL THESE MODELS INTO A "DAILY" Table
# - ID, DATE, USER AND THEN COLUMNS FOR THE 4 TYPES
# ADD ROUTES FOR ALL MY "MOOD" DAYS
# ADD URL QUERY PARAMETERS FOR FILTERING WHICH TYPE OF DATAPOINT WE WANT (E.G. FILTER BY MOOD)
# BCRYPT FOR PASSWORD ENCRYPTION
# LOOK FOR CORRELATIONS
        # SKLEARN scikit learn
        # pytorch
        # pandas
        # correlation constants b/w -1 and 1
        # analyze from user's standpoint
        # full analytics on everyone
# restrict emojis
