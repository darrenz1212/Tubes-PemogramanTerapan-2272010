from flask import Flask, request, jsonify
from Model import Base, Mahasiswa, DokumenPengajuan, Fakultas, JenisBeasiswa, PengajuanBeasiswa, PeriodePengajuan,User,ProgramStudi
from dbConfig import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

app = Flask(__name__)

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
@app.before_first_request
def setup():
    Base.metadata.create_all(engine)

# ==================================== MAHASISWA CONTROLLER ====================================
@app.route('/mahasiswa', methods=['GET'])
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
@app.route('/mahasiswa/<nrp>')

def getMahasiswaById(nrp):
    session = SessionLocal()
    query = session.query(
        Mahasiswa.nrp,
        Mahasiswa.user_id,
        Mahasiswa.nama_mahasiswa,
        Mahasiswa.program_studi_id,
        Mahasiswa.ipk_terakhir,
        Mahasiswa.status_aktif
    ).filter(Mahasiswa.nrp == nrp)
    if not query : 
        return jsonify({
            'message': 'Mahasiswa not found'
        })
    
    result = [
        {
            'nrp': m.nrp,
            'user_id': m.user_id,
            'nama_mahasiswa': m.nama_mahasiswa,
            'prodi': m.program_studi_id,
            'ipk': m.ipk_terakhir,
            'status': m.status_aktif
        }
        for m in query
    ]
    
    session.close()
    return jsonify(result)


def getUserInfoById(user_id):
    session = SessionLocal()
    query = session.query(User.username, User.program_studi_id).filter(User.user_id == user_id)
    result = query.first()
    session.close()
    return result

@app.route('/mahasiswa/<userID>', methods=['POST'])
def addMahasiswa(userID):
    data = request.get_json()
    session = SessionLocal()

    # Ambil informasi user
    user_info = getUserInfoById(userID)
    if not user_info:
        return jsonify({'message': 'User not found'}), 404

    new_mahasiswa = Mahasiswa(
        nrp=data.get('nrp'),
        user_id=userID,
        nama_mahasiswa=user_info.username,
        program_studi_id=user_info.program_studi_id,
        ipk_terakhir=data.get('ipk'),
        status_aktif=data.get('status')
    )

    session.add(new_mahasiswa)
    session.commit()

    # Akses atribut sebelum menutup sesi
    nrp = new_mahasiswa.nrp
    nama_mahasiswa = new_mahasiswa.nama_mahasiswa

    session.close()

    return jsonify({
        'message': 'Mahasiswa added successfully',
        'nrp': nrp,
        'nama_mahasiswa': nama_mahasiswa,
        'program_studi_id': user_info.program_studi_id
    })

@app.route('/mahasiswa/<nrp>', methods=['PUT'])
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

@app.route('/mahasiswa/<nrp>', methods=['DELETE'])
def deleteMahasiswa(nrp):
    session = SessionLocal()

    mahasiswa = session.query(Mahasiswa).filter(Mahasiswa.nrp == nrp).first()
    if not mahasiswa:
        return jsonify({'message': 'Mahasiswa not found'}), 404

    session.delete(mahasiswa)
    session.commit()
    session.close()
    return jsonify({'message': 'Mahasiswa deleted successfully'})


# ==================================== MAHASISWA CONTROLLER END ====================================




# ==================================== USER CONTROLLER ====================================

@app.route('/user',methods=['GET'])
def getUser():
    sesion = SessionLocal()
    userList = sesion.query(User).all()
    result = [
        {
            'user_id': u.user_id,
            'usename': u.username,
            'password': u.password,
            'role': u.role,
            'program_studi_id':u.program_studi_id,
            'fakultas_id':u.fakultas_id
        }
        for u in userList
    ]
    sesion.close()
    return jsonify({'user': result})

@app.route('/user/<userID>', methods=['GET'])
def getUserByID(userID):
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == userID).first()

    if user:
        result = {
            'user_id': user.user_id,
            'username': user.username, 
            'role': user.role,
            'program_studi_id': user.program_studi_id,
            'fakultas_id': user.fakultas_id
        }
    else:
        result = None
    
    session.close()
    return jsonify({'user': result})


@app.route('/user', methods=['POST'])
def addUser():

    data = request.get_json()
    session = SessionLocal()
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    addUser = User(
        user_id = data.get('user_id'),
        username = data.get('username'),
        password = hashed_password,
        role = data.get('role'),
        program_studi_id = data.get('data_prodi'),
        fakultas_id = data.get('fakultas_id')       
    )

    session.add(addUser)
    session.commit()

    session.close()
    return jsonify({'message': 'User added successfully'})



@app.route('/user/<userID>', methods=['PUT'])
def updateUser(userID):
    data = request.get_json()
    session = SessionLocal()

    user = session.query(User).filter(User.user_id == userID).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.username = data.get('username', user.username)
    user.password = hashlib.sha256(data.get('password', user.password).encode()).hexdigest()
    user.role = data.get('role', user.role)
    user.program_studi_id = data.get('program_studi_id', user.program_studi_id)
    user.fakultas_id = data.get('fakultas_id', user.fakultas_id)

    session.commit()
    session.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/user/<userID>', methods=['DELETE'])
def deleteUser(userID):
    session = SessionLocal()

    user = session.query(User).filter(User.user_id == userID).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    session.delete(user)
    session.commit()
    session.close()
    return jsonify({'message': 'User deleted successfully'})



# ==================================== USER CONTROLLER END ====================================


if __name__ == '__main__':
    app.run(debug=True)
