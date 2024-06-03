import os
from datetime import datetime
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from app.Model import PengajuanBeasiswa, Mahasiswa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL

UPLOAD_FOLDER = 'dokumenPengajuan'
ALLOWED_EXTENSIONS = {'pdf','jpeg'}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pengajuanBp = Blueprint('pengajuan', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pengajuanBp.route('/submit', methods=['POST'])
def submitPengajuan():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        sessionDb = SessionLocal()
        
        nrp = session.get('userId')
        if not nrp:
            return jsonify({'message': 'User not logged in'}), 401

        newPengajuan = PengajuanBeasiswa(
            nrp=nrp,
            beasiswaId=request.form.get('beasiswaId'),
            periodeId=request.form.get('periodeId'),
            tanggalPengajuan=datetime.today().strftime('%Y-%m-%d'),
            statusPengajuan='diajukan',
            statusPengajuanFakultas='Diajukan',
            dokumenPengajuan=filepath
        )

        sessionDb.add(newPengajuan)
        sessionDb.commit()
        sessionDb.close()

        return jsonify({'message': 'Pengajuan submitted successfully'}), 201
    else:
        return jsonify({'message': 'File type not allowed'}), 400
