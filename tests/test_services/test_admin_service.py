import pytest
from app.services import admin_service
from app.schemas.admin_schemas import (
    RoleCreate, RoleUpdate,
    BusinessElementCreate, AccessRuleCreate, UserRoleUpdate
)
from fastapi import HTTPException
from tests.tests_utils import str_to_user_id

class TestAdminService:
    @pytest.mark.asyncio
    async def test_get_all_roles(self, test_db):
        roles = await admin_service.get_all_roles(test_db)
        
        assert len(roles) == 3
        role_names = [role.name for role in roles]
        assert "admin" in role_names
        assert "user" in role_names

    @pytest.mark.asyncio
    async def test_create_role_success(self, test_db):
        role_data = RoleCreate(
            name="moderator",
            description="Moderator role"
        )
        
        role = await admin_service.create_role(test_db, role_data)
        
        assert role.name == "moderator"
        assert role.description == "Moderator role"

    @pytest.mark.asyncio
    async def test_create_role_duplicate_name(self, test_db):
        role_data = RoleCreate(
            name="admin",
            description="Another admin"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await admin_service.create_role(test_db, role_data)
        
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_update_role_success(self, test_db):
        role_data = RoleUpdate(description="Updated admin description")
        
        updated_role = await admin_service.update_role(test_db, 1, role_data)
        
        assert updated_role.id == 1
        assert updated_role.description == "Updated admin description"

    @pytest.mark.asyncio
    async def test_update_role_not_found(self, test_db):
        role_data = RoleUpdate(description="Test")
        
        with pytest.raises(HTTPException) as exc_info:
            await admin_service.update_role(test_db, 999, role_data)
        
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_delete_role_success(self, test_db):
        role_data = RoleCreate(name="temp", description="Temporary role")
        role = await admin_service.create_role(test_db, role_data)
        
        await admin_service.delete_role(test_db, role.id)
        
        roles = await admin_service.get_all_roles(test_db)
        role_ids = [r.id for r in roles]
        assert role.id not in role_ids

    @pytest.mark.asyncio
    async def test_delete_role_with_users(self, test_db):
        with pytest.raises(HTTPException) as exc_info:
            await admin_service.delete_role(test_db, 1)
        
        assert exc_info.value.status_code == 400
        assert "users with this role" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_all_business_elements(self, test_db):
        elements = await admin_service.get_all_business_elements(test_db)
        
        assert len(elements) == 3
        element_names = [e.name for e in elements]
        assert "users" in element_names
        assert "products" in element_names

    @pytest.mark.asyncio
    async def test_create_business_element_success(self, test_db):
        element_data = BusinessElementCreate(
            name="categories",
            description="Product categories"
        )
        
        element = await admin_service.create_business_element(test_db, element_data)
        
        assert element.name == "categories"
        assert element.description == "Product categories"

    @pytest.mark.asyncio
    async def test_get_all_access_rules(self, test_db):
        rules = await admin_service.get_all_access_rules(test_db)

        assert rules is not None
        assert isinstance(rules, list)

    @pytest.mark.asyncio
    async def test_create_access_rule_success(self, test_db):
        rule_data = AccessRuleCreate(
            role_id=2,
            element_id=1,
            read_permission=True,
            create_permission=False
        )
        
        rule = await admin_service.create_access_rule(test_db, rule_data)
        
        assert rule.role_id == 2
        assert rule.element_id == 1
        assert rule.read_permission == True
        assert rule.create_permission == False

    @pytest.mark.asyncio
    async def test_create_access_rule_duplicate(self, test_db):
        rule_data = AccessRuleCreate(
            role_id=1,
            element_id=1,
            read_permission=True
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await admin_service.create_access_rule(test_db, rule_data)
        
        assert exc_info.value.status_code == 400
        assert "already exists" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_all_users(self, test_db):
        users = await admin_service.get_all_users(test_db)
        
        assert len(users) >= 2
        user_emails = [u.email for u in users]
        assert "admin@test.com" in user_emails
        assert "user@test.com" in user_emails

    @pytest.mark.asyncio
    async def test_update_user_role_success(self, test_db, regular_user):
        role_data = UserRoleUpdate(role_id=2)

        user_id = str_to_user_id(regular_user.id)

        updated_user = await admin_service.update_user_role(test_db, user_id, role_data)
        
        assert updated_user.role_id == 2
        assert updated_user.id == regular_user.id

    @pytest.mark.asyncio
    async def test_toggle_user_status(self, test_db, regular_user):
        initial_status = regular_user.is_active

        user_id = str_to_user_id(regular_user.id)
        
        toggled_user = await admin_service.toggle_user_status(test_db, user_id)
        
        assert toggled_user.is_active == (not initial_status)