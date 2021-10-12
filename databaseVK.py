import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DSN = ''
engine = sq.create_engine(DSN)
session = sessionmaker(bind=engine)


class Candidates(Base):
    __tablename__ = 'Candidates'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40))


Base.metadata.create_all(engine)