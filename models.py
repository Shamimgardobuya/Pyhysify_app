from app import db, redis_client
from sqlalchemy import func

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
    
    def update_data_in_cache(self):
        try:
            db.session.add(self)
            db.session.commit()

            new_total_vote_count = db.session.query(
                    func.count(Votes.id)
                ).filter_by(answer_id = self.answer_id).scalar()
            
            redis_client.set('ans'+str(self.answer_id), new_total_vote_count)
            return new_total_vote_count
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()

