import sys
import os

# Adiciona a raiz do projeto ao PYTHONPATH para que o botão 'Run' do VS Code funcione
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import inference

app = FastAPI(
    title="API de Detecção - Aedes Aegypti",
    description="Backend para receber imagens e retornar a inferência do YOLOv8",
    version="1.0.0"
)

# Permitir todas as origens na fase de testes em rede local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas da API
app.include_router(inference.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Detecção de Larvas Aedes Aegypti!"}

if __name__ == "__main__":
    import uvicorn
    # Permite rodar o servidor apertando o play do VS Code diretamente neste arquivo
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
