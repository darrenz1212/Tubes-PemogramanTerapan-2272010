from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Model import Base
from app.mahasiswaController import mahasiswaBp
from app.userController import userBp
from app.auth.login import loginBp
from app.auth.register import registerBp
from app.pengajuan.pengajuanController import pengajuanBp
from dbConfig import DATABASE_URL

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['UPLOAD_FOLDER'] = 'dokumenPengajuan'

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.before_first_request
def setup():
    Base.metadata.create_all(engine)

# Register blueprints
app.register_blueprint(mahasiswaBp, url_prefix='/mahasiswa')
app.register_blueprint(userBp, url_prefix='/user')
app.register_blueprint(loginBp, url_prefix='/auth')
app.register_blueprint(registerBp, url_prefix='/auth')
app.register_blueprint(pengajuanBp, url_prefix='/pengajuan')

if __name__ == '__main__':
    app.run(debug=True)
