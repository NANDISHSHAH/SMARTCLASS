from flask import Flask, render_template, redirect, flash, url_for, jsonify
from flask import request
import processor
import json
import pickle
import numpy as np
import re
import os
from docs import document
from sentients import review,summary
from werkzeug.utils import secure_filename
import pymongo

pos = 0
neg = 0
l=[]
s=[]
URI = "mongodb+srv://kadamsolanki:kadavani00@cluster0.a8two.mongodb.net/symbalfeed?retryWrites=true&w=majority"
Client = pymongo.MongoClient(URI)
db = Client['symbalfeed']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 's#12qdqwjqlwehehleje'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video')
def video():
    return render_template("video.html")


@app.route('/chat', methods=["GET", "POST"])
def indexs():
    return render_template('chatbot.html', **locals())


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']
        print(the_question)
        response = processor.chatbot_response(the_question)
        print(response)
    return jsonify({"response": response})


@app.route('/feed', methods=["GET", "POST"])
def feed():
    pos=db.feeds.count_documents({'sentiment':'POSITIVE'})
    neg=db.feeds.count_documents({'sentiment':'NEGATIVE'})
    return render_template('feed.html',count=pos,count2=neg)


@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    feeds = db.feeds  # database table name
    name1 = request.form.get('name')
    id1 = request.form.get('id')
    sub1 = request.form.get('subject')
    feedback1 = request.form.get('feedbacks')
    sentiment = review(feedback1)

    if request.method == 'POST':
        feeds.insert_one({'Lecturer id': id1, 'Subject': sub1, 'feedback': feedback1,
                         'sentiment': sentiment})  # insert into database mongo db
      
        pos=db.feeds.count_documents({'sentiment':'POSITIVE'})
        neg=db.feeds.count_documents({'sentiment':'NEGATIVE'})

        return render_template('feed.html',count=pos,count2=neg)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/upload', methods=["GET", "POST"])
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        path1 = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #transcript
        longtext = document(filename)
        # sum1=summary(longtext)
        l.clear()
        l.append(longtext)
        # print(longtext)
        s.clear()
        sum1=summary(longtext)
        s.append(sum1)

        # transcript(longtext)
        print('upload_video filename: ' + filename)
        flash('Video successfully uploaded and displayed below')
        return render_template('video.html',filename=filename)

@app.route('/trans', methods=["GET", "POST"])
def transcript():
    if request.method == 'POST':

        return render_template('para.html',transc=l,summ=s)
   

# @app.route('/summ', methods=["GET", "POST"])
# def summary():
#     if request.method == 'POST':

#         return render_template('para.html',summary=s)

@app.route('/display/<filename>')
def display_video(filename):
    print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":

    app.run(debug=False)
