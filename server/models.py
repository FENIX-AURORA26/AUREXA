from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
id: Column[int] = Column(Integer, primary_key=True, index=True)
email = Column(String, unique=True, index=True)
senha = Column(String)
plano = Column(String, default="free")

