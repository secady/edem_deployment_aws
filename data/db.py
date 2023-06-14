import psycopg2
import pandas as pd
from credentials.Credentials import credentials_data


c = credentials_data()
class Database:
    def __init__ (self):
        database = c.databaser()
        self.url = c.urler()
        self.con = psycopg2.connect(
            host= c.hoster(),
            user= c.userer(),
            password= c.passworder(),
            port= c.porter()
        )
    def close (self):
        self.con.close()

    def get_categories (self):
        query = "SELECT * FROM categories"
        result = pd.read_sql_query(query, self.con)
        return result.to_json()

    def get_events (self):
        query = "SELECT * FROM events"
        result = pd.read_sql_query(query, self.con)
        return result.to_json()

    def get_students (self):
        query = "SELECT * FROM students"
        result = pd.read_sql_query(query, self.con)
        return result.to_json()

 
    



