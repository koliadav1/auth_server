from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token
from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.auth_schemas import Token, TokenRefresh
from app.services.auth_service import authenticate_user, register_user, update_user_profile, soft_delete_user
from app.core.dependencies import get_current_user
from app.models import User
from app.services.token_service import create_refresh_token_record, revoke_all_user_tokens, revoke_refresh_token, verify_refresh_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    user = await register_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Вход в систему - возвращает access и refresh токены
    """
    user = await authenticate_user(db, login_data)
    
    access_token = create_access_token(data={"user_id": str(user.id)})
    refresh_token = await create_refresh_token_record(db, user)
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление access токена с помощью refresh токена
    """
    refresh_token = await verify_refresh_token(db, refresh_data.refresh_token)
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = create_access_token(data={"user_id": str(refresh_token.user_id)})
    new_refresh_token = await create_refresh_token_record(db, refresh_token.user)
    
    await revoke_refresh_token(db, refresh_data.refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Выход из системы - ревокаем все refresh токены пользователя
    """
    await revoke_all_user_tokens(db, str(current_user.id))
    
    return {"message": "Successfully logged out"}

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление профиля пользователя
    """
    user = await update_user_profile(db, current_user, update_data.model_dump(exclude_unset=True))
    return user

@router.delete("/profile")
async def delete_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Мягкое удаление аккаунта
    """
    await revoke_all_user_tokens(db, str(current_user.id))
    user = await soft_delete_user(db, current_user)
    return {"message": "User account deactivated successfully"}