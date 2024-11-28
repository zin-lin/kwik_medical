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
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'  # allows CORS
app.config['SECRETE_KEY'] = 'kwik-pat-service-llbt-34whatis67'  # set up Database with SQLAlchemy
app.secret_key = 'kwik-pat-service-llbt-34whatis67'
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

patients = [
    {'nhs': 1232323201, 'dob': "12/12/2012", 'name': "Micheal Andrick", 'age': 41, 'gender': "M",
     'medical': "Arthritis", 'allergies': "celery", 'address': "171 Okay Road, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID124350A", 'injury': "Fractured arm", 'action_taken': "Applied ice pack", 'timestamp': "2023-10-15 14:23:45"},

    {'nhs': 2345678902, 'dob': "05/11/1980", 'name': "Sarah Thompson", 'age': 43, 'gender': "F",
     'medical': "Hypertension", 'allergies': "penicillin", 'address': "22 King Street, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID657980B", 'injury': "Head injury", 'action_taken': "Bandaged", 'timestamp': "2023-10-10 10:45:32"},

    {'nhs': 3456789003, 'dob': "09/03/1991", 'name': "John Doe", 'age': 32, 'gender': "M",
     'medical': "Diabetes", 'allergies': "none", 'address': "15 Queen Street, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID907123C", 'injury': "Back pain", 'action_taken': "Administered pain relief", 'timestamp': "2023-10-08 16:23:11"},

    {'nhs': 4567890104, 'dob': "15/07/1985", 'name': "Emily Clark", 'age': 38, 'gender': "F",
     'medical': "Asthma", 'allergies': "dust", 'address': "78 Elm Avenue, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID543212D", 'injury': "Sprained ankle", 'action_taken': "Gave crutches", 'timestamp': "2023-10-12 09:12:09"},

    {'nhs': 5678901205, 'dob': "22/02/1979", 'name': "Michael Brown", 'age': 45, 'gender': "M",
     'medical': "High Cholesterol", 'allergies': "peanuts", 'address': "5 Oak Drive, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID324910E", 'injury': "Laceration", 'action_taken': "Applied stitches", 'timestamp': "2023-10-14 18:30:22"},

    {'nhs': 6789012306, 'dob': "11/12/1992", 'name': "Jessica Adams", 'age': 30, 'gender': "F",
     'medical': "Eczema", 'allergies': "pollen", 'address': "12 Maple Lane, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID982341F", 'injury': "Bruised ribs", 'action_taken': "Monitored vital signs", 'timestamp': "2023-10-13 12:45:18"},

    {'nhs': 7890123407, 'dob': "25/04/1967", 'name': "Paul White", 'age': 56, 'gender': "M",
     'medical': "Osteoporosis", 'allergies': "shellfish", 'address': "32 Pine Road, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID891234G", 'injury': "Chest pain", 'action_taken': "Referred to X-ray", 'timestamp': "2023-10-09 20:12:34"},

    {'nhs': 8901234508, 'dob': "03/10/1976", 'name': "Rachel Green", 'age': 47, 'gender': "F",
     'medical': "Arthritis", 'allergies': "latex", 'address': "66 Cedar Avenue, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID745012H", 'injury': "Concussion", 'action_taken': "Wound cleaned", 'timestamp': "2023-10-17 11:21:54"},

    {'nhs': 2345678911, 'dob': "07/05/1955", 'name': "Tom Baker", 'age': 68, 'gender': "M",
     'medical': "Parkinson's Disease", 'allergies': "none", 'address': "98 Elmwood Road, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID768091I", 'injury': "Leg cramp", 'action_taken': "Massaged", 'timestamp': "2023-10-05 14:01:00"},

    {'nhs': 3456789012, 'dob': "12/01/1960", 'name': "Anna Murphy", 'age': 63, 'gender': "F",
     'medical': "Hypertension", 'allergies': "shellfish", 'address': "34 Hawthorn Avenue, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID458912J", 'injury': "Swollen knee", 'action_taken': "Applied ice pack", 'timestamp': "2023-10-11 08:33:25"},

    {'nhs': 4567890123, 'dob': "20/10/1982", 'name': "James Wilson", 'age': 41, 'gender': "M",
     'medical': "Asthma", 'allergies': "mold", 'address': "71 Fir Street, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID328914K", 'injury': "Ankle sprain", 'action_taken': "Gave crutches", 'timestamp': "2023-10-12 19:14:47"},

    {'nhs': 5678901234, 'dob': "15/09/1995", 'name': "Lucy Harris", 'age': 28, 'gender': "F",
     'medical': "Diabetes", 'allergies': "wheat", 'address': "29 Hazel Grove, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID112903L", 'injury': "Fractured wrist", 'action_taken': "Applied splint", 'timestamp': "2023-10-08 16:22:38"},

    {'nhs': 6789012345, 'dob': "28/12/1970", 'name': "Robert Johnson", 'age': 53, 'gender': "M",
     'medical': "Chronic Fatigue", 'allergies': "soy", 'address': "103 Alder Drive, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID672814M", 'injury': "Neck pain", 'action_taken': "Gave neck brace", 'timestamp': "2023-10-14 10:45:01"},

    {'nhs': 7890123456, 'dob': "14/03/1988", 'name': "Clara Lewis", 'age': 35, 'gender': "F",
     'medical': "None", 'allergies': "none", 'address': "45 Holly Road, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID315489N", 'injury': "Shoulder strain", 'action_taken': "Administered pain relief", 'timestamp': "2023-10-16 18:22:59"},

    {'nhs': 8901234567, 'dob': "08/07/1979", 'name': "Simon Hughes", 'age': 44, 'gender': "M",
     'medical': "Asthma", 'allergies': "penicillin", 'address': "99 Ivy Street, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID498120O", 'injury': "Burn on hand", 'action_taken': "Applied burn cream", 'timestamp': "2023-10-17 14:37:45"},

    {'nhs': 9012345678, 'dob': "13/11/1963", 'name': "Barbara Miller", 'age': 60, 'gender': "F",
     'medical': "Hypertension", 'allergies': "egg", 'address': "24 Spruce Lane, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID546123P", 'injury': "Bruised knee", 'action_taken': "Applied ice pack", 'timestamp': "2023-10-06 08:19:30"},

    {'nhs': 8834567890, 'dob': "29/02/1992", 'name': "Jack Robinson", 'age': 31, 'gender': "M",
     'medical': "Anxiety", 'allergies': "cats", 'address': "76 Poplar Road, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID921307Q", 'injury': "Sprained finger", 'action_taken': "Taped finger", 'timestamp': "2023-10-13 17:14:08"},

    {'nhs': 2345618901, 'dob': "17/08/1999", 'name': "Olivia Evans", 'age': 24, 'gender': "F",
     'medical': "None", 'allergies': "dairy", 'address': "38 Walnut Street, Edinburgh", 'hospital_code': "WGEDB",
     'id': "ID673218R", 'injury': "Bruised elbow", 'action_taken': "Monitored vital signs", 'timestamp': "2023-10-09 15:08:12"},

    {'nhs': 3456783012, 'dob': "21/06/1978", 'name': "Henry King", 'age': 45, 'gender': "M",
     'medical': "Arthritis", 'allergies': "none", 'address': "83 Ash Grove, Edinburgh", 'hospital_code': "RIEDB",
     'id': "ID891034S", 'injury': "Twisted ankle", 'action_taken': "Applied compression", 'timestamp': "2023-10-07 20:11:47"},

    {'nhs': 4567892123, 'dob': "04/04/1984", 'name': "Sophia Turner", 'age': 39, 'gender': "F",
     'medical': "Diabetes", 'allergies': "peanuts", 'address': "52 Redwood Court, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID215380T", 'injury': "Neck strain", 'action_taken': "Gave neck brace", 'timestamp': "2023-10-10 22:16:25"},

    {'nhs': 4567112183, 'dob': "12/12/2012", 'name': "Michelle S. Aubery", 'age': 12, 'gender': "F",
     'medical': "Diabetes", 'allergies': "peanuts", 'address': "52 Redwood Court, Edinburgh", 'hospital_code': "ECHEDB",
     'id': "ID873291U", 'injury': "Broken finger", 'action_taken': "Splint applied", 'timestamp': "2023-10-18 12:45:33"}
]


# Create database
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    return "Hey there"

@app.route('/add_to_database')
def add_to_database():
    for p in patients:
        db.session.add(Patient(nhs = p['nhs'], dob = p['dob'], name = p['name'], age = p['age'], gender = p['gender'], medical = p['medical'],
                               allergies = p['allergies'], hospital_code = p['hospital_code'], address = p['address'], injury = p['injury'],
                               action_taken = p['action_taken'], timestamp = p['timestamp']
                               ))
        db.session.commit()  # Finalize the transaction by committing it

    return "Done"

# Update Patient if not exist create
@app.route('/update/<pid>', methods = ['GET', 'POST'])
@cross_origin()
def update_patient(pid):

    nhs = request.form.get('nhs')
    dob = request.form.get('dob')
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    medical = request.form.get('medical')
    allergies = request.form.get('allergies')
    hospital_code = request.form.get('hospital_code')
    address = request.form.get('address')
    action_taken =request.form.get('action_taken')
    injury = request.form.get('injury')
    action_taken = request.form.get('action_taken')
    timestamp = datetime.datetime.utcnow()

    try:
        patient = Patient.query.get(pid)
        if patient is None:
            db.session.add(Patient(nhs=nhs, dob=dob, name=name, age=age, gender=gender,
                                   medical=medical,
                                   allergies=allergies, hospital_code= hospital_code, address= address,
                                   injury= injury,
                                   action_taken= action_taken, timestamp= timestamp
                                   ))
            db.session.commit()
            return "Added"

        else:
            patient.dob = dob
            patient.name = name
            patient.age = age
            patient.gender = gender
            patient.medical = medical
            patient.allergies = allergies
            patient.hospital_code = hospital_code
            patient.address = address
            patient.injury = injury
            patient.action_taken = action_taken
            patient.timestamp = timestamp

            db.session.commit()
            return "Successful Update"

    except:
        return jsonify({'msg': 'error'})

@app.route('/getAdd/<pid>', methods = ['GET', 'POST'])
@cross_origin()
def get_patient_or_add(pid):
    nhs = request.form.get('nhs')
    dob = request.form.get('dob')
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    medical = request.form.get('medical')
    allergies = request.form.get('allergies')
    hospital_code = request.form.get('hospital_code')
    address = request.form.get('address')
    injury = request.form.get('injury')
    timestamp = request.form.get('timestamp')
    action_taken =request.form.get('action_taken')

    try:
        patient = Patient.query.get(pid)
        if patient is None:
            db.session.add(Patient(nhs=nhs, dob=dob, name=name, age=age, gender=gender,
                                   medical=medical,
                                   allergies=allergies, hospital_code= hospital_code, address= address,
                                   injury= injury,
                                   action_taken= action_taken, timestamp= timestamp
                                   ))
            db.session.commit()
            return "Added"

        patient = Patient.query.get(pid)
        return jsonify({'patient': patient})

    except:
        return jsonify({'msg': 'error'})

@app.route('/get/<pid>')
@cross_origin()
def get_patient(pid):
    patient = db.session.get(Patient,pid)
    if patient is None:
        return jsonify({'msg': 'error'})

    print(patient.name)
    return jsonify({'nhs': patient.nhs, 'dob':patient.dob, 'name': patient.name,
                    'age':patient.age, 'gender':patient.gender, 'medical':patient.medical,
                    'allergies':patient.allergies, 'hospital_code': patient.hospital_code, 'address': patient.address,
                    'injury':patient.injury, 'timestamp':patient.timestamp, 'action_taken':patient.action_taken
                    })


@app.route('/updateFromKwik/<pid>/<code>', methods = ['GET', 'POST'])
@cross_origin()
def updateFromKwik(pid, code):
    patient = db.session.get(Patient, pid)
    if patient:
        patient.hospital_code = code
        db.session.commit()
        return jsonify({'msg': 'success'})
    return jsonify({'msg': 'error'})

@app.route('/addFromKwik/<pid>', methods=['GET', 'POST'])
@cross_origin()
def add_from_kwik(pid):
    dob = request.form.get('dob')
    name = request.form.get('name')
    address = request.form.get('address')
    injury = request.form.get('injury')
    timestamp = datetime.datetime.utcnow()

    patient = db.session.get(Patient,pid)
    if patient is None:
        db.session.add(Patient(nhs=pid, dob=dob, name=name, age="age", gender="N/A",
                               medical="N/A",
                               allergies="N/A", hospital_code="N/A", address=address,
                               injury=injury,
                               action_taken="N/A", timestamp=timestamp
                               ))
        db.session.commit()
        return "Added"

    else:
        patient.name = name
        patient.dob = dob
        patient.address = address
        patient.injury = injury
        patient.timestamp = timestamp
        db.session.commit()
        return "Updated"

@app.route('/getAll/<hid>')
@cross_origin()
def get_patients_hospital(hid):
    try:
        patients = Patient.query.filter(Patient.hospital_code == hid).all()
        print(len(patients))
        if len(patients) == 0:
            return jsonify([])
        return jsonify([p.to_dict() for p in patients ])
    except Exception as e:
        return jsonify({'msg': e})



if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
