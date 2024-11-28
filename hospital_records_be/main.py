# Author: Zin Lin Htun

from flask import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'hh2sd3ifj3isj56bhb3we4usd384u8wey8$56%$%'  # Change this to a random secret key
jwt = JWTManager(app)

app.config['SECRETE_KEY'] = 'annex-hos-ll22c4bt34whatis67' # set up Database with SQLAlchemy
app.secret_key = 'annex-hos-ll22c4bt34whatis67'

CORS(app, supports_credentials=True)  # Adjust according to your needs


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/login', methods=['POST'])
def login():
    app_id = request.json.get('app_id')
    if app_id == "kwik_fe_101":
        access_token = create_access_token(identity="user_id")
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid app_id"})


@app.route('/api/test', methods=['GET'])
@jwt_required()
def get_data():
    return "Hello world @sensitive"


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
