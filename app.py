import email
from ntpath import realpath
from operator import index, le
import os, requests
import queue
from re import T
from tokenize import Double
from unittest import result
from wsgiref import validate
from unicodedata import category, name
import smtplib
import jwt
import string
from datetime import date, datetime, timedelta
from flask import Flask, request, abort, jsonify, json
import asyncio
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import Boolean, Column, asc, asc, desc
import math
import random
import pyrebase
from flask_migrate import Migrate
from sqlalchemy.sql.expression import delete, true
from werkzeug.utils import secure_filename
from email.message import EmailMessage
from firebase_admin import storage as admin_storage, credentials, firestore
import firebase_admin
# __________________________________________________________________________________________

# DATABASE CONNECTION
# __________________________________________________________________________________________
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:youssef@localhost:5432/neoncrm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Q8bM!@NKJniUUYTVlknjh+_/$&JoE$Albert$&Nour'
db = SQLAlchemy(app)
CORS(app)
migrate = Migrate(app, db)
# __________________________________________________________________________________________

# FIREBASE CONNECTION
# __________________________________________________________________________________________

Config = {
    "apiKey": "AIzaSyBsQNofO3tv0EM8BqYds8uyr3ieyM-cumE",
    "authDomain": "neoncrm-3ade1.firebaseapp.com",
    "databaseURL": "https://neoncrm-3ade1-default-rtdb.firebaseio.com",
    "projectId": "neoncrm-3ade1",
    "storageBucket": "neoncrm-3ade1.appspot.com",
    "serviceAccount": "connection.json"
}

cred = credentials.Certificate(json.load(open('connection.json')))
admin = firebase_admin.initialize_app(cred, {
    'storageBucket': 'neoncrm-3ade1.appspot.com'})

firabase_storage = pyrebase.initialize_app(Config)
storage = firabase_storage.storage()
bucket = admin_storage.bucket()

# __________________________________________________________________________________________

# DATABASE CREATE
# __________________________________________________________________________________________
class Department(db.Model):
    __tablename__ = 'department'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Offs(db.Model):
    __tablename__ = 'offs'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def format(self):
        x = {
            

            "id": self.id,
            "start": self.start ,
            "end": self.end ,
            "type":self.type
            
        }
        return x
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String)
    end = db.Column(db.String)
    type = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class Submit(db.Model):
    __tablename__ = 'submit'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    task_id = db.Column(db.String)

class Task_relpy(db.Model):
    __tablename__ = 'task_relpy'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    reply = db.Column(db.String)
    task_real_id = db.Column(db.String)

class Employee(db.Model):
    __tablename__ = 'employee'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        department_name = Department.query.get(self.department_id).name
        x = {
            

            "id": self.id,
            "name": self.name ,
            "department":department_name
            
        }
        return x

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String)
    name = db.Column(db.String)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    receive_id = db.relationship('Receive', backref='Employee', lazy=True)


class Request(db.Model):
    __tablename__ = 'request'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        x = {
            

            "subject": self.subject ,
            "description":self.description ,
            "action_by":self.action_by ,
            "status":self.status ,
            "real_id":self.real_id 
            
        }
        return x

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    description = db.Column(db.String)
    action_by  = db.Column(db.String)
    reply  = db.Column(db.String)
    status = db.Column(db.String)
    real_id = db.Column(db.String)
    date = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    react_id = db.relationship('React', backref='Request', lazy=True)

    
class React(db.Model):
    __tablename__ = 'react'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()


    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    action = db.Column(db.Boolean, unique=False , default=False)
    request_real_id = db.Column(db.String)
    date =  db.Column(db.String)

class Admin(db.Model):
    __tablename__ = 'admin'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(120))
    name = db.Column(db.String(120))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    react_id = db.relationship('React', backref='Admin', lazy=True)


     
class Ticket(db.Model):
    __tablename__ = 'ticket'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def format(self):
        daata = Ticket.query.filter_by(real_id=self.real_id).all()
        for i in daata:
            if i.admin_id:
                admin_id=i.admin_id
                break
            else:
                admin_id=23456789
        admin_name = Admin.query.filter_by(id=admin_id).first()
        if admin_name:
            took_by=admin_name.name
        else:
            took_by = 'waiting'
        x = {
            

            "subject": self.subject ,
            "description":self.description ,
            "action_by":self.action_by ,
            "status":self.status ,
            "took_by":took_by ,
            "date":self.date,
            "real_id":self.real_id 
            
        }
        return x
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    description = db.Column(db.String)
    action_by  = db.Column(db.String)
    status = db.Column(db.String)
    reply  = db.Column(db.String)
    file  = db.Column(db.String)
    real_id = db.Column(db.String)
    date =  db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)

class Receive(db.Model):
    __tablename__ = 'receive'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()


    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    date =  db.Column(db.String)
    receive_date =  db.Column(db.String)
    task_real_id = db.Column(db.String)
    received = db.Column(db.Boolean, unique=False , default=False)

class Task(db.Model):
    __tablename__ = 'task'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'), nullable=False)
    title = db.Column(db.String)
    todo = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    files = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    real_id = db.Column(db.String)
    status = db.Column(db.String)
    date =  db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    receive_id = db.relationship('Receive',backref='Task',lazy=True)

class Queue(db.Model):
    __tablename__ = 'queue'

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

# __________________________________________________________________________________________

# API ACCESS

# __________________________________________________________________________________________

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
#     response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
#     return response
# __________________________________________________________________________________________

# LOGIN

# __________________________________________________________________________________________
@app.route('/admin_login', methods=['POST'])
def admin_login():
    take=request.get_json()
    if not (take.get('uid')):
        abort(422)
    uid = take.get('uid', "")
    # try:
    user = Admin.query.filter_by(uid=uid).all()
    emp = Employee.query.all()
    req = Request.query.all()
    q= Queue.query.all()
    tick = Ticket.query.all()
    dep = Department.query.all()
    tak = Task.query.all()
    if user :
        if not q :
            add_fake_title = Queue(id=1,title="deleted")
            add_fake_title.insert()

        if not dep :
            add_fake_Department = Department(id=1,name="deleted")
            add_fake_Department.insert()

        if not emp :
            add_fake_Employee = Employee(id=1,name="deleted",department_id=1)
            add_fake_Employee.insert()

        if not req :
            add_fake_Request = Request(id=1,subject="deleted",employee_id=1)
            add_fake_Request.insert()
        if not tick :    
            add_fake_Ticket = Ticket(id=1,subject="deleted",employee_id=1)
            add_fake_Ticket.insert()

        if not tak :
            add_fake_Task = Task(id=1,todo="deleted",queue_id=1,admin_id=1)
            add_fake_Task.insert()
        get_id = user[0].id
        return jsonify({'success': True,'admin_id':get_id})
    else:
        return jsonify({'success': False})

    # except:

    #     abort(422)

@app.route('/employee_login', methods=['POST'])
def employee_login():
    take=request.get_json()
    if not (take.get('uid')):
        abort(422)
    uid = take.get('uid', "")
    try:
        user = Employee.query.filter_by(uid=uid).all()
        if user :
            get_id = user[0].id
            return jsonify({'success': True,'employee_id':get_id})
        else:
            return jsonify({'success': False})

    except:

        abort(422)

# __________________________________________________________________________________________

# GET FUNCTIONS

# __________________________________________________________________________________________
@app.route('/employee_onshift', methods=['GET'])
def employee_onshift():
    try:
        result = {}
        employees = Employee.query.order_by(asc(Employee.id)).all()

        for employe in employees:
            if employe.id == 1 :
                continue
            offs = Offs.query.filter_by(employee_id=employe.id).order_by(asc(Offs.id)).all()
            name = employe.name
            result[name] = []
            for off in offs:
                result[name].append(off.format())
        return jsonify({"result": result})

    except:

        abort(500)


@app.route('/show_requests/<admin_bool>/<user_id>', methods=['GET'])
def show_requests(admin_bool,user_id):
    try:
        if admin_bool == 'true':
        
            requests = Request.query.all()
            closed = []
            pending  = []
            inreview  = []

            for requestt in requests:
                if requestt.reply  == None:
                    if requestt.status == "closed":
                        closed.append(requestt.format())
                    if requestt.status == "pending":
                        pending.append(requestt.format()) 
                    if requestt.status == "inreview":
                        inreview.append(requestt.format()) 

            return jsonify({"closed": closed,"pending": pending,"inreview": inreview})
        else:
            requests = Request.query.filter_by(employee_id=user_id).all()
            closed = []
            pending  = []
            inreview  = []

            for requestt in requests:
                if requestt.reply  == None:
                    if requestt.status == "closed":
                        closed.append(requestt.format())
                    if requestt.status == "pending":
                        pending.append(requestt.format()) 
                    if requestt.status == "inreview":
                        inreview.append(requestt.format()) 

            return jsonify({"closed": closed,"pending": pending,"inreview": inreview})

    except:

        abort(500)
    
@app.route('/show_request/<real_id>', methods=['GET'])
def show_request(real_id):
    # try:
    the_request = Request.query.filter_by(real_id=str(real_id)).order_by(asc(Request.date)).all()
    requests = {}

    for requestt in the_request:         
        if requestt.reply == None and len(the_request)!=1:
            continue
        if not requestt.reply:
            reply= 'waiting'
            action_by ='waiting'
            date = 'waiting'
        else:
            reply=requestt.reply
            action_by =requestt.action_by 
            date = requestt.date 
        if requestt.real_id in requests.keys():
            requests[requestt.real_id]["items_list"].append(
                                                    {
                                                    "action_by": action_by,
                                                    "reply ": reply,
                                                    "date":date
                                                    })

        else:
            user = Employee.query.get(requestt.employee_id)
            requests[requestt.real_id] = {
                "user": user.name,
                "description": requestt.description,
                "subject": requestt.subject,
                "items_list": [
                            {
                            "action_by": action_by,
                            "reply ": reply,
                            "date": date
                            }
                            ],
                "status": requestt.status,
            }

    return jsonify({"requests": requests})

    # except:

    #     abort(500)

@app.route('/show_tickets/<admin_bool>/<user_id>', methods=['GET'])
def show_tickets(admin_bool,user_id):
    try:
        if admin_bool == 'true':
            tickets = Ticket.query.all()
            closed = []
            pending  = []
            inreview  = []

            for tickett in tickets:
                if tickett.reply  == None:
                    if tickett.status == "closed":
                        closed.append(tickett.format())
                    if tickett.status == "pending":
                        pending.append(tickett.format()) 
                    if tickett.status == "inreview":
                        inreview.append(tickett.format()) 

            return jsonify({"closed": closed,"pending": pending,"inreview": inreview})
        else:
            tickets = Ticket.query.filter_by(employee_id=user_id).all()
            closed = []
            pending  = []
            inreview  = []

            for tickett in tickets:
                if tickett.reply  == None:
                    if tickett.status == "closed":
                        closed.append(tickett.format())
                    if tickett.status == "pending":
                        pending.append(tickett.format()) 
                    if tickett.status == "inreview":
                        inreview.append(tickett.format()) 

            return jsonify({"closed": closed,"pending": pending,"inreview": inreview})

    except:

        abort(500)
    
@app.route('/show_ticket/<real_id>', methods=['GET'])
def show_ticket(real_id):
    try:
        the_ticket = Ticket.query.filter_by(real_id=str(real_id)).order_by(asc(Ticket.date)).all()
        
        tickets = {}

        for tickett in the_ticket:
            if tickett.reply == None and len(the_ticket)!=1:
                continue
            if not tickett.reply:
                reply= 'waiting'
                action_by ='waiting'
                date = 'waiting'
            else:
                reply=tickett.reply
                action_by =tickett.action_by 
                date = tickett.date
            if tickett.real_id in tickets.keys():
                tickets[tickett.real_id]["items_list"].append(
                                                        {
                                                        "action_by": action_by ,
                                                        "reply ":reply ,
                                                        "date": date
                                                        })
                


            else:
                tickets[tickett.real_id] = {
                    "description": tickett.description,
                    "subject": tickett.subject,
                    "file": tickett.file,
                    "items_list": [
                                {
                                "action_by": action_by ,
                                "reply ":reply ,
                                "date": date
                                }
                                ],
                    "status": tickett.status,
                }

        return jsonify({"ticket": tickets})

    except:

        abort(500)

@app.route('/show_tasks/<admin_bool>/<user_id>', methods=['GET'])
def show_tasks(admin_bool,user_id):
    try:
        real_ids = []
        taskat = []
        
        task_real = Task.query.all()
        for taskk in task_real:
            if taskk.id == 1:
                continue
            real_ids.append(taskk.real_id)
        real_ids = list(set(real_ids))
        for tasks in real_ids:
            recieve = Receive.query.filter_by(task_real_id=tasks).all()
            for i in recieve:
                
                
                if int(i.employee_id) == int(user_id):
                    passing = True
                    break
                else:
                    passing = False
            print(admin_bool)   
            if admin_bool=="true" or passing == True: 
                data = Task.query.filter_by(real_id = tasks).first()
                taskat.append({'title':data.title ,'todo ':data.todo,'status ':data.status,'real_id ':data.real_id})
        return jsonify({'success': True,"taskat": taskat})
    except:

        abort(500)

@app.route('/show_task/<real_id>/<admin_bool>/<user_id>', methods=['GET'])
def show_task(real_id,admin_bool,user_id):
    try:
        the_taskt = Task.query.filter_by(real_id=str(real_id)).order_by(asc(Task.date)).all()
        taskat = {}
        queue_name=''
        reply=[]
        recieve = Receive.query.filter_by(task_real_id=real_id).all()
        for i in recieve:

            if int(i.employee_id) == int(user_id):
                passing = True
                break
            else:
                passing = False
        if admin_bool=="true" or passing == True: 
            for tasks in the_taskt:
                admin_name = Admin.query.get(tasks.admin_id).name
                queue_name = Queue.query.get(tasks.queue_id).title
                task_realpy  = Task_relpy.query.filter_by(task_id=tasks.id).all()
                if task_realpy:
                    for i in task_realpy:
                        reply.append(i.reply)
                else:
                    reply=None
                if tasks.real_id in taskat.keys():
                    
                    taskat[tasks.real_id]["items_list"].append(
                                                            {
                                                            "queue_name": queue_name,
                                                            "files":tasks.files,
                                                            "task_reply":reply,
                                                            "status": tasks.status,
                                                            "date": tasks.date 
                                                            })

                else:
                    

                    taskat[tasks.real_id] = {
                        "title": tasks.title,
                        "todo": tasks.todo,
                        "admin_name":admin_name,
                        "items_list": [
                                    {
                                    "queue_name": queue_name,
                                    "files":tasks.files,
                                    "task_reply":reply,
                                    "status": tasks.status,
                                    "date": tasks.date 
                                    }
                                    ],
                        
                    }
            return jsonify({'success': True,"taskat": taskat})
        else:
            return jsonify({'success': False,"taskat": "you have no permission"})
       

    except:

        abort(500)
# ______________________________________________________________

# DELETE FUNCTIONS

# __________________________________________________________________________________________
@app.route('/delete_offs/<id>', methods=['DELETE'])
def delete_offs(id):
    try:
        delete = Offs.query.get(id)

        delete.delete()

        return jsonify({'success': True})
    except:

        abort(422)


@app.route('/delete_admin/<id>', methods=['DELETE'])
def delete_admin(id):
    try:
        delete_React= React.query.filter_by(admin_id=id).all()
        if delete_React:
            for i in delete_React:
                i.delete()
        update_ticket= Ticket.query.filter_by(admin_id=id).all()
        if update_ticket:
            for i in update_ticket:
                i.admin_id=1
                i.update()
        update_task= Task.query.filter_by(admin_id=id).all()
        if update_task:
            for i in update_task:
                i.admin_id=1  
                i.update()
        delete = Admin.query.get(id)

    
        delete.delete()
        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/delete_employee/<id>', methods=['DELETE'])
def delete_employee(id):
    # try:
        update_request= Request.query.filter_by(employee_id=id).all()
        if update_request:
            for i in update_request:
                i.employee_id=1
                i.update()

        update_ticket= Ticket.query.filter_by(employee_id=id).all()
        if update_ticket:
            for i in update_ticket:
                i.employee_id=1
                i.update()

        update_task= Task.query.filter_by(employee_id=id).all()
        if update_task:
            for i in update_task:
                i.employee_id=1
                i.update()

        delete = Employee.query.get(id)
        delete.delete()
        return jsonify({'success': True})
    # except:

    #     abort(422)

@app.route('/delete_request/<real_id>', methods=['DELETE'])
def delete_request(real_id):
    # try:
    update_react= React.query.filter_by(request_real_id=real_id).all()
    print(update_react)
    if update_react:
        for i in update_react:
            i.request_id=1
            i.update()
    delete_request= Request.query.filter_by(real_id=real_id).all()
    if delete_request:
        for i in delete_request:
            i.delete()
    return jsonify({'success': True})
    # except:

    #     abort(422)

@app.route('/delete_ticket/<real_id>', methods=['DELETE'])
def delete_ticket(real_id):
    try:
        delete_Ticket= Ticket.query.filter_by(real_id=real_id).all()
        if delete_Ticket:
            for i in delete_Ticket:
                i.delete()
        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/delete_task/<real_id>', methods=['DELETE'])
def delete_task(real_id):
    try:
        delete_Receive= Receive.query.filter_by(task_real_id=real_id).all()
        if delete_Receive:
            for i in delete_Receive:
                i.delete()
        delete_Task= Task.query.filter_by(real_id=real_id).all()
        if delete_Task:
            for i in delete_Task:
                i.delete()
        return jsonify({'success': True})
    except:

        abort(422)

# __________________________________________________________________________________________

# UPDATE FUNCTIONS

# __________________________________________________________________________________________

@app.route('/update_employee/<id>', methods=['POST'])
def update_employee(id):
    update = Employee.query.get(id)

    uid = request.form.get('uid', '')
    department_id = request.form.get('department_id', '')
    name = request.form.get('name', '')
    try:

        
        update.uid=uid,
        update.name=name
        update.department_id=department_id
        update.update()

        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/update_admin/<id>', methods=['POST'])
def update_admin(id):
    update = Admin.query.get(id)

    uid = request.form.get('uid', '')
    department_id = request.form.get('department_id', '')
    name = request.form.get('name', '')
    try:

        
        update.uid=uid,
        update.name=name
        update.department_id=department_id
        update.update()

        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/update_ticket_admin/<real_id>', methods=['POST'])
def update_ticket_admin(real_id):
    update = Ticket.query.filter_by(real_id=real_id).all()

    new_admin_id = request.form.get('new_admin_id', '')
    try:

        for i in update:
            i.admin_id=new_admin_id,
            i.update()

        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/update_task_query/<task_id>', methods=['PATCH'])
def update_task_query(task_id):
    update = Task.query.get(task_id)
    try:
        if update.files or update.content or update.description:
            submit_check = Submit.query.filter_by(task_id=task_id).first()
            if submit_check:
                return jsonify({'success': False, "comment":'there is someone else insert in this queue'})
            else: 
                content = request.form.get('content', '')
                description = request.form.get('description', '')
                try:
                    file1 = request.files['file1']
                except:
                    file1 = request.form.get('file1', "")

                try:
                    file2 = request.files['file2']
                except:
                    file2 = request.form.get('file2', "")
                try:
                    file3 = request.files['file3']
                except:
                    file3 = request.form.get('file', "")
                try:
                    file4 = request.files['file4']
                except:
                    file4 = request.form.get('file4', "")
                try:
                    file5 = request.files['file5']
                except:
                    file5 = request.form.get('file5', "")
            
                files = []
                if file1:
                    if type(file1) == str:
                        url1 = file1
                        files.append(url1)
                    else:
                        storage.child("file/" + update.task_real_id + "/file1").put(file1, file1.mimetype)
                        url1 = storage.child("file/" + update.task_real_id + "/file").get_url(None)
                        files.append(url1)
                else:
                    test = storage.child("file/" + update.task_real_id + "/file1").get_url(None)
                    if test:
                        try:
                            blob1 = bucket.blob("file/" + update.task_real_id + "/file1")
                            blob1.delete()
                        except:
                            pass
                if file2:
                    if type(file2) == str:
                        url2 = file2
                        files.append(url2)
                    else:
                        storage.child("file/" + update.task_real_id + "/file2").put(file2, file2.mimetype)
                        url2 = storage.child("file/" + update.task_real_id + "/file2").get_url(None)
                        files.append(url2)
                else:
                    test = storage.child("file/" + update.task_real_id + "/file2").get_url(None)
                    if test:
                        try:
                            blob1 = bucket.blob("file/" + update.task_real_id + "/file2")
                            blob1.delete()
                        except:
                            pass
                if file3:
                    if type(file3) == str:
                        url3 = file3
                        files.append(url3)
                    else:
                        storage.child("file/" + update.task_real_id + "/file3").put(file3, file3.mimetype)
                        url3 = storage.child("file/" + update.task_real_id + "/file3").get_url(None)
                        files.append(url3)
                else:
                    test = storage.child("file/" + update.task_real_id + "/file3").get_url(None)
                    if test:
                        try:
                            blob1 = bucket.blob("file/" + update.task_real_id + "/file3")
                            blob1.delete()
                        except:
                            pass
                if file4:
                    if type(file4) == str:
                        url4 = file4
                        files.append(url4)
                    else:
                        storage.child("file/" + update.task_real_id + "/file4").put(file4, file4.mimetype)
                        url4 = storage.child("file/" + update.task_real_id + "/file4").get_url(None)
                        files.append(url4)
                else:
                    test = storage.child("file/" + update.task_real_id + "/file4").get_url(None)
                    if test:
                        try:
                            blob1 = bucket.blob("file/" + update.task_real_id + "/file4")
                            blob1.delete()
                        except:
                            pass
                if file5:
                    if type(file5) == str:
                        url5 = file5
                        files.append(url5)
                    else:
                        storage.child("file/" + update.task_real_id + "/file5").put(file5, file5.mimetype)
                        url5 = storage.child("file/" + update.task_real_id + "/file5").get_url(None)
                        files.append(url5)
                else:
                    test = storage.child("file/" + update.task_real_id + "/file5").get_url(None)
                    if test:
                        try:
                            blob1 = bucket.blob("file/" + update.task_real_id + "/file5")
                            blob1.delete()
                        except:
                            pass

                update.content = content
                update.description = description
                update.files = files
                update.update()

                return jsonify({'success': True})
    except:

        abort(422)

@app.route('/update_task_status/<task_real_id>', methods=['POST'])
def update_task_status(task_real_id):
    update = Task.query.filter_by(task_real_id=task_real_id).all()
    status = request.form.get('status', '')
    try:
        for i in update:
            i.status = status
            i.update()

            return jsonify({'success': True})
    except:

        abort(422)


@app.route('/received/<employee_id>/<task_real_id>', methods=['POST'])
def received(employee_id,task_real_id):
    update = Receive.query.filter_by(employee_id=employee_id,task_real_id=task_real_id).all()
    try:
        for i in update:
            i.receive_date = str(datetime.now())
            i.received = True
            i.update()

            return jsonify({'success': True})
    except:

        abort(422)

@app.route('/update_ticket_closed/<ticket_real_id>', methods=['PATCH'])
def update_ticket_closed(ticket_real_id):

    status = 'closed'
    
    try:
        tickett = Ticket.query.filter_by(real_id=str(ticket_real_id)).all()
        for i in tickett:
            i.status= status
            i.update()


        return jsonify({'success': True, "comment" : ""})
    except:

        abort(422)
@app.route('/update_task_completed/<task_id>', methods=['PATCH'])
def update_task_completed(task_id):

    status = 'completed'
    
    try:
        tickett = Ticket.query.get(task_id)
        tickett.status= status
        tickett.update()
        return jsonify({'success': True, "comment" : ""})
    except:

        abort(422)

@app.route('/update_offs/<id>', methods=['POST'])
def update_offs(id):
    update = Offs.query.get(id)
    employee_id = request.form.get('employee_id', '')
    start = request.form.get('start', '')
    end = request.form.get('end', '')
    type = request.form.get('type', '')
    try:

        update.update.start=start
        update.end=end
        update.type=type
        update.employee_id=employee_id
        update.update()

        return jsonify({'success': True})
    except:
        abort(422)

# __________________________________________________________________________________________

# POST FUNCTIONS

# __________________________________________________________________________________________
@app.route('/add_offs', methods=['POST'])
def add_offs():
    if not (request.form.get('start') and request.form.get('end') and  request.form.get('type') ):
        return jsonify({'success': False, 'comment': "Something Missed"})
    employee_id = request.form.get('employee_id', '')
    start = request.form.get('start', '')
    end = request.form.get('end', '')
    type = request.form.get('type', '')
    try:

        fill_offs_table = Offs(start=start,end=end,type=type,employee_id=employee_id)
        fill_offs_table.insert()

        return jsonify({'success': True})
    except:
        abort(422)

@app.route('/add_department', methods=['POST'])
def add_department():
    if not (request.form.get('name')):
        return jsonify({'success': False, 'comment': "Something Missed"})
    name = request.form.get('name', '')
    try:

        fill_department_table = Department(name=name)
        fill_department_table.insert()

        return jsonify({'success': True})
    except:
        abort(422)

@app.route('/add_queue', methods=['POST'])
def add_queue():
    if not (request.form.get('title')):
        return jsonify({'success': False, 'comment': "Something Missed"})
    title = request.form.get('title', '')
    try:

        fill_queue_table = Queue(title=title)
        fill_queue_table.insert()

        return jsonify({'success': True})
    except:
        abort(422)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if not (request.form.get('uid') and request.form.get('name') and request.form.get('department_id')):
        return jsonify({'success': False, 'comment': "Something Missed"})

    uid = request.form.get('uid', '')
    department_id = request.form.get('department_id', '')
    name = request.form.get('name', '')
    try:

        fill_employee_table = Employee(uid=uid, name=name, department_id=department_id)
        fill_employee_table.insert()

        return jsonify({'success': True})
    except:

        abort(422)

@app.route('/add_admin', methods=['POST'])
def add_admin():
    if not (request.form.get('uid') and request.form.get('name') and request.form.get('department_id')):
        return jsonify({'success': False, 'comment': "Something Missed"})

    uid = request.form.get('uid', '')
    department_id = request.form.get('department_id', '')
    name = request.form.get('name', '')
    # try:
    print("hi")
    fill_admin_table = Admin(uid=uid, name=name, department_id=department_id)
    fill_admin_table.insert()

    return jsonify({'success': True})
    # except:

    #     abort(422)

@app.route('/add_request', methods=['POST'])
def add_request():
    if not (request.form.get('subject') and request.form.get('description') and request.form.get('employee_id')):
        return jsonify({'success': False, 'comment': "Something Missed"})

    employee_id = request.form.get('employee_id', '')
    subject = request.form.get('subject', '')
    description = request.form.get('description', '')
    status = 'pending'
    real_order_id = random.randint(100000, 9999999999999999)
    all_real_id = Request.query.filter_by(real_id=str(real_order_id)).all()
    employee_name = Employee.query.get(employee_id).name
    admin_data = Admin.query.all()
    while real_order_id in all_real_id:
        real_order_id = random.randint(100000, 9999999999999999)
    date = str(datetime.now())
    try:

        fill_request_table = Request(employee_id=employee_id,
                                subject=subject, 
                                description=description,
                                status=status,
                                date = date,
                                action_by =employee_name,
                                real_id=str(real_order_id))
        fill_request_table.insert()
        request_id = Request.query.filter_by(real_id=str(real_order_id)).first().id
        for i in admin_data:
            fill_react_table = React(request_id=request_id,date=date, admin_id=i.id,request_real_id=str(real_order_id))
            fill_react_table.insert()


        return jsonify({'success': True, "comment" : ""})
    except:

        abort(422)

        
@app.route('/add_request_reply/<request_real_id>', methods=['POST'])
def add_request_reply(request_real_id):
    if not (request.form.get('reply')):
        
        return jsonify({'success': False, 'comment': "Something Missed"})
    
    admin_id = request.form.get('admin_id', '')
       
    reply = request.form.get('reply', '')
    status = 'inreview'
    request_first = Request.query.filter_by(real_id=str(request_real_id)).first()
    date = str(datetime.now())
    try:
        
        if admin_id :
            
            admin_data = Admin.query.get(admin_id)
            action_by = admin_data.name
            requestt = Request.query.filter_by(real_id=str(request_real_id)).all()
            react_id = React.query.filter_by(request_real_id=request_real_id , admin_id= admin_id).first()
            react_id.action = True
            react_id.update()
            fill_request_table = Request(reply=reply,
                                    status=status,
                                    subject=request_first.subject,
                                    description=request_first.description,
                                    employee_id = request_first.employee_id,
                                    action_by=action_by,
                                    date = date,
                                    real_id=request_real_id)
            fill_request_table.insert()
            for i in requestt:
                i.status= status
                i.update()
        else:
            employee_name = Employee.query.get(request_first.employee_id).name
            fill_request_table = Request(reply=reply,
                                    status=request_first.status,
                                    subject=request_first.subject,
                                    description=request_first.description,
                                    employee_id = request_first.employee_id,
                                    action_by= employee_name,
                                    date = date,
                                    real_id=request_real_id)
            fill_request_table.insert()

        return jsonify({'success': True, "comment" : ""})
    except:

        abort(422)


@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    if not (request.form.get('subject') and request.form.get('description') and request.form.get('employee_id')):
        return jsonify({'success': False, 'comment': "Something Missed"})

    employee_id = request.form.get('employee_id', '')
    subject = request.form.get('subject', '')
    description = request.form.get('description', '')
    try:
        file = request.files['file']
    except:
        pass
    status = 'pending'
    employee_name = Employee.query.get(employee_id).name
    real_order_id = random.randint(100000, 9999999999999999)
    all_real_id = Ticket.query.filter_by(real_id=str(real_order_id)).all()
    while real_order_id in all_real_id:
        real_order_id = random.randint(100000, 9999999999999999)
    date = str(datetime.now())
    # try:
    if file:
        storage.child("ticket_file/" + str(real_order_id)).put(file, file.mimetype)
        url = storage.child("ticket_file/" + str(real_order_id)).get_url(None)
    fill_Ticket_table = Ticket(employee_id=employee_id,
                            subject=subject, 
                            description=description,
                            status=status,
                            date = date,
                            file=url,
                            action_by =employee_name,
                            real_id=str(real_order_id))
    fill_Ticket_table.insert()

    return jsonify({'success': True, "comment" : ""})
    # except:

    #     abort(422)

@app.route('/add_ticket_reply/<ticket_real_id>', methods=['POST'])
def add_ticket_reply(ticket_real_id):
    if not (request.form.get('reply')):
        return jsonify({'success': False, 'comment': "Something Missed"})

    admin_id = request.form.get('admin_id', '')
    reply = request.form.get('reply', '')
    status = 'inreview'
    request_first = Ticket.query.filter_by(real_id=str(ticket_real_id)).first()
    
    date = str(datetime.now())
    
    
    # try:
        
    if admin_id :
        if not request_first.admin_id:
            request_first.admin_id= admin_id
            request_first.update()
        requestt = Ticket.query.filter_by(real_id=str(ticket_real_id)).all()
        for i in requestt:
            if i.admin_id:
                ad_id = i.admin_id
                break
            else:
                continue
        admin_data = Admin.query.get(ad_id)
        action_by = admin_data.name
        if ad_id == int(admin_id):

            fill_Ticket_table = Ticket(reply=reply,
                                    status=status,
                                    subject=request_first.subject,
                                    description=request_first.description,
                                    employee_id = request_first.employee_id,
                                    admin_id = admin_id,
                                    action_by=action_by,
                                    date = date,
                                    real_id=ticket_real_id)
            fill_Ticket_table.insert()
            requests = Ticket.query.filter_by(real_id=str(ticket_real_id)).all()
            for i in requests:
                i.status= status
                i.update()
            return jsonify({'success': True, "comment" : ""})
        else:
            
            return jsonify({'success': False , "comment" : action_by + " took this ticket"  })
    else:
        employee_name = Employee.query.get(request_first.employee_id).name
        fill_Ticket_table = Ticket(reply=reply,
                                status=request_first.status,
                                subject=request_first.subject,
                                description=request_first.description,
                                employee_id = request_first.employee_id,
                                action_by=employee_name,
                                date = date,
                                real_id=ticket_real_id)
        fill_Ticket_table.insert()

        return jsonify({'success': True, "comment" : "" })
    # except:

    #     abort(422)

  

@app.route('/add_task', methods=['POST'])
def add_task():
    if not (request.form.get('queue_ids') and request.form.get('employee_ids') and request.form.get('title')):
        return jsonify({'success': False, 'comment': "Something Missed"})
    admin_id = request.form.get('admin_id', '')
    employee_ids = request.form.get('employee_ids', '')
    queue_ids = request.form.get('queue_ids', '')
    todo = request.form.get('todo', '')
    title = request.form.get('title', '')
    status = 'pending'


    real_order_id = random.randint(100000, 9999999999999999)
    all_real_id = Ticket.query.filter_by(real_id=str(real_order_id)).all()
    while real_order_id in all_real_id:
        real_order_id = random.randint(100000, 9999999999999999)
    date = str(datetime.now())
    # try:


    if len(employee_ids) > 1 and employee_ids[0] == '[':
            arr1 = employee_ids[1:-1]
            arr1 = ''.join(arr1).split(",")
    if len(queue_ids) > 1 and queue_ids[0] == '[':
            arr2 = queue_ids[1:-1]
            arr2 = ''.join(arr2).split(",")
    print(arr1)
    print(arr2)
    for i in arr2:


        fill_task_table = Task(queue_id=i,
                                title=title, 
                                todo=todo,
                                status=status,
                                date = date,
                                real_id=str(real_order_id),
                                admin_id=admin_id)
        fill_task_table.insert()
    task_data = Task.query.filter_by(real_id=str(real_order_id)).all()
    for i in arr1:
        
        for j in task_data:
            fill_task_table = Receive(employee_id=i,
                                    task_id=j.id, 
                                    task_real_id=str(real_order_id),
                                    date = date)
            fill_task_table.insert()

    return jsonify({'success': True})
    # except:

    #     abort(422)
@app.route('/add_task_query/<task_id>', methods=['POST'])
def add_task_query(task_id):
    update = Task.query.get(task_id)
    user_id = request.form.get('user_id', '')
    content = request.form.get('content', '')
    description = request.form.get('description', '')
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    file4 = request.files['file4']
    file5 = request.files['file5']
    date = str(datetime.now())
    try:
        submit_check = Submit.query.filter_by(task_id=task_id).first()
        if update.files or update.content or update.description and submit_check:

            files = []
            if file1:
                storage.child("file/" + update.task_real_id + "/file1").put(file1, file1.mimetype)
                url1 = storage.child("file/" + update.task_real_id + "/file1").get_url(None)
                files.append(url1)
            if file2:
                storage.child("file/" + update.task_real_id + "/file2").put(file2, file2.mimetype)
                url2 = storage.child("file/" + update.task_real_id + "/file2").get_url(None)
                files.append(url2)
            if file3:
                storage.child("file/" + update.task_real_id + "/file3").put(file3, file3.mimetype)
                url3 = storage.child("file/" + update.task_real_id + "/file3").get_url(None)
                files.append(url3)
            if file4:
                storage.child("file/" + update.task_real_id + "/file4").put(file4, file4.mimetype)
                url4 = storage.child("file/" + update.task_real_id + "/file4").get_url(None)
                files.append(url4)
            if file5:
                storage.child("file/" + update.task_real_id + "/file5").put(file5, file5.mimetype)
                url5 = storage.child("file/" + update.task_real_id + "/file5").get_url(None)
                files.append(url5)

            update.files =files
            update.content =content
            update.date =date
            update.status ="inprocess"
            update.description =description
            update.update()

            return jsonify({'success': True, "comment":""})

        elif not update.files or not update.content or not update.description:
            files = []
            if file1:
                storage.child("file/" + update.task_real_id + "/file1").put(file1, file1.mimetype)
                url1 = storage.child("file/" + update.task_real_id + "/file1").get_url(None)
                files.append(url1)
            if file2:
                storage.child("file/" + update.task_real_id + "/file2").put(file2, file2.mimetype)
                url2 = storage.child("file/" + update.task_real_id + "/file2").get_url(None)
                files.append(url2)
            if file3:
                storage.child("file/" + update.task_real_id + "/file3").put(file3, file3.mimetype)
                url3 = storage.child("file/" + update.task_real_id + "/file3").get_url(None)
                files.append(url3)
            if file4:
                storage.child("file/" + update.task_real_id + "/file4").put(file4, file4.mimetype)
                url4 = storage.child("file/" + update.task_real_id + "/file4").get_url(None)
                files.append(url4)
            if file5:
                storage.child("file/" + update.task_real_id + "/file5").put(file5, file5.mimetype)
                url5 = storage.child("file/" + update.task_real_id + "/file5").get_url(None)
                files.append(url5)

            update.files =files
            update.content =content
            update.status ="inprocess"
            update.date =date
            update.description =description
            update.update()

            fill_submit_table = Submit(task_id=task_id, user_id=user_id) 
            fill_submit_table.insert()

        elif update.files or update.content or update.description and not submit_check:
            return jsonify({'success': False, "comment":'there is someone else insert in this queue'})

        else:
            return jsonify({'success': False, "comment":'there is someone else insert in this queue'})
    except:

        abort(422)

@app.route('/add_task_reply/<task_real_id>/<task_id>', methods=['POST'])
def add_task_reply(task_real_id,task_id):
    
    reply = request.form.get('reply', '')
    # try:
    fill_Task_relpy_table = Task_relpy(task_real_id=task_real_id, task_id=task_id, reply=reply)
    fill_Task_relpy_table.insert()

    return jsonify({'success': True})
    # except:

    #     abort(422)
# __________________________________________________________________________________________

# ERROR HANDLING

# __________________________________________________________________________________________

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def handle404(error):
    return jsonify({"success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(401)
def handle401(error):
    return jsonify({"success": False,
                    "error": 401,
                    "message": "authentication error"
                    }), 401


@app.errorhandler(400)
def handle400(error):
    return jsonify({"success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400


if __name__ == '__main__':
    app.run()