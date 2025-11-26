from fastapi import FastAPI
from routes import router
from database import create_tables

app = FastAPI(title="Microservicio de Pedidos - Didi Food")

create_tables()
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Microservicio de Pedidos activo"}