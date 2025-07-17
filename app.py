from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///app.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    password = db.Column(db.String(140))
    questions = db.relationship('Questions', backref='users')

    def __repr__(self):
        return f"<Users {self.name}>"
    
class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_url = db.Column(db.String, nullable=True)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    answers = db.relationship('Answers', backref='questions')

class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default = db.func.now())
    
class QuestionTags(db.Model):
    __tablename__ = "question_tags"
    questionId = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default = db.func.now())

    
class Answers(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_url = db.Column(db.String, nullable=True)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    votes = db.relationship('Votes', backref='answers')
    
class Formulas(db.Model):
    __tablename__= "formulas"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
class Votes(db.Model):
    __tablename__= "votes"
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer,  db.ForeignKey('answers.id'))    

