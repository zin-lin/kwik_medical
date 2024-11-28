# Author: Zin Lin Htun
import sys
import eventlet
from flask import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS, cross_origin
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask_socketio import SocketIO, emit
import queue

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['JWT_SECRET_KEY'] = 'hh2sd3ifj3isj56bhb3we4usd384u8wey8$56%$%'  # Change this to a random secret key
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up CORS

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# allows CORS


# Set up Firebase and Cloud Firestore
cred = credentials.Certificate("./keys/kwik.json")
firebase_admin.initialize_app(cred)
# Firestore
db = firestore.client()
cases_cache = {}

# queues set up
cases_queue = queue.Queue()


document_queues = {}
# # Global cache for document tracking
cases_cache = {}
listeners = {}


def start_document_listener(doc_id):
    def on_snapshot(doc_snapshot, changes, read_time):
        global cases_cache
        for doc in doc_snapshot:
            doc_data = doc.to_dict()
            doc_data['time'] = str(doc_data['time'])
            cases_cache[doc_id] = doc_data
            print(f"Document {doc_id} updated, pushing to WebSocket...")
            # Emit update via WebSocket to clients
            socketio.emit('document_update', {"doc": doc_data},)

    # Attach Firestore listener to the document
    doc_ref = db.collection('cases').document(doc_id)
    doc_ref.on_snapshot(on_snapshot)


def start_documents_listener():
    def on_snapshot(doc_snapshot, changes, read_time):
        cases_dic = {}
        for doc in doc_snapshot:
            doc_data = doc.to_dict()
            doc_data['time'] = str(doc_data['time'])

            print(f"Document {doc_data} updated, pushing to WebSocket...")
            cases_dic[doc.id] = doc_data
            # Emit update via WebSocket to clients

        socketio.emit('document_update', cases_dic)

    docs_ref = db.collection('cases')
    docs_ref.on_snapshot(on_snapshot)

# WebSocket event when client connects
@socketio.on('connect')
def handle_connect():
    print("Client connected")


# WebSocket event to track a document (Client sends doc_id to track)
@socketio.on('track_document')
def handle_track_document(data):
    doc_id = data.get('doc_id')
    if doc_id:
        if doc_id not in listeners:
            listeners[doc_id] = doc_id
            start_document_listener(doc_id)
        emit('track_started', {'msg': f"Started tracking document {doc_id}"})
    else:
        emit('error', {'msg': "No document ID provided"})


@socketio.on('track_documents')
def handle_track_document():
    start_documents_listener()


@app.route('/') 
def home():
    return app.send_static_file('index.html')


@app.route('/login', methods=['POST'])
def login():
    app_id = request.json.get('app_id')
    if app_id == "kwik_fe_101":
        access_token = create_access_token(identity="app_id")
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid app_id"})


@app.route('/api/test', methods=['GET'])
@jwt_required()
def get_data():
    return "Hello world @sensitive"


@app.route('/api/add-case/', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def add():
    print(request.method)

    name = request.form.get('pname')
    dob = request.form.get('dob')
    address = request.form.get('address')
    postcode = request.form.get('postcode')
    des = request.form.get('des')
    nature = request.form.get('nature')
    cases = db.collection('cases')
    nhs = request.form.get('nhs')

    try:
        ref = cases.document()
        ref.set({'pname': name, 'a_num': 'N/A', 'address': address, 'postcode': postcode, 'des': des, 'type': nature,
                'dob': dob, 'time': datetime.datetime.utcnow(), 'hospital': 'N/A', 'status': 0, 'nhs':nhs})
        return jsonify({"msgs": "Successfully Added", "id": ref.id})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/get/<cid>', methods=['GET'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def get_case(cid):
    cases = db.collection('cases')
    doc = cases.document(cid)

    return jsonify(doc.get().to_dict())


@app.route('/api/getAll/', methods=['GET'])
@cross_origin()
def get_cases():
    try:
        collection = db.collection('cases')
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


if __name__ == '__main__':
    socketio.run(app, port=8000, host='0.0.0.0' )
