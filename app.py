import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, send_file


app = Flask(__name__)

f = open("credentials_railway_hospitable-direction.txt")
lines=f.readlines()
host=lines[0][7:-1].strip()
database=lines[1][11:].strip()
user=lines[2][7:].strip()
password=lines[3][11:].strip()
port=lines[4][7:].strip()
url=lines[5][6:].strip()
f.close()


# ENDPOINT 1 - Home
@app.route('/', methods=['GET'])
def home():
    message = f"""
    Welcome! To extract data, please see the following instructions:

    <br><br>endpoint: '/get_db_users' 

    
    """
    return message


# ENDPOINT 2 - Get EDEM's students data (fake data)
@app.route('/get_db_users', methods=['GET'])
def get_db_users():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    result = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return jsonify(result.to_dict(orient="records"))



if __name__ == '__main__':
    app.run(debug=True)