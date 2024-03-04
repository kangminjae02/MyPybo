from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.email import email_schema
from domain.user import user_crud
from env import Settings

settings = Settings()

router = APIRouter(
    prefix="/api/email"
)

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@router.post("/password-reset", status_code=status.HTTP_204_NO_CONTENT)
async def send_password_reset_email(email: email_schema.PasswordResetEmail,
                                    db: Session = Depends(get_db)):
    # validation check
    db_user = user_crud.get_user_by_email(db=db, email=email.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="사용자를 찾을 수 없습니다.")
    
    # issue a token
    data = {
        "sub": email.email,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES_FOR_EMAIL)
    }
    access_token = jwt.encode(data, settings.SECRET_KEY_FOR_EMAIL, algorithm=settings.ALGORITHM)

    # make a message
    html = f"""<a href="http://localhost:5173/#/reset-password/{access_token}">비밀번호 재설정</a>"""

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email.email],
        body=html,
        subtype=MessageType.html
    )

    # send the email
    fm = FastMail(conf)
    await fm.send_message(message)