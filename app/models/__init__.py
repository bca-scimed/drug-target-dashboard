from app.models.database import Base, engine
from app.models.targets import Target, Structure
from app.models.diseases import Disease, TargetDiseaseRelation
from app.models.compounds import Compound, CompoundActivity

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)