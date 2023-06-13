from flask import Flask, jsonify, request
from data.db import Database
from config import error_handling
from functions.bad_language import TextFilter
from functions.events_recommendation_class import EventRecommendation
import json

app = Flask(__name__)

# Página informativa de los endpoints:
@app.route('/', methods=['GET'])
def home():
    message = f"""
    Welcome! To extract data, please see the following instructions:

    <br><br>endpoint: '/get_db_events' 
    <br><br>endpoint: '/get_db_categories' 
    <br><br>endpoint: '/get_db_students' 
    <br><br>endpoint: '/get_scrap_startups'
    <br><br>endpoint: '/get_bad_language_filter' --> Params: "text"
    
    """
    return message

# Endpoints de recursos [GET]:

@app.route('/get_db_categories', methods=['GET'])
def get_db_categories():
    db = Database()
    result = db.get_categories()
    db.close()
    return jsonify(result)


@app.route('/get_db_events', methods=['GET'])
def get_db_events():
    db = Database()
    result = db.get_events()
    db.close()
    return jsonify(result)


@app.route('/get_db_students', methods=['GET'])
def get_db_students():
    db = Database()
    result = db.get_students()
    db.close()
    return jsonify(result)

@app.route('/get_scrap_startups', methods=['GET'])
def get_scrap_startups():
    with open("Scrap\startups_data.json", "r", encoding= "utf-8") as file:
        result = json.load(file)  
    return result

@app.route('/get_recommendation_events', methods=['GET'])
def get_recommendation_events():
    student_dict = EventRecommendation().get_sorted_events_dict()
    return jsonify(student_dict)


if __name__ == '__main__':
    app.run(debug=True)

