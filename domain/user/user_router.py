from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from env import Settings

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login", auto_error=False)

router = APIRouter(
    prefix="/api/user"
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.put("/update/password", status_code=status.HTTP_204_NO_CONTENT)
def user_password_update(token: str,
                         _user_update: user_schema.UserUpdatePassword, 
                         db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_FOR_EMAIL, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            print("No email")
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        db_user = user_crud.get_user_by_email(db, email)
        user_crud.update_user_password(db=db, db_user=db_user, user_update=_user_update)

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES_FOR_LOGIN)
    }
    access_token = jwt.encode(data, settings.SECRET_KEY_FOR_LOGIN, algorithm=settings.ALGORITHM)

    return{
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not token:
            print('Not autherized')
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY_FOR_LOGIN, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user