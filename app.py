import datetime

import flask_jwt
from flask_jwt import JWT
from auth import authenticate, identity
from flask_restful import Api
from flask import Flask
from resources.routes import initialize_routes

# Configure Flask app
app = Flask(__name__)
app.debug = True

# Configure RESTful API
api = Api(app)
initialize_routes(api)

# Configure JWT auth
key_file = open("keys/secret.txt", "rb")
key = key_file.read(64)
key_file.close()
app.config['JWT_SECRET_KEY'] = key
# Next line enables sending token as 'Authorization' : 'Bearer _____'  instead of  'JWT _____'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
jwt = JWT(app, authenticate, identity)
app.config['PROPAGATE_EXCEPTIONS'] = True


if __name__ == '__main__':
    app.run()
