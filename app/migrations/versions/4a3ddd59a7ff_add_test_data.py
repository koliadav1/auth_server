"""Add test data

Revision ID: 4a3ddd59a7ff
Revises: 1a3a751d95e9
Create Date: 2025-11-29 21:44:48.587852

"""
from typing import Sequence, Union

from alembic import op
import bcrypt
from app.core.security import get_password_hash
import uuid


# revision identifiers, used by Alembic.
revision: str = '4a3ddd59a7ff'
down_revision: Union[str, Sequence[str], None] = '1a3a751d95e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Роли
    op.execute("""
        INSERT INTO roles (name, description) VALUES
        ('admin', 'Administrator with full access'),
        ('manager', 'Manager with limited admin rights'),
        ('user', 'Regular user'),
        ('guest', 'Guest user with minimal access')
    """)

    # 2. Бизнес-элементы
    op.execute("""
        INSERT INTO business_elements (name, description) VALUES
        ('users', 'User management'),
        ('products', 'Product catalog'),
        ('orders', 'Order management'),
        ('stores', 'Store management'),
        ('access_rules', 'Access rules management')
    """)

    # 3. Пользователи
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password1 = pwd_context.hash("123")
    hashed_password2 = pwd_context.hash("456")
    hashed_password3 = pwd_context.hash("789")
    hashed_password4 = pwd_context.hash("1234")
    
    user1_id = uuid.uuid4()
    user2_id = uuid.uuid4()
    user3_id = uuid.uuid4()
    user4_id = uuid.uuid4()
    
    op.execute(f"""
        INSERT INTO users (id, email, password_hash, first_name, last_name, role_id, is_active, created_at) VALUES
        ('{user1_id}', 'admin@example.com', '{hashed_password1}', 'Admin', 'User', 1, true, NOW()),
        ('{user2_id}', 'manager@example.com', '{hashed_password2}', 'Manager', 'User', 2, true, NOW()),
        ('{user3_id}', 'user@example.com', '{hashed_password3}', 'Regular', 'User', 3, true, NOW()),
        ('{user4_id}', 'guest@example.com', '{hashed_password4}', 'Guest', 'User', 4, true, NOW())
    """)

    # 4. Права доступа для админа (все права на все элементы)
    op.execute("""
        INSERT INTO access_rules (role_id, element_id, read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission) VALUES
        (1, 1, true, true, true, true, true, true, true),
        (1, 2, true, true, true, true, true, true, true),
        (1, 3, true, true, true, true, true, true, true),
        (1, 4, true, true, true, true, true, true, true),
        (1, 5, true, true, true, true, true, true, true)
    """)

    # 5. Права доступа для менеджера (ограниченные права)
    op.execute("""
        INSERT INTO access_rules (role_id, element_id, read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission) VALUES
        (2, 1, true, true, true, true, false, true, false),
        (2, 2, true, true, true, true, false, true, false),
        (2, 3, true, true, true, true, false, true, false),
        (2, 4, true, true, true, true, false, true, false),
        (2, 5, false, false, false, false, false, false, false)
    """)

    # 6. Права доступа для обычного пользователя (минимальные права)
    op.execute("""
        INSERT INTO access_rules (role_id, element_id, read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission) VALUES
        (3, 1, true, false, false, true, false, true, false),
        (3, 2, true, false, false, false, false, false, false),
        (3, 3, true, false, false, false, false, false, false),
        (3, 4, true, false, false, false, false, false, false),
        (3, 5, false, false, false, false, false, false, false)
    """)

    # 7. Права доступа для гостя (только просмотр)
    op.execute("""
        INSERT INTO access_rules (role_id, element_id, read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission) VALUES
        (4, 1, false, false, false, false, false, false, false),
        (4, 2, true, false, false, false, false, false, false),
        (4, 3, true, false, false, false, false, false, false),
        (4, 4, true, false, false, false, false, false, false),
        (4, 5, false, false, false, false, false, false, false)
    """)

    # 8. Refresh токены (пример)
    op.execute("""
        INSERT INTO refresh_tokens (user_id, token, expires_at, is_revoked) VALUES
        ('{user1_id}', 'mock_refresh_token_1', NOW() + INTERVAL '7 days', false),
        ('{user3_id}', 'mock_refresh_token_2', NOW() + INTERVAL '7 days', false)
    """.format(user1_id=user1_id, user3_id=user3_id))


def downgrade() -> None:
    op.execute("DELETE FROM refresh_tokens WHERE token IN ('mock_refresh_token_1', 'mock_refresh_token_2')")
    op.execute("DELETE FROM access_rules WHERE role_id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM users WHERE email IN ('admin@example.com', 'manager@example.com', 'user@example.com', 'guest@example.com')")
    op.execute("DELETE FROM business_elements WHERE id IN (1, 2, 3, 4, 5)")
    op.execute("DELETE FROM roles WHERE id IN (1, 2, 3, 4)")
