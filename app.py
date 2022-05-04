import os 
from flask import Flask, redirect, request, flash, url_for
from flask import render_template 
from flask_sqlalchemy import SQLAlchemy 
import datetime

# ---- time -----
t = datetime.datetime.today()
y = t.year
m = t.month
d = t.day
timeNow = str(t.time().hour) + ":" + str(t.time().minute)



current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "test3.db")

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model): 
    __tablename__ = 'user'
    user_id = db.Column(db.String, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

class Physical(db.Model): 
    __tablename__ = 'physical'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.String, nullable=False)
    timeStamp = db.Column(db.String, nullable=False)
    activity = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String)
    time = db.Column(db.String, nullable=False)
    year = db.Column(db.Numeric)
    month = db.Column(db.Numeric)
    day = db.Column(db.String)

class Emotional(db.Model):
    __tablename__ = 'emotional'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.String, nullable=False)
    timeStamp = db.Column(db.String, nullable=False)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    note = db.Column(db.String)
    time = db.Column(db.String, nullable=False)
    year = db.Column(db.Numeric)
    month = db.Column(db.Numeric)
    day = db.Column(db.String)

class Social(db.Model): 
    __tablename__ = 'social'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.String, nullable=False)
    timeStamp = db.Column(db.String, nullable=False)
    note = db.Column(db.String)
    score = db.Column(db.Integer)
    time = db.Column(db.String, nullable=False)
    year = db.Column(db.Numeric)
    month = db.Column(db.Numeric)
    day = db.Column(db.String)

class Spiritual(db.Model): 
    __tablename__ = 'spiritual'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timeStamp = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    length = db.Column(db.Numeric, nullable=False)
    note = db.Column(db.String)
    time = db.Column(db.String, nullable=False)
    year = db.Column(db.Numeric)
    month = db.Column(db.Numeric)
    day = db.Column(db.String)

class Intellectual(db.Model): 
    __tablename__ = 'intellectual2'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.String, nullable=False)
    timeStamp = db.Column(db.String, nullable=False)
    activity = db.Column(db.String)
    length = db.Column(db.Numeric, nullable=False)
    note = db.Column(db.String)
    time = db.Column(db.String, nullable=False)
    year = db.Column(db.Numeric)
    month = db.Column(db.Numeric)
    day = db.Column(db.String)

#-----home and login page 
@app.route("/", methods=['GET', 'POST'])
def home():
     return render_template("login.html")


user1 = ''

@app.route("/home/", methods=['GET', 'POST'])
def login():
    user_exists = False 
    correct = False
    u_name = request.form['u_name']
    pass_word = request.form['pass']
    data = User.query.filter(User.user_id == u_name).first()
    if data != None:  
        correct = False 
        user_exists = True
        if data.password == pass_word:
            correct = True
            #user1 = u_name
        
    return render_template("dash.html", username=u_name, logged = correct, correct = correct, user_exists=user_exists, already_there=False)

@app.route("/<user>/", methods=['GET', 'POST'])
def dashboard(user): 
    if request.method == 'GET' or request.method == 'POST': 
        u1 = User.query.filter(User.user_id == user).first() 
        uname = u1.user_id
        return render_template("dashboard.html", username=uname, logged=True)

@app.route("/new", methods=['GET', 'POST'])
def new_user():
    u_name = request.form['u_name']
    pass_word = request.form['pass']
    name = request.form['name']
    data = User.query.filter(User.user_id == u_name).first()
    if data == None: 
        new = User(user_id = u_name, password = pass_word, name = name)
        db.session.add(new)
        db.session.commit()
        correct = True
        return render_template("dash.html", username = u_name, logged = correct, correct = correct, user_exists=True, already_there=False)
    return render_template("dash.html", already_there=True)


#---- trackers  ------
@app.route("/<string:user>/add/<string:type>/", methods=['GET', 'POST'])
def add_tracker(user,type): 
    name = User.query.filter_by(user_id = user).all()
    return render_template("add_tracker.html", type=type, username=user, logged = True, add = True, update=False)

@app.route("/<string:user>/social/", methods=['GET', 'POST'])
def social(user): 
    data = Social.query.filter(Social.user == user).all()
    grouping = db.session.execute("SELECT sum(s.score), s.day FROM social as s WHERE s.user = :u GROUP BY s.day;", {'u': user}).fetchall()
    y_data = [i[0] for i in grouping]
    x_data = [i[1] for i in grouping]
    if request.method == "GET":
        return render_template("social.html", data=data, labels = x_data, values = y_data, username=user, logged = True)
        #return render_template("test.html")
    elif request.method == 'POST': 
        note = request.form['note']
        year, month, day,time = y,m,d,timeNow
        day2 = str(month) + "-" + str(day) + "-" + str(year)
        ques = [request.form['q1'], request.form['q2'], request.form['q3'], request.form['q4'], request.form['q5']]
        score = ques.count('y')
    

        row = Social(score = score,note=note, time = time, year = year, month = month, day = day2, timeStamp = t, user=user)
        try: 
            db.session.add(row)
            db.session.commit()

            return render_template("added.html", username=user, logged = True, track_type='Social')
            #return render_template("test.html")
        except: 
            "ISSUE"
        return redirect("/social/")

@app.route("/<string:user>/emotional/", methods=['GET', 'POST'])
def emotional(user):
    data = Emotional.query.filter(Emotional.user == user).all()
    #x_data = [i.day for i in data]
    #y_data = []
    grouping = db.session.execute("SELECT sum(e.q1), sum(e.q2), sum(e.q3),sum(e.q4), sum(e.q5), sum(e.q6),sum(e.q7), sum(e.q8), e.day FROM emotional as e WHERE e.user = :u GROUP BY e.day;", {'u': user}).fetchall()
    x_data = [i[8] for i in grouping]
    q1_data = [i[0] for i in grouping]
    q2_data = [i[1] for i in grouping]
    q3_data = [i[2] for i in grouping]
    q4_data = [i[3] for i in grouping]
    q5_data = [i[4] for i in grouping]
    q6_data = [i[5] for i in grouping]
    q7_data = [i[6] for i in grouping]
    q8_data = [i[7] for i in grouping]

    
    if request.method == "GET":
        return render_template("emotional.html", data=data, labels = x_data, q1_data=q1_data, q2_data=q2_data,q3_data=q3_data,q4_data=q4_data,q5_data=q5_data,q6_data=q6_data,q7_data=q7_data,q8_data=q8_data, username=user, logged = True)
        #return render_template("test.html")
    elif request.method == 'POST': 
        note = request.form['note']
        year, month, day,time = y,m,d,timeNow
        q1,q2,q3,q4,q5,q6,q7,q8 = request.form['q1'], request.form['q2'], request.form['q3'],request.form['q4'], request.form['q5'], request.form['q6'],request.form['q7'], request.form['q8']
        day2 = str(month) + "-" + str(day) + "-" + str(year)

        row = Emotional(q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,note=note, time = time, year = year, month = month, day = day2, timeStamp = t, user=user)
        try: 
            db.session.add(row)
            db.session.commit()

            return render_template("added.html", username=user, logged = True, track_type='Emotional')
            #return render_template("test.html")
        except: 
            "ISSUE"
        return redirect("/emotional/")


#"{{ url_for('physical', user=user) }}"
@app.route("/<string:user>/physical/", methods=['GET', 'POST'])
def physical(user): 
    data = Physical.query.filter(Physical.user.in_([user])).all()
    #y_data = [float(i.length) for i in data]
    #x_data = [i.day for i in data]
    grouping = db.session.execute("SELECT sum(p.length), p.day FROM physical as p WHERE p.user = :u GROUP BY p.day;", {'u': user}).fetchall()
    y_data = [i[0] for i in grouping]
    x_data = [i[1] for i in grouping]

    if request.method == "GET":
       # data = Physical.query.filter_by().all()
        return render_template("physical.html", data=data, labels = x_data, values = y_data, username=user, logged = True)
        #return render_template("test.html")
    elif request.method == 'POST': 
        activity = request.form['activity']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        length = 60 * hours + minutes
        note = request.form['note']
        year, month, day,time = y,m,d,timeNow
        day2 = str(month) + "-" + str(day) + "-" + str(year)

        row = Physical(user = user, activity=activity, length=length,note=note, time = time, year = year, month = month, day = day2, timeStamp = t)
        try: 
            db.session.add(row)
            db.session.commit()

            return render_template("added.html", username=user, logged = True, track_type='Physical')
            #return render_template("test.html")
        except: 
            "ISSUE"
        return redirect("/physical/")

@app.route("/<string:user>/intellectual/", methods=['GET', 'POST'])
def intellectual(user): 
    data = Intellectual.query.filter(Intellectual.user == user).all()
    grouping = db.session.execute("SELECT sum(i.length), i.day FROM intellectual2 as i WHERE i.user = :u GROUP BY i.day;", {'u': user}).fetchall()
    y_data = [i[0] for i in grouping]
    x_data = [i[1] for i in grouping]
    if request.method == "GET":
        return render_template("intellectual.html", data=data, labels = x_data, values = y_data, username=user, logged = True)
        #return render_template("test.html")
    elif request.method == 'POST': 
        activity = request.form['activity']
        length = request.form['minutes']
        note = request.form['note']
        year, month, day,time = y,m,d,timeNow
        day2 = str(month) + "-" + str(day) + "-" + str(year)

        row = Intellectual(user = user, activity=activity, length=length,note=note, time = time, year = year, month = month, day = day2, timeStamp = t)
        try: 
            db.session.add(row)
            db.session.commit()

            return render_template("added.html", username=user, logged = True, track_type='Intellectual')
            #return render_template("test.html")
        except: 
            "ISSUE"
        return redirect("/intellectual/")

@app.route("/<string:user>/spiritual/", methods=['GET', 'POST'])
def spiritual(user): 
    data = Spiritual.query.filter(Spiritual.user == user).all()
    grouping = db.session.execute("SELECT sum(s.length), s.day FROM spiritual as s WHERE s.user = :u GROUP BY s.day;", {'u': user}).fetchall()
    y_data = [i[0] for i in grouping]
    x_data = [i[1] for i in grouping]
    if request.method == "GET":
        return render_template("spiritual.html", data=data, labels = x_data, values = y_data, username=user, logged = True)
        #return render_template("test.html")
    elif request.method == 'POST': 
        
        length = request.form['minutes']
        note = request.form['note']
        year, month, day,time = y,m,d,timeNow
        day2 = str(month) + "-" + str(day) + "-" + str(year)

        row = Spiritual(user = user, length=length,note=note, time = time, year = year, month = month, day = day2, timeStamp = t)
        try: 
            db.session.add(row)
            db.session.commit()

            return render_template("added.html", username=user, logged = True, track_type='Spiritual')
            #return render_template("test.html")
        except: 
            "ISSUE"
        return redirect("/spiritual/")

#----------------------------

@app.route("/<string:user>/delete/<string:type>/<t_id>", methods=['GET', 'POST'])
def delete_tracker(user, type, t_id): 
    if type == 'physical':
        tracker = Physical.query.filter(Physical.id == t_id).first()
    if type == 'emotional': 
        tracker = Emotional.query.filter(Emotional.id == t_id).first()
    if type == 'social': 
        tracker = Social.query.filter(Social.id == t_id).first()
    if type == 'intellectual': 
        tracker = Intellectual.query.filter(Intellectual.id == t_id).first()
    if type == 'spiritual': 
        tracker = Spiritual.query.filter(Spiritual.id == t_id).first()
    db.session.delete(tracker)
    db.session.commit()
    return redirect(url_for(type, user=user))

@app.route("/<string:user>/update/<string:type>/<t_id>", methods=['GET', 'POST'])
def update(user, type, t_id): 
    if type == 'physical': 
        tracker = Physical.query.filter(Physical.id == t_id).first()
    if type == 'emotional': 
        tracker = Emotional.query.filter(Emotional.id == t_id).first()
    if type == 'social': 
        tracker = Social.query.filter(Social.id == t_id).first() 
    if type == 'intellectual': 
        tracker = Intellectual.query.filter(Intellectual.id == t_id).first()
    if type == 'spiritual': 
        tracker = Spiritual.query.filter(Spiritual.id == t_id).first()
    return render_template('add_tracker.html', type=type, item=tracker, add=False, update=True, username=user)

@app.route("/<string:user>/updated/<string:type>/<t_id>", methods=['GET', 'POST'])
def update_tracker(user, type, t_id): 
    if type == 'physical': 
        tracker = Physical.query.filter(Physical.id == t_id).first()
        tracker.activiy = request.form['activity']
        tracker.length = request.form['hours']
        tracker.note = request.form['note']
    if type == 'emotional': 
        tracker = Emotional.query.filter(Emotional.id == t_id).first()
        tracker.q1 = request.form['q1']
        tracker.q2 = request.form['q2']
        tracker.q3 = request.form['q3']
        tracker.note = request.form['note']
    if type == 'social': 
        tracker = Social.query.filter(Physical.id == t_id).first()
        ques = [request.form['q1'], request.form['q2'], request.form['q3'], request.form['q4'], request.form['q5']]
        score = ques.count('y')
        tracker.note = request.form['note'] 
        tracker.score = score
    if type == 'intellectual': 
        tracker = Intellectual.query.filter(Intellectual.id == t_id).first()
        tracker.activiy = request.form['activity']
        tracker.length = request.form['minutes']
        tracker.note = request.form['note'] 
    if type == 'spiritual': 
        tracker = Spiritual.query.filter(Spiritual.id == t_id).first()
        tracker.length = request.form['minutes']
        tracker.note = request.form['note']
    db.session.commit()
    return redirect(url_for(type, user=user))


if __name__ == '__main__': 
    app.secret_key='123456'
    app.run(debug=True)
    