import psycopg2
from datetime import datetime


class Notice:
    def __init__(self):
        self.conn = None
        self.host = None
        self.database = None
        self.user = None
        self.password = None
        self.port = None

    def connect(self, host, port, database, user, password):
        """
        Connect to the PostgreSQL database server
        :param host: database host
        :param port: database port
        :param database: database name
        :param user: database user
        :param password: database password


        :return conn: connection object
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        print("Connecting to the PostgreSQL database...")

        try:
            self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password,
                                         port=self.port)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return self.conn

    def close(self, conn):
        """
        close database connection
        :param conn:
        :return:
        """
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    def create_tables(self, conn):
        """
        Create tables
        :param conn: connection object
        :return:
        """

        commands = (
            """
            CREATE TABLE IF NOT EXISTS notice (
                entity_id text PRIMARY KEY NOT NULL,
                forename text,
                date_of_birth date,
                nationalities text[],
                name text,
                link_self text,
                link_image text,
                link_thumbnail text,
                created_at timestamp,
                updated_at timestamp,
                is_deleted boolean                
                )
            """,
        )

        print("Creating tables...")
        try:
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert(self, conn, data):
        """
        Insert notice into table
        :param conn:
        :param data:
        :return:
        """
        sql = """INSERT INTO notice(entity_id, forename, date_of_birth, nationalities, name, link_self,
                link_image, link_thumbnail, created_at, updated_at, is_deleted )  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        try:
            cur = conn.cursor()
            print(cur.execute(sql, data))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update(self, conn, data):
        """
        Update notice

        :param conn:
        :param data:
        :return:
        """
        sql = """UPDATE notice SET forename = %s, date_of_birth = %s,  nationalities = %s, name = %s, link_self = %s, link_image = %s,
                link_thumbnail = %s, created_at = %s, updated_at = %s, is_deleted = %s
                WHERE entity_id = %s
                """

        '''
        notice = self.prepare_notice(data)
        print("Inserting notice: ", notice)
        '''
        try:
            cur = conn.cursor()
            cur.execute(sql, data)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def delete(self, conn, id):
        """
        Delete notice
        :param conn:
        :param id:
        :return:
        """
        sql = """DELETE FROM notice WHERE id = %s"""
        try:
            cur = conn.cursor()
            cur.execute(sql, (id,))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_all(self, conn):
        """
        Get all notices
        :param conn:
        :return data: list of notices
        """
        sql = """SELECT * FROM notice"""
        try:
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            conn.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_all_deleted(self, conn):
        """
        Get all deleted notices
        :param conn:
        :return:
        """
        sql = """SELECT * FROM notice WHERE is_deleted = true"""
        try:
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_all_not_deleted(self, conn):
        """
        Get all not deleted notices
        :param conn:
        :return:
        """
        sql = """SELECT * FROM notice WHERE is_deleted = false"""
        try:
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_by_name(self, conn, name):
        """
        Get all notices by name
        :param conn:
        :param name:
        :return:
        """
        sql = """SELECT * FROM notice WHERE name = %s"""
        try:
            cur = conn.cursor()
            cur.execute(sql, (name,))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_by_entity_id(self, conn, entity_id):
        """
        Get all notices by entity_id
        :param conn:
        :param entity_id:
        :return:
        """
        sql = """SELECT * FROM notice WHERE entity_id = %s"""
        try:
            cur = conn.cursor()
            cur.execute(sql, (entity_id,))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def prepare_notice(self, data):
        """
        Prepare notice data for insert or update
        :param data:
        :return:
        """
        print(data)
        notice = {}
        if data['nationalities'] is None:
            notice['nationalities'] = []
        else:
            notice['nationalities'] = data['nationalities']

        if data['created_at'] is None:
            notice['created_at'] = datetime.now()

        if data['updated_at'] is None:
            notice['updated_at'] = datetime.now()

        if data['is_deleted'] is None:
            notice['is_deleted'] = False

        notice['entity_id'] = data['entity_id']
        notice['forename'] = data['forename']
        notice['date_of_birth'] = data['date_of_birth']
        notice['nationalities'] = '{' + ' '.join(data['nationalities']) + '}' if data['nationalities'] is not None else None
        notice['name'] = data['name']
        notice['link_self'] = data['_links']['self']['href']
        notice['link_image'] = data['_links']['images']['href']
        notice['link_thumbnail'] = data['_links']['thumbnail']['href']
        notice['created_at'] = data['created_at']
        notice['updated_at'] = data['updated_at']
        notice['is_deleted'] = data['is_deleted']

        notice_tuple = (notice['entity_id'], notice['forename'], notice['date_of_birth'],notice['nationalities'], notice['name'], notice['link_self'],
                        notice['link_image'], notice['link_thumbnail'], notice['created_at'], notice['updated_at'], notice['is_deleted'])

        return notice_tuple

'''
if __name__ == '__main__':

    db_host = 'localhost'
    db_name = 'interpol'
    db_port = 5432
    db_user = 'admin'
    db_password = '123456'

    notice = Notice()
    conn = notice.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)

    # notice.create_tables(conn)
    noti = notice.get_all(conn)
    print(noti)
'''