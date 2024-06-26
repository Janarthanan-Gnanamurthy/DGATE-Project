from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float,Boolean, Table
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define association table for many-to-many relationship between User and Test
user_test_association = Table('user_test_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('test_id', Integer, ForeignKey('test.id'))
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    number = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    department = Column(String)
    tests = relationship('Test', secondary=user_test_association, backref='users')
    results = relationship('Results', back_populates='user')

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    title = Column(String)  
    instructors = Column(String)
    duration = Column(Integer)
    prerequisites = Column(String)
    
    topics = relationship('Topics', back_populates='course')

class Topics(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))
    
    course = relationship('Course', back_populates='topics')
    questions = relationship('Questions', back_populates='topic')
    test = relationship('Test', back_populates='topic')

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    statement = Column(String, nullable=False)
    description = Column(String)
    question_uri = Column(String)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    answer = Column(String)
    answer_uri = Column(String)
    explanation = Column(String)
    difficulty = Column(String)
    topic_id = Column(Integer, ForeignKey('topics.id'))

    topic = relationship('Topics', back_populates='questions')

test_questions_association = Table(
    'test_questions_association',
    Base.metadata,
    Column('test_id', Integer, ForeignKey('test.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    name = Column(String, nullable=False)
    parameters = Column(JSONB)

    # Establishing relationships
    topic = relationship('Topics', back_populates='test')
    questions = relationship('Questions', secondary=test_questions_association, backref='test')

class Results(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    test_id = Column(Integer, ForeignKey('test.id'), nullable=False)
    score = Column(Float)
    selected_options = Column(JSONB, nullable=False)
    metrics = Column(JSONB)
    
    # Establishing relationships
    user = relationship('User', back_populates='results')
    test = relationship('Test', backref='results')

