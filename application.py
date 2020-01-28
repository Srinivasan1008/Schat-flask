from flask import Flask, render_template,redirect,url_for,flash 
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from flask_socketio import SocketIO,send,emit
from wtform_fields import *
from models import *
#Configure app

app = Flask(__name__) #instance(standards-webserver gateway interface)
#app.config['SECRET_KEY'] = 'secret!'
app.secret_key = 'replace later'
#configure db
app.config['SQLALCHEMY_DATABASE_URI']='postgres://rsppnikzkjceam:c85b4480d3a6dd17538c11359ebca2e1b77e634c52e43777024da075dedba7c0@ec2-3-224-165-85.compute-1.amazonaws.com:5432/ddjrmcfnsr110v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#intialize flask-socketio
socketio = SocketIO(app)

#configure flask login
login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    #Updated db if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
   #hash password
        hashed_pswd = pbkdf2_sha256.hash(password)#salts&iteration is taken care

        #add user to db
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully.Please login.','success')
        #print('hi')
        return  redirect(url_for('login'))
    return render_template("index.html",form=reg_form)
@app.route("/login",methods=['GET','POST'])
def login():
    login_form= LoginForm()

    #allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/chat",methods=['GET','POST'])
#@login_required
def chat():
    #if not current_user.is_authenticated:
     #   flash('Please login.','danger')
      #  return redirect(url_for('login'))
    return render_template('chat.html')


@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully','success')
    return redirect(url_for('login'))

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send(data) #send msg to connected client
    emit('some-event','this is a custom event message')

if __name__ == "__main__":
    socketio.run(app,debug=True) #always runs,debug to avoid restarting server while updating
