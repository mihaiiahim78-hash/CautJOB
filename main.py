import os
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

# Dicționarul de traduceri oficial pentru JobiQ (Trilingv)
TRANSLATIONS = {
    'ro': {
        'title': "JobiQ - Motor Inteligent de Căutare Locuri de Muncă",
        'search_btn': "Scanează Joburi",
        'placeholder_q': "Meserie (ex: Șofer, Casier, Mecanic)...",
        'placeholder_l': "Oraș (ex: Arad, Deva, Pitești) sau lasă gol...",
        'sub': "Aplicație inteligentă care agreghează mii de rezultate reale.",
        'unlock_title': "🔓 Accesează Rezultatele Reale din Toate Platformele",
        'unlock_desc': "Plătește o singură dată 2 LEI pentru a debloca accesul instant la zeci de pagini live din surse oficiale (OLX, eJobs, BestJobs, Publi24).",
        'pay_btn': "💳 Plătește 2 LEI și Vezi Joburile",
        'click_to_see': "Apasă pe platforma dorită pentru a deschide toate paginile cu joburi reale:",
        'back': "← Înapoi la căutare"
    },
    'en': {
        'title': "JobiQ - Smart Search Engine for Live Jobs",
        'search_btn': "Scan Jobs",
        'placeholder_q': "Job title (ex: Driver, Cashier, Mechanic)...",
        'placeholder_l': "City or leave empty for all country...",
        'sub': "Smart application aggregating thousands of live result pages.",
        'unlock_title': "🔓 Access Real Results From All Platforms",
        'unlock_desc': "Pay once 2 RON to instantly unlock access to thousands of live ads from official sources.",
        'pay_btn': "💳 Pay 2 RON & View Jobs",
        'click_to_see': "Click on your preferred platform to open all real job pages:",
        'back': "← Back to search"
    },
    'hu': {
        'title': "JobiQ - Intelligens Álláskereső Keresőmotor",
        'search_btn': "Állások Szkennelése",
        'placeholder_q': "Szakma (pl: Sofőr, Pénztáros)...",
        'placeholder_l': "Város vagy hagyd üresen...",
        'sub': "Intelligens alkalmazás, amely több tucat élő találati oldalt gyűjt össze.",
        'unlock_title': "🔓 Valós Találatok Feloldása Minden Platformról",
        'unlock_desc': "Fizessen egyszer 2 RON-t a hivatalos forrásokból származó élő hirdetések azonnali eléréséhez.",
        'pay_btn': "💳 Fizessen 2 RON-t az Állásokért",
        'click_to_see': "Kattintson a kívánt platformra a valós állások megtekintéséhez:",
        'back': "← Vissza a kereséshez"
    }
}

def genereaza_linkuri_realetime(q, l):
    """Construiește URL-urile exacte de căutare dinamică."""
    q_curat = q.strip().lower()
    l_curat = l.strip().lower()
    
    q_encoded = urllib.parse.quote(q_curat)
    l_encoded = urllib.parse.quote(l_curat)
    
    url_olx = f"https://olx.ro{l_encoded}/q-{q_encoded}/" if l_curat else f"https://olx.roq-{q_encoded}/"
    url_ejobs = f"https://ejobs.ro{l_encoded}/{q_encoded}/" if l_curat else f"https://ejobs.ro{q_encoded}/"
    url_bestjobs = f"https://bestjobs.eu{q_encoded}&location={l_encoded}" if l_curat else f"https://bestjobs.eu{q_encoded}"
    url_publi24 = f"https://publi24.ro{l_encoded}/?q={q_encoded}" if l_curat else f"https://publi24.ro?q={q_encoded}"

    return [
        {"nume": "OLX Locuri de Muncă (Toate Paginile)", "url": url_olx, "desc": f"Deschide direct pe OLX zecile de pagini cu anunțuri de {q if q else 'orice job'} în {l if l else 'Toată România'}."},
        {"nume": "eJobs România (Live)", "url": url_ejobs, "desc": f"Baza completă de date eJobs sortată pentru {q if q else 'toate domeniile'} în {l if l else 'toată țara'}."},
        {"nume": "BestJobs", "url": url_bestjobs, "desc": f"Anunțuri de angajare în timp real din rețeaua BestJobs în {l if l else 'România'}."},
        {"nume": "Publi24 Jobs", "url": url_publi24, "desc": f"Locuri de muncă adăugate direct de angajatori din zona {l if l else 'României'}."}
    ]

@app.route('/')
def home():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
        
    cuvant_cheie = request.args.get('q', '')
    locatie = request.args.get('l', '')
    
    # Rulăm dacă utilizatorul a introdus MĂCAR una din opțiuni (job sau oraș)
    if cuvant_cheie.strip() or locatie.strip():
        platforme = genereaza_linkuri_realetime(cuvant_cheie, locatie)
        return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=True, q=cuvant_cheie, l=locatie, platforme=platforme)
        
    return render_template('index.html', t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
