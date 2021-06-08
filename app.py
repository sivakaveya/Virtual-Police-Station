import base64

from flask import Flask, render_template, request, session, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
from datetime import datetime
import os
#import immersive

import speech_recognition as sr
#import pygame
from pygame import mixer
from google_trans_new import google_translator
from gtts import gTTS
import pyttsx3 as tts
from time import sleep


translator = google_translator()
mixer.init()
engine=tts.init()


def translation(s, lang):
    s = translator.translate(s, lang)
    return s

i=0

def speak(text, lang):
    global i
    text = translation(text, lang)
    print(text)
    #engine.say(text)
    #engine.runAndWait()
    speech = gTTS(text,lang=lang)
    if i%2==0:
        with open('file1.mp3','wb') as file:
            speech.write_to_fp(file)
    #speech.save("C:\\Users\\sivaa\\PycharmProjects\\Virtual_Police_Station\\voice.mp3")
        mixer.music.load("file1.mp3")
        mixer.music.play(1)
        sleep(1)
    else:
        with open('file2.mp3','wb') as file:
            speech.write_to_fp(file)
        mixer.music.load('file2.mp3')
        mixer.music.play(1)
        sleep(1)
    i+=1


def speech_recognition():
    r = sr.Recognizer()
    print("Speak a sentence: ")
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, 2, 8)
            text = r.recognize_google(audio)
            return text
        except:
            print("Not Audible!")




app = Flask(__name__)
app.secret_key = "abcd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Virtual_Police_Station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

class Login(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username=username
        self.password=password

class Car(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone=db.Column(db.String(15))
    v_des=db.Column(db.String(200))
    v_no=db.Column(db.String(10))
    v_ls_place=db.Column(db.String(200))
    pincode=db.Column(db.String(10))
    v_ls_date=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    img=db.Column(db.Text)
    mimetype=db.Column(db.Text)
    img_name=db.Column(db.String(300))
    days=db.Column(db.Integer)
    status=db.Column(db.String(20),default="form")
    type=db.Column(db.String(10), default='car')

    def __init__(self, name, phone, v_des, v_no, v_ls_place, pincode, v_ls_date, person_detail, other_detail, img, mimetype, img_name, days):
        self.name=name
        self.phone=phone
        self.v_des=v_des
        self.v_no=v_no
        self.v_ls_place=v_ls_place
        self.pincode=pincode
        self.v_ls_date=v_ls_date
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.img=img
        self.mimetype=mimetype
        self.img_name=img_name
        self.days=days


class Accident(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    date=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    days = db.Column(db.Integer)
    status=db.Column(db.String(20),default="form")

    def __init__(self, name, phone, place, pincode, date, person_detail, other_detail, img, mimetype, img_name, days):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.date=date
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name
        self.days=days


class Woman(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    type_crime=db.Column(db.String(20))
    date=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    days = db.Column(db.Integer)
    status=db.Column(db.String(20),default="form")


    def __init__(self, name, phone, place, pincode, type_crime, date, person_detail, other_detail, witness, img, mimetype, img_name, days):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.type_crime=type_crime
        self.date=date
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name
        self.days=days



class Cyber_crime(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    type_crime=db.Column(db.String(50))
    date=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    status=db.Column(db.String(20),default="form")

    def __init__(self, name, phone, place,pincode, type_crime, date, person_detail, other_detail, witness, img, mimetype, img_name):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.type_crime=type_crime
        self.date=date
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name


class Civil(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    type_crime=db.Column(db.String(50))
    date=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    status=db.Column(db.String(20),default="form")

    def __init__(self, name, phone, place, pincode, type_crime, date, person_detail, other_detail, witness, img, mimetype, img_name):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.type_crime=type_crime
        self.date=date
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name

class Crime(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    type_crime=db.Column(db.String(50))
    date=db.Column(db.String(20))
    #time=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    status=db.Column(db.String(20),default="form")

    def __init__(self, name, phone, place, pincode, type_crime, date, person_detail, other_detail, witness, img, mimetype, img_name):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.type_crime=type_crime
        self.date=date
        #self.time=time
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name

class Common(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    type_crime=db.Column(db.String(50))
    date=db.Column(db.String(20))
    #time=db.Column(db.String(20))
    person_detail=db.Column(db.String(200))
    other_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    status=db.Column(db.String(20),default="form")

    def __init__(self, name, phone, place, pincode, type_crime, date, person_detail, other_detail, witness, img, mimetype, img_name):
        self.name=name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.type_crime=type_crime
        self.date=date
        #self.time=time
        self.person_detail=person_detail
        self.other_detail=other_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name

class Missing(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date_complaint=db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(50))
    phone = db.Column(db.String(15))
    name_missing=db.Column(db.String(50))
    place=db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(10))
    date=db.Column(db.String(20))
    #time=db.Column(db.String(20))
    lastseen=db.Column(db.String(200))
    person_detail=db.Column(db.String(200))
    missing_detail=db.Column(db.String(200))
    witness=db.Column(db.String(200))
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    img_name = db.Column(db.String(300))
    status=db.Column(db.String(20),default="form")
    type=db.Column(db.String(10), default="missing")

    def __init__(self, name, phone, place, pincode, name_missing, age, gender, date, lastseen, person_detail, missing_detail, witness, img, mimetype, img_name):
        self.name = name
        self.phone = phone
        self.place=place
        self.pincode = pincode
        self.name_missing = name_missing
        self.age=age
        self.gender=gender
        self.date=date
        #self.time=time
        self.lastseen=lastseen
        self.person_detail=person_detail
        self.missing_detail=missing_detail
        self.witness=witness
        self.img = img
        self.mimetype = mimetype
        self.img_name = img_name

class Ids(db.Model):
    sr=db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    name = db.Column(db.String(50))
    pincode = db.Column(db.String(10))

    def __init__(self, id, type, name, pincode):
        self.id = id
        self.type = type
        self.name = name
        self.pincode = pincode

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == "POST":



        if request.form.get('login')=='police':
            username = request.form['username']
            password = request.form['password']
            session['username'] = username
            admins = Login.query.all()
            for admin in admins:
                try:
                    if username == admin.username:
                        if password == admin.password:
                            return render_template('home_police.html', login=1)
                        else:
                            return render_template('index.html', credentials_incorrect=1)
                except:
                    return "There is an error in logging in"
        elif request.form.get('login')=='citizen':
            Aadharcardno = request.form['Aadharcardno']
            otpp = request.form['otpp']
            session['aadhar'] = Aadharcardno
            admins = Login.query.all()
            for admin in admins:
                try:
                    if Aadharcardno == admin.username:
                        if otpp == admin.password:
                            return render_template('home_citizen.html', login=1, conplaint_id="None")
                        else:
                            return render_template('index.html', credentials_incorrect=1)
                except:
                    return "There is an error in logging in"



    else:
        return render_template('index.html', credentials_incorrect=0)


#####POLICE CODE#####
@app.route('/home_police', methods=['GET', 'POST'])
def home_police():
    if 'username' in session:
        if request.method == "POST":
            if request.form.get("form_name") == 'car':

                complaints = Car.query.all()
                #date_format = "%Y-%m-%d"
                #a = datetime.strptime(complaints.v_ls_date[0:10], date_format)
                #b = complaints.date_complaint
                #delta = b - a
                #print(delta.days)
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'accident':
                complaints = Accident.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'woman':
                complaints = Woman.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'cyber':
                complaints = Cyber_crime.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'civil':
                complaints = Civil.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'crime':
                complaints = Crime.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'common':
                complaints = Common.query.all()
                return render_template('view_complaint.html', complaints=complaints)
            elif request.form.get("form_name") == 'missing':
                complaints = Missing.query.all()
                return render_template('view_complaint.html', complaints=complaints)


        else:
            return render_template('home_police.html', login=1)

    else:
        return redirect(url_for('index'))


@app.route('/view_complaint', methods=['GET', 'POST'])
def view_complaint():
    if 'username' in session:   #check if the username is in session logged in
        if request.method == "POST":      #check is there is post req ie to see if any button is clicked or not
            view_id = request.form.get("view")
            ids = Ids.query.filter_by(id=view_id).first()

            #checking the type of the complaint
            if ids.type == 'car':
                details = Car.query.filter_by(id = view_id).first()

                img=send_file(BytesIO(details.img), as_attachment=True, attachment_filename=details.img_name, mimetype=details.mimetype)
                with open(details.img_name,'wb') as f:
                    f.write(details.img)


                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    #pic= 'C:\Users\sivaa\PycharmProjects\Virtual_Police_Station\ '+ details.img_name
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'accident':
                details = Accident.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'woman':
                details = Woman.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'cyber_crime':
                details = Cyber_crime.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'civil':
                details = Civil.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'crime':
                details = Crime.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'common':
                details = Common.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

            elif ids.type == 'missing':
                details = Missing.query.filter_by(id = view_id).first()
                if details.status == "form":
                    details.status = 'viewed'
                    db.session.commit()
                    return render_template('view_individual.html', details=details, status='viewed')
                elif details.status == 'verified':
                    return render_template('view_individual.html', details=details, status='verified')
                elif details.status == 'registered':
                    return render_template('view_individual.html', details=details, status='registered')
                else:
                    return render_template('view_individual.html', details=details, status='case_closed')

        else:
            return render_template('view_complaint.html', complaints=None)
    else:
        return redirect(url_for('index'))

@app.route('/view', methods=['POST','GET'])
def view():
    if 'username' in session:
        if request.method == 'POST':
            update_id=request.form['id_form']
            if (int(update_id)>=1000) and (int(update_id)<=1999):
                details = Car.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=2000) and (int(update_id)<=2999):
                details = Accident.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=3000) and (int(update_id)<=3999):
                details = Woman.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=4000) and (int(update_id)<=4999):
                details = Cyber_crime.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=5000) and (int(update_id)<=5999):
                details = Civil.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=6000) and (int(update_id)<=6999):
                details = Crime.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=7000) and (int(update_id)<=7999):
                details = Common.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()
            elif (int(update_id)>=8000) and (int(update_id)<=8999):
                details = Missing.query.filter_by(id=update_id).first()
                if request.form.get('btn') == 'verify':
                    details.status = 'verified'
                    db.session.commit()
                elif request.form.get('btn') == 'register':
                    details.status = 'registered'
                    db.session.commit()
                else:
                    details.status = 'case_closed'
                    db.session.commit()


            return redirect(url_for('home_police',login=0))



        else:
            return render_template('view_individual.html', details=None)

    else:
        return redirect(url_for('index'))


#######START OF VICTIM SIDE#####
@app.route('/home_victim')
def home_victim():
    if 'aadhar' in session:
        return render_template('home_citizen.html', login=0, complaint_id="None")


    else:
        return redirect(url_for('index'))

@app.route('/car_missing', methods=['POST', 'GET'])
def car():
    if 'aadhar' in session:

        if (request.method=="POST") and (request.form.get("lang") == "lang"):
            c=request.form["language"]
            print(c)
            session['language']=c
        elif (request.method=="POST"):
            #if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
        if (request.method == 'POST') and (request.form.get("mic")=="name"):
            name = speech_recognition()
            print(name)
            return render_template("vehicle.html", name=name)

        if (request.method == 'POST') and (request.form.get("mic") == "des"):
            name=request.form['name']
            no=request.form['phone']
            des = speech_recognition()
            print(des)
            return render_template("vehicle.html", des=des, name=name, phone=no)

        if (request.method == 'POST') and (request.form.get("mic") == "v_ls_place"):
            name = request.form['name']
            print(name)
            no = request.form['phone']
            des = request.form['v_des']
            v_no=request.form['v_no']


            v_ls_place=speech_recognition()
            print(des)
            return render_template("vehicle.html", des=des, name=name, phone=no,v_no=v_no, v_ls_place=v_ls_place)

        if (request.method == 'POST') and (request.form.get("mic") == "des_per"):
            name = request.form['name']
            no = request.form['phone']
            des = request.form['v_des']
            v_no = request.form['v_no']
            v_ls_place = request.form['v_ls_place']
            pincode=request.form['pincode']
            date=request.form['date']
            des_per=speech_recognition()

            print(des)
            return render_template("vehicle.html", des=des, name=name, phone=no, date=date, v_no=v_no, v_ls_place=v_ls_place, des_per=des_per, pincode=pincode)

        if (request.method == 'POST') and (request.form.get("mic") == "des_other"):
            name = request.form['name']
            no = request.form['phone']
            des = request.form['v_des']
            v_no = request.form['v_no']
            v_ls_place = request.form['v_ls_place']
            pincode = request.form['pincode']
            date = request.form['date']
            des_per = request.form['person_detail']
            des_other=speech_recognition()

            print(des)
            return render_template("vehicle.html", des=des, name=name, phone=no, date=date, v_no=v_no, v_ls_place=v_ls_place, des_per=des_per, pincode=pincode, des_other=des_other)
            #elif request.form.get("immersive") == "Contact":
                #immersive.speak("Contact number", session['language']) it worked once


        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            print(name)
            phone=request.form['phone']
            print(phone)
            v_des=request.form['v_des']
            print(v_des)
            v_no=request.form['v_no']
            v_ls_place=request.form['v_ls_place']
            pincode=request.form['pincode']
            v_ls_date=request.form['v_ls_date']
            print(v_ls_date)
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            img = request.files['img']
            filename = secure_filename(img.filename)
            print(filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            #print(name)

            new_entry=Car(name=name, phone=phone, v_des=v_des, v_no=v_no, v_ls_place=v_ls_place, pincode=pincode, v_ls_date=v_ls_date, person_detail=person_detail, other_detail=other_detail, img=img.read(), mimetype=mimetype, img_name=filename, days=0)

            #try:
            db.session.add(new_entry)
            db.session.commit()
            #details = Car.query.filter_by(v_des=v_des).first()
            details = Car.query.order_by(Car.id.desc()).first()
            date_format = "%Y-%m-%d"
            a = datetime.strptime(details.v_ls_date[0:10], date_format)
            b = details.date_complaint
            delta = b - a
            details.days=delta.days
            db.session.commit()
            #days=Car(days=delta.days)
            #db.session.query(Car).order_by(Car.id.desc()).first().update({Car.days: delta.days}, synchronize_session=False)

            new_entry_id = Ids(id=details.id, name=name, type='car', pincode=pincode)
            db.session.add(new_entry_id)
            db.session.commit()
            return render_template('home_citizen.html', complaint_id=details.id, login=0)
            #except:
                #return "There is an error in sending the form"

        else:
            return render_template('vehicle.html')
    else:
        return redirect(url_for('index'))

@app.route('/road_accident', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def road_accident():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once

        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            date=request.form['date']
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            img = request.files['img']
            filename = secure_filename(img.filename)
            print(filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Accident(name=name, phone=phone, place=place, pincode=pincode, date=date, person_detail=person_detail, other_detail=other_detail, img=img.read(), mimetype=mimetype, img_name=filename, days=0)

            #try:
            db.session.add(new_entry)
            db.session.commit()
            details = Accident.query.order_by(Accident.id.desc()).first()
            date_format = "%Y-%m-%d"
            a = datetime.strptime(details.date[0:10], date_format)
            b = details.date_complaint
            delta = b - a
            details.days = delta.days
            db.session.commit()
            new_entry_id = Ids(id=details.id, name=name, type='accident', pincode=pincode)
            db.session.add(new_entry_id)
            db.session.commit()
            return render_template('home_citizen.html', complaint_id=details.id, login=0)
            #except:
                #return "There is an error in sending the form"

        else:
            return render_template('road_accident.html')
    else:
        return redirect(url_for('index'))

@app.route('/woman', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def woman():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once

        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
                name=request.form['name']
                phone=request.form['phone']
                place=request.form['place']
                pincode = request.form['pincode']
                type_crime = request.form['type_crime']
                date=request.form['date']
                person_detail=request.form['person_detail']
                other_detail=request.form['other_detail']
                witness=request.form['witness']
                img = request.files['img']
                filename = secure_filename(img.filename)
                mimetype = img.mimetype
                target = os.path.join(APP_ROOT, 'static/images/')
                destination = "/".join([target, filename])
                img.save(destination)
                new_entry=Woman(name=name, phone=phone, place=place, pincode=pincode, type_crime=type_crime, date=date, person_detail=person_detail, other_detail=other_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename, days=0)

                #try:
                db.session.add(new_entry)
                db.session.commit()
                details = Woman.query.order_by(Woman.id.desc()).first()
                date_format = "%Y-%m-%d"
                a = datetime.strptime(details.date[0:10], date_format)
                b = details.date_complaint
                delta = b - a
                details.days = delta.days
                db.session.commit()
                new_entry_id = Ids(id=details.id, name=name, type='woman', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
                #except:
                    #return "There is an error in sending the form"

        else:
            return render_template('woman.html')
    else:
        return redirect(url_for('index'))

@app.route('/cyber_crime', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def cyber_crime():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once
        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            type_crime=request.form['type_crime']
            date=request.form['date']
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            witness=request.form['witness']
            img = request.files['img']
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Cyber_crime(name=name, phone=phone, place=place,pincode=pincode, type_crime=type_crime, date=date, person_detail=person_detail, other_detail=other_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename)

            try:
                db.session.add(new_entry)
                db.session.commit()
                details = Cyber_crime.query.order_by(Cyber_crime.id.desc()).first()
                new_entry_id = Ids(id=details.id, name=name, type='cyber_crime', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
            except:
                return "There is an error in sending the form"

        else:
            return render_template('cyber.html')
    else:
        return redirect(url_for('index'))

@app.route('/civil', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def civil():
    if 'aadhar' in session:
        if (request.method=="POST") and (request.form.get("lang") == "lang"):
            c=request.form["language"]
            print(c)
            session['language']=c
        elif (request.method=="POST"):
            #if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            #elif request.form.get("immersive") == "Contact":
                #immersive.speak("Contact number", session['language']) it worked once
        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            type_crime = request.form['type_crime']
            date=request.form['date']
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            witness=request.form['witness']
            img = request.files['img']
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Civil(name=name, phone=phone, place=place, pincode=pincode,type_crime=type_crime, date=date, person_detail=person_detail, other_detail=other_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename)

            try:
                db.session.add(new_entry)
                db.session.commit()
                details = Civil.query.order_by(Civil.id.desc()).first()
                new_entry_id = Ids(id=details.id, name=name, type='civil', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
            except:
                return "There is an error in sending the form"

        else:
            return render_template('civil.html')
    else:
        return redirect(url_for('index'))

@app.route('/crime', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def crime():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once
        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            type_crime = request.form['type_crime']
            date=request.form['date']
            #time=request.form['time']
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            witness=request.form['witness']
            img = request.files['img']
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Crime(name=name, phone=phone, place=place, pincode=pincode,type_crime=type_crime, date=date, person_detail=person_detail, other_detail=other_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename)

            try:
                db.session.add(new_entry)
                db.session.commit()
                details = Crime.query.order_by(Crime.id.desc()).first()
                new_entry_id = Ids(id=details.id, name=name, type='crime', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
            except:
                return "There is an error in sending the form"

        else:
            return render_template('crime.html')
    else:
        return redirect(url_for('index'))

@app.route('/common', methods=['POST', 'GET']) # name, phone, place, date, person_detail, other_detail, witness)
def common():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once
        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            type_crime = request.form['type_crime']
            date=request.form['date']
            #time=request.form['time']
            person_detail=request.form['person_detail']
            other_detail=request.form['other_detail']
            witness=request.form['witness']
            img = request.files['img']
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Common(name=name, phone=phone, place=place, pincode=pincode,type_crime=type_crime, date=date, person_detail=person_detail, other_detail=other_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename)

            try:
                db.session.add(new_entry)
                db.session.commit()
                details = Common.query.order_by(Common.id.desc()).first()
                new_entry_id = Ids(id=details.id, name=name, type='common', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
            except:
                return "There is an error in sending the form"

        else:
            return render_template('common.html')
    else:
        return redirect(url_for('index'))

@app.route('/missing', methods=['POST', 'GET']) # name, phone, place, name_missing, age, gender, date, time, lastseen, person_detail, missing_detail, witness
def missing():
    if 'aadhar' in session:
        if (request.method == "POST") and (request.form.get("lang") == "lang"):
            c = request.form["language"]
            print(c)
            session['language'] = c
        elif (request.method == "POST"):
            # if request.form.get("immersive") == "Name of owner":
            speak(request.form.get("immersive"), session['language'])
            # elif request.form.get("immersive") == "Contact":
            # immersive.speak("Contact number", session['language']) it worked once
        if (request.method == 'POST') and (request.form.get("submit") == "submit"):
            name=request.form['name']
            phone=request.form['phone']
            place=request.form['place']
            pincode = request.form['pincode']
            name_missing=request.form['name_missing']
            age = request.form['age']
            gender=request.form['gender']
            date=request.form['date']
            #time=request.form['time']
            lastseen=request.form['lastseen']
            person_detail=request.form['person_detail']
            missing_detail=request.form['other_detail']
            witness=request.form['witness']
            img = request.files['img']
            filename = secure_filename(img.filename)
            mimetype = img.mimetype
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/".join([target, filename])
            img.save(destination)
            new_entry=Missing(name=name, phone=phone, place=place, pincode=pincode, name_missing=name_missing, age=age, gender=gender, date=date, lastseen=lastseen,  person_detail=person_detail, missing_detail=missing_detail, witness=witness, img=img.read(), mimetype=mimetype, img_name=filename)

            try:
                db.session.add(new_entry)
                db.session.commit()
                details = Missing.query.order_by(Missing.id.desc()).first()
                new_entry_id = Ids(id=details.id, name=name, type='missing', pincode=pincode)
                db.session.add(new_entry_id)
                db.session.commit()
                return render_template('home_citizen.html', complaint_id=details.id, login=0)
            except:
                return "There is an error in sending the form"

        else:
            return render_template('report_missing_person.html')
    else:
        return redirect(url_for('index'))

@app.route('/select_complaint', methods=['GET', 'POST'])
def select_complaint():
    if 'aadhar' in session:
        if request.method == "POST":
            status_id=request.form.get('view')
            if (int(status_id)>=1000) and (int(status_id)<=1999):
                details = Car.query.filter_by(id=status_id).first()
                return render_template('status.html', details=details)
            elif (int(status_id)>=2000) and (int(status_id)<=2999):
                details = Accident.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=3000) and (int(status_id)<=3999):
                details = Woman.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=4000) and (int(status_id)<=4999):
                details = Cyber_crime.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=5000) and (int(status_id)<=5999):
                details = Civil.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=6000) and (int(status_id)<=6999):
                details = Crime.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=7000) and (int(status_id)<=7999):
                details = Common.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            elif (int(status_id)>=8000) and (int(status_id)<=8999):
                details = Missing.query.filter_by(id=status_id).first()
                return render_template('status.html', details = details)
            return 'Problem'
        else:
            details = Ids.query.filter_by(name=session['aadhar']).all()
            return render_template('select_complaint.html', details=details)

    else:
        return redirect(url_for('index'))

@app.route('/status')
def status():
    if 'aadhar' in session:
        return render_template('status.html', status='None')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
