from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    correct_option = Column(Integer)

class UserQuizSession(Base):
    __tablename__ = "user_quiz_session"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    score = Column(Integer)
