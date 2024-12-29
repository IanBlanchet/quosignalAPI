from sqlalchemy import Column, Integer, BigInteger, String , Boolean, Float, Date, ForeignKey, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base, engine
from datetime import date
from sqlalchemy.dialects.postgresql import JSONB

class Abonne(Base):
    __tablename__='abonne'
    id = Column(Integer, primary_key= True)
    nom = Column(String(100), index = True)
    prenom = Column(String(100), index = True)
    date_naissance = Column(Date, index = True)
    telephone = Column(BigInteger, unique= True)
    adresse = Column(String(100))
    ville = Column(String(75))
    heure = Column(Time, unique = True)
    actif = Column(Boolean, default = True)
    langue = Column(String(30))
    date_insc = Column(Date, default = date.today)
    centre_id = Column(Integer, ForeignKey('centre.id'))
    appels = relationship('Appel', lazy='joined', back_populates="abonne")
    centre = relationship('Centre', back_populates="abonnes")

class Usager(Base):
    __tablename__='usager'
    id = Column(Integer, primary_key= True)	
    nom = Column(String(50), index = True)
    prenom = Column(String(50), index = True)
    email = Column(String(60), unique = True)
    password_hash = Column(String(128))
    niveau = Column(String(20), default='attente')
    centre_id = Column(Integer, ForeignKey('centre.id'))
    appels = relationship('Appel', back_populates="usager", lazy='joined')
    centre = relationship('Centre', back_populates="usagers")


class Appel(Base):
    __tablename__='appel'
    id = Column(Integer, primary_key= True)
    date = Column(Date)
    resultat = Column(String(25))
    alerte = Column(String(15))
    commentaire = Column(String(300))
    usager_id = Column(Integer, ForeignKey('usager.id'))
    abonne_id = Column(Integer,  ForeignKey('abonne.id'))
    abonne = relationship('Abonne', back_populates='appels') 
    usager = relationship('Usager', back_populates='appels')
    __table_args__ = (
        UniqueConstraint('date', 'abonne_id', name='uq_date_abonne'),
    )

class Centre(Base):
    __tablename__='centre'
    id = Column(Integer, primary_key= True)
    nom = Column(String(80))
    adresse = Column(String(100))
    ville = Column(String(100))
    telephone = Column(BigInteger, unique= True)
    usagers = relationship('Usager', back_populates='centre', lazy='joined')
    abonnes = relationship('Abonne', back_populates='centre', lazy='joined')

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)