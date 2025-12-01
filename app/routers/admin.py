from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.core.dependencies import require_permission_dependency
from app.models import AccessRule, BusinessElement, Role, User
from app.services.admin_service import (
    get_all_roles, 
    create_role, 
    update_role, 
    delete_role, 
    get_all_business_elements, 
    toggle_user_status, 
    create_business_element,
    update_business_element,
    delete_business_element,
    get_all_access_rules,
    create_access_rule,
    update_access_rule,
    delete_access_rule,
    get_all_users,
    update_user_role
)
from app.schemas.admin_schemas import *

router = APIRouter(prefix="/admin", tags=["admin"])

# === Role Management Endpoints ===
@router.get("/roles", response_model=List[RoleResponse])
async def get_all_roles_api(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "read"))
):
    """
    Получить все роли (требует права read на access_rules)
    """
    return await get_all_roles(db)

@router.post("/roles", response_model=RoleResponse)
async def create_role_api(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "create"))
):
    """
    Создать новую роль (требует права create на access_rules)
    """
    return await create_role(db, role_data)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role_api(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "update"))
):
    """
    Обновить роль (требует права update на access_rules)
    """
    return await update_role(db, role_id, role_data)

@router.delete("/roles/{role_id}")
async def delete_role_api(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "delete"))
):
    """
    Удалить роль (требует права delete на access_rules)
    """
    await delete_role(db, role_id)
    return {"message": "Role deleted successfully"}

# === Business Element Management Endpoints ===
@router.get("/business-elements", response_model=List[BusinessElementResponse])
async def get_all_business_elements_api(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "read"))
):
    """
    Получить все бизнес-элементы (требует права read на access_rules)
    """
    return await get_all_business_elements(db)

@router.post("/business-elements", response_model=BusinessElementResponse)
async def create_business_element_api(
    element_data: BusinessElementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "create"))
):
    """
    Создать новый бизнес-элемент (требует права create на access_rules)
    """
    return await create_business_element(db, element_data)

@router.put("/business-elements/{element_id}", response_model=BusinessElementResponse)
async def update_business_element_api(
    element_id: int,
    element_data: BusinessElementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "update"))
):
    """
    Обновить бизнес-элемент (требует права update на access_rules)
    """
    return await update_business_element(db, element_id, element_data)

@router.delete("/business-elements/{element_id}")
async def delete_business_element_api(
    element_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "delete"))
):
    """
    Удалить бизнес-элемент (требует права delete на access_rules)
    """
    await delete_business_element(db, element_id)
    return {"message": "Business element deleted successfully"}

# === Access Rule Management Endpoints ===
@router.get("/access-rules", response_model=List[AccessRuleResponse])
async def get_all_access_rules_api(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "read"))
):
    """
    Получить все правила доступа (требует права read на access_rules)
    """
    rules = await get_all_access_rules(db)
    
    response_rules = []
    for rule in rules:
        rule_dict = {**rule.__dict__}
        rule_dict["role_name"] = rule.role.name
        rule_dict["element_name"] = rule.element.name
        response_rules.append(AccessRuleResponse(**rule_dict))
    
    return response_rules

@router.post("/access-rules", response_model=AccessRuleResponse)
async def create_access_rule_api(
    rule_data: AccessRuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "create"))
):
    """
    Создать новое правило доступа (требует права create на access_rules)
    """
    rule = await create_access_rule(db, rule_data)

    result = await db.execute(
        select(AccessRule)
        .options(
            selectinload(AccessRule.role),
            selectinload(AccessRule.element)
        )
        .filter(AccessRule.id == rule.id)
    )
    rule_with_names = result.scalar_one_or_none()
    rule_dict = {**rule_with_names.__dict__}
    rule_dict["role_name"] = rule_with_names.role.name
    rule_dict["element_name"] = rule_with_names.element.name
    
    return AccessRuleResponse(**rule_dict)

@router.put("/access-rules/{rule_id}", response_model=AccessRuleResponse)
async def update_access_rule_api(
    rule_id: int,
    rule_data: AccessRuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "update"))
):
    """
    Обновить правило доступа (требует права update на access_rules)
    """
    rule = await update_access_rule(db, rule_id, rule_data)
    
    result = await db.execute(select(AccessRule).join(Role).join(BusinessElement).filter(AccessRule.id == rule.id))
    rule_with_names = result.scalar_one_or_none()
    rule_dict = {**rule_with_names.__dict__}
    rule_dict["role_name"] = rule_with_names.role.name
    rule_dict["element_name"] = rule_with_names.element.name
    
    return AccessRuleResponse(**rule_dict)

@router.delete("/access-rules/{rule_id}")
async def delete_access_rule_api(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("access_rules", "delete"))
):
    """
    Удалить правило доступа (требует права delete на access_rules)
    """
    await delete_access_rule(db, rule_id)
    return {"message": "Access rule deleted successfully"}

# === User Management Endpoints ===
@router.get("/users", response_model=List[UserDetailResponse])
async def get_all_users_api(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("users", "read_all"))
):
    """
    Получить всех пользователей (требует права read_all на users)
    """
    users = await get_all_users(db)
    
    response_users = []
    for user in users:
        user_dict = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "patronymic": user.patronymic,
            "is_active": user.is_active,
            "role_id": user.role_id,
            "role_name": user.role.name
        }
        response_users.append(UserDetailResponse(**user_dict))
    
    return response_users

@router.put("/users/{user_id}/role")
async def update_user_role_api(
    user_id: str,
    role_data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("users", "update_all"))
):
    """
    Изменить роль пользователя (требует права update_all на users)
    """
    user = await update_user_role(db, user_id, role_data)
    return {
        "message": "User role updated successfully",
        "user_id": str(user.id),
        "new_role_id": user.role_id
    }

@router.post("/users/{user_id}/toggle-status")
async def toggle_user_status_api(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission_dependency("users", "update_all"))
):
    """
    Активировать/деактивировать пользователя (требует права update_all на users)
    """
    user = await toggle_user_status(db, user_id)
    status_text = "activated" if user.is_active else "deactivated"
    return {
        "message": f"User {status_text} successfully",
        "user_id": str(user.id),
        "is_active": user.is_active
    }