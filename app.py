from flask import Flask, jsonify, request
from data.db import Database
from config import error_handling
from functions.bad_language import TextFilter
from functions.events_recommendation_class import EventRecommendation
from sqlalchemy import create_engine, text, MetaData
from joblib import load
import json
import pandas as pd
import requests
from sqlalchemy import create_engine, text, MetaData
from classes import RecommendUsers

app = Flask(__name__)

# Information page of the endpoints:
@app.route('/', methods=['GET'])
def home():
    message = f"""
    Welcome! To extract data, please see the following instructions:

    <br><br>endpoint: '/get_db_events' 
    <br><br>endpoint: '/get_db_categories' 
    <br><br>endpoint: '/get_db_students' 
    <br><br>endpoint: '/get_scrap_startups'
    <br><br>endpoint: '/get_recommendation_events' --> Params: "requested_student_id"
    <br><br>endpoint: '/get_bad_language_filter' --> Params: "text"
    <br><br>endpoint: '/recommend_users' 
    
    """
    return message


# ENDPOINT 1 - Get a dict with the table "categories"
@app.route('/get_db_categories', methods=['GET'])
def get_db_categories():
    db = Database()
    result = db.get_categories()
    db.close()
    return jsonify(result)

# ENDPOINT 2 - Get a dict with the table "events"
@app.route('/get_db_events', methods=['GET'])
def get_db_events():
    db = Database()
    result = db.get_events()
    db.close()
    return jsonify(result)

# ENDPOINT 3 - Get a dict with the table "students"
@app.route('/get_db_students', methods=['GET'])
def get_db_students():
    db = Database()
    result = db.get_students()
    db.close()
    return jsonify(result)

# ENDPOINT 4 - Get a dict with information of start-ups
@app.route('/get_scrap_startups', methods=['GET'])
def get_scrap_startups():
    engine = create_engine("postgresql://postgres:edemdb1234@database-1.chaf71z5ycev.eu-north-1.rds.amazonaws.com:5432/")
    with engine.connect() as connection:
        cursor = connection.execute(text("select * from scrapped"))
        data = cursor.fetchall() 
        connection.close()
    result = {}
    labels = ['name', 'phase', 'topics', 'description', 'url', 'logo_link']
    for ind,row in enumerate(data):
        result[str(ind)] = {}
        for ind_2,value in enumerate(row[1:]):
            result[str(ind)][labels[ind_2]] = value
    return jsonify(result)

# ENDPOINT 5 - Get a list of events ids ordenated by preference given a requested student id
@app.route('/get_recommendation_events', methods=['GET'])
def get_recommendation_events():
    event_recommendation = EventRecommendation()
    requested_student_id = request.args.get('requested_student_id')

    interests_list = event_recommendation.get_interests_for_student(requested_student_id)
    
    return jsonify(interests_list)

# ENDPOINT 6 - Bad language filter (English & Spanish)
@app.route('/get_bad_language_filter', methods=['GET'])
def get_bad_language_filter():
    if "text" in request.args:
        if request.args["text"] == "":
            return "Please fill the text value"
        else:
            user_text = request.args["text"]
            text_filter = TextFilter().filter_text(user_text)
            return text_filter
    else:
        return "Error: 'text' parameter is missing or empty"
# ENDPOINT 7 - Recommend similar users
@app.route('/recommend_users', methods=['GET'])
def recommend_users():
    requested_student_id = request.args.get('requested_student_id')
    friends_list = RecommendUsers().group_users(requested_student_id=requested_student_id)
    return friends_list
    
if __name__ == '__main__':
    app.run(debug=True)

