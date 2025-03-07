from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base

class Compound(Base):
    __tablename__ = "compounds"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    smiles = Column(Text, nullable=False)
    molecular_formula = Column(String(100), nullable=True)
    molecular_weight = Column(Float, nullable=True)
    logp = Column(Float, nullable=True)
    development_stage = Column(String(50), nullable=False)  # hit, lead, clinical, approved
    origin = Column(String(100), nullable=True)  # literature, proprietary, purchased
    patent_status = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    targets = relationship("CompoundActivity", back_populates="compound")

class CompoundActivity(Base):
    __tablename__ = "compound_activities"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id"))
    target_id = Column(Integer, ForeignKey("targets.id"))
    activity_type = Column(String(50), nullable=False)  # IC50, EC50, Ki, etc.
    activity_value = Column(Float, nullable=False)
    activity_unit = Column(String(20), nullable=False)  # nM, μM, etc.
    mechanism = Column(String(100), nullable=True)  # inhibitor, activator, etc.
    notes = Column(Text, nullable=True)
    
    # Relationships
    compound = relationship("Compound", back_populates="targets")
    target = relationship("Target", back_populates="compounds")