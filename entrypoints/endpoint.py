from data import db, Database


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
    return db.get_categories()


@app.route('/get_db_events', methods=['GET'])
def get_db_events():
    return db.get_events()


@app.route('/get_db_students', methods=['GET'])
def get_db_students():
    return db.get_students()

db.close()