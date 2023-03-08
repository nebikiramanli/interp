import config
import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""

    commands = (
        """
        CREATE TABLE IF NOT EXISTS notice (
            id uuid PRIMARY KEY NOT NULL,
            forename text,
            date_of_birth date,
            entity_id text,
            nationalities json,
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
    conn = None
    try:
        conn = config.connect()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
