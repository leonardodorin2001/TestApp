from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column("Username", String)
    password = Column("Password", String)

    def __repr__(self):
        return f'<Users username={self.username}, password= {self.password}>'


class Task(Base):
    __tablename__ = "Task"
    
    id = Column(Integer, primary_key=True)
    task = Column("Task",String)
    info = Column("Info", String)

    def __repr__(self):
        return f'<Task task={self.task}, info= {self.info}>'
    
