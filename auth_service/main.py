from fastapi import FastAPI
from routes import router
from database import create_tables

app = FastAPI(title="Microservicio de Autenticación - Didi Food")

create_tables()
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Microservicio de Autenticación activo"}