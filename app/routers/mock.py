from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import require_permission_dependency
from app.models import User

router = APIRouter(prefix="/mock", tags=["mock"])

# Mock данные для демонстрации
MOCK_PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "price": 999.99, "category": "Электроника", "owner_id": "user1"},
    {"id": 2, "name": "Книга", "price": 19.99, "category": "Образование", "owner_id": "user2"},
    {"id": 3, "name": "Телефон", "price": 699.99, "category": "Электроника", "owner_id": "user1"},
]

MOCK_ORDERS = [
    {"id": 1, "product_id": 1, "quantity": 1, "status": "completed", "owner_id": "user1"},
    {"id": 2, "product_id": 2, "quantity": 3, "status": "pending", "owner_id": "user2"},
    {"id": 3, "product_id": 3, "quantity": 1, "status": "shipped", "owner_id": "user1"},
]

MOCK_STORES = [
    {"id": 1, "name": "Магазин техники", "location": "Москва", "owner_id": "user1"},
    {"id": 2, "name": "Книжный магазин", "location": "Новосибирск", "owner_id": "user2"},
]

@router.get("/products")
def get_products(
    current_user: User = Depends(require_permission_dependency("products", "read")),
    db: Session = Depends(get_db)
):
    """
    Получить список продуктов (требует права read на products)
    """
    return {
        "message": "Mock products data",
        "data": MOCK_PRODUCTS,
        "total": len(MOCK_PRODUCTS)
    }

@router.post("/products")
def create_product(
    current_user: User = Depends(require_permission_dependency("products", "create")),
    db: Session = Depends(get_db)
):
    """
    Создать новый продукт (требует права create на products)
    """
    new_product = {
        "id": len(MOCK_PRODUCTS) + 1,
        "name": "New Product",
        "price": 49.99,
        "category": "General",
        "owner_id": str(current_user.id)
    }
    MOCK_PRODUCTS.append(new_product)
    
    return {
        "message": "Product created successfully",
        "data": new_product
    }

@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    current_user: User = Depends(require_permission_dependency("products", "update")),
    db: Session = Depends(get_db)
):
    """
    Обновить продукт (требует права update на products)
    """
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["name"] = f"Updated {product['name']}"
    
    return {
        "message": f"Product {product_id} updated successfully",
        "data": product
    }

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(require_permission_dependency("products", "delete")),
    db: Session = Depends(get_db)
):
    """
    Удалить продукт (требует права delete на products)
    """
    global MOCK_PRODUCTS
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    MOCK_PRODUCTS = [p for p in MOCK_PRODUCTS if p["id"] != product_id]
    
    return {
        "message": f"Product {product_id} deleted successfully"
    }

@router.get("/orders")
def get_orders(
    current_user: User = Depends(require_permission_dependency("orders", "read")),
    db: Session = Depends(get_db)
):
    """
    Получить список заказов (требует права read на orders)
    """
    return {
        "message": "Mock orders data",
        "data": MOCK_ORDERS,
        "total": len(MOCK_ORDERS)
    }

@router.get("/stores")
def get_stores(
    current_user: User = Depends(require_permission_dependency("stores", "read")),
    db: Session = Depends(get_db)
):
    """
    Получить список магазинов (требует права read на stores)
    """
    return {
        "message": "Mock stores data",
        "data": MOCK_STORES,
        "total": len(MOCK_STORES)
    }

@router.get("/users")
def get_users(
    current_user: User = Depends(require_permission_dependency("users", "read")),
    db: Session = Depends(get_db)
):
    """
    Получить список пользователей (требует права read на users)
    """
    mock_users = [
        {"id": "user1", "email": "user1@example.com", "name": "John Doe"},
        {"id": "user2", "email": "user2@example.com", "name": "Jane Smith"},
    ]
    
    return {
        "message": "Mock users data",
        "data": mock_users,
        "total": len(mock_users)
    }