from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models import User, Role, BusinessElement, AccessRule
from app.schemas.admin_schemas import (
    RoleCreate, RoleUpdate, 
    BusinessElementCreate, BusinessElementUpdate,
    AccessRuleCreate, AccessRuleUpdate,
    UserRoleUpdate
)
from fastapi import HTTPException, status


async def get_all_roles(db: AsyncSession) -> List[Role]:
    result = await db.execute(select(Role))
    return result.scalars().all()

async def create_role(db: AsyncSession, role_data: RoleCreate) -> Role:
    result = await db.execute(select(Role).filter(Role.name == role_data.name))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists"
        )
        
    db_role = Role(**role_data.model_dump())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def update_role(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Role:
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
        
    for field, value in role_data.model_dump(exclude_unset=True).items():
        setattr(role, field, value)
        
    await db.commit()
    await db.refresh(role)
    return role

async def delete_role(db: AsyncSession, role_id: int) -> None:
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
        
    result = await db.execute(select(func.count(User.id)).filter(User.role_id == role_id))
    users_with_role = result.scalar()
    if users_with_role > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role. There are {users_with_role} users with this role"
        )
        
    await db.delete(role)
    await db.commit()

async def get_all_business_elements(db: AsyncSession) -> List[BusinessElement]:
    result = await db.execute(select(BusinessElement))
    return result.scalars().all()

async def create_business_element(db: AsyncSession, element_data: BusinessElementCreate) -> BusinessElement:
    result = await db.execute(select(BusinessElement).filter(BusinessElement.name == element_data.name))
    existing_element = result.scalar_one_or_none()
    if existing_element:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business element with this name already exists"
        )

    db_element = BusinessElement(**element_data.model_dump())
    db.add(db_element)
    await db.commit()
    await db.refresh(db_element)
    return db_element

async def update_business_element(db: AsyncSession, element_id: int, element_data: BusinessElementUpdate) -> BusinessElement:
    result = await db.execute(select(BusinessElement).filter(BusinessElement.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business element not found"
        )
        
    for field, value in element_data.model_dump(exclude_unset=True).items():
        setattr(element, field, value)
        
    await db.commit()
    await db.refresh(element)
    return element

async def delete_business_element(db: AsyncSession, element_id: int) -> None:
    result = await db.execute(select(BusinessElement).filter(BusinessElement.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business element not found"
        )

    result = await db.execute(select(func.count(AccessRule.id))).filter(AccessRule.element_id == element_id)
    access_rules_count = result.scalar()
    if access_rules_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete business element. There are {access_rules_count} access rules for this element"
        )
        
    await db.delete(element)
    await db.commit()

async def get_all_access_rules(db: AsyncSession) -> List[AccessRule]:
    stmt = select(AccessRule).options(
        selectinload(AccessRule.role),
        selectinload(AccessRule.element)
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_access_rule(db: AsyncSession, rule_id: int) -> AccessRule:
    result = await db.execute(select(AccessRule).filter(AccessRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access rule not found"
        )
    return rule

async def create_access_rule(db: AsyncSession, rule_data: AccessRuleCreate) -> AccessRule:
    result = await db.execute(select(Role).filter(Role.id == rule_data.role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
        
    result = await db.execute(select(BusinessElement).filter(BusinessElement.id == rule_data.element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business element not found"
        )
        
    result = await db.execute(
        select(AccessRule).filter(
            AccessRule.role_id == rule_data.role_id, 
            AccessRule.element_id == rule_data.element_id
        )
    )
    existing_rule = result.scalar_one_or_none()

    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access rule for this role and element already exists"
        )
        
    db_rule = AccessRule(**rule_data.model_dump())
    db.add(db_rule)
    await db.commit()
    await db.refresh(db_rule)
    return db_rule

async def update_access_rule(db: AsyncSession, rule_id: int, rule_data: AccessRuleUpdate) -> AccessRule:
    result = await db.execute(select(AccessRule).filter(AccessRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access rule not found"
        )
        
    for field, value in rule_data.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
        
    await db.commit()
    await db.refresh(rule)
    return rule

async def delete_access_rule(db: AsyncSession, rule_id: int) -> None:
    result = await db.execute(select(AccessRule).filter(AccessRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access rule not found"
        )
        
    await db.delete(rule)
    await db.commit()

async def get_all_users(db: AsyncSession) -> List[User]:
    stmt = select(User).options(selectinload(User.role))
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_user_role(db: AsyncSession, user_id: str, role_data: UserRoleUpdate) -> User:
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    result = await db.execute(select(Role).filter(Role.id == role_data.role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
        
    user.role_id = role_data.role_id
    await db.commit()
    await db.refresh(user)
    return user

async def toggle_user_status(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    user.is_active = not user.is_active
    await db.commit()
    await db.refresh(user)
    return user