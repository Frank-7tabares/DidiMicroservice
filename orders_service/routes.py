from fastapi import APIRouter, HTTPException
from models import OrderCreate, OrderUpdate, Order, OrderDetail, OrderItem
from database import (
    get_orders, get_orders_by_user, get_order, get_order_items,
    add_order, update_order, delete_order
)

router = APIRouter()


@router.get("/orders", response_model=list[Order])
def listar_ordenes():
    return get_orders()


@router.get("/orders/user/{user_id}", response_model=list[Order])
def listar_ordenes_usuario(user_id: int):
    return get_orders_by_user(user_id)


@router.get("/orders/{order_id}", response_model=OrderDetail)
def obtener_orden(order_id: int):
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    items = get_order_items(order_id)
    return {
        **order,
        "items": items
    }


@router.post("/orders", response_model=OrderDetail, status_code=201)
def crear_orden(order: OrderCreate):
    # Calcular total si no viene
    total = sum(item.cantidad * item.precio_unitario for item in order.items)

    items_data = [
        {
            "product_id": item.product_id,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario
        }
        for item in order.items
    ]

    new_order = add_order(
        order.user_id,
        order.direccion_entrega,
        total,
        items_data
    )

    if not new_order:
        raise HTTPException(status_code=400, detail="Error al crear la orden")

    items = get_order_items(new_order["id"])
    return {
        **new_order,
        "items": items
    }


@router.put("/orders/{order_id}", response_model=Order)
def actualizar_orden(order_id: int, order: OrderUpdate):
    updated = update_order(order_id, order.estado, order.direccion_entrega)
    if not updated:
        raise HTTPException(status_code=404, detail="Orden no encontrada o sin cambios")
    return updated


@router.delete("/orders/{order_id}")
def eliminar_orden(order_id: int):
    deleted = delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada correctamente"}