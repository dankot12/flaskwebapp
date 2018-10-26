import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imageup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image_url = db.Column(db.String(1000))


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    user_name = request.form["name"]
    file = request.files["file"]
    # print(file)
    # print(user_name)
    filename = file.filename
    filename = user_name + ".jpg"
    destination = "/".join([target, filename])
    # print(destination)
    file.save(destination)

    signature = Users(name=user_name, image_url=destination)
    db.session.add(signature)
    db.session.commit()

    return render_template("complete.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
