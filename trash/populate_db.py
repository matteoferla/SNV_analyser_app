from sqlalchemy.exc import DBAPIError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import analyser_app.models as models


session = sessionmaker(bind=create_engine('sqlite:///../analyser_app.sqlite'))()

query = session.query(models.ProteinNames)
one = query.filter(models.ProteinNames.name == 'POLR2A').first()


