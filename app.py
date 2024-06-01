from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Model import Base
from app.mahasiswaController import mahasiswaBp
from app.userController import userBp
from dbConfig import DATABASE_URL

app = Flask(__name__)

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.before_first_request
def setup():
    Base.metadata.create_all(engine)

# Register blueprints
app.register_blueprint(mahasiswaBp, url_prefix='/mahasiswa')
app.register_blueprint(userBp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
