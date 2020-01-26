from flask import Flask, render_template #import-Flask-class

app = Flask(__name__) #instance(standards-webserver gateway interface)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():


    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True) #always runs,debug to avoid restarting server while updating
