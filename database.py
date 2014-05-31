from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(100), nullable=True)
    
    def __init__(self, parent, ip):
        self.parent = parent
        self.ip_address = ip
    
    def __repr__(self):
        return '<User(parent=%s, ip_address=%s)>' % (self.parent, self.ip_address)
    
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('responses', lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question',
        backref=db.backref('responses', lazy='dynamic'))
    answer = db.Column(db.String(1000)) # Should be JSON

    def __init__(self, user_id, question_id, answer):
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer
        
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(100))
    data = db.Column(db.String(1000))
    title = db.Column(db.String(100), unique=True)
    
    def __init__(self, type, title, data):
        self.type = type
        self.title = title
        self.data = data
    
    def __repr__(self):
        return '<Question(id=%d, type=%s, data=%s, title=%s)>' % (self.id, self.type, str(self.data), self.title)
    
    __str__ = __repr__
