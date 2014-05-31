from flask import Flask, render_template, request, jsonify
from json import *
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/admin/')
def admin():
    return render_template("admin.html")
    
app.run(port=int(os.environ['PORT']), debug=True, host='0.0.0.0')