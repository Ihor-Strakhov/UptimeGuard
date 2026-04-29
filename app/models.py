from sqlalchemy import Column, Integer, String
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    interval_minutes = Column(Integer)