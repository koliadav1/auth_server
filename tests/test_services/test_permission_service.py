import pytest
from app.services import permission_service
from fastapi import HTTPException

class TestPermissionService:
    @pytest.mark.asyncio
    async def test_check_permission_admin_always_true(self, test_db, admin_user):
        result = await permission_service.check_permission(
            test_db, admin_user, "any_element", "any_action"
        )
        assert result == True

    @pytest.mark.asyncio
    async def test_check_permission_user_has_read_access(self, test_db, regular_user):
        result = await permission_service.check_permission(
            test_db, regular_user, "users", "read"
        )
        assert result == True

    @pytest.mark.asyncio
    async def test_check_permission_user_no_create_access(self, test_db, regular_user):
        result = await permission_service.check_permission(
            test_db, regular_user, "users", "create"
        )
        assert result == False

    @pytest.mark.asyncio
    async def test_check_permission_nonexistent_element(self, test_db, regular_user):
        result = await permission_service.check_permission(
            test_db, regular_user, "nonexistent", "read"
        )
        assert result == False

    @pytest.mark.asyncio
    async def test_require_permission_success(self, test_db, regular_user):
        result = await permission_service.require_permission(
            test_db, regular_user, "users", "read"
        )
        assert result == True

    @pytest.mark.asyncio
    async def test_require_permission_forbidden(self, test_db, regular_user):
        with pytest.raises(HTTPException) as exc_info:
            await permission_service.require_permission(
                test_db, regular_user, "users", "create"
            )
        
        assert exc_info.value.status_code == 403
        assert "permissions" in exc_info.value.detail