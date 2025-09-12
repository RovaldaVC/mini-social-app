from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from .routes import setDatabase
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
    
def The_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object("config.Config")
    app.config["JWT_SECRET_KEY"] = app.config["JWT_CODE"]
    JWTManager(app)
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client["social-app"]
    setDatabase(app)
    return app