from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    password = fields.Str()
    
class VotesSchema(Schema):
    id = fields.Int(required=False)
    answer_id = fields.Int()
    votes_count = fields.Int(required=False)
    

class AnswersSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    question_id = fields.Int()
    image_url = fields.Str()
    text = fields.Str()
    votes = fields.List(fields.Nested(VotesSchema))
    
class QuestionsSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    image_url = fields.Str()
    text = fields.Str()
    answers = fields.List(fields.Nested(AnswersSchema))
    


    
user_schema = UserSchema()
quest_schema = QuestionsSchema()
ans_schema = AnswersSchema()
votes_schema = VotesSchema()