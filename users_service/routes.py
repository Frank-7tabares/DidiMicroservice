from fastapi import APIRouter, HTTPException
from models import UserCreate, UserUpdate, User
from database import (
    get_users, get_user, add_user, update_user, delete_user
)

router = APIRouter()

@router.get("/users", response_model=list[User])
def listar_usuarios():
    return get_users()

@router.get("/users/{user_id}", response_model=User)
def obtener_usuario(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/users", response_model=User)
def crear_usuario(user: UserCreate):
    return add_user(user.email, user.nombre, user.apellido, user.role)

@router.put("/users/{user_id}", response_model=User)
def actualizar_usuario(user_id: int, user: UserUpdate):
    updated = update_user(user_id, user.email, user.nombre, user.apellido, user.role)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin cambios")
    return updated

@router.delete("/users/{user_id}")
def eliminar_usuario(user_id: int):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}