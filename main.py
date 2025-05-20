from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Permitir CORS para que el frontend (Vercel) pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o poné tu dominio Vercel específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/precios")
def obtener_precios():
    url = "https://www.cac.bcr.com.ar/es/precios-de-pizarra"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tabla = soup.find("table", class_="table")
    precios = []

    if tabla:
        rows = tabla.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                precios.append({
                    "producto": cols[0].text.strip(),
                    "entrega": cols[1].text.strip(),
                    "precio": cols[2].text.strip()
                })

    return {"precios": precios}
