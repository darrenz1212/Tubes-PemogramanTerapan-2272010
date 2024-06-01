from flask import Blueprint, request, jsonify
from app.Model import Mahasiswa, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mahasiswaBp = Blueprint('mahasiswa', __name__)

@mahasiswaBp.route('/', methods=['GET'])
def getMahasiswa():
    session = SessionLocal()
    mahasiswa_list = session.query(Mahasiswa).all()
    result = [
        {
            'nrp': m.nrp,
            'user_id': m.user_id,
            'nama_mahasiswa': m.nama_mahasiswa,
            'prodi': m.program_studi_id,
            'ipk': m.ipk_terakhir,
            'status': m.status_aktif
        }
        for m in mahasiswa_list
    ]
    session.close()
    return {'mahasiswa': result}

@mahasiswaBp.route('/<nrp>', methods=['GET'])
def getMahasiswaById(nrp):
    session = SessionLocal()
    mahasiswa = session.query(Mahasiswa).filter(Mahasiswa.nrp == nrp).first()
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa not found'}), 404
    
    result = {
        'nrp': mahasiswa.nrp,
        'user_id': mahasiswa.user_id,
        'nama_mahasiswa': mahasiswa.nama_mahasiswa,
        'prodi': mahasiswa.program_studi_id,
        'ipk': mahasiswa.ipk_terakhir,
        'status': mahasiswa.status_aktif
    }
    
    session.close()
    return jsonify(result)

def getUserInfoById(userId):
    session = SessionLocal()
    user = session.query(User.username, User.program_studi_id).filter(User.user_id == userId).first()
    session.close()
    return user

@mahasiswaBp.route('/<userId>', methods=['POST'])
def addMahasiswa(userId):
    data = request.get_json()
    session = SessionLocal()

    user_info = getUserInfoById(userId)
    if not user_info:
        return jsonify({'message': 'User not found'}), 404

    new_mahasiswa = Mahasiswa(
        nrp=data.get('nrp'),
        user_id=userId,
        nama_mahasiswa=user_info.username,
        program_studi_id=user_info.program_studi_id,
        ipk_terakhir=data.get('ipk'),
        status_aktif=data.get('status')
    )

    session.add(new_mahasiswa)
    session.commit()

    nrp = new_mahasiswa.nrp
    nama_mahasiswa = new_mahasiswa.nama_mahasiswa

    session.close()

    return jsonify({
        'message': 'Mahasiswa added successfully',
        'nrp': nrp,
        'nama_mahasiswa': nama_mahasiswa,
        'program_studi_id': user_info.program_studi_id
    })

@mahasiswaBp.route('/<nrp>', methods=['PUT'])
def updateMahasiswa(nrp):
    data = request.get_json()
    session = SessionLocal()

    mahasiswa = session.query(Mahasiswa).filter(Mahasiswa.nrp == nrp).first()
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa not found'}), 404

    mahasiswa.nama_mahasiswa = data.get('nama_mahasiswa', mahasiswa.nama_mahasiswa)
    mahasiswa.program_studi_id = data.get('program_studi_id', mahasiswa.program_studi_id)
    mahasiswa.ipk_terakhir = data.get('ipk', mahasiswa.ipk_terakhir)
    mahasiswa.status_aktif = data.get('status', mahasiswa.status_aktif)

    session.commit()
    session.close()
    return jsonify({'message': 'Mahasiswa updated successfully'})

@mahasiswaBp.route('/<nrp>', methods=['DELETE'])
def deleteMahasiswa(nrp):
    session = SessionLocal()

    mahasiswa = session.query(Mahasiswa).filter(Mahasiswa.nrp == nrp).first()
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa not found'}), 404

    session.delete(mahasiswa)
    session.commit()
    session.close()
    return jsonify({'message': 'Mahasiswa deleted successfully'})

