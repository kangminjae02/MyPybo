from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')
    views = Column(Integer, nullable=False, server_default='0')

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

reply_voter = Table(
    'reply_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('reply_id', Integer, ForeignKey('reply.id'), primary_key=True)
)

class Reply(Base):
    __tablename__ = "reply"

    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("answer.id"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    answer = relationship("Answer", backref="replies")
    user = relationship("User", backref="reply_users")
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    voter = relationship("User", secondary=reply_voter, backref="reply_voters")