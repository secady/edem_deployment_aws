import pandas as pd
from flask import Flask, request, jsonify, send_file
import json

app = Flask(__name__)


# ENDPOINT 5 - Get Lanzadera/startups' data (scrap)
@app.route('/get_scrap_startups', methods=['GET'])
def get_scrap_startups():
    with open("Scrap/startups_data.json", "r") as file:
        result = json.load(file)  
    return result



if __name__ == '__main__':
    app.run(debug=True)