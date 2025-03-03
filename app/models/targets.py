from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base

class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    alternative_names = Column(Text, nullable=True)
    organism = Column(String(100), nullable=False)  # human, viral, bacterial, fungal
    category = Column(String(100), nullable=False)  # cardiovascular, viral, fungal, etc.
    validation_status = Column(String(50), nullable=False)  # novel, partially validated, established
    priority = Column(String(20), nullable=False)  # high, medium, low
    description = Column(Text, nullable=False)
    mechanism = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    molecular_weight = Column(Float, nullable=True)
    cellular_location = Column(String(255), nullable=True)
    
    # Relationships
    structures = relationship("Structure", back_populates="target")
    diseases = relationship("TargetDiseaseRelation", back_populates="target")
    compounds = relationship("CompoundActivity", back_populates="target")

class Structure(Base):
    __tablename__ = "structures"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id"))
    pdb_id = Column(String(10), nullable=True)
    resolution = Column(Float, nullable=True)
    file_path = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    target = relationship("Target", back_populates="structures")