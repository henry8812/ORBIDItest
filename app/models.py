from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class APICall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String)
    params = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
