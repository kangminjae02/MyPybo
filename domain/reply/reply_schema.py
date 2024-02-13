import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

class Reply(BaseModel):
    id: int
    answer_id: int
    content: str
    user: User | None
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

class ReplyList(BaseModel):
    total: int
    reply_list: list[Reply]
    
class ReplyCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class ReplyUpdate(ReplyCreate):
    reply_id: int

class ReplyDelete(BaseModel):
    reply_id: int

class ReplyVote(BaseModel):
    reply_id: int