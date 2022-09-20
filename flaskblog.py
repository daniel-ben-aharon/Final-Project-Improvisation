import oauth as oauth
import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, url_for, redirect, session, request, flash
import music21
import os



charlie_parker_scores = ["Another_Hairdo.xml","Anthropology.xml","An_Oscar_For_Treadwell.xml","Au_Private_1.xml","Au_Private_2.xml","Back_Home_Blues.xml","Barbados.xml","Billies's_Bounce.xml","Bird_Gets_The_Worm.xml","Bloomdido.xml","Blues_For_Alice.xml","Blue_Bird.xml","Buzzy.xml","Card_Board.xml","Celerity.xml","Chasing_The_Bird.xml","Cheryl.xml","Chi_Chi.xml","Confirmation.xml","Cosmic_Rays.xml","Dewey_Square.xml","Diverse.xml","Donna_Lee.xml","KC_Blues.xml","Kim_1.xml","Kim_2.xml","Ko_Ko.xml","Laird_Baird.xml","Marmaduke.xml","Mohawk_1.xml","Mohawk_2.xml","Moose_The_Mooche.xml","My_Little_Suede_Shoes.xml","Now's_The_Time_1.xml","Now's_The_Time_2.xml","Ornithology.xml","Passport.xml","Perhaps.xml","Red_Cross.xml","Relaxing_With_Lee.xml","Scrapple_From_The_Apple.xml","Segment.xml","Shawnuff.xml","Si_Si.xml","Steeplechase.xml","The_Bird.xml","Thriving_From_A_Riff.xml","Visa.xml","Warming_Up_A_Riff.xml","Yardbird_Suite.xml"]
###   To run FLASK
###   in windows OS:
###   1. set the variable environment of FLASK_APP
###      in this case write in terminal pycharm the following: set FLASK_APP=flaskblog.py
###   2. Run the application using the following command in terminal:  flask run
###   3. To run in 'Debug mode' write terminal python the following command:  set  FLASK_DEBUG = 1

###   in Mac:
###   1. set the variable environment of FLASK_APP
###      in this case write in terminal pycharm the following: export FLASK_APP=flaskblog.py
###   2. Run the application using the following command in terminal:  flask run

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField   # BooleanField for checkbox
from wtforms.validators import InputRequired, Email, Length

from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy        # transfer data is in SQL into python objects
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'  # arbitrary value



Bootstrap(app)

class LoginForm(FlaskForm):            # inherit from FlaskForm
    username = StringField('username', validators=[InputRequired(),Length(min=3,max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
     email = StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
     username = StringField('username',validators=[InputRequired(),Length(min=3,max=15)])
     password = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])
     #create_time = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])


# configure to mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////users.db' # users is name of our DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:danielmysql123benaharondb#&12*-a@localhost/userdb' # userdb is name of our DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = 'danielmysql123benaharondb#&12*-a'
app.config['MYSQL_DB'] = 'userdb'
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow ,nullable=False, unique=True)

    #Create a function to return a string when we add something
    def __repr__(self):
        return '<Name %r' % self.id


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)    # BLOB = Binary Large Object : use LargeBinary to store arbitrary binary data-type in DB

# oauth config
# https://www.youtube.com/watch?v=BfYsdNaHrps&ab_channel=Vuka
oauth = OAuth(app)
google = oauth.register(
    name='google',  # client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_id='1036027860865-hvb11o0o2is9co5ddmvu1mvrli7ejcif.apps.googleusercontent.com', #'1036027860865-urhmpve4q51gig9gu985n89tfpgr09qs.apps.googleusercontent.com',
    client_secret='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', #'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',  # os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},      #  scope=what we want google to give back using token and get method
)


# route direct to if the authentication was successful
@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()   # {'id': '100273396375222979702', 'email': 'danielair100@gmail.com', 'verified_email': True, 'name': 'Daniel BA', 'given_name': 'Daniel', 'family_name': 'BA', 'picture': 'https://lh3.googleusercontent.com/a/AItbvmkMwn_Jf6bzv7k7nU23e9p-KfBfzUMZg9UbEXRS=s96-c', 'locale': 'he'}
    # do something with the token and profile

    session['email'] = user_info['email']
    #session['name'] = user_info['given_name']

    # check if user exists already
    user = Users.query.filter_by(email= user_info['email']).first()
    if user is None:
         return render_template('signin.html')  # sign in if you don't have an account
    return render_template("upload.html")


@app.route('/submit-form', methods = ['POST'])
def submitForm():
    selectValue = request.form.get('select1')
    return(str(selectValue))


#  http://127.0.0.1:5000/    ip of machine
@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    if request.method == 'POST':
        # Fest form data
        file = request.files['file']
            #return f'Uploaded: {file.filename}'
        upload = Upload(filename = file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return render_template('home.html',data = charlie_parker_scores)

        # userDetails = request.form
        # name = userDetails['name']
        # email = userDetails['email']
        # password = userDetails['password']
        # date = datetime.now()
        # id = 0
        # cur = db.connection.cursor()
        # cur.execute("INSERT INTO users(username,email,password,create_time,id) VALUES(%s, %s, %s, %s, %d)",(name, email,password,date, id))
        # db.connection.commit()
        # cur.close()
        # return 'success'

    return render_template('home.html',data = charlie_parker_scores)
    # n = music21.note.Note("G5")
    # return "<p>" + n.name + "</p>"


# Route for handling the login page with google account
@app.route("/loginWithGoogle")
def loginWithGoogle():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():    #  check to works if form is submitted
        return '<h1>' + form.username.data + ' ' + form.password.data + '<h1>'

    return render_template('login.html',form=form)

@app.route("/signin", methods=['GET'])        # register
def signinGet():
   form = RegisterForm()

   print('signin get')
   
   return render_template('signin.html',form=form)


@app.route("/signin", methods=['POST'])        # register
def signinPost():
   form = RegisterForm()
   name = None
   print('signin')
   if form and form.validate_on_submit():
       user = Users.query.filter_by(email=form.email.data).first()
       if user is None:
           user = Users(name=form.username.data, email=form.email.data, password=form.password.data)
           # # Hash the password!!!
           # hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
           # user = Users(username=form.username.data, name=form.name.data, email=form.email.data,password_hash=hashed_pw)
           db.session.add(user)
           db.session.commit()
       name = form.username.data

       # clean the form
       form.username.data = ''
       form.password.data = ''
       form.email.data = ''
       flash("User Added Successfully!")
       our_users = Users.query.order_by(Users.date_added)
       return render_template("upload.html", name=name, user_id = user.id)
   return render_template('signin.html',form=form)

@app.route("/upload",methods=['GET'])
def uploadGet():
    print('uploadget')
    return render_template("upload.html")

@app.route("/uploaded",methods=['POST'])
def uploadPost():
    print('upload post')
    file = request.files['file'] # input of algorithm
    file.save(os.path.join(app.root_path,'static',file.filename))
    # algorithm should run here
    # some result music.
        
    music_xml = file # output of the algorithm
    return render_template("verovio.html", music_xml=music_xml, filename=file.filename)
        # upload = Upload(filename = file.filename, data=file.read())
        # db.session.add(upload)
        # db.session.commit()


@app.route('/logout')
def logout():
    for key in list(session.key()):
        session.pop(key)
    return redirect('/')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)


#  To create a DB:
#  https://www.youtube.com/watch?v=hQl2wyJvK5k&ab_channel=Codemy.com
#  1.  Create Model  (Class)
#  2.  Add command that add data to DB
#  3.  Add command of commit:             db.session.commit()
#  4.  From terminal write the following commands:
#     (i)  from flaskblog.py import db
#     (ii) db.create_all()

# s = converter.parse(r'C:\Users\Daniel ben aharon\Desktop\Final Project\charlie_parker\Cheryl.xml')
# print(s)
