from flask import Flask, jsonify
from data import db, Database
from Scrap import startups_scrap
from config import error_handling

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    message = f"""
    Welcome! To extract data, please see the following instructions:

    <br><br>endpoint: '/get_db_events' 
    <br><br>endpoint: '/get_db_categories' 
    <br><br>endpoint: '/get_db_students' 
    <br><br>endpoint: '/get_scrap_startups'
    
    """
    return message

db = Database()

@app.route('/get_db_categories', methods=['GET'])
def get_db_categories():
    result = db.get_categories()
    db.close()
    return jsonify(result)


@app.route('/get_db_events', methods=['GET'])
def get_db_events():
    result = db.get_events()
    db.close()
    return jsonify(result)


@app.route('/get_db_students', methods=['GET'])
def get_db_students():
    result = db.get_students()
    db.close()
    return jsonify(result)

@app.route('/get_scrap_startups', methods=['GET'])
def get_scrap_startups():
    with open("Scrap\startups_data.json", "r", encoding= "utf-8") as file:
        result = json.load(file)  
    return result


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)

