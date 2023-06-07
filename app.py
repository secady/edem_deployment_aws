import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, send_file


app = Flask(__name__)

f = open("credentials/credentials_aws.txt")
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

    <br><br>endpoint: '/get_db_events' 
    <br><br>endpoint: '/get_db_categories' 
    <br><br>endpoint: '/get_db_students' 

    
    """
    return message


# ENDPOINT 2 - Get EDEM's categories data (fake data)
@app.route('/get_db_categories', methods=['GET'])
def get_db_categories():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )

    result = pd.read_sql_query("SELECT * FROM categories", conn)
    conn.close()
    return jsonify(result.to_dict(orient="records"))


# ENDPOINT 3 - Get EDEM's events data (fake data)
@app.route('/get_db_events', methods=['GET'])
def get_db_events():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )

    result = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return jsonify(result.to_dict(orient="records"))


# ENDPOINT 4 - Get EDEM's students data (fake data)
@app.route('/get_db_students', methods=['GET'])
def get_db_students():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )

    result = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return jsonify(result.to_dict(orient="records"))


# ENDPOINT 5 - Get Lanzadera/startups' data (scrap)
@app.route('/get_scrap_startups', methods=['GET'])
def get_scrap_startups():
    with open("Scrap/startups_data.json", "r") as file:
        result = json.load(file)  
    return result


if __name__ == '__main__':
    app.run(debug=True)