from unittest.mock import patch
import pytest
from app.services import auth_service
from app.schemas.user_schemas import UserCreate, UserLogin
from fastapi import HTTPException

class TestAuthService:
    @pytest.mark.asyncio
    async def test_register_user_success(self, test_db):
        user_data = UserCreate(
            email="newuser@test.com",
            password="pass123",
            password_confirm="pass123",
            first_name="New",
            last_name="User"
        )
        
        mock_hash = patch('app.services.auth_service.get_password_hash')
        with mock_hash as mock_hash_func:
            mock_hash_func.return_value = "mocked_hash"
            user = await auth_service.register_user(test_db, user_data)
        
        assert user.email == "newuser@test.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.role_id == 3
        assert user.is_active == True
        assert user.password_hash == "mocked_hash"

    @pytest.mark.asyncio
    async def test_register_user_password_mismatch(self, test_db):
        user_data = UserCreate(
            email="test@test.com",
            password="password123",
            password_confirm="different",
            first_name="Test",
            last_name="User"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.register_user(test_db, user_data)
        
        assert exc_info.value.status_code == 400
        assert "Passwords do not match" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, test_db):
        user_data = UserCreate(
            email="admin@test.com",
            password="password123",
            password_confirm="password123",
            first_name="Test",
            last_name="User"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.register_user(test_db, user_data)
        
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, test_db):
        user_data = UserCreate(
            email="testauth@test.com",
            password="auth123",
            password_confirm="auth123",
            first_name="Test",
            last_name="Auth"
        )
        
        mock_hash = patch('app.services.auth_service.get_password_hash')
        with mock_hash as mock_hash_func:
            mock_hash_func.return_value = "mocked_hash"
            await auth_service.register_user(test_db, user_data)
        
        login_data = UserLogin(
            email="testauth@test.com",
            password="auth123"
        )
        with patch('app.services.auth_service.verify_password', return_value=True):
            user = await auth_service.authenticate_user(test_db, login_data)
        assert user.email == "testauth@test.com"

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, test_db):
        user_data = UserCreate(
            email="testwrong@test.com",
            password="pass123",
            password_confirm="pass123",
            first_name="Test",
            last_name="Wrong"
        )

        mock_hash = patch('app.services.auth_service.get_password_hash')
        with mock_hash as mock_hash_func:
            mock_hash_func.return_value = "mocked_hash"
            await auth_service.register_user(test_db, user_data)
        
        login_data = UserLogin(
            email="testwrong@test.com",
            password="wrongpassword"
        )

        with patch('app.services.auth_service.verify_password', return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await auth_service.authenticate_user(test_db, login_data)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent_email(self, test_db):
        login_data = UserLogin(
            email="nonexistent@test.com",
            password="password123"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.authenticate_user(test_db, login_data)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_update_user_profile(self, test_db, regular_user):
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        updated_user = await auth_service.update_user_profile(test_db, regular_user, update_data)
        
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.email == regular_user.email

    @pytest.mark.asyncio
    async def test_soft_delete_user(self, test_db, regular_user):
        assert regular_user.is_active == True
        
        deleted_user = await auth_service.soft_delete_user(test_db, regular_user)
        
        assert deleted_user.is_active == False
        assert deleted_user.email == regular_user.email