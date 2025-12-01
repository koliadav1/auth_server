from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    patronymic: Optional[str] = None

class UserCreate(UserBase):
    password: str
    password_confirm: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    role_id: int

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str