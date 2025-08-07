from flask import  request, jsonify
from flask_sqlalchemy import SQLAlchemy
import app
from models import Users,  Questions, Answers, Votes
from flask_restful import Resource, Api, reqparse
from dotenv import load_dotenv
import os, cloudinary
import cloudinary.uploader
import cloudinary
from pix2text import Pix2Text
import requests
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, create_refresh_token
from serializer import quest_schema, votes_schema
from sqlalchemy import func
import json
load_dotenv()
from websockets.asyncio.server import serve
from app import redis_client, db, bcrypt , api, create_app, sock, pagination, jwt
import gevent
from pagination import Pagination
from datetime import timedelta
cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))

@sock.route('/upvote')
def handler(websocket):
    while True:
        try:
                count_with_ans_id = websocket.receive()#array of counter and answer id
                print(count_with_ans_id)
                answer_id, count = json.loads(count_with_ans_id)
                if count > 0: 
                #insert vote count
                    new_vote = Votes(answer_id = answer_id)
                    new_vote.update_data_in_cache()
            
                new_count = redis_client.get('ans'+str(answer_id))
                if new_count: 
                    websocket.send(new_count)
                else:
                    new_count = redis_client.set('ans'+str(answer_id), 0)
                    websocket.send(new_count)                                  

        except Exception as e:
                websocket.send(json.dumps(
                        
                        str(e)
                    ))
                

class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        acces_token  = create_access_token(identity=identity)
        return jsonify({'access_token': acces_token})
    
class TokenBlacklistResource(Resource):

    @jwt_required()
    def post(self):
            token = get_jwt()['jti']
            redis_client.set(token,'', ex=timedelta(hours=1) )
            return token is not None

class SingleQuestionResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('question_id', type = int, required = True, help = 'No question identifier provided')
        super(SingleQuestionResource, self).__init__()
        
    def get(self, question_id):
        try:
            if (question_id):
                questions = quest_schema.dump(Questions.query.filter_by(id=question_id).first())
            return { 'message' : "Questions fetched successfully" , 'data' : questions}, 200

        except Exception as e:
            raise e
        

class QuestionResource(Resource):
    @jwt_required()
    def post(self):
        try:
            user_name = get_jwt_identity()

            user = Users.query.filter_by(name=user_name).first()
            if user: 
                upload_file =  request.files['file'] 
                if (upload_file ) : 
                    
                    upload_result = cloudinary.uploader.upload(upload_file)
                    url_ = upload_result['secure_url']
                    local_path = download_image_from_url(url_, "temp_math_image.png")

                    text = text_from_image(local_path)
                    image_url = url_
                    question = Questions(user_id=user.id,image_url= image_url, text=text )
                    question_exists = Questions.query.filter_by(text=text).first()
                    if not question_exists:
                        db.session.add(question)
                        db.session.commit()
                        
                        response = jsonify({"message": "Question uploaded successfully", 'data' : [question.text,question.image_url]})
                        response.status_code = 201
                        return response    
                    response = jsonify({"message": "Question exists", 'data' : [question_exists.text,question_exists.image_url]})
                    response.status_code = 200
                    return response  
                
            else:
                return jsonify({"message": "Error user not found with the provided credentials", "data": []})
        except Exception as e:
            print(e)
            raise e
    
    def get(self):
        try:
            import sqlalchemy as sa
            
            query = sa.select(Questions).order_by(Questions.created_at.desc())
            page = request.args.get("page", type = int)
            if (page) :
                instance_pagination = Pagination()
                question_data = instance_pagination.paginate(query, page)
                questions = quest_schema.dump(question_data.items,many=True)

                
                response = {"message": "Questions loaded successfully", 
                            'data' : questions, 
                            'next_page_data': quest_schema.dump((instance_pagination.paginate(query, question_data.next_num).items),many=True),
                            'prev_page_data': quest_schema.dump(instance_pagination.paginate(query, question_data.prev_num).items, many=True )}, 200
                return response   

        except Exception as e:
            raise e
        

class AnswersResource(Resource):
    @jwt_required()
    def post(self):
        try:
            user_name = get_jwt_identity()
            # app.logger.info(f'request{user_name}')

            user = Users.query.filter_by(name=user_name).first()
            if user: 
                upload_file =  request.files['file'] 
                if (upload_file ) : 
                    
                    upload_result = cloudinary.uploader.upload(upload_file)
                    url_ = upload_result['secure_url']
                    local_path = download_image_from_url(url_, "temp_math_image.png")

                    text = text_from_image(local_path)
                    question = request.form.get('question_id')
                    image_url = url_
                    answer = Answers(user_id=user.id,question_id=question,image_url= image_url, text=text )
                    answer_exists = Answers.query.filter_by(text=text).first()
                    if not answer_exists:
                        db.session.add(answer)
                        db.session.commit()
                                
                        # app.logger.info(f'request{request.form.get("question")}')
                        response = jsonify({"message": "Answer uploaded successfully", 'data' : [answer.text,answer.image_url]})
                        response.status_code = 201
                        return response    
                    response = jsonify({"message": "Answer exists", 'data' : [answer_exists.text,answer_exists.image_url]})
                    response.status_code = 200
                    return response  
                    
                    
            else:
                response = jsonify({"message": "Error user not found with the provided credentials", "data": []})
                response.status_code = 400
                return response  
        except Exception as e:
            raise e
        
    def get(self):
        try:
            answers = Answers.query.all()
            answers_list = [ {"id": ans.id,"text": ans.text, "image_url": ans.image_url, "question_id": ans.question_id}  for ans in answers]      
            response = jsonify({"message" : "Answers fetched successfully", "data" : answers_list})
            response.status_code = 200
            return response

        except Exception as e:
            raise e
        
        
        
class VotingTrackerResource(Resource):
    def post(self):
        answer_id = request.form.get('answer_id')
        answer_exist = Answers.query.filter_by(id=answer_id).first()
        app.logger.info(f"here{answer_id}")
        if  answer_exist:
            vote = Votes(answer_id=answer_exist.id)
            try:
                db.session.add(vote)
                db.session.commit()
                response = votes_schema.dump(vote)
                return response, 201
            except Exception as e:
                raise e
        else :
            response = jsonify({"message": "Can't upvote, Answer record does not exist"})
            response.status = 400
            return response

    def get(self):
        try:
            if redis_client.keys("*ans*"):
                all_vote_records = Votes.query.all()
                for vote in all_vote_records:
                    key_name = 'ans'+str(vote.answer_id)
                    if key_name not in  redis_client.keys("*ans*"):
                        vote_count = db.session.query(
                            func.count(Votes.id)
                        ).filter_by(answer_id=vote.answer_id).all()
                        
                        redis_client.set(key_name, vote_count)
                    
                data = [{'answer_id': int(key[3:]), 'votes_count': int(redis_client.get(key))} for key in redis_client.keys("*ans*")]
                response = votes_schema.dump(data, many=True)
                return response
        
        except Exception as e:
            raise e
        
class UserResource(Resource):
    def check_user_exist(self, username):
        user = Users.query.filter_by(name=username).first()
        return user is not None
    def get(self):
        try:
            users = Users.query.all()
            user_list = [ {"name": user.name} for user in users]
            return {"message": "Users fetched successfully", "data": user_list}, 200
        except Exception as e:
            raise e
    
    def post(self):
        
        if (request.args.get("login")) :
            data = request.get_json()
            password = data.get("password")
            name = data.get("name")
            try:
                user = Users.query.filter_by(name=name).first()
                if (user and bcrypt.check_password_hash(user.password, password) ):
                    access_token = create_access_token(identity=user.name)
                    refresh_token = create_refresh_token(identity=user.name)
                    return {'message': 'Login Success', 'data': access_token, 'refresh_token' : refresh_token} , 200                 
            except Exception as e:
                raise e
        else:
            password = request.form.get("password")
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            username = request.form.get("name")
            exist_user = self.check_user_exist(username)
            if (not exist_user):
                user = Users(name=request.form.get("name"), password=hashed_password)
                
                try:
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({"message": "User created successfully", "user": user.name})
                except Exception as e:
                    raise e
            response = jsonify({"message": "User with name exists"})
            response.status_code = 400
            return response
                


def clean_latex_output(raw_latex: str) -> str:
    cleaned = raw_latex.strip()
    if cleaned.startswith("$$"):
        cleaned = cleaned[2:]
    if cleaned.endswith("$$"):
        cleaned = cleaned[:-2]

    cleaned = cleaned.replace("\n", " ").strip()

    cleaned = re.sub(r'\\textbf\{(.*?)\}', r'\1', cleaned)

    cleaned = re.sub(r'(?<=\w) (?=\w)', '', cleaned)  

    return cleaned.strip()

    


def text_from_image(img):
    p2t = Pix2Text.from_config()
    outs = p2t.recognize_text_formula(img, resized_shape=768, return_text=True)
    os.remove(img) 
    return clean_latex_output(outs)

def download_image_from_url(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    else:
        raise Exception("Failed to download image")

api.add_resource(QuestionResource, '/questions')
api.add_resource(SingleQuestionResource,'/questions/<int:question_id>')
api.add_resource(AnswersResource, '/answers')
api.add_resource(VotingTrackerResource, '/votes')
api.add_resource(UserResource, '/users')
api.add_resource(TokenRefreshResource, '/users/refresh')
api.add_resource(TokenBlacklistResource, '/logout')
