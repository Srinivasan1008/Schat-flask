from flask import Flask, render_template #import-Flask-class

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
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #add user to db
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB"
    return render_template("index.html",form=reg_form)


if __name__ == "__main__":
    app.run(debug=True) #always runs,debug to avoid restarting server while updating
