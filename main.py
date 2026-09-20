import os
import io
import re
import math
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from docx import Document
from colector import cauta_joburi_externe

app = FastAPI(title="CAUT JOB")
templates = Jinja2Templates(directory="templates")
templates.env.cache = None

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

Baza_Recenzii_Companii = [
    {"companie": "Kaufland", "autor": "Anonim (Fost Casier)", "mail": "securizat@cautjob.ro", "telefon": "0722000000", "note_salariu": 4, "note_management": 3, "comentariu": "Salariul vine fix la dată, tichetele de masă sunt consistente. Volumul de muncă este însă foarte solicitant în zilele de weekend.", "data": "18.09.2026"},
    {"companie": "Continental", "autor": "Anonim (Fost Operator)", "mail": "verificat@cautjob.ro", "telefon": "0744000000", "note_salariu": 5, "note_management": 4, "comentariu": "Condiții excelente de lucru în fabrică, echipamente noi și training asigurat din prima zi. Managementul pune accent pe siguranță.", "data": "20.09.2026"}
]

def extrage_text_din_cv_stream(continut_bytes, extensie):
    text = ""
    try:
        if extensie == ".pdf":
            stream = io.BytesIO(continut_bytes)
            cititor = PdfReader(stream)
            for pagina in cititor.pages: text += pagina.extract_text() or ""
        elif extensie in [".docx", ".doc"]:
            stream = io.BytesIO(continut_bytes)
            doc = Document(stream)
            for paragraf in doc.paragraphs: text += paragraf.text + "\n"
    except Exception: pass
    return text.lower().strip()

def calculeaza_compatibilitate_precisa(text_cv, job, lang):
    procent = 25 
    if not text_cv: return procent, "Introducere de bază. Încarcă fișierul CV."
    abilitati_job = [s.strip().lower() for s in job["skills"].split(",")]
    abilitati_gasite = [s for s in habilitati_job if s in text_cv and s != ""] if 'habilitati_job' in locals() else [s for s in abilitati_job if s in text_cv and s != ""]
    procent += len(abilitati_gasite) * 20
    return min(max(procent, 25), 100), f"Scor: {procent}% compatibilitate. Abilități: {', '.join(abilitati_gasite)}."

def calculeaza_medie_companie(nume_companie):
    recenzii = [r for r in Baza_Recenzii_Companii if r["companie"].lower() == nume_companie.lower()]
    if not recenzii: return 0, 0
    medie_salariu = sum([r["note_salariu"] for r in recenzii]) / len(recenzii)
    medie_mgm = sum([r["note_management"] for r in recenzii]) / len(recenzii)
    return round((medie_salariu + medie_mgm) / 2, 1), len(recenzii)

@app.get("/", response_class=HTMLResponse)
async def pagina_principala_get(request: Request, q: str = "", locatie: str = "Bucuresti", tip: str = "Toate", lang: str = "ro", msg: str = "", page: int = 1):
    joburi_totale = cauta_joburi_externe(cuvant_cheie=q, locatie=locatie, tip_job=tip)
    ELEMENTE_PER_PAGINA = 15
    total_elemente = len(joburi_totale)
    total_pagini = math.ceil(total_elemente / ELEMENTE_PER_PAGINA)
    page = max(1, min(page, total_pagini if total_pagini > 0 else 1))
    start_idx = (page - 1) * ELEMENTE_PER_PAGINA
    end_idx = start_idx + ELEMENTE_PER_PAGINA
    joburi_paginate = joburi_totale[start_idx:end_idx]
    
    for job in joburi_paginate:
        medie, total = calculeaza_medie_companie(job["companie"])
        job["rating_mediu"] = medie
        job["total_recenzii"] = total
        job["match_score"] = 25
        job["match_reason"] = "Sistemul este pregătit. Încarcă fișierul CV."

    context = {"request": request, "joburi": joburi_paginate, "q": q, "locatie": locatie, "tip": tip, "lang": lang, "cv_incarcat": False, "msg": msg, "toate_recenziile": Baza_Recenzii_Companii, "current_page": page, "total_pages": total_pagini, "total_items": total_elemente}
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post("/", response_class=HTMLResponse)
async def pagina_principala_post(request: Request, q: str = Form(""), locatie: str = Form("Bucuresti"), tip: str = Form("Toate"), lang: str = Form("ro"), cv_file: UploadFile = File(None), page: int = 1):
    joburi_totale = cauta_joburi_externe(cuvant_cheie=q, locatie=locatie, tip_job=tip)
    text_cv = ""
    try:
        if cv_file and hasattr(cv_file, 'filename') and cv_file.filename:
            extensie = os.path.splitext(cv_file.filename).lower()
            continut_bytes = await cv_file.read()
            if continut_bytes: text_cv = extrage_text_din_cv_stream(continut_bytes, extensie)
    except Exception: pass

    for job in joburi_totale:
        medie, total = calculeaza_medie_companie(job["companie"])
        job["rating_mediu"] = medie
        job["total_recenzii"] = total
        procent, explicatie = calculeaza_compatibilitate_precisa(text_cv, job, lang)
        job["match_score"] = procent
        job["match_reason"] = explicatie

    if text_cv: joburi_totale = sorted(joburi_totale, key=lambda k: k["match_score"], reverse=True)

    ELEMENTE_PER_PAGINA = 15
    total_elemente = len(joburi_totale)
    total_pagini = math.ceil(total_elemente / ELEMENTE_PER_PAGINA)
    start_idx = (page - 1) * ELEMENTE_PER_PAGINA
    end_idx = start_idx + ELEMENTE_PER_PAGINA
    joburi_paginate = joburi_totale[start_idx:end_idx]

    context = {"request": request, "joburi": joburi_paginate, "q": q, "locatie": locatie, "tip": tip, "lang": lang, "cv_incarcat": bool(text_cv), "msg": "", "toate_recenziile": Baza_Recenzii_Companii, "current_page": page, "total_pages": total_pagini, "total_items": total_elemente}
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post("/adauga-recenzie-globala")
async def adauga_recenzie_globala(companie: str = Form(...), autor: str = Form(...), mail: str = Form(...), telefon: str = Form(...), note_salariu: int = Form(...), note_mgm: int = Form(...), comentariu: str = Form(...), q: str = Form(""), locatie: str = Form("Bucuresti")):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail) or not re.match(r"^[0-9]{10}$", telefon.strip()): return RedirectResponse(url=f"/?q={q}&locatie={locatie}&msg=invalid", status_code=303)
    Baza_Recenzii_Companii.insert(0, {"companie": companie.strip().capitalize(), "autor": autor.strip() if autor else "Anonim", "mail": mail, "telefon": telefon, "note_salariu": note_salariu, "note_management": note_mgm, "comentariu": comentariu.strip(), "data": "Azi"})
    return RedirectResponse(url=f"/?q={q}&locatie={locatie}&msg=success", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def pagina_admin(request: Request): return HTMLResponse("<h1>Admin Panel</h1>")
