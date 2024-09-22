from flask import Flask
from flask import request, render_template, url_for, redirect,flash,jsonify, send_from_directory
import matplotlib.pyplot as plt
from model import *
from flask_cors import CORS
from datetime import date,timedelta,datetime
import os
from celery import Celery
from caching import cache
from mail import mailer
import numpy as np
import pandas as pd
import flask_excel as excel


user_datastore = SQLAlchemySessionUserDatastore(db.session,user,role)


def make_celery(app):
    
    c_app=Celery(app.name)
    c_app.config_from_object("celeryconfig")
    app.extensions["celery"]=c_app
    return c_app

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///projdb.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'QWERTYALPHA'
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SECURITY_PASSWORD_SALT'] = 'TOOSALTYPASSWORD'
    app.config['SECURITY_REGISTRABLE'] = True
    app.config['SECURITY_TRACKABLE'] = True    
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost' # '127.0.0.1'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60 # caching it for 1 min/ 60 sec
    app.config['MAIL_SERVER'] = 'localhost' # '127.0.0.1'
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@a.com'



    CORS(app)
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    security=Security(app, user_datastore)
    createdata(user_datastore)
    mailer.init_app(app)
    cache.init_app(app)
    cel = make_celery(app)

    return app, cel



app, c_app = create_app()
# celery -A app.c_app worker --loglevel=INFO







import task





@app.route('/mailtest', methods=["GET","POST"])
def mailtest():
    task.mail_report.delay()
    return 'done'


@app.route('/csvtest', methods=["GET","POST"])
def csvtest():
    task.create_csv.delay()
    return 'done'



from celery.schedules import crontab

c_app.conf.beat_schedule = {
    'daily-mail': {
        'task': 'task.mail_reminder',
        'schedule': crontab(minute=00, hour=18)
    },
    'monthly-mail': {
        'task': 'task.mail_report',
        'schedule': crontab(minute=00, hour=00, day_of_month=1)
    }
}







@app.route('/', methods=["GET","POST"])
def loginpage():
        a = request.get_json()
        mail = a["email"]
        passw = a["password"]
        em = user.query.filter_by(Email = mail).first()
        if em != None and verify_password(passw, em.Password):
            tk = em.get_auth_token()
            message = {"email" : mail,"token" : tk, "role":"user"}
            return jsonify(message),200
        else:
            message = {"message" : "Invalid Credentials"}
            return jsonify(message),401
   

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
            input = request.get_json()
            name = input["name"]
            email = input["email"]
            passw = input['password']

            if user_datastore.find_user(Email = email):
                 return jsonify({"msg":"Email Id already exists, please use another Email Id"}),401
            
            us = user_datastore.create_user(Name = name,Email=email,Password = passw)
            db.session.commit()    
            return jsonify({"msg": "User Created Successfully! Please login"}),201


@app.route("/admin", methods = ["GET","POST"])
def admin():
    if request.method == "POST":
        a = request.get_json()
        email = a["email"]
        passw = a["password"]
        em = user.query.filter_by(Email = email).first()
        if em != None and  verify_password(passw, em.Password) and any(i.name == 'admin' for i in em.roles):
            tk = em.get_auth_token()
            message = {"email" : email,"token" : tk, "role":"admin"}
            return jsonify(message),200
        else:
            message = {"message" : "Invalid Credentials"}
            return jsonify(message),401
        


@app.route("/allinfo", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def allinfo():
    if request.method == "GET":
        usr = user.query.all()
        sec = section.query.all()
        bk = book.query.all()

         # Setup the Agg backend
        plt.switch_backend('Agg')

        # 1. Section Books 3D Pie Chart
        def plot_section_books_pie_chart():
            sections = sec
            section_data = {sec.Title: book.query.filter_by(Section=sec.ID).count() for sec in sections}
            
            if section_data:
                labels = list(section_data.keys())
                sizes = list(section_data.values())
                
                plt.figure()
                wedges, texts, autotexts = plt.pie(
                    sizes, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True,
                    wedgeprops=dict(width=0.3))  # Adjust width for the donut effect
                
                plt.setp(autotexts, size=10, weight="bold")
                plt.setp(texts, size=12)

                plt.title('Number of Books in Each Section')
                
                # Draw a white circle at the center for the donut effect
                center_circle = plt.Circle((0, 0), 0.70, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)
                
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                plt.savefig('./frontend/vite-project/public/section_books_pie_chart.png')
                plt.close()


       
        # 3. Violin Plot of Book Requests
        def plot_violin_requests():
            book_ids = [req.bid for req in issuebook.query.all()]
            if book_ids:
                df = pd.DataFrame({'book_id': book_ids})
                plt.figure()
                plt.violinplot(df['book_id'])
                plt.title('Distribution of Book Requests')
                plt.xlabel('Books')
                plt.ylabel('Request Count')
                plt.savefig('./frontend/vite-project/public/violin_requests.png')
                plt.close()

      
        # Generate and save plots
        plot_section_books_pie_chart()
        plot_violin_requests()


        return jsonify({"users":len(usr),"sections":len(sec),"books":len(bk)}),200


         

@app.route("/newsection",methods =["GET","POST"])
@auth_required("token")
@roles_required('admin')
def newsection():
    if request.method == "POST":
        input = request.get_json()
        name = input["title"]
        date = input["date"]
        desc = input['desc']

        sec = section.query.filter_by(Title = name).first()
        if sec:
            return jsonify({"msg":"Section already exists, please use another name"}),401
        sc = section(Title = name, Date = date, Description = desc)
        db.session.add(sc)
        db.session.commit()
        return jsonify({"msg": "Section Created Successfully!"}),200
    



@app.route("/allsections", methods = ["GET","POST"])
@auth_required("token")
@cache.cached(timeout=15)
def adminallsection():
    if request.method == "GET":
        sec = section.query.all()
        list = []
        for i in sec:
            d= {}
            d["Id"] = i.ID
            d["Title"] = i.Title
            d["Date"] = i.Date
            d["Description"] = i.Description
            list.append(d)
        return jsonify(list), 200


@app.route("/secbooks/<id>", methods = ["GET","POST"])
@auth_required("token")
def secbooks(id):
    if request.method == "GET":
        usr = current_user
        seci = section.query.filter_by(ID = id).first()
        print(seci)
        books = db.session.query(book).filter(book.Section==id).all()
        sdict = {}
        blist = []
        sdict["Id"] = seci.ID
        sdict["Title"] = seci.Title
        sdict["Date"] = seci.Date
        sdict["Description"] = seci.Description

        for b in books:
            avg = 0
            rev = review.query.filter_by(bid = b.ID).all()
            if len(rev) != 0:
                for r in rev:
                    avg = avg + int(r.Review)
                avg = avg/len(rev)
            
            issue = b.issues
            fis = 'None'
            for i in issue:
                if i.uid == usr.ID:
                    fis = i
            if fis == 'None':
                d = {}
                d['Id'] = b.ID
                d["Title"] = b.Title
                d["Author"] = b.Author
                d["Issuedate"] = 'None'
                d["Duedate"] = 'None'
                d['Status'] = 'None'
                d['Rev'] = avg
                blist.append(d)

            else:
                d = {}
                d["Id"] = b.ID
                d["Title"] = b.Title
                d["Author"] = b.Author
                d["Issuedate"] = fis.doi
                d["Duedate"] = fis.dor                
                d['Status'] = fis.cstatus
                d['Rev'] = avg
                blist.append(d)
        print(sdict, blist)
        return jsonify({"sdict":sdict, "blist": blist}), 200


@app.route("/reqest/<id>", methods = ["GET","POST"])
@auth_required("token")
def reqest(id):
    if request.method == "GET":
        usr = current_user
        ise = issuebook.query.filter_by(bid = id, uid = usr.ID).first() 
        a = issuebook.query.filter_by(uid = usr.ID, cstatus = 'Approved').all()
        if len(a)<5:  
            if not ise:
                issu = issuebook(bid = id, uid = usr.ID, cstatus = 'Pending')
                db.session.add(issu)
                db.session.commit()
                return jsonify({'msg':'Request Sent Successfully!'}), 200
            else:
                return jsonify({'msg':'Request Already Sent!'}), 401
        return jsonify({"msg":"You can only read 5 books at a time!"}),401
        

@app.route("/retrn/<id>", methods = ["GET","POST"])
@auth_required("token")
def retrn(id):
    if request.method == "GET":
        usr = current_user
        ise = issuebook.query.filter_by(bid = id, uid = usr.ID).first()
        db.session.delete(ise)
        db.session.commit()
        return jsonify({'msg':'Your book is returned Successfully!'}), 200
    
        




@app.route("/newbook/<id>", methods = ["GET", "POST"])
@auth_required("token")
@roles_required('admin')
def newbook(id):
    if request.method == "POST":
        title = request.form.get("Title")
        tl = book.query.filter_by(Title = title, Section = id).first()
        if tl:
            return jsonify({'msg':'Please choose different Title!'}), 401

        auth = request.form.get("Author")
        add = book(Title = title, Author = auth, Section = id)
        db.session.add(add)
        db.session.commit()

        file = request.files.get("File")
        file.save('./static/'+str(add.ID)+'.pdf')
        return jsonify({'msg':'New book added to this Section Successfully!'}), 200


@app.route("/book/<id>", methods = ["GET","POST"])
def bk(id):
    return send_from_directory('./static/',id)


@app.route("/dltsection/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def dltsection(id):
    if request.method == "GET":
        sec = section.query.filter_by(ID = id).first()
        bks = book.query.filter_by(Section = id).all()
        for i in bks:
            db.session.query(issuebook).filter_by(bid = i.ID).delete()
            db.session.query(review).filter_by(bid = i.ID).delete()
            db.session.delete(i)
            os.remove('./static/'+str(i.ID)+'.pdf')
        db.session.delete(sec)
        db.session.commit()
        return jsonify({"msg": "Section Deleted Successfully!"}),200



@app.route("/updsection/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def updsection(id):
    if request.method == "POST":
        input = request.get_json()
        name = input["title"]
        date = input["date"]
        desc = input['desc']
        sec = section.query.filter_by(ID = id).first()
        if sec:
            sec.Title = name
            sec.Date = date
            sec.Description = desc
            db.session.commit()
            return jsonify({"msg": "Section Updated Successfully!"}),200
        return jsonify({"msg": "Section Not Found!"}),401
    if request.method == "GET":
        sec = section.query.filter_by(ID = id).first()
        d = {}
        d["title"] = sec.Title
        d["date"] = sec.Date
        d["desc"] = sec.Description
        return jsonify({"d":d}),200
        



@app.route("/usersnreqs/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def usersnreqs(id):
    if request.method == "GET":
        isr = issuebook.query.filter_by(bid = id, cstatus = 'Pending').all()
        plist = []
        for i in isr:
            usr = user.query.filter_by(ID = i.uid).first()
            d = {}
            d["Id"] = i.ID
            d["Name"] = usr.Name
            d["Email"] = usr.Email
            d["Status"] = i.cstatus
            plist.append(d)
        ir = issuebook.query.filter_by(bid = id, cstatus = 'Approved').all()
        alist = []
        for i in ir:
            usr = user.query.filter_by(ID = i.uid).first()
            d = {}
            d["Id"] = i.ID
            d["Name"] = usr.Name
            d["Email"] = usr.Email
            d["Issuedate"] = i.doi
            d["Returndate"] = i.dor
            d["Status"] = i.cstatus
            alist.append(d)
        return jsonify({"plist":plist, "alist":alist}),200


@app.route("/approve/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def approve(id):
    if request.method == "GET":
        ib = issuebook.query.filter_by(ID = id).first()
        a = issuebook.query.filter_by(uid = ib.uid, cstatus = 'Approved').all()
        if len(a)<5:
            ib.cstatus = 'Approved'
            ib.doi = date.today()
            ib.dor = ib.doi + timedelta(days = 7)
            db.session.commit()
            return jsonify({"msg": "Request Approved Successfully!"}),200
        return jsonify({"msg":"Can't approve more than 5 requests at a time!"}),401    


@app.route("/decline/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')    
def decline(id):
    if request.method == "GET":
        ib = issuebook.query.filter_by(ID = id).first()
        ib.cstatus = 'Rejected'
        db.session.commit()
        return jsonify({"msg": "Request Declined Successfully!"}),200
    

@app.route("/rrevoke/<id>", methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def rrevoke(id):
    if request.method == "GET":
        ib = issuebook.query.filter_by(ID = id).first()
        db.session.delete(ib)
        db.session.commit()
        return jsonify({"msg": "Book Revoked Successfully!"}),200



@app.route("/dltbook/<id>",methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def dltbook(id):
    if request.method == "GET":
        db.session.query(issuebook).filter_by(bid = id).delete()
        db.session.query(review).filter_by(bid = id).delete()
        b = book.query.filter_by(ID = id).first()
        db.session.delete(b)
        os.remove('./static/'+str(id)+'.pdf')
        db.session.commit()
        return jsonify({"msg": "Book Deleted Successfully!"}),200



@app.route('/updbook/<id>', methods = ["GET","POST"])
@auth_required("token")
@roles_required('admin')
def updbook(id):
    if request.method == "GET":
        b = book.query.filter_by(ID = id).first()
        title = b.Title
        author = b.Author
        return jsonify({"title":title,"author":author}),200
    if request.method == "POST":
        title = request.form.get("Title")
        auth = request.form.get("Author")
        b = book.query.filter_by(ID = id).first()
        if b:
            a = book.query.filter_by(Title=title).first()
            if title != b.Title and a:
                return jsonify({"msg": "Book Title Already Exists!"}),401
            
            b.Title = title
            b.Author = auth
            db.session.commit()
            file = request.files.get("File")
            if file:
                file.save('./static/'+str(b.ID)+'.pdf')
            return jsonify({"msg": "Book Updated Successfully!"}),200
        return jsonify({"msg": "Book Not Found!"}),401


def perform_query(model, column, data):
    return db.session.query(model).filter(column.ilike(f'%{data}%')).all()


@app.route('/find/<find>',methods = ['GET','POST'])
@auth_required("token")
def find(find):
    find = find[1:]
    usr = current_user
    if request.method == "GET":
        if (find == None) or (len(find) == 0) or (find.isspace()):
            return jsonify({"books":[],"sections":[],"authors":[]}),200
        bks = perform_query(book, book.Title, find)
        secs = perform_query(section, section.Title, find)
        auths = perform_query(book, book.Author, find)

        fbk = []
        for i in bks:

            issue = i.issues
            fis = 'None'
            for j in issue:
                if j.uid == usr.ID:
                    fis = j
            if fis == 'None':
                d = {}
                d['ID'] = i.ID
                d["Title"] = i.Title
                d["Author"] = i.Author
                d["Issuedate"] = 'None'
                d["Duedate"] = 'None'
                d['Status'] = 'None'
                fbk.append(d)
                
            else:
                d = {}
                d["ID"] = i.ID
                d["Title"] = i.Title
                d["Author"] = i.Author
                d["Issuedate"] = fis.doi
                d["Duedate"] = fis.dor                
                d['Status'] = fis.cstatus
                fbk.append(d)




        print(fbk)


        fsec = []
        for i in secs:
            d = {}
            d["ID"] = i.ID
            d["Title"] = i.Title
            d["Description"] = i.Description
            fsec.append(d)
        fauth = []
        for i in auths:
            d = {}
            d["ID"] = i.ID
            d["Title"] = i.Title
            d["Author"] = i.Author
            fauth.append(d)

        return jsonify({"books":fbk,"sections":fsec,"authors":fauth}),200



@app.route('/rev/<id>',methods = ['GET','POST'])
@auth_required("token")
def rev(id):
    usr = current_user
    if request.method == "GET":
        d = {}
        d['ID'] = None,
        d['uid'] = None,
        d['bid'] = None,
        d['review'] = None
        rev = review.query.filter_by(bid=id,uid=usr.ID).first()
        sec = book.query.filter_by(ID=id).first()
        if rev:
            d['ID'] = rev.ID
            d['uid'] = rev.uid
            d['bid'] = rev.bid
            d['review'] = rev.Review

        avg = None
        rate = review.query.filter_by(bid=id).all()
        if len(rate) != 0:
            sum = 0
            for r in rate:
                sum += r.Review
            avg = sum/len(rate)

        return jsonify({"data":d, 'sec':sec.Section, 'avg':avg}),200
    
    if request.method == "POST":
        input = request.get_json()
        r = input['rev']
        rev = review.query.filter_by(bid=id,uid=usr.ID).first()
        if rev == None:
            entry = review(bid=id,uid=usr.ID,Review=r)
            db.session.add(entry)
        else:
            rev.Review = r
        db.session.commit()
        return jsonify({"msg": "Noted your review!"}),200
            

@app.route("/auto_revoke")
def auto_revoke():
    date_format = "%Y-%m-%d"
    today = date.today()

    issued_books = db.session.query(issuebook).all()

    overdue_books = []
    for issue in issued_books:
        if issue.dor != None:
            return_date = datetime.strptime(issue.dor, date_format).date()
            if (today - return_date).days > 0:
                overdue_books.append(issue)

    if overdue_books:
        for i in overdue_books:
            db.session.delete(i)
        db.session.commit()

        return jsonify({"msg": "Access for Books with Due Date passed have been revoked"}), 201
    else:
        return jsonify({"msg": "No books to revoke"}), 200


@app.route("/export_csv", methods=["GET", "POST"])
def export_csv():
    task.create_csv.delay()
    return jsonify({"msg": "Exporting CSV File to your mail"}), 201
    

@app.route('/profile',methods = ['GET','POST'])
@auth_required("token")
def profile():
    usr = current_user
    if request.method == "GET":
        bi = issuebook.query.filter_by(uid=usr.ID, cstatus = 'Approved').all()
        l = []
        for i in bi:
            d = {}
            b = book.query.filter_by(ID=i.bid).first()
            d['Id'] = b.ID
            d['Title']=b.Title
            d['Author']=b.Author
            d['IssueDate'] = i.doi
            d['ReturnDate'] = i.dor
            l.append(d)

        return jsonify({"data":l, "Name": usr.Name, "Email": usr.Email}),200
    












if __name__ == '__main__':
    excel.init_excel(app)
    app.run(debug=True)




