from sqlalchemy import create_engine
import psycopg2
from send_data_users import send_personal_value
from send_photos_data import send_photos_data
token = input("Введите токен")
yours_id = input("Введите Ваш id")
users_personal = send_personal_value(token, yours_id)
data_photos = send_photos_data(token, yours_id)
db = 'postgresql://arkadiy:gringo98@localhost:5432/findedpeople'
engine = create_engine(db)
connection = engine.connect()
count = 0
links = [ ]
for data_user in users_personal:
    if data_user["id"] == data_photos["id_user"]:
        for element in data_photos["data_photos"]:
            for title_par, value_par in element.items():
                links.append(title_par)
count = """SELECT id FROM mens"""
value_id = count[-1] + 1
finished_value = value_id + len(links)
for data_user in users_personal:
    for n in range(value_id, finished_value):
        column = """INSERT INTO mens(id, first_name, last_name, photos_link) VALUES(%s, %s, %s, %s)"""
        data = (n, data_user["first_name"], data_user["last_name"], links)
        connection.execute(column, data)
