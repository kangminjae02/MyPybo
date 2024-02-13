
from datetime import datetime

from sqlalchemy.orm import Session

from domain.reply.reply_schema import Reply, ReplyCreate, ReplyUpdate, ReplyVote
from models import Reply, Answer, User

def create_reply(db: Session, answer: Answer, reply_create: ReplyCreate, user: User):
    db_reply = Reply(answer=answer,
                     content=reply_create.content,
                     create_date=datetime.now(),
                     user=user)
    db.add(db_reply)
    db.commit()

def get_reply(db: Session, reply_id: int):
    return db.query(Reply).get(reply_id)

def get_reply_list(db: Session, answer_id: int, skip: int = 0, limit: int = 5):
    reply_list = db.query(Reply).filter(Reply.answer_id == answer_id)
    
    total = reply_list.distinct().count()
    reply_list = reply_list.order_by(Reply.id.desc()).offset(skip).limit(limit).distinct().all()
    return total, reply_list

def update_reply(db: Session, db_reply: Reply, reply_update: ReplyUpdate):
    db_reply.content = reply_update.content
    db_reply.modify_date = datetime.now()
    db.add(db_reply)
    db.commit()

def delete_reply(db: Session, db_reply: Reply):
    db.delete(db_reply)
    db.commit()

def vote_reply(db: Session, db_reply: Reply, db_user: User):
    db_reply.voter.append(db_user)
    db.commit()