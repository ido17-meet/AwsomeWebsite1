from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	email = Column(String(255))
	name = Column(String(255))
	photos = relationship("Photo", back_populates='user')
	password = Column(String(255))
	
class Photo(Base):
	__tablename__ = 'photo'
	avgRanking = Column(Float)
	numOfVotes = Column(Integer)
	imgURL = Column(String(255), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	comp_id = Column(Integer, ForeignKey('competition.id'))
	user = relationship("User", back_populates='photos')

class Comp(Base):
	__tablename__ = 'competition'
	id = Column(Integer, primary_key=True)
	expiration_date = Column(DateTime)
	running = Column(Boolean) 
	subject = Column(String(255))
	description = Column(String(255))
	photos = relationship("Photo")

	def ExpirationMechanism(self):
		if self.expiration_date>datetime.today():
			self.running = True
		else:
			self.running = False

	def addPhoto(self, photo):
		self.photos.append(photo)


class Assosiacion(Base):
	__tablename__ = 'assosiacion'
	photoURL = Column(String(255), ForeignKey('photo.imgURL'), primary_key=True)
	voted_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	favorite_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

engine = create_engine('sqlite:///PhotoComps.db')

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

