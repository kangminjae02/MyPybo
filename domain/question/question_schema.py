import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    category: str | None
    subject: str
    content: str
    user: User | None
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    answers: list[Answer] = []
    voter: list[User] = []
    views: int

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []
    
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int

class QuestionIncreaseViews(BaseModel):
    question_id: int