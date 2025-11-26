from fastapi import APIRouter, HTTPException
from models import ProductCreate, ProductUpdate, Product
from database import (
    get_products, get_product, add_product, update_product, delete_product
)

router = APIRouter()

@router.get("/products", response_model=list[Product])
def listar_productos():
    return get_products()

@router.get("/products/{product_id}", response_model=Product)
def obtener_producto(product_id: int):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/products", response_model=Product)
def crear_producto(product: ProductCreate):
    return add_product(product.nombre, product.precio, product.descripcion)

@router.put("/products/{product_id}", response_model=Product)
def actualizar_producto(product_id: int, product: ProductUpdate):
    updated = update_product(product_id, product.nombre, product.precio, product.descripcion)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado o sin cambios")
    return updated

@router.delete("/products/{product_id}")
def eliminar_producto(product_id: int):
    deleted = delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}