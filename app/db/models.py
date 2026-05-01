from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    interval_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)

    site_id = Column(Integer, ForeignKey("sites.id"))

    status = Column(String)
    status_code = Column(Integer)

    checked_at = Column(DateTime, default=datetime.utcnow)