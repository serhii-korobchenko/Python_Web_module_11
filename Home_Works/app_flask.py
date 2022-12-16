from flask import Flask, render_template, request, redirect, flash
from models import Email, Record, Adress, Phone
from db import db_session
from Pekemons_IT_CLI_bot_with_SQLite import main

app = Flask(__name__)
app.secret_key = b'bbcec4566'
app.debug = True
app.env = "development"

class Record_Object:
    def __init__(self, name, phone, adress=None, email=None):
        self.name = name
        self.phone = phone
        self.adress = adress
        self.email = email


@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
def index():


    command = None
    records = db_session.query(Record).all()
    phones = db_session.query(Phone).all()

    record_list = []
    for record in records:
        record_id = record.id
        phone = db_session.query(Phone.phone_name).filter(Phone.rec_id == record.id).all() if db_session.query(Phone.phone_name).filter(Phone.rec_id == record.id).all() else '*'
        adress = db_session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all() if db_session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all() else '*'
        email = db_session.query(Email.email_name).filter(Email.rec_id == record.id).all() if db_session.query(Email.email_name).filter(Email.rec_id == record.id).all() else '*'
        item_rec = Record_Object(record.name, phone, adress, email)
        item_rec.record_id = record_id

        record_list.append(item_rec)

    if request.method == "POST":
        command = request.form.get("command")
        main(command)


        return redirect("/")



    return render_template("index.html", records=records, phones=phones, record_list=record_list)











    #return render_template("index.html", records=records, phones=phones, record_list=record_list)



if __name__ == "__main__":
    app.run()
