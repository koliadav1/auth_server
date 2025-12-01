from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models import RefreshToken, User
from app.core.security import create_refresh_token, verify_token
from app.config import Config


async def create_refresh_token_record(db: AsyncSession, user: User) -> str:
    refresh_token = create_refresh_token(data={"user_id": str(user.id)})
    expires_at = datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)

    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at
    )
    
    db.add(db_refresh_token)
    await db.commit()
    await db.refresh(db_refresh_token)
    
    return refresh_token

async def revoke_refresh_token(db: AsyncSession, token: str) -> None:
    result = await db.execute(
        select(RefreshToken).filter(RefreshToken.token == token)
    )
    refresh_token = result.scalar_one_or_none()
    
    if refresh_token:
        refresh_token.is_revoked = True
        await db.commit()

async def revoke_all_user_tokens(db: AsyncSession, user_id: str) -> None:
    await db.execute(
        delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    await db.commit()

async def verify_refresh_token(db: AsyncSession, token: str) -> RefreshToken:
    payload = verify_token(token, is_refresh=True)
    if not payload or payload.get("type") != "refresh":
        return None
    
    result = await db.execute(
        select(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
    )
    refresh_token = result.scalar_one_or_none()
    
    return refresh_token

async def cleanup_expired_tokens(db: AsyncSession):
    """Очистка просроченных токенов"""
    await db.execute(
        delete(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc))
    )
    await db.commit()