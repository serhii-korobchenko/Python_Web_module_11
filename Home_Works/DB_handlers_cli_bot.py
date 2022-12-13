from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Email, Record, Adress, Phone
from sqlalchemy import and_
from sqlalchemy.schema import MetaData
from sqlalchemy import or_




def look_up_DB (text):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()


    """
    SELECT r.name, r.created, p.phone_name
    FROM records r
    LEFT JOIN phones p ON r.id = p.rec_id
    """
    # result = session.query\
    #     (Record.name, Record.created, Phone.phone_name, Email.email_name) \
    #     .select_from(Record)\
    #     .join(Email) \
    #     .join(Adress) \
    #     .join(Phone).all()
    #
    # print (result)
    query_list = [(Record.name, Record.id), (Record.created, Record.id), (Email.email_name, Email.rec_id),\
                  (Adress.adress_name, Adress.rec_id), (Phone.phone_name, Phone.rec_id)]
    for item in query_list:

        if session.query(item[0]).all():
            #print(session.query(item[0], item[1]).all())
            rec_id = session.query(item[1]).all()
            #print(f'rec_id = {rec_id}')

            for outer in session.query(item[0], item[1]).all():
                #print (outer[0])

                if type(outer[0]) != str:
                    lookup_res = outer[0].strftime('%A %d %B %Y')
                else:
                    lookup_res = outer[0]

                if lookup_res.lower().find(text.lower()) >= 0:
                    print(
                        f'Looked up text was found in next statement: "{lookup_res}" in record: "{session.query(Record.name).filter(Record.id == outer[1]).first()[0]}"')
















"""
    Знайти 5 студентів з найбільшим середнім балом по всім предметам
    :return:
    """
# result = session.query
#     (Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
#     .select_from(Grade).\
#     join(Student).\
#     group_by(Student.id).\
#     order_by(desc('avg_grade')).\
#     imit(5).all()
# return result


# SELECT s.name_student, round (avg(g.grade), 2) AS avg_grade
# FROM grades g
# LEFT JOIN students s ON s.id = g.student_id
# GROUP BY s.id
# ORDER BY avg_grade DESC
# LIMIT 5;



def add_records_DB(name, phone):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    phone1 = Phone(phone_name=phone)
    rec1 = Record(name=name, phone=[phone1])
    session.add(rec1)
    session.commit()
    session.close()

def change_phone_DB(name, new_phone):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    phone1 = session.query(Phone).filter(Phone.rec_id == str(session.query(Record.id).filter(Record.name == name).first()[0]))
    phone1.update({'phone_name': new_phone})
    session.commit()
    session.close()

def add_phone_DB(name, phone):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    phone1 = Phone(phone_name=phone, rec_id=str(session.query(Record.id).filter(Record.name == name).first()[0]))
    session.add(phone1)
    session.commit()
    session.close()

def del_phone_DB(name, phone):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    phone1 = session.query(Phone).filter(and_(Phone.phone_name == phone, Phone.rec_id==str(session.query(Record.id).filter(Record.name == name).first()[0])))
    phone1.delete()
    session.commit()
    session.close()

def del_rec_DB(name):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    rec1 = session.query(Record).filter(Record.name == name)
    rec1.delete()
    session.commit()
    session.close()

def add_email_DB(name, email):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    email1 = Email(email_name=email, rec_id=str(session.query(Record.id).filter(Record.name == name).first()[0]))
    session.add(email1)
    session.commit()
    session.close()

def change_email_DB(name, new_email):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    email1 = session.query(Email).filter(Email.rec_id == str(session.query(Record.id).filter(Record.name == name).first()[0]))
    email1.update({'email_name': new_email})
    session.commit()
    session.close()

def add_adress_DB(name, adress):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    adress1 = Adress(adress_name=adress, rec_id=str(session.query(Record.id).filter(Record.name == name).first()[0]))
    session.add(adress1)
    session.commit()
    session.close()

def change_adress_DB(name, new_adress):
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    adress1 = session.query(Adress).filter(Adress.rec_id == str(session.query(Record.id).filter(Record.name == name).first()[0]))
    adress1.update({'adress_name': new_adress})
    session.commit()
    session.close()


def load_DB():
    engine = create_engine("sqlite:///cli_bot.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    records_DB = session.query(Record).all()

    DB_dict = {}
    for record in records_DB:
        record_dict = {
            'Name': record.name,
            'Phone': session.query(Phone.phone_name).filter(Phone.rec_id == record.id).one()[0],
            'Birthday': None,
            'Email': session.query(Email.email_name).filter(Email.rec_id == record.id).all(),
            'Adress': session.query(Adress.adress_name).filter(Adress.rec_id == record.id).all()
        }
        DB_dict[record.name] = record_dict

    return DB_dict
    # self.data[name] = Record()

    # def __init__(self) -> None:
    #
    #     self.name = Name()
    #     self.phone = Phone(add_book.phone)
    #     self.email = Email()
    #     self.adress = Adress()
    #     self.record_dict = {
    #         'Name': self.name.value,
    #         'Phone': [self.phone.value],
    #         'Birthday': None,
    #         'Email': None,
    #         'Adress': None
    #     }


if __name__ == '__main__':
    # add_records_DB('Andrii', '888888888')
    # change_phone_DB('Bumba', '111111111')
    # add_phone_DB('Bumba', '2222222222')
    # del_phone_DB('Bumba', '2222222222')
    # del_rec_DB('Andrii')
    # add_email_DB('Bumba', '1@1.1')
    # change_email_DB('Bumba', '2@2.2')
    # add_adress_DB('Bumba', 'Vinica')
    # change_adress_DB('Bumba', 'Lviv')
    #look_up_DB ('11')
    res= load_DB()
    print(res)






