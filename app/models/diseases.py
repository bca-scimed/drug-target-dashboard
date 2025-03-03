from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    etiology = Column(String(100), nullable=True)  # viral, genetic, etc.
    prevalence = Column(String(255), nullable=True)
    patient_population = Column(Text, nullable=True)
    treatment_landscape = Column(Text, nullable=True)
    unmet_needs = Column(Text, nullable=True)
    
    # Relationships
    targets = relationship("TargetDiseaseRelation", back_populates="disease")

class TargetDiseaseRelation(Base):
    __tablename__ = "target_disease_relations"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id"))
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    relationship_type = Column(String(100), nullable=False)  # primary, secondary, exploratory
    evidence_level = Column(String(50), nullable=False)  # strong, moderate, hypothetical
    
    # Relationships
    target = relationship("Target", back_populates="diseases")
    disease = relationship("Disease", back_populates="targets")