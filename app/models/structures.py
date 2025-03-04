from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class Structure(Base):
    __tablename__ = "structures"
    
    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id"), index=True)
    pdb_id = Column(String, index=True)
    resolution = Column(Float)
    file_path = Column(String)
    
    # Relationship
    target = relationship("Target", back_populates="structures")