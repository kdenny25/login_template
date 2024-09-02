import psycopg2

class Database:
    def __init__(self, connection_string):
        self.con = psycopg2.connect(connection_string)
        self.cursor = self.con.cursor()
        self.create_user_table()


    def create_user_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users( "
                            "userid SERIAL PRIMARY KEY, "
                            "name varchar(50) NOT NULL, "
                            "email varchar(150) NOT NULL, "
                            "password varchar(100) NOT NULL, "
                            "profile_pic BYTEA NOT NULL, "
                            "theme varchar(20) NOT NULL, "
                            "google_account BOOLEAN NOT NULL, "
                            "google_name varchar(50), "
                            "google_email varchar(150)) "
                            )

    def email_exists(self, email):
        """Checks if email already exists in the database"""
        self.cursor.execute("SELECT email "
                            "FROM users "
                            "WHERE email = %s;", (email, ))

        results = self.cursor.fetchall()
        if len(results) == 0:
            return False
        else:
            return True

    def register_user(self, name, email, password, image):
        self.cursor.execute("INSERT INTO users(name, email, password, profile_pic, theme, google_account) "
                            "VALUES(%s, %s, %s, %s, %s, %s);", (name, email, password, psycopg2.Binary(image), 'light', False))
        self.con.commit()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * "
                            "FROM users "
                            "WHERE email = %s;", (email, ))
        result = self.cursor.fetchall()[0]

        return result

    def get_user_by_id(self, userid):
        self.cursor.execute("SELECT * "
                            "FROM users "
                            "WHERE userid = %s;", (userid, ))
        result = self.cursor.fetchall()[0]

        return result

    def update_pic(self, id, image):
        self.cursor.execute("UPDATE users "
                            "SET profile_pic = %s "
                            "WHERE userid = %s", (psycopg2.Binary(image), id))

        self.con.commit()
