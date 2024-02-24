from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.reply import reply_schema, reply_crud
from domain.answer import answer_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/reply"
)

@router.post("/create/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def reply_create(answer_id: int,
                  reply_create: reply_schema.ReplyCreate,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    #create reply
    answer = answer_crud.get_answer(db=db, answer_id=answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    reply_crud.create_reply(db=db,
                            answer=answer,
                            reply_create=reply_create,
                            user=user)

@router.get("/detail/{reply_id}", response_model=reply_schema.Reply)
def get_reply(reply_id: int, db: Session = Depends(get_db)):
    reply = reply_crud.get_reply(db=db, reply_id=reply_id)
    return reply

@router.get("/list/{answer_id}", response_model=reply_schema.ReplyList)
def get_reply_list(answer_id: int,
                   db: Session = Depends(get_db),
                   page: int = 0, size: int = 20):
    total, reply_list = reply_crud.get_reply_list(
        db=db,
        answer_id=answer_id,
        skip= page*size,
        limit = size
    )

    return {
        'total' : total,
        'reply_list' : reply_list
    }

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def reply_update(reply_update: reply_schema.ReplyUpdate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_reply = reply_crud.get_reply(db=db, reply_id=reply_update.reply_id)
    if not db_reply:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_reply.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    reply_crud.update_reply(db=db,
                            db_reply = db_reply,
                            reply_update=reply_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def reply_delete(reply_delete: reply_schema.ReplyDelete,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_reply = reply_crud.get_reply(db=db, reply_id=reply_delete.reply_id)
    if not db_reply:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_reply.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    reply_crud.delete_reply(db=db, db_reply=db_reply)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def reply_vote(reply_vote: reply_schema.ReplyVote,
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    db_reply = reply_crud.get_reply(db=db, reply_id=reply_vote.reply_id)
    if not db_reply:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    reply_crud.vote_reply(db=db, db_reply=db_reply, db_user=user)
