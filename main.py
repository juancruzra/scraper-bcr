from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Permitir llamadas desde Vercel o cualquier dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O mejor: ["https://tu-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/precios")
def obtener_precios():
    url = "https://www.cac.bcr.com.ar/es/precios-de-pizarra"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    granos = ["trigo", "maiz", "girasol", "soja", "sorgo"]
    precios = []

    for grano in granos:
        board = soup.find("div", class_=f"board-{grano}")
        if board:
            nombre = board.find("h3").get_text(strip=True)
            precio = board.find("div", class_="price").get_text(strip=True)
            precios.append({"producto": nombre, "precio": precio})

    return {"precios": precios}
