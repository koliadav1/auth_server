import pytest
from app.services import token_service
from app.models import RefreshToken
from tests.tests_utils import str_to_user_id
from sqlalchemy import select

class TestTokenService:
    @pytest.mark.asyncio
    async def test_create_refresh_token_record(self, test_db, regular_user):
        token = await token_service.create_refresh_token_record(test_db, regular_user)
        
        assert token is not None
        assert len(token) > 0
        
        result = await test_db.execute(
            select(RefreshToken).filter(RefreshToken.user_id == regular_user.id)
        )
        db_token = result.scalar_one_or_none()
        assert db_token is not None
        assert db_token.token == token

    @pytest.mark.asyncio
    async def test_revoke_refresh_token(self, test_db, regular_user):
        token = await token_service.create_refresh_token_record(test_db, regular_user)
        
        await token_service.revoke_refresh_token(test_db, token)
        
        from sqlalchemy import select
        result = await test_db.execute(
            select(RefreshToken).filter(RefreshToken.token == token)
        )
        db_token = result.scalar_one()
        assert db_token.is_revoked == True

    @pytest.mark.asyncio
    async def test_revoke_all_user_tokens(self, test_db, regular_user):
        import asyncio
        token1 = await token_service.create_refresh_token_record(test_db, regular_user)
        await asyncio.sleep(1)
        token2 = await token_service.create_refresh_token_record(test_db, regular_user)
        
        user_id = str_to_user_id(regular_user.id)
        
        await token_service.revoke_all_user_tokens(test_db, user_id)
        
        result = await test_db.execute(
            select(RefreshToken).filter(RefreshToken.user_id == regular_user.id)
        )
        tokens = result.scalars().all()
        assert len(tokens) == 0

    @pytest.mark.asyncio
    async def test_verify_refresh_token_valid(self, test_db, regular_user):
        token = await token_service.create_refresh_token_record(test_db, regular_user)
        
        verified_token = await token_service.verify_refresh_token(test_db, token)
        
        assert verified_token is not None
        assert verified_token.token == token
        assert verified_token.user_id == regular_user.id

    @pytest.mark.asyncio
    async def test_verify_refresh_token_revoked(self, test_db, regular_user):
        token = await token_service.create_refresh_token_record(test_db, regular_user)
        await token_service.revoke_refresh_token(test_db, token)
        
        verified_token = await token_service.verify_refresh_token(test_db, token)
        
        assert verified_token is None