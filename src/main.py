import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
from pydantic import BaseModel, Field

app = FastAPI()

# Configuración de CORS (Equivalente a CORS(app))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todos los orígenes
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    titulo: str
    comentario: str

db = [Post(titulo="Primer post", comentario="Este es el primer post"),
      Post(titulo="Segundo post", comentario="Este es el segundo post")]


@app.get("/posts", response_model=list[Post])
def get_all():
    # En FastAPI no hace falta jsonify, devuelve el dict o lista directamente
    return db

@app.post("/posts", status_code=201)
def create_post(post: Post):
    db.append(post)
    return {"status": "creado"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for i in range(len(db)):
        if db[i].id == post_id:
            db.pop(i)
            return {"status": "eliminado"}

    raise HTTPException(status_code=404, detail="No se encontró el post para eliminar")

def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_app()