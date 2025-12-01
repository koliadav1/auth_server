from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# Схемы для Role
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# Схемы для BusinessElement
class BusinessElementBase(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessElementCreate(BusinessElementBase):
    pass

class BusinessElementUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class BusinessElementResponse(BusinessElementBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# Схемы для AccessRule
class AccessRuleBase(BaseModel):
    role_id: int
    element_id: int
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False

class AccessRuleCreate(AccessRuleBase):
    pass

class AccessRuleUpdate(BaseModel):
    read_permission: Optional[bool] = None
    read_all_permission: Optional[bool] = None
    create_permission: Optional[bool] = None
    update_permission: Optional[bool] = None
    update_all_permission: Optional[bool] = None
    delete_permission: Optional[bool] = None
    delete_all_permission: Optional[bool] = None

class AccessRuleResponse(AccessRuleBase):
    id: int
    role_name: str
    element_name: str

    model_config = {
        "from_attributes": True
    }

# Схемы для управления User
class UserRoleUpdate(BaseModel):
    role_id: int

class UserDetailResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    is_active: bool
    role_id: int
    role_name: str

    model_config = {
        "from_attributes": True
    }