from flask import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS, cross_origin
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask_socketio import SocketIO, emit
import queue
from flask_bcrypt import *

from models import *

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['CORS_HEADERS'] = 'Content-Type' # allows CORS
app.config['SECRETE_KEY'] = 'kwik-amb-service-llbt34whatis67' # set up Database with SQLAlchemy
app.secret_key = 'kwik-amb-ervice-llbt34whatis67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'

# Make sessions permanent
app.config['SESSION_PERMANENT'] = True
# configuration
cors = CORS(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

#inits
bcrypt = Bcrypt(app)
db.init_app(app)


# Set up Firebase and Cloud Firestore
cred = credentials.Certificate("./keys/kwik.json")
firebase_admin.initialize_app(cred)
# Firestore
fdb = firestore.client()


# Create database
with app.app_context():
    db.create_all()
    db.session.commit()


ambulances = [
    {'id': "ED12 ABC", 'lat': "55.950000", 'lon': "-3.200000", 'password': "ambulance123"},  # Edinburgh
    {'id': "GL34 DEF", 'lat': "55.864200", 'lon': "-4.251800", 'password': "ambulance123"},  # Glasgow
    {'id': "FA56 GHI", 'lat': "56.000000", 'lon': "-3.776000", 'password': "ambulance123"},  # Falkirk
    {'id': "ED78 JKL", 'lat': "55.947000", 'lon': "-3.215000", 'password': "ambulance123"},  # Edinburgh
    {'id': "GL90 MNO", 'lat': "55.870000", 'lon': "-4.299000", 'password': "ambulance123"},  # Glasgow
    {'id': "FA12 PQR", 'lat': "55.996000", 'lon': "-3.776500", 'password': "ambulance123"},  # Falkirk
    {'id': "ED34 STU", 'lat': "55.948000", 'lon': "-3.210000", 'password': "ambulance123"},  # Edinburgh
    {'id': "GL56 VWX", 'lat': "55.857300", 'lon': "-4.239600", 'password': "ambulance123"},  # Glasgow
    {'id': "FA78 YZA", 'lat': "56.002500", 'lon': "-3.769500", 'password': "ambulance123"},  # Falkirk
    {'id': "ED90 BCD", 'lat': "55.955000", 'lon': "-3.190000", 'password': "ambulance123"},  # Edinburgh
]

@app.route('/')
def home():
    return app.send_static_file('index.html')

# @app.route('/add_to_database')
# def add_to_database():
#     for ambulance in ambulances:
#         db.session.add(Ambulance(id= ambulance['id'], lat= ambulance['lat'], lon= ambulance['lon'], password= ambulance['password']))
#         db.session.commit()
#     return ""

def app_check():
    id = request.form.get('app_id')
    if id != "ambulance_service-234234234sadnnbqweh2u3":
        return jsonify({'message': "Cannot authenticate application"})


@app.route('/api/authed', methods=['POST', 'GET'])
@cross_origin()
def authed():
    app_check()
    if session.get('user_id') is not None:
        return jsonify({'id': session.get('user_id'), 'message': 'You are now logged in'})
    return jsonify({'id': ''})


# login, check if user id exist in database
@app.route("/api/login", methods=["GET", "POST"])
@cross_origin()
def login():
    plate = request.form.get('plate')
    password = request.form.get('password')

    user_exists=None
    try:
        user_exists = Ambulance.query.filter_by(id=plate).first()

    except:
        print("table hasn't been created, creating table")

    if user_exists is None:
        return jsonify({"error":"unauthed"}), 401 # invalid credential

    if password != user_exists.password:
        return jsonify({"error":"wrong credentials"}), 401 # invalid credential

    session['user_id'] = user_exists.id
    return "Successful Login"

@app.route('/api/getAll/', methods=['GET'])
@cross_origin()
def get_cases():
    try:
        collection = fdb.collection('cases')
        cases =collection.order_by('time', direction=firestore.Query.DESCENDING).stream()
        cases_list = []
        for doc in cases:
            doc_data = doc.to_dict()
            doc_data['time'] = str(doc_data['time'])
            doc_data['id'] = str(doc.id)
            cases_list.append(doc_data)

        return jsonify(cases_list), 200
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/get/<cid>', methods=['GET'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def get_case(cid):
    cases = fdb.collection('cases')
    doc = cases.document(cid)

    return jsonify(doc.get().to_dict())


@app.route('/api/update/<cid>/', methods=['GET'])
@cross_origin()
def update_case(cid):
    app_check()
    aid = session.get('user_id')
    cases = fdb.collection('cases')
    doc = cases.document(cid)
    doc.update({'a_num':aid, 'status': 2})
    return jsonify({'message':'Successful update'}), 200

@app.route('/api/updateStatus/<cid>/', methods=['GET'])
@cross_origin()
def update_case_status(cid):
    app_check()
    aid = session.get('user_id')
    if aid:
        cases = fdb.collection('cases')
        doc = cases.document(cid)
        doc.update({'status': 3})
        return jsonify({'message':'Successful update'}), 200
    else:
        return


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8001)
