import pytest_asyncio
from httpx import AsyncClient, patch
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import User, Role, BusinessElement, AccessRule
from app.core.security import get_password_hash

@pytest_asyncio.fixture(scope="function")
async def test_db():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncTestingSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async def override_get_db():
        async with AsyncTestingSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncTestingSessionLocal() as session:
        await create_test_data(session)
        yield session
    
    app.dependency_overrides.clear()
    await engine.dispose()

async def create_test_data(session: AsyncSession):
    """Создание тестовых данных"""
    roles = [
        Role(id=1, name="admin", description="Administrator"),
        Role(id=2, name="manager", description="Manager"), 
        Role(id=3, name="user", description="Regular user"),
    ]
    
    elements = [
        BusinessElement(id=1, name="users", description="User management"),
        BusinessElement(id=2, name="products", description="Product catalog"),
        BusinessElement(id=3, name="access_rules", description="Access rules"),
    ]
    
    for role in roles:
        session.add(role)
    for element in elements:
        session.add(element)
    
    access_rules = [
        AccessRule(role_id=1, element_id=1, read_permission=True, read_all_permission=True, 
                  create_permission=True, update_permission=True, update_all_permission=True, 
                  delete_permission=True, delete_all_permission=True),
        AccessRule(role_id=1, element_id=2, read_permission=True, read_all_permission=True,
                  create_permission=True, update_permission=True, update_all_permission=True,
                  delete_permission=True, delete_all_permission=True),
        AccessRule(role_id=1, element_id=3, read_permission=True, read_all_permission=True,
                  create_permission=True, update_permission=True, update_all_permission=True,
                  delete_permission=True, delete_all_permission=True),
        
        AccessRule(role_id=3, element_id=1, read_permission=True, read_all_permission=False, 
                  create_permission=False, update_permission=True, update_all_permission=False, 
                  delete_permission=True, delete_all_permission=False),
        AccessRule(role_id=3, element_id=2, read_permission=True, read_all_permission=False, 
                  create_permission=False, update_permission=False, update_all_permission=False, 
                  delete_permission=False, delete_all_permission=False),
    ]
    
    for rule in access_rules:
        session.add(rule)
    
    users = [
        User(
            email="admin@test.com",
            password_hash="admin123",
            first_name="Admin",
            last_name="User", 
            role_id=1,
            is_active=True
        ),
        User(
            email="user@test.com", 
            password_hash="user123",
            first_name="Regular",
            last_name="User",
            role_id=3, 
            is_active=True
        ),
    ]
    
    for user in users:
        session.add(user)
    
    await session.commit()

@pytest_asyncio.fixture
async def client(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def admin_user(test_db):
    from sqlalchemy import select
    result = await test_db.execute(select(User).filter(User.email == "admin@test.com"))
    return result.scalar_one()

@pytest_asyncio.fixture  
async def regular_user(test_db):
    from sqlalchemy import select
    result = await test_db.execute(select(User).filter(User.email == "user@test.com"))
    return result.scalar_one()

@pytest_asyncio.fixture
def mock_password_hash():
    with patch('app.core.security.get_password_hash.pwd_context.hash', return_value="hashed_password") as mock:
        yield mock