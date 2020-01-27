from flask import Flask, render_template,redirect,url_for 


from wtform_fields import *
from models import *
#Configure app

app = Flask(__name__) #instance(standards-webserver gateway interface)
app.secret_key = 'replace later'
#configure db
app.config['SQLALCHEMY_DATABASE_URI']='postgres://rsppnikzkjceam:c85b4480d3a6dd17538c11359ebca2e1b77e634c52e43777024da075dedba7c0@ec2-3-224-165-85.compute-1.amazonaws.com:5432/ddjrmcfnsr110v'
db = SQLAlchemy(app)
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
        return  redirect(url_for('login'))
    return render_template("index.html",form=reg_form)
@app.route("/login",methods=['GET','POST'])
def login():
    login_form= LoginForm()

    #allow login if validation success
    if login_form.validate_on_submit():
        return "Logged in,finally"
    return render_template("login.html", form=login_form)

if __name__ == "__main__":
    app.run(debug=True) #always runs,debug to avoid restarting server while updating
