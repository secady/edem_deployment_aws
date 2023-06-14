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
    model = load('pipeline.pkl') 
    url_users = "https://edem-students-backend.vercel.app/users/dataGetAll"
    headers = {"Authorization": "desafio2023"}
    payload = ""
    response = requests.get(url_users,headers=headers, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_users = response.json()  # Assuming the response contains JSON data
        # Convert the data to a DataFrame
        users_df = pd.DataFrame(data_users)
    else:
        return 'Error: Failed to fetch users data from the webpage'
    
    category_id_list = []
    category_name_list = []

    # Iterate over each event row
    for user in users_df["categoryIds"]:
        category_ids = []
        category_names = []

        # Iterate over each category in the event
        for category in user:
            category_ids.append(category["_id"])
            category_names.append(category["name"])

        # Append the category details to the lists
        category_id_list.append(category_ids)
        category_name_list.append(category_names)

    # Assign the category details to the DataFrame
    users_df["category_id"] = category_id_list
    users_df["category_name"] = category_name_list

    #programs ----------------------------------------------------------
    url_programs = "https://edem-students-backend.vercel.app/programs/dataGetAll"
    headers = {"Authorization": "desafio2023"}
    payload = ""

    response = requests.get(url_programs,headers=headers, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_programs = response.json()  # Assuming the response contains JSON data
        
        # Convert the data to a DataFrame
        programs_df = pd.DataFrame(data_programs)
    else:
        return 'Error: Failed to fetch programs data from the webpage'

    # Create a dictionary mapping program IDs to program names
    program_dict = dict(zip(programs_df["_id"], programs_df["name"]))

    # Use the map function to create the new column "program_name"
    users_df["program_name"] = users_df["program"].map(program_dict)
    #---------------------------------------------------------------------
    users_id = users_df['_id']
    users_df.drop(['role','chatIds','roleMde','program','connections','eventIds','confirmed','createdAt','updatedAt','__v','image','bio','category_id'],axis=1,inplace=True)
    users_df.rename(columns={'_id': 'student_id','categoryIds': 'category_id','category_name':'category','program_name':'programme'},inplace=True, errors='raise')

    # Define the mapping of values to labels
    mapping = {'1': '1st year', '2': '2nd year', '3': '3rd year', '4': '4th year'}

    # Replace values in the 'year_of_study' column
    users_df['year'] = users_df['year'].replace(mapping)
    users_df = users_df.dropna()
    users_df = model.transform(users_df)
    df_final = pd.DataFrame(users_df,columns=['cluster'])
    df_final['_id'] = users_id
    # Convert DataFrame to JSON
    json_data = df_final.to_json(orient='records')
    # Return JSON response
    return json_data
    
if __name__ == '__main__':
    app.run(debug=True)

