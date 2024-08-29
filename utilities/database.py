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
                            "profile_pic BYTEA NOT NULL)")

    def email_exists(self, email):
        """Checks if email already exists in the database"""
        self.cursor.execute("SELECT email "
                            "FROM users "
                            "WHERE email = %s;", (email, ))

        results = self.cursor.fetchall()
        print(results)
        if len(results) == 0:
            return False
        else:
            return True

    def register_user(self, name, email, password, image):
        self.cursor.execute("INSERT INTO users(name, email, password, profile_pic) "
                            "VALUES(%s, %s, %s, %s);", (name, email, password, image))
        self.con.commit()

    def get_user(self, email):
        self.cursor.execute("SELECT * "
                            "FROM users "
                            "WHERE email = %s;", (email, ))
        result = self.cursor.fetchall()[0]

        return result