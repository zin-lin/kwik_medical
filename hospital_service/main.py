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
import helpers

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['CORS_HEADERS'] = 'Content-Type' # allows CORS
app.config['SECRETE_KEY'] = 'kwik-hoservice-llbt34whatis67' # set up Database with SQLAlchemy
app.secret_key = 'kwik-hoservice-llbt34whatis67'
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

hospitals = [
    {
        'id': "WGEDB",
        'lat': "55.9574",
        'lon': "-3.2289",
        'name': "Western General Hospital",
        'password': "WGHpassword"
    },
    {
        'id': "RIEDB",
        'lat': "55.9204",
        'lon': "-3.1281",
        'name': "Royal Infirmary Edinburgh",
        'password': "RIEpassword"
    },
    {
        'id': "ECHEDB",
        'lat': "55.9435",
        'lon': "-3.1864",
        'name': "Edinburgh Children's Hospital",
        'password': "ECHpassword"
    },
    {
        'id': "SMHEDB",
        'lat': "55.9500",
        'lon': "-3.2028",
        'name': "Spire Murrayfield Hospital",
        'password': "SMHpassword"
    },
    {
        'id': "SCHEDB",
        'lat': "55.9365",
        'lon': "-3.2393",
        'name': "St Columba's Hospice",
        'password': "SCHpassword"
    },
    {
        'id': "AAHEDB",
        'lat': "55.9750",
        'lon': "-3.1725",
        'name': "Astley Ainslie Hospital",
        'password': "AAHpassword"
    },
    {
        'id': "RHSCEDB",
        'lat': "55.9457",
        'lon': "-3.1112",
        'name': "Royal Hospital for Sick Children",
        'password': "RHSCpassword"
    },
    {
        'id': "QMDUNF",
        'lat': "56.1140",
        'lon': "-3.9428",
        'name': "Queen Margaret Hospital, Dunfermline",
        'password': "QMHpassword"
    },
    {
        'id': "VHKIRK",
        'lat': "56.0702",
        'lon': "-3.1745",
        'name': "Victoria Hospital, Kirkcaldy",
        'password': "VHKpassword"
    },
    {
        'id': "FVRHSTIR",
        'lat': "56.1560",
        'lon': "-3.7516",
        'name': "Forth Valley Royal Hospital",
        'password': "FVRHpassword"
    }
]



@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/add_to_database')
def add_to_database():
    try:
        for h in hospitals:
            db.session.add(Hospital(id = h['id'], lat = h['lat'], lon = h['lon'], name = h['name'], password = h['password']))
            db.session.commit()
        return "Done"
    except:
        return "Error"


@app.route('/api/authed', methods = ['GET', 'POST'])
@cross_origin()
def authed():
    if session.get('hos_id') is not None:
        return jsonify({'id': session.get('hos_id'), 'message': 'You are now logged in'})
    return jsonify({'id': ''})



# logging in as a hospital
@app.route('/api/hlogin', methods=['GET', 'POST'])
@cross_origin()
def login():
    hospital_code = request.form.get('hospital')
    password = request.form.get('password')

    hospital = db.session.get(Hospital,hospital_code)
    if hospital:
        if hospital.password == password:
            session['hos_id'] = hospital.id
            return jsonify({'msg':'logged in', 'id': hospital.id})
        else:
            return jsonify({'msg':'wrong password'})
    return jsonify({'msg': 'no record'})


@app.route('/api/assign/<cid>', methods=['GET',])
@cross_origin()
def assign(cid):
    doc = fdb.collection('cases').document(cid).get()
    if doc:
        postcode = doc.to_dict()['postcode']
        try:
            from geopy.geocoders import Nominatim
            from geopy.extra.rate_limiter import RateLimiter

            # Instance of the Nominatim geocoder
            geolocator = Nominatim(user_agent="uk_postcode_locator")

            # Use RateLimiter to handle limits
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            # wee geo-location function
            def postcode_latlon(postcode):
                try:

                    location = geocode(postcode)
                    if location:
                        return location.latitude, location.longitude
                    else:
                        return None, None
                except Exception as e:
                    print(f"Error fetching coordinates for postcode '{postcode}': {e}")
                    return None, None

            # case lattitude and case longitude
            clat, clon = postcode_latlon(postcode)
            hospitals = Hospital.query.all()
            min = 90000
            min_code = ''
            for h in hospitals:
                dis = helpers.distance_between_latlon(eval(h.lat), eval(h.lon), clat, clon)
                if dis < min:
                    min = dis
                    min_code = h.id

            fdb.collection('cases').document(cid).update({'hospital':min_code, 'status':1})
            print(min_code)
            return jsonify({'msg':'success', 'code':min_code})
        except Exception as e:
            return jsonify({'msg': 'error', 'error': str(e)})

    else:
        return jsonify({'msg':'no case'})


@app.route('/test/<postcode>')
@cross_origin()
def tester(postcode):

    try:
        from geopy.geocoders import Nominatim
        from geopy.extra.rate_limiter import RateLimiter

        # Instance of the Nominatim geocoder
        geolocator = Nominatim(user_agent="uk_postcode_locator")

        # Use RateLimiter to handle limits
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        # wee geo-location function
        def postcode_latlon(postcode):
            try:

                location = geocode(postcode)
                if location:
                    return location.latitude, location.longitude
                else:
                    return None, None
            except Exception as e:
                print(f"Error fetching coordinates for postcode '{postcode}': {e}")
                return None, None

        # case lattitude and case longitude
        clat, clon = postcode_latlon(postcode)

        hospitals = Hospital.query.all()
        min = 90000

        min_code = ''
        for h in hospitals:
            dis = helpers.distance_between_latlon(eval(h.lat), eval(h.lon), clat, clon)
            print(dis)
            if dis < min:
                min = dis
                min_code = h.id


        return jsonify({'code': min_code})
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})


# main method
if __name__ == "__main__":
    app.run(debug=True, port=8888, host='0.0.0.0')
