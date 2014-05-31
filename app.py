from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from json import *
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://starlight:starlight@localhost/starlight'
db = SQLAlchemy(app)
db.session.rollback()

if __name__ == '__main__':
    from database import User, Question, Response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/admin')
def admin():
    questionss= Question.query.all()
    questions = {}
    for i in questionss:
        questions[i.id] = loads(i.data)
    u = User.query.all()
    udict = {}
    for i in u:
        udict[i] = Response.query.filter(Response.user_id == i.id).all()
    udict2 = {}
    for i in udict:
        templist = []
        for j in udict[i]:
            templist.append({"question_id": j.question_id, "answer": loads(str(j.answer))})
        udict2[i] = templist
    return render_template('admin.html', i=udict2, q=questions)
    
def jsonify2(error_code, **x):
    # Return a response with an error code set
    resp = jsonify(**x)
    resp.status_code = error_code
    return resp

def err(code, desc, **x):
    return jsonify2(code, error=True, description=desc, **x)

@app.route('/endpoint', methods=['POST'])
def endpoint():
    # Should be passed a dictionary
    # request holds type of request
    # 'request'='submit' means that a form is being submitted - 'data' should have the responses
    req = request.get_json(force=True)
    print(req)
    if not req:
        return err(400, 'Expected valid JSON data')
    if 'request' not in req:
        return err(400, 'No request type specified.')
    if req['request'] == 'submit':
        if 'data' not in req:
            return err(400, 'No data specified.')
        d = req['data']
        try:
            u = User(parent=False, ip=request.remote_addr)
            db.session.add(u)
            db.session.commit()
            for title, answer in d['questions']:
                q = Question.query.filter(Question.title==title).one()
                print(repr(q))
                
                resp = Response(user_id=u.id, question_id=q.id, answer=dumps(answer))
                db.session.add(resp)
                db.session.commit()
            return jsonify(error=False, success=True)
        except Exception as e:
            return err(400, repr(e))
    elif req['request'] == 'getstats':
        questions = Question.query.all()
        questions_ret = {}
        for q in questions:
            q2 = {}
            q2['id'] = q.id
            q2['type'] = q.type
            q2['data'] = loads(q.data)
            q2['responses'] = []
            for response in q.responses.all():
                resp = {}
                resp['user'] = response.user_id
                resp['answer'] = loads(response.answer)
                q2['responses'].append(resp)
            questions_ret[q.title]=q2
        return jsonify(error=False, questions=questions_ret)
            
    else:
        return err(400, 'Invalid request type.')
    

if __name__ == '__main__':
    app.run(port=int(os.environ['PORT']), debug=True, host='0.0.0.0')