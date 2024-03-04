from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class OAuth2EmailRequestForm(BaseModel):
    email: EmailStr
    
class Token(BaseModel):
    access_token: str
    token_type: str
    email: str

class PasswordResetEmail(BaseModel):
    email: EmailStr
