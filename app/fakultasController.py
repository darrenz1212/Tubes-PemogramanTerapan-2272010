from flask import Blueprint, request, jsonify
from app.Model import PengajuanBeasiswa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fakultasBp = Blueprint('fakultas', __name__)

def get_session():
    return SessionLocal()

def create_response(data, status=200):
    return jsonify(data), status

@fakultasBp.route('/pengajuan', methods=['GET'])
def get_all_pengajuan():
    session = get_session()
    pengajuan_list = session.query(PengajuanBeasiswa).all()
    session.close()
    
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

    return create_response({'pengajuan': result})

@fakultasBp.route('/pengajuan/approvedByProdi', methods=['GET'])
def get_approved_by_prodi_pengajuan():
    session = get_session()
    pengajuan_list = session.query(PengajuanBeasiswa).filter(PengajuanBeasiswa.status_pengajuan == 'Disetujui Prodi').all()
    session.close()
    
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

    return create_response({'pengajuan': result})

@fakultasBp.route('/pengajuan/approve/<int:pengajuan_id>', methods=['PUT'])
def approve_pengajuan(pengajuan_id):
    session = get_session()
    pengajuan = session.query(PengajuanBeasiswa).filter_by(pengajuan_id=pengajuan_id).first()

    if not pengajuan:
        return create_response({'message': 'Pengajuan not found'}, 404)

    if pengajuan.status_pengajuan == 'Disetujui Prodi':
        pengajuan.status_pengajuan_fakultas = 'Disetujui Fakultas'
        session.commit()
        session.close()
        return create_response({'message': 'Pengajuan approved by Fakultas'})

    session.close()
    return create_response({'message': 'Pengajuan not approved by program studi'}, 400)

@fakultasBp.route('/pengajuan/decline/<int:pengajuan_id>', methods=['PUT'])
def decline_pengajuan(pengajuan_id):
    session = get_session()
    pengajuan = session.query(PengajuanBeasiswa).filter_by(pengajuan_id=pengajuan_id).first()

    if not pengajuan:
        return create_response({'message': 'Pengajuan not found'}, 404)

    if pengajuan.status_pengajuan == 'disetujui_prodi':
        pengajuan.status_pengajuan_fakultas = 'Tidak Disetujui Fakultas'
        session.commit()
        session.close()
        return create_response({'message': 'Pengajuan not approved by Fakultas'})

    session.close()
    return create_response({'message': 'Pengajuan not approved by program studi'}, 400)
