import os
import math
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from colector import cauta_joburi_externe

app = FastAPI(title="CAUT JOB")
templates = Jinja2Templates(directory="templates")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

Baza_Recenzii_Companii = [
    {"companie": "Kaufland", "autor": "Anonim", "comentariu": "Salariul vine la timp, dar e muncă multă în weekend.", "data": "Azi"},
    {"companie": "Lidl", "autor": "Anonim", "comentariu": "Salarii bune pe piață, management strict.", "data": "Ieri"}
]

@app.get("/", response_class=HTMLResponse)
async def pagina_principala_get(request: Request, q: str = "", locatie: str = "Bucuresti", page: int = 1):
    joburi_totale = cauta_joburi_externe(cuvant_cheie=q, locatie=locatie)
    ELEMENTE_PER_PAGINA = 15
    total_elemente = len(joburi_totale)
    total_pagini = math.ceil(total_elemente / ELEMENTE_PER_PAGINA)
    
    start_idx = (page - 1) * ELEMENTE_PER_PAGINA
    joburi_paginate = joburi_totale[start_idx:start_idx + ELEMENTE_PER_PAGINA]

    for j in joburi_paginate:
        j["rating_mediu"] = 4.2
        j["total_recenzii"] = 5
        j["match_score"] = 100
        j["match_reason"] = "Compatibilitate perfectă"

    context = {"request": request, "joburi": joburi_paginate, "q": q, "locatie": locatie, "lang": "ro", "toate_recenziile": Baza_Recenzii_Companii, "current_page": page, "total_pages": total_pagini, "total_items": total_elemente}
    return templates.TemplateResponse("index.html", context)

@app.post("/", response_class=HTMLResponse)
async def pagina_principala_post(request: Request, q: str = Form(""), locatie: str = Form("Bucuresti"), page: int = 1):
    return await pagina_principala_get(request, q, locatie, page)

@app.get("/admin", response_class=HTMLResponse)
async def pagina_admin(request: Request):
    return HTMLResponse("<h1>Panou Admin Protejat</h1>")
