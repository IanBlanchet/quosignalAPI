from sqlalchemy import Column, Integer, BigInteger, String , Boolean, Float, Date, ForeignKey, Time
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

class Usager(Base):
    __tablename__='usager'
    id = Column(Integer, primary_key= True)	
    nom = Column(String(50), index = True)
    prenom = Column(String(50), index = True)
    email = Column(String(60), unique = True)
    password_hash = Column(String(128))
    niveau = Column(String(20), default='attente')
	#centre = db.Column(db.Integer, db.ForeignKey('centres.id'))
	#appel = db.relationship('StatAbon', backref='le_benevole', lazy='dynamic')


class Appel(Base):
    __tablename__='appel'
    id = Column(Integer, primary_key= True)
    date = Column(Date)
    resultat = Column(String(25))
    alerte = Column(String(15))
    commentaire = Column(String(300))
    #benevole = db.Column(db.Integer, db.ForeignKey('benevole.id'))
	#abonne = db.Column(db.Integer,  db.ForeignKey('liste.id'))

class Centre(Base):
    __tablename__='centre'
    id = Column(Integer, primary_key= True)
    nom = Column(String(80))
    adresse = Column(String(100))
    ville = Column(String(100))
    telephone = Column(BigInteger, unique= True)
	#benevole = db.relationship('Benevole', backref='centres', lazy='dynamic')
	#abonne = db.relationship('Liste', backref='centres', lazy='dynamic')

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)