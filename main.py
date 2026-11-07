import os
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

# Dicționarul de traduceri pentru interfața JobiQ (Trilingv)
TRANSLATIONS = {
    'ro': {
        'title': "JobiQ - Motor Internațional de Căutare Locuri de Muncă",
        'search_btn': "Scanează Joburi",
        'placeholder_q': "Meserie (ex: Șofer, Casier, Mecanic)...",
        'placeholder_l': "Oraș (ex: Arad, Deva, Pitești) sau lasă gol...",
        'sub': "Scanează în timp real zeci de pagini de rezultate din platformele oficiale.",
        'click_to_see': "Apasă pe platforma dorită pentru a accesa TOATE joburile live (fără limită de pagini):",
        'results_for': "Rezultate pentru",
        'in': "în",
        'back': "← Înapoi la căutare"
    },
    'en': {
        'title': "JobiQ - Smart Search Engine for Live Jobs",
        'search_btn': "Scan Jobs",
        'placeholder_q': "Job title (ex: Driver, Cashier)...",
        'placeholder_l': "City or region (or leave empty)...",
        'sub': "Scans dozens of live result pages from official platforms in real time.",
        'click_to_see': "Click on your preferred platform to access ALL live jobs (unlimited pages):",
        'results_for': "Results for",
        'in': "in",
        'back': "← Back to search"
    },
    'hu': {
        'title': "JobiQ - Intelligens Álláskereső Keresőmotor",
        'search_btn': "Állások Szkennelése",
        'placeholder_q': "Szakma (pl: Sofőr, Pénztáros)...",
        'placeholder_l': "Város vagy régió (vagy hagyd üresen)...",
        'sub': "Valós időben pásztázza a hivatalos platformok álláshirdetéseit.",
        'click_to_see': "Kattintson a kívánt platformra az ÖSSZES élő állás megtekintéséhez (korlátlan oldal):",
        'results_for': "Találatok a következőre:",
        'in': "itt:",
        'back': "← Vissza a kereséshez"
    }
}

def genereaza_linkuri_realetime(q, l):
    q_curat = q.strip().lower() if q else ""
    l_curat = l.strip().lower() if l else ""
    
    q_encoded = urllib.parse.quote(q_curat)
    l_encoded = urllib.parse.quote(l_curat)
    
    # URL-urile oficiale care conțin TOATE paginile existente pe platforme
    url_olx = f"https://olx.ro{l_encoded}/q-{q_encoded}/" if l_curat else f"https://olx.roq-{q_encoded}/"
    url_ejobs = f"https://ejobs.ro{l_encoded}/{q_encoded}/" if l_curat else f"https://ejobs.ro{q_encoded}/"
    url_bestjobs = f"https://bestjobs.eu{q_encoded}&location={l_encoded}" if l_curat else f"https://bestjobs.eu{q_encoded}"
    url_publi24 = f"https://publi24.ro{l_encoded}/?q={q_encoded}" if l_curat else f"https://publi24.ro?q={q_encoded}"

    return [
        {"nume": "OLX Locuri de Muncă (Mii de anunțuri)", "url": url_olx, "desc": f"Deschide direct pe OLX absolut toate paginile cu rezultate reale."},
        {"nume": "eJobs România (Live)", "url": url_ejobs, "desc": f"Baza oficială eJobs în timp real, completă."},
        {"nume": "BestJobs Europe", "url": url_bestjobs, "desc": f"Toate pozițiile active disponibile din rețeaua BestJobs."},
        {"nume": "Publi24 Jobs", "url": url_publi24, "desc": f"Anunțuri directe de la angajatori, paginate integral."}
    ]

@app.route('/')
def home():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
        
    cuvant_cheie = request.args.get('q', '')
    locatie = request.args.get('l', '')
    
    if cuvant_cheie.strip() or locatie.strip():
        platforme = genereaza_linkuri_realetime(cuvant_cheie, locatie)
        return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=True, q=cuvant_cheie, l=locatie, platforme=platforme)
        
    return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
