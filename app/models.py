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
    telephone2 = Column(BigInteger, default=None)
    adresse = Column(String(100))
    ville = Column(String(75))
    heure = Column(Time, unique = True)
    actif = Column(Boolean, default = True)
    langue = Column(String(30))
    date_insc = Column(Date, default = date.today)
    noCle = Column(Integer, default=None)
    infoSupp = Column(JSONB, default={})
    jours = Column(JSONB, default={'jours':['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']})
    centre_id = Column(Integer, ForeignKey('centre.id'))
    appels = relationship('Appel', back_populates="abonne", lazy='joined')
    centre = relationship('Centre', back_populates="abonnes")
    contactUrgences = relationship('ContactUrgence', back_populates="abonnes", secondary='ass_abonne_contactUrgence')
    associations = relationship('Ass_abonne_contactUrgence', back_populates='abonne', overlaps="contactUrgences,abonnes")

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

class ContactUrgence(Base):
    __tablename__='contactUrgence'
    id = Column(Integer, primary_key= True)
    nomComplet = Column(String(100))
    telephone = Column(BigInteger)
    telephone2 = Column(BigInteger, default=None)
    cleDispo = Column(Boolean)
    abonnes = relationship('Abonne', back_populates="contactUrgences",secondary='ass_abonne_contactUrgence')
    associations = relationship('Ass_abonne_contactUrgence', back_populates='contactUrgence', overlaps="contactUrgences,abonnes")

class Ass_abonne_contactUrgence(Base):
    __tablename__ = 'ass_abonne_contactUrgence'    
    abonne_id = Column(Integer, ForeignKey('abonne.id'), primary_key=True)
    contactUrgence_id = Column(Integer, ForeignKey('contactUrgence.id'), primary_key=True)
    lien = Column(String(30))
    abonne = relationship('Abonne', back_populates='associations', overlaps="contactUrgences,abonnes")
    contactUrgence = relationship('ContactUrgence', back_populates='associations', overlaps="contactUrgences,abonnes")
    __table_args__ = ( UniqueConstraint('abonne_id', 'contactUrgence_id', name='uq_abonne_contactUrgence'), )


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
#Base.metadata.create_all(engine)