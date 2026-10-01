import os
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

# Dicționarul de traduceri (Interfață Internațională)
TRANSLATIONS = {
    'ro': {
        'title': "Caut Job - Motor Internațional de Căutare",
        'search_btn': "Caută Joburi",
        'placeholder_q': "Meserie sau cuvânt cheie (ex: Șofer, Casier)...",
        'placeholder_l': "Oraș sau Țară (ex: Arad, Timișoara)...",
        'sub': "Sistem centralizat de căutare globală în timp real.",
        'unlock_title': "🔓 Deblochează Toate Rezultatele Reale (Zeci de Pagini)",
        'unlock_desc': "Plătește o singură dată 2 LEI pentru a accesa instant absolut toate locurile de muncă live din baza de date a celor mai mari platforme.",
        'pay_btn': "💳 Plătește 2 LEI cu Card / Google Pay",
        'click_to_see': "Apasă pe platforma dorită pentru a accesa instant toate joburile live:",
        'results_for': "Rezultate generate pentru",
        'in': "în",
        'back': "← Înapoi"
    },
    'en': {
        'title': "Job Search - International Search Engine",
        'search_btn': "Search Jobs",
        'placeholder_q': "Job title or keyword (ex: Driver, Accountant)...",
        'placeholder_l': "City or Country...",
        'sub': "Centralized global real-time search system.",
        'unlock_title': "🔓 Unlock All Real Results (Dozens of Pages)",
        'unlock_desc': "Pay once 2 RON (approx. 0.40 EUR) to instantly access absolutely all live jobs from the biggest platforms.",
        'pay_btn': "💳 Secure Pay with Card / Google Pay",
        'click_to_see': "Click on your preferred platform to instantly access all live jobs:",
        'results_for': "Results generated for",
        'in': "in",
        'back': "← Back"
    },
    'hu': {
        'title': "Álláskereső - Nemzetközi Keresőmotor",
        'search_btn': "Állások Keresése",
        'placeholder_q': "Szakma vagy kulcsszó (pl: Sofőr, Pénztáros)...",
        'placeholder_l': "Város vagy Ország...",
        'sub': "Központosított globális valós idejű keresőrendszer.",
        'unlock_title': "🔓 Minden Valós Találat Feloldása (Több Oldal)",
        'unlock_desc': "Fizessen egyszer 2 RON-t az összes élő állás azonnali eléréséhez a legnagyobb platformokról.",
        'pay_btn': "💳 Biztonságos Fizetés Kártyával",
        'click_to_see': "Kattints a kívánt platformra az élő állások azonnali eléréséhez:",
        'results_for': "Találatok a következőre:",
        'in': "itt:",
        'back': "← Vissza"
    }
}

def genereaza_linkuri_platforme(q, l):
    """Construiește URL-urile reale de căutare dinamică."""
    q_curat = q.strip().lower()
    l_curat = l.strip().lower()
    
    # Encodare pentru URL (înlocuiește spațiile cu caractere speciale de link)
    q_encoded = urllib.parse.quote(q_curat)
    l_encoded = urllib.parse.quote(l_curat)
    
    # 1. Logică OLX
    if l_curat:
        url_olx = f"https://olx.ro{l_encoded}/q-{q_encoded}/"
    else:
        url_olx = f"https://olx.roq-{q_encoded}/"
        
    # 2. Logică eJobs
    if l_curat:
        url_ejobs = f"https://ejobs.ro{l_encoded}/{q_encoded}/"
    else:
        url_ejobs = f"https://ejobs.ro{q_encoded}/"
        
    # 3. Logică BestJobs
    if l_curat:
        url_bestjobs = f"https://bestjobs.eu{q_encoded}&location={l_encoded}"
    else:
        url_bestjobs = f"https://bestjobs.eu{q_encoded}"
        
    # 4. Logică Publi24
    if l_curat:
        url_publi24 = f"https://publi24.ro{l_encoded}/?q={q_encoded}"
    else:
        url_publi24 = f"https://publi24.ro?q={q_encoded}"

    return [
        {"nume": "OLX Locuri de Muncă", "url": url_olx, "desc": f"Toate anunțurile live de pe OLX pentru {q} în {l if l else 'Toată România'} (Zeci de pagini reale)."},
        {"nume": "eJobs România", "url": url_ejobs, "desc": f"Poziții active, salarii transparente și companii de top care angajează în {l if l else 'România'}."},
        {"nume": "BestJobs", "url": url_bestjobs, "desc": f"Locuri de muncă din toate domeniile disponibile acum în {l if l else 'țară'}."},
        {"nume": "Publi24 - Locuri de Muncă", "url": url_publi24, "desc": f"Anunțuri directe de la angajatori locali, fără intermediari, în {l if l else 'România'}."}
    ]

@app.route('/')
def home():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
        
    cuvant_cheie = request.args.get('q', '')
    locatie = request.args.get('l', '')
    
    # Dacă utilizatorul a completat căutarea
    if cuvant_cheie.strip():
        platforme = genereaza_linkuri_platforme(cuvant_cheie, locatie)
        return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=True, q=cuvant_cheie, l=locatie, platforme=platforme)
        
    return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
