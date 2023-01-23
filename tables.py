from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, INTEGER, Text, Column

Base = declarative_base()

class famous_people(Base):
    __tablename__ = 'Famous People'

    id = Column(INTEGER, primary_key=True, autoincrement = True)
    profession = Column(Text)
    name = Column(Text)
    born = Column(Text)
    birthplace = Column(Text)
    died = Column(Text)
    description = Column(Text)