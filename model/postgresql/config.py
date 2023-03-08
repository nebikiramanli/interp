import os
import psycopg2
from dotenv import load_dotenv
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load Environment Variables
load_dotenv(os.path.join(main_project_dir, '.env'))


class Config:
    # Database Environment Variables
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'dbname': Config.DB_NAME
        }
        print(params)
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


def close(conn):
    """
    close database connection
    :param conn:  to close
    """

    if conn is not None:
        conn.close()
        print('Database connection closed.')


if __name__ == '__main__':
    connect()
