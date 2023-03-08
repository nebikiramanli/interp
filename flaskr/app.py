from flask import Flask, render_template
import os
import json
from flaskr.config import Config
from flaskr import listen_rabbitmq
from model.postgresql.notice import Notice

app = Flask(__name__, template_folder='templates')
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

RABBITMQ_HOST = Config.RABBITMQ_HOST
RABBITMQ_PORT = Config.RABBITMQ_PORT
RABBITMQ_QUEUE = Config.RABBITMQ_QUEUE
RABBITMQ_ROUTING_KEY = Config.RABBITMQ_ROUTING_KEY

DB_HOST = Config.DB_HOST
DB_PORT = Config.DB_PORT
DB_USER = Config.DB_USER
DB_PASSWORD = Config.DB_PASSWORD
DB_NAME = Config.DB_NAME
print(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

@app.route('/')
def index():
    name = "TURK.AI"
    return render_template('index.html', name=name)


@app.route('/notices')
def list_notices():
    notice = Notice()
    conn = notice.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    notices_from_db = notice.get_all(conn)
    notice_list = []
    for row in notices_from_db:
        notice_ = {
            'entity_id': row[0],
            'forename': row[1],
            'date_of_birth': row[2],
            'nationalities': row[3],
            'name': row[4],
            'link_self': row[5],
            'link_image': row[6],
            'link_thumbnail': row[7],
            'created_at': row[8],
            'updated_at': row[9],
            'is_deleted': row[10]
        }
        notice_list.append(notice_)

    notice.close(conn)
    headers = ['entity_id', 'forename', 'date_of_birth', 'nationalities', 'name', 'link_self', 'link_image', 'link_thumbnail', 'created_at', 'updated_at', 'is_deleted']

    return render_template('notices.html', notices=notice_list, schema=headers)


if __name__ == '__main__':
    app.run(debug=True)


