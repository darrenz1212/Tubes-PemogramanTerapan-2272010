from flask import Blueprint, request, jsonify
from app.Model import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL
import hashlib

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

registerBp = Blueprint('register', __name__)

@registerBp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    session_db = SessionLocal()
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(
        username = data.get('username'),
        password = hashed_password,
        role = data.get('role'),
        program_studi_id = data.get('program_studi_id'),
        fakultas_id = data.get('fakultas_id')
    )

    session_db.add(new_user)
    session_db.commit()
    session_db.close()
    return jsonify({'message': 'User registered successfully'})
