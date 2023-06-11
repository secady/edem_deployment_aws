import psycopg2


host= "database-1.chaf71z5ycev.eu-north-1.rds.amazonaws.com"
database= "database-1"
user= "postgres"
password= "edemdb1234"
port= 5432
url= "postgresql://postgres:edemdb1234@database-1.chaf71z5ycev.eu-north-1.rds.amazonaws.com:5432/"


class Database:
    def __init__ (self):
        self.database = database
        self.url = url
        self.con = psycopg2.connect(
            host= host,
            user= user,
            password= password,
            port= port
        )
    def close (self):
        self.con.close()

    def get_categories (self):
        query = "SELECT * FROM categories"
        cursor = self.con.cursor()
        return cursor.execute(query).fetchall()

    def get_events (self):
        query = "SELECT * FROM events"
        cursor = self.con.cursor()
        return cursor.execute(query).fetchall()

    def get_students (self):
        query = "SELECT * FROM students"
        cursor = self.con.cursor()
        return cursor.execute(query).fetchall()
    



