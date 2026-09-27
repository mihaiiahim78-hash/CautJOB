import os
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

# Dicționarul de traduceri pentru cele 3 limbi (Interfață Internațională)
TRANSLATIONS = {
    'ro': {
        'title': "Caut Job - Motor Internațional de Căutare",
        'search_btn': "Caută Joburi",
        'placeholder_q': "Meserie sau cuvânt cheie (ex: Șofer, Programator)...",
        'placeholder_l': "Oraș sau Țară...",
        'sub': "Sistem centralizat de căutare globală în timp real.",
        'support': "☕ Îți place aplicația? Susține proiectul internațional!",
        'coffee': "Cumpără-mi o cafea ☕",
        'results_for': "Rezultate externe generate pentru",
        'in': "în",
        'click_to_see': "Apasă pe platforma dorită pentru a accesa instant toate joburile live:",
        'back': "← Înapoi",
        'all_platforms': "Toate platformele active"
    },
    'en': {
        'title': "Job Search - International Search Engine",
        'search_btn': "Search Jobs",
        'placeholder_q': "Job title or keyword (ex: Driver, Developer)...",
        'placeholder_l': "City or Country...",
        'sub': "Centralized global real-time search system.",
        'support': "☕ Like this app? Support this international project!",
        'coffee': "Buy me a coffee ☕",
        'results_for': "External results generated for",
        'in': "in",
        'click_to_see': "Click on your preferred platform to instantly access all live jobs:",
        'back': "← Back",
        'all_platforms': "All active platforms"
    },
    'hu': {
        'title': "Álláskereső - Nemzetközi Keresőmotor",
        'search_btn': "Állások Keresése",
        'placeholder_q': "Szakma vagy kulcsszó (pl: Sofőr, Programozó)...",
        'placeholder_l': "Város vagy Ország...",
        'sub': "Központosított globális valós idejű keresőrendszer.",
        'support': "☕ Tetszik az alkalmazás? Támogasd a nemzetközi projektet!",
        'coffee': "Vegyél nekem egy kávét ☕",
        'results_for': "Külső találatok generálva a következőre",
        'in': "itt:",
        'click_to_see': "Kattints a kívánt platformra az élő állások azonnali eléréséhez:",
        'back': "← Vissza",
        'all_platforms': "Minden aktív platform"
    }
}

def genereaza_linkuri_platforme(q, l):
    """Construiește URL-urile de căutare live pentru absolut toate joburile de pe platforme."""
    q_encoded = urllib.parse.quote(q.strip())
    l_encoded = urllib.parse.quote(l.strip())
    
    locatie_olx = l_encoded if l.strip() else ""
    
    return [
        {
            "nume": "OLX Jobs (România & Internațional)",
            "url": f"https://olx.ro{q_encoded}/" if not l.strip() else f"https://olx.ro{locatie_olx}/q-{q_encoded}/",
            "desc": "Accesează baza completă de joburi operaționale, șoferi, retail și servicii."
        },
        {
            "nume": "eJobs (Național & Remote)",
            "url": f"https://ejobs.ro{q_encoded}/" if not l.strip() else f"https://ejobs.ro{l_encoded}/{q_encoded}/",
            "desc": "Toate pozițiile de specialiști, management și joburi de birou active."
        },
        {
            "nume": "BestJobs (European & Global)",
            "url": f"https://bestjobs.eu{q_encoded}" if not l.strip() else f"https://bestjobs.eu{q_encoded}&location={l_encoded}",
            "desc": "Locuri de muncă în corporații internaționale și oportunități în Uniunea Europeană."
        },
        {
            "nume": "EuroJobs (Aplicație Internațională)",
            "url": f"https://eurojobs.com{q_encoded}",
            "desc": "Platformă globală dedicată joburilor transfrontaliere în toată Europa și SUA."
        },
        {
            "nume": "LinkedIn Job Search",
            "url": f"https://linkedin.com{q_encoded}&location={l_encoded if l.strip() else 'Worldwide'}",
            "desc": "Cea mai mare rețea profesională din lume pentru joburi tech și corporații."
        },
        {
            "nume": "Jooble (Agregator Global de Joburi)",
            "url": f"https://jooble.org{q_encoded}" if not l.strip() else f"https://jooble.org{q_encoded}&rgn={l_encoded}",
            "desc": "Agreghează în timp real absolut toate anunțurile de pe site-urile de recrutare mici."
        }
    ]

@app.route('/')
def home():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
    return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")

@app.route('/cauta')
def cauta():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
        
    cuvant_cheie = request.args.get('q', '')
    locatie = request.args.get('l', '')
    
    if not cuvant_cheie.strip():
        return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")
        
    platforme = genereaza_linkuri_platforme(cuvant_cheie, locatie)
    
    return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=True, q=cuvant_cheie, l=locatie, platforme=platforme)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
