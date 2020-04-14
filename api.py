from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
jwt_manager: JWTManager = JWTManager()
