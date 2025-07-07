from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    payload: str
    nonce: str
    tag: str

class PayloadEncrypt(BaseModel):
    payload: str
    nonce: str
    tag: str
