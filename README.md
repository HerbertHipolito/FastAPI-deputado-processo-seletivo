# Deputados informação

API desenvolvida em Python utilizando FASTAPI para o processo seletivo da Insight. Essa API lista as informações básicas dos deputados federais, por exemplo, nome, partido, discursos, despesas etc. A api pública utilizada como fonte foi a https://dadosabertos.camara.leg.br/swagger/api.html .

## Documentação

Após seguir os passos para instalação, a documentação com Swagger da api pode ser acessada via http://localhost:8000/docs 

## Instalação

Clone esse repositório para sua máquina:
```
git clone https://github.com/HerbertHipolito/FastAPI-deputado-processo-seletivo
```
Entre dentro da pasta da aplicação que foi clonada agora.

Construa a imagem docker da aplicação com o comando:
```
docker build -t api_deputado_insight .
```
Rode o programa:

```
docker run -it -p 8000:8000 api_deputado_insight
```

A documentação da aplicação usando Swagger juntamente com as rotas é para esta disponivel em: http://localhost:8000/docs

