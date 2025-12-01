from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.database import get_db
from app.models import User
from app.services.permission_service import require_permission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    
    result = await db.execute(
        select(User).filter(User.id == user_id, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def require_permission_dependency(element: str, action: str):
    """
    Фабрика зависимостей для проверки прав доступа
    """
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        await require_permission(db, current_user, element, action)
        return current_user
    
    return permission_dependency