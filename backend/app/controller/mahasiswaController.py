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

mahasiswaBp = Blueprint('pengajuan', __name__)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mahasiswaBp.route('/submit/<nrp>', methods=['POST'])
def submitPengajuan(nrp):
    # if 'file' not in request.files:
    #     return jsonify({'message': 'No file part'}), 400

    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({'message': 'No selected file'}), 400

    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     filepath = os.path.join(UPLOAD_FOLDER, filename)
    #     file.save(filepath)

        sessionDb = SessionLocal()
        
        # nrp = session.get('userId')
        # if not nrp:
        #     return jsonify({'message': 'User not logged in'}), 401
        data = request.get_json()
        newPengajuan = PengajuanBeasiswa(
            nrp=nrp,
            beasiswa_id=data.get('beasiswaId'),
            periode_id=data.get('periodeId'),
            tanggal_pengajuan=datetime.today().strftime('%Y-%m-%d'),
            status_pengajuan='diajukan',
            status_pengajuan_fakultas='Diajukan',
            dokumen_pengajuan="filepath"
        )

        sessionDb.add(newPengajuan)
        sessionDb.commit()
        sessionDb.close()

        return jsonify({'message': 'Pengajuan submitted successfully'}), 201

@mahasiswaBp.route('/showBeasiswa/<int:nrp>', methods=['GET'])
def get_beasiswa_by_nrp(nrp):
    sessionDb = SessionLocal()
    pengajuan_list = sessionDb.query(PengajuanBeasiswa).filter(PengajuanBeasiswa.nrp == nrp).all()
    sessionDb.close()
    
    result = [{
        'pengajuan_id': p.pengajuan_id,
        'nrp': p.nrp,
        'beasiswa_id': p.beasiswa_id,
        'periode_id': p.periode_id,
        'tanggal_pengajuan': p.tanggal_pengajuan,
        'status_pengajuan': p.status_pengajuan,
        'status_pengajuan_fakultas': p.status_pengajuan_fakultas,
        'dokumen_pengajuan': p.dokumen_pengajuan
    } for p in pengajuan_list]

    return jsonify({'pengajuan': result})


@mahasiswaBp.route('/deletePengajuan/<pengajuanId>', methods=['DELETE'])
def deletePengajuan(pengajuanId):
    session = SessionLocal()

    pengajuan = session.query(PengajuanBeasiswa).filter(PengajuanBeasiswa.pengajuan_id == pengajuanId).first()
    if not pengajuan:
        return jsonify({'message': 'Pengajuan not found'}), 404
    session.delete(pengajuan)
    session.commit()
    session.close()
    return jsonify({'message': 'Pengajuan deleted successfully'})