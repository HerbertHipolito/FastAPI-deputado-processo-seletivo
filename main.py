from fastapi import FastAPI, HTTPException
from router import router

#api link = https://dadosabertos.camara.leg.br/swagger/api.html
app = FastAPI(
    title="Insight - Processo seletivo",
    description="Desafio do processo seletivo para vaga de Back-end Python. A API pública a ser é a https://dadosabertos.camara.leg.br/swagger/api.html",
    version="0.0.1"
)

app.include_router(router)
