from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Numeric, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('administrator','mahasiswa','program_studi','fakultas'), nullable=False)
    program_studi_id = Column(Integer, ForeignKey('program_studi.program_studi_id'), nullable=True)
    fakultas_id = Column(Integer, ForeignKey('fakultas.fakultas_id'), nullable=True)

    program_studi = relationship('ProgramStudi', back_populates='users')
    fakultas = relationship('Fakultas', back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

class ProgramStudi(Base):
    __tablename__ = 'program_studi'
    
    program_studi_id = Column(Integer, primary_key=True, autoincrement=True)
    nama_program_studi = Column(String(100), nullable=False)
    fakultas_id = Column(Integer, ForeignKey('fakultas.fakultas_id'), nullable=False)

    fakultas = relationship('Fakultas', back_populates='program_studi')
    users = relationship('User', back_populates='program_studi')

    def __repr__(self):
        return f'<ProgramStudi {self.nama_program_studi}>'

class Fakultas(Base):
    __tablename__ = 'fakultas'
    
    fakultas_id = Column(Integer, primary_key=True, autoincrement=True)
    nama_fakultas = Column(String(100), nullable=False)

    program_studi = relationship('ProgramStudi', back_populates='fakultas')
    users = relationship('User', back_populates='fakultas')

    def __repr__(self):
        return f'<Fakultas {self.nama_fakultas}>'

class Mahasiswa(Base):
    __tablename__ = 'mahasiswa'
    nrp = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    nama_mahasiswa = Column(String(255), nullable=False)
    program_studi_id = Column(Integer, nullable=True)
    ipk_terakhir = Column(Numeric(3, 2), nullable=False)
    status_aktif = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'<Mahasiswa {self.nama_mahasiswa}>'

class DokumenPengajuan(Base):
    __tablename__ = 'dokumen_pengajuan'
    
    dokumen_id = Column(Integer, primary_key=True)
    pengajuan_id = Column(Integer, nullable=True)
    nama_dokumen = Column(String(255), nullable=False)
    path_dokumen = Column(String(255), nullable=False)

    def __repr__(self):
        return f'<DokumenPengajuan {self.nama_dokumen}>'

class JenisBeasiswa(Base):
    __tablename__ = 'jenis_beasiswa'
    
    beasiswa_id = Column(Integer, primary_key=True)
    nama_beasiswa = Column(String(255), nullable=False)
    deskripsi_beasiswa = Column(Text, nullable=True)

    def __repr__(self):
        return f'<JenisBeasiswa {self.nama_beasiswa}>'

class PengajuanBeasiswa(Base):
    __tablename__ = 'pengajuan_beasiswa'
    
    pengajuan_id = Column(Integer, primary_key=True)
    nrp = Column(Integer, ForeignKey('mahasiswa.nrp'), nullable=True)
    beasiswa_id = Column(Integer, ForeignKey('jenis_beasiswa.beasiswa_id'), nullable=True)
    periode_id = Column(Integer, nullable=True)
    tanggal_pengajuan = Column(DateTime, nullable=False)
    status_pengajuan = Column(Enum('Diajukan','Disetujui Prodi','Tidak Disetujui Prodi'), nullable=False)
    status_pengajuan_fakultas = Column(Enum('Diajukan','Disetujui Fakultas','Tidak Disetujui Fakultas'), nullable=False)
    dokumen_pengajuan = Column(String(255), nullable=False)

    mahasiswa = relationship('Mahasiswa', backref='pengajuan_beasiswa')
    jenis_beasiswa = relationship('JenisBeasiswa', backref='pengajuan_beasiswa')

    def __repr__(self):
        return f'<PengajuanBeasiswa {self.pengajuan_id}>'

class PeriodePengajuan(Base):
    __tablename__ = 'periode_pengajuan'
    
    periode_id = Column(Integer, primary_key=True)
    nama_periode = Column(String(255), nullable=False)
    tanggal_mulai = Column(DateTime, nullable=False)
    tanggal_selesai = Column(DateTime, nullable=False)
    fakultas_id = Column(Integer, ForeignKey('fakultas.fakultas_id'), nullable=True)

    fakultas = relationship('Fakultas', backref='periode_pengajuan')

    def __repr__(self):
        return f'<PeriodePengajuan {self.nama_periode}>'
