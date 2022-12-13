from flask import Flask, render_template, request, redirect
from models import Email, Record, Adress, Phone
from db import db_session

app = Flask(__name__)
app.debug = True
app.env = "development"


@app.route("/", strict_slashes=False)
def index():
    records = db_session.query(Record).all()
    phones = db_session.query(Phone).all()
    return render_template("index.html", records=records, phones=phones)




if __name__ == "__main__":
    app.run()
