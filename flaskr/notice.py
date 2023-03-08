from model.postgresql.notice import Notice
import psycopg2
import config


def get_all_notices(db_host, db_port, db_name, db_user, db_password):
    """
    Get all notices
    :param db_host:
    :param db_name:
    :param db_user:
    :param db_password:
    :return notices:
    """
    notices = []
    try:
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        notice = Notice()
        notices = notice.get_all(conn)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return notices



if __name__ == '__main__':
    db_host = config.Config.DB_HOST
    db_port = config.Config.DB_PORT
    db_name = config.Config.DB_NAME
    db_user = config.Config.DB_USER
    db_password = config.Config.DB_PASSWORD

    notices = get_all_notices(db_host, db_port, db_name, db_user, db_password)

