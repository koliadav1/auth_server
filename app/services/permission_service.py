from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User, AccessRule, BusinessElement
from fastapi import HTTPException, status


async def check_permission(db: AsyncSession, user: User, element_name: str, action: str) -> bool:
    if user.role_id == 1:
        return True
    
    result = await db.execute(select(BusinessElement).filter(BusinessElement.name == element_name))
    element = result.scalar_one_or_none()

    if not element:
        return False

    result = await db.execute(
        select(AccessRule).filter(
            AccessRule.role_id == user.role_id,
            AccessRule.element_id == element.id
        )
    )
    access_rule = result.scalar_one_or_none()
        
    if not access_rule:
        return False

    permission_mapping = {
        "read": "read_permission",
        "read_all": "read_all_permission",
        "create": "create_permission",
        "update": "update_permission",
        "update_all": "update_all_permission",
        "delete": "delete_permission",
        "delete_all": "delete_all_permission"
    }
        
    permission_field = permission_mapping.get(action)
    if not permission_field:
        return False
        
    return getattr(access_rule, permission_field, False)

async def require_permission(db: AsyncSession, user: User, element: str, action: str):
    if not await check_permission(db, user, element, action):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return True