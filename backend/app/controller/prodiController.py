from flask import Blueprint, request, jsonify
from app.Model import PengajuanBeasiswa, Mahasiswa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

prodiBp = Blueprint('prodi', __name__)

def get_session():
    return SessionLocal()

def create_response(data, status=200):
    return jsonify(data), status

@prodiBp.route('/pengajuan/<int:periode_id>', methods=['GET'])
def get_pengajuan_by_periode(periode_id):
    session = get_session()
    pengajuan_list = session.query(PengajuanBeasiswa).filter_by(periode_id=periode_id).all()
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

@prodiBp.route('/pengajuan/detail/<int:pengajuan_id>', methods=['GET'])
def get_pengajuan_detail(pengajuan_id):
    session = get_session()
    pengajuan = session.query(PengajuanBeasiswa).filter_by(pengajuan_id=pengajuan_id).first()
    mahasiswa = session.query(Mahasiswa).filter_by(nrp=pengajuan.nrp).first()

    if not pengajuan:
        return create_response({'message': 'Pengajuan not found'}, 404)

    result = {
        'pengajuan': {
            'pengajuan_id': pengajuan.pengajuan_id,
            'nrp': pengajuan.nrp,
            'beasiswa_id': pengajuan.beasiswa_id,
            'periode_id': pengajuan.periode_id,
            'tanggal_pengajuan': pengajuan.tanggal_pengajuan,
            'status_pengajuan': pengajuan.status_pengajuan,
            'status_pengajuan_fakultas': pengajuan.status_pengajuan_fakultas,
            'dokumen_pengajuan': pengajuan.dokumen_pengajuan
        },
        'mahasiswa': {
            'nrp': mahasiswa.nrp,
            'nama_mahasiswa': mahasiswa.nama_mahasiswa,
            'program_studi_id': mahasiswa.program_studi_id,
            'ipk_terakhir': mahasiswa.ipk_terakhir,
            'status_aktif': mahasiswa.status_aktif
        }
    }

    session.close()
    return create_response(result)

@prodiBp.route('/pengajuan/approve/<int:pengajuan_id>', methods=['PUT'])
def approve_pengajuan(pengajuan_id):
    session = get_session()
    pengajuan = session.query(PengajuanBeasiswa).filter_by(pengajuan_id=pengajuan_id).first()

    if not pengajuan:
        return create_response({'message': 'Pengajuan not found'}, 404)

    pengajuan.status_pengajuan = 'Disetujui Prodi'
    session.commit()
    session.close()
    return create_response({'message': 'Pengajuan approved by Program Studi'})

@prodiBp.route('/pengajuan/decline/<int:pengajuan_id>', methods=['PUT'])
def decline_pengajuan(pengajuan_id):
    session = get_session()
    pengajuan = session.query(PengajuanBeasiswa).filter_by(pengajuan_id=pengajuan_id).first()

    if not pengajuan:
        return create_response({'message': 'Pengajuan not found'}, 404)

    pengajuan.status_pengajuan = 'Tidak Disetujui Prodi'
    session.commit()
    session.close()
    return create_response({'message': 'Pengajuan declined by Program Studi'})
