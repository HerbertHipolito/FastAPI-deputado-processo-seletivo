from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Insight - Processo seletivo",
    description="Desafio do processo seletivo para vaga de Full-stack Python. A API pública a ser consumida é a https://dadosabertos.camara.leg.br/swagger/api.html",
    version="0.0.1"
)

app.include_router(router)
