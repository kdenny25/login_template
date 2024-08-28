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
                            "password varchar(100) NOT NULL)")

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


