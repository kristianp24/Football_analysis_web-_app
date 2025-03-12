from database import create_or_check_database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import dotenv
from routes import register_blueprints
dotenv.load_dotenv(dotenv_path='backend/app/.env')


app = Flask(__name__)
register_blueprints(app)
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')

# Configure database (update this with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    engine = create_or_check_database(app, migrate)


if __name__ == '__main__':
    app.run()
