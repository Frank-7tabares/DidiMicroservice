from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    cantidad: int
    precio_unitario: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int
    direccion_entrega: str
    total: float


class OrderCreate(BaseModel):
    user_id: int
    direccion_entrega: str
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    estado: Optional[str] = None
    direccion_entrega: Optional[str] = None


class Order(OrderBase):
    id: int
    estado: str
    fecha_creacion: str

    class Config:
        from_attributes = True


class OrderDetail(Order):
    items: List[OrderItem]