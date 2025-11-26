from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    role: str = "cliente"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    role: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True