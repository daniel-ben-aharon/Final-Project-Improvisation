import oauth as oauth
from authlib.integrations.flask_client import OAuth

from extractNotes import improvise, add2dict

from flask import Flask, render_template, url_for, redirect, session, request, flash
import music21
from music21 import *
import os
import mysql.connector
import os
import pickle

# connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    #passwd="danielmysql123benaharondb#&12*-a",
    database="userdb"
)

db_cursor = mydb.cursor(buffered=True)

charlie_parker_scores = ["Another_Hairdo.xml","Anthropology.xml","An_Oscar_For_Treadwell.xml","Au_Private_1.xml","Au_Private_2.xml","Back_Home_Blues.xml","Barbados.xml","Billies's_Bounce.xml","Bird_Gets_The_Worm.xml","Bloomdido.xml","Blues_For_Alice.xml","Blue_Bird.xml","Buzzy.xml","Card_Board.xml","Celerity.xml","Chasing_The_Bird.xml","Cheryl.xml","Chi_Chi.xml","Confirmation.xml","Cosmic_Rays.xml","Dewey_Square.xml","Diverse.xml","Donna_Lee.xml","KC_Blues.xml","Kim_1.xml","Kim_2.xml","Ko_Ko.xml","Laird_Baird.xml","Marmaduke.xml","Mohawk_1.xml","Mohawk_2.xml","Moose_The_Mooche.xml","My_Little_Suede_Shoes.xml","Now's_The_Time_1.xml","Now's_The_Time_2.xml","Ornithology.xml","Passport.xml","Perhaps.xml","Red_Cross.xml","Relaxing_With_Lee.xml","Scrapple_From_The_Apple.xml","Segment.xml","Shawnuff.xml","Si_Si.xml","Steeplechase.xml","The_Bird.xml","Thriving_From_A_Riff.xml","Visa.xml","Warming_Up_A_Riff.xml","Yardbird_Suite.xml"]

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length

from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy      # transfer data is in SQL into python objects
from datetime import datetime

dictionary = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'  # arbitrary value



Bootstrap(app)

class LoginForm(FlaskForm):            
    username = StringField('username', validators=[InputRequired(),Length(min=3,max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
     email = StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
     username = StringField('username',validators=[InputRequired(),Length(min=3,max=15)])
     password = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])
     #create_time = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])

class ChosenXmlForm(FlaskForm):
     xml_filename = SelectField('filename',validators=[InputRequired()])
     speed = StringField('speed',validators=[InputRequired()])
    
   
# configure to mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////users.db' # users is name of our DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost/userdb' # userdb is name of our DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'userdb'
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow ,nullable=False, unique=True)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)    # BLOB = Binary Large Object : use LargeBinary to store arbitrary binary data-type in DB

# create the db tables automatically when the application rises
with app.app_context():
    db.create_all()
    db.session.commit()

# oauth config
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
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
)


# route direct to if the authentication was successful
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()
    print(token)
    resp = google.get('userinfo')
    resp.raise_for_status()
    # {'id': '100273396375222979702', 'email': 'danielair100@gmail.com', 'verified_email': True, 'name': 'Daniel BA', 'given_name': 'Daniel', 'family_name': 'BA', 'picture': 'https://lh3.googleusercontent.com/a/AItbvmkMwn_Jf6bzv7k7nU23e9p-KfBfzUMZg9UbEXRS=s96-c', 'locale': 'he'}
    user_info = resp.json()   
    print(user_info)
    # do something with the token and profile

    session['email'] = user_info['email']
    session['name'] = user_info['name']

    xmls = get_xmls()
    return render_template("profile.html", name=user_info['name'], email=user_info['email'],xmls=xmls)


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
    return render_template('home.html',data = charlie_parker_scores)



# Route for handling the login page with google account
@app.route("/loginWithGoogle")
def loginWithGoogle():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():    
        query = 'SELECT * FROM users WHERE name="'+form.username.data + '"'
        print(query)
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        user = results[0]
        print(user)
        password = user[3]
        if password == form.password.data:
            print('user authenticated')
            # clean the form
            form.username.data = ''
            form.password.data = ''
            xmls = get_xmls()
            return render_template("profile.html", name=user[1], email=user[2],xmls=xmls)

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
    print('signin post')
    if form and form.validate_on_submit():
        print(form.email.data)
        query = 'SELECT * FROM users WHERE email="'+form.email.data + '"'
        print(query)
        user = db_cursor.execute(query)
        print(user)
        if user is None:
            print('new user')
            query = f'INSERT INTO users (name, email, password) VALUES ("{form.username.data}", "{form.email.data}", "{form.password.data}");'
            print(query)
            user = db_cursor.execute(query)
            mydb.commit()
        
        name = form.username.data
        email = form.email.data

        # clean the form
        form.username.data = ''
        form.password.data = ''
        form.email.data = ''
        flash("User Added Successfully!")

        xmls = get_xmls()

        return render_template("profile.html", name=name, email=email,xmls=xmls)
    return render_template('signin.html',form=form)

@app.route("/profile", methods=['GET'])        
def profile():
    query = 'SELECT * from xmltable2'
    db_cursor.execute(query)
    xmls = db_cursor.fetchall()
    for xml in xmls:
        print(xml[1])
    return render_template("profile.html", name='Anonymous', email='Anonymous',xmls=xmls)


@app.route("/upload",methods=['GET'])
def uploadGet():
    print('uploadget')
    return render_template("upload.html")

@app.route("/uploaded",methods=['POST'])
def uploadPost():
    
    file = request.files['file'] # input of algorithm
    speed = int(request.form.get('speed'))
    print(speed)
    content = file.stream.read().decode('utf-8')
    
    # check if the file is already exists in db
    EXIST_QUERY = f'SHOW COLUMNS FROM userdb.xmltable2 LIKE \'%{file.filename}%\''
    
    # if if is a new file
    if db_cursor.execute(EXIST_QUERY) is not None:
        INSERT_QUERY = f"INSERT INTO XMLTable (XML, name) VALUES (%s, %s)"
        values = (content, file.filename)
        db_cursor.execute(INSERT_QUERY,values)
        mydb.commit()
        
        # if it is a new file data to dict
        add2dict(file.filename,dictionary,content)
    
    INSERT_QUERY = f"INSERT INTO XMLTable2 (XML, name) VALUES (%s, %s)"
    values = (content, file.filename)
    db_cursor.execute(INSERT_QUERY,values)
    mydb.commit()
    

    improv = improvise(file.filename, content, speed)
    INSERT_QUERY = f"INSERT INTO improvs (XML, name) VALUES (%s, %s)"
    improv_values = (improv, file.filename)
    db_cursor.execute(INSERT_QUERY,improv_values)
    mydb.commit()
    #file.save(os.path.join(app.root_path,'static',file.filename))
    # algorithm should run here
    # some result music.
    # newFile = algo(file)
    # newFile.save(os.path.join(app.root_path,'static',newFile.filename))
    
    return render_template("verovio.html", music_xml_improv=improv, music_xml_original=content, filename=file.filename)
  

@app.route("/chosen",methods=['POST'])
def chosenXml():
    print('chosenXml')
    form = ChosenXmlForm()
    xml_filename=form.xml_filename.data
    speed = int(form.speed.data)
    print(speed)
    query = f'SELECT * from xmltable2 WHERE name="{xml_filename}"'
    db_cursor.execute(query)
    xml = db_cursor.fetchall()[0]
   
    
    original_music_xml = xml[2]
    improv = improvise(xml_filename, original_music_xml, speed)
    INSERT_QUERY = f"INSERT INTO improvs (XML, name) VALUES (%s, %s)"
    improv_values = (improv, xml_filename)
    db_cursor.execute(INSERT_QUERY,improv_values)
    mydb.commit()
    
    # algorithm should run here
    # some result music.
    # newFile = algo(file)
    # newFile.save(os.path.join(app.root_path,'static',newFile.filename))
        
    return render_template("verovio.html", music_xml_improv=improv,music_xml_original=original_music_xml, filename=xml_filename)


@app.route('/logout')
def logout():
    for key in list(session.key()):
        session.pop(key)
    return redirect('/')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


def get_xmls():
    query = 'SELECT * from xmltable2'
    db_cursor.execute(query)
    xmls = db_cursor.fetchall()
    return xmls


if __name__ == '__main__':
    # Specify path
    # path = '/usr/local/bin/'  # for linux
    path = 'dictcache'
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if isExist:
        # load dictionary from file
        with open('dictcache', 'rb') as f:
            dictionary = pickle.load(f)
            
    app.run(debug=True)
