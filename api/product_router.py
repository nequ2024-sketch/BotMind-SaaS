from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from models.products import Product

router = APIRouter(prefix="/products", tags=["Products"])

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str = ""

@router.post("/add/{user_id}")
def add_product(user_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(user_id=user_id, name=product.name, price=product.price, description=product.description)
    db.add(new_product)
    db.commit()
    return {"message": "تمت إضافة المنتج بنجاح!"}

@router.get("/list/{user_id}")
def list_products(user_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.user_id == user_id).all()