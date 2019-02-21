from sqlalchemy import (
    Column,
    Index,
    Boolean,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from .meta import Base

class ProteinNames(Base):
    __tablename__ = 'protein'
    id = Column(Integer, primary_key=True)
    name = Column(Text) # gene name
    ac = Column(Text) # accession
