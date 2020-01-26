from flask import Flask, render_template #import-Flask-class

from wtform_fields import *
#Configure app

app = Flask(__name__) #instance(standards-webserver gateway interface)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Great success"
    return render_template("index.html",form=reg_form)


if __name__ == "__main__":
    app.run(debug=True) #always runs,debug to avoid restarting server while updating
