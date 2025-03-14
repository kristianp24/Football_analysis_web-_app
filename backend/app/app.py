from database import create_or_check_database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
import dotenv
from routes import register_blueprints
from routes.credentials import USER, PASSWORD, HOST, DATABASE, PORT, JWT_SECRET_KEY
from flask_jwt_extended import JWTManager
dotenv.load_dotenv(dotenv_path='backend/app/.env')


app = Flask(__name__)
CORS(app)
register_blueprints(app)

# Configure database (update this with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY 
jwt = JWTManager(app)
app.config['JWT'] = jwt 


db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    engine = create_or_check_database(app, migrate)


if __name__ == '__main__':
    app.run()
