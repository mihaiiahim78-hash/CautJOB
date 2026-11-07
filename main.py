import os
import urllib.parse
from flask import Flask, request, render_template_string

app = Flask(__name__)

TRANSLATIONS = {
    'ro': {
        'title': "JobiQ - Motor Inteligent de Căutare",
        'search_btn': "Scanează Joburi",
        'placeholder_q': "Meserie (ex: Șofer, Casier, Mecanic)...",
        'placeholder_l': "Oraș (ex: Arad, Orșova, Pitești) sau lasă gol...",
        'sub': "Aplicație inteligentă care agreghează mii de rezultate reale.",
        'click_to_see': "Apasă pe platforma dorită pentru a deschide toate paginile cu joburi reale:",
        'results_for': "Rezultate pentru",
        'in': "în",
        'back': "← Înapoi la căutare"
    },
    'en': {
        'title': "JobiQ - Smart Search Engine for Live Jobs",
        'search_btn': "Scan Jobs",
        'placeholder_q': "Job title (ex: Driver, Cashier)...",
        'placeholder_l': "City or region...",
        'sub': "Smart application aggregating thousands of live result pages.",
        'click_to_see': "Click on your preferred platform to open all real job pages:",
        'results_for': "Results for",
        'in': "in",
        'back': "← Back to search"
    },
    'hu': {
        'title': "JobiQ - Intelligens Álláskereső Keresőmotor",
        'search_btn': "Állások Szkennelése",
        'placeholder_q': "Szakma (pl: Sofőr, Pénztáros)...",
        'placeholder_l': "Város vagy régió...",
        'sub': "Intelligens alkalmazás, amely több tucat élő találati oldalt gyűjt össze.",
        'unlock_title': "🔓 Valós Találatok Feloldása Minden Platformról",
        'click_to_see': "Kattintson a kívánt platformra a valós állások megtekintéséhez:",
        'results_for': "Találatok a következőre:",
        'in': "itt:",
        'back': "← Vissza a kereséshez"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 750px; margin: 0 auto; background: white; padding: 35px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
        .lang-picker { text-align: right; margin-bottom: 20px; }
        .lang-btn { background: #e2e8f0; color: #4a5568; border: none; padding: 6px 12px; margin-left: 5px; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: bold; }
        .lang-btn.active { background: #3182ce; color: white; }
        h1 { color: #2d3748; text-align: center; margin-bottom: 5px; }
        .sub-text { text-align: center; color: #718096; margin-bottom: 30px; font-size: 15px; }
        .search-box { display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px; }
        input, button { padding: 14px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 16px; }
        input:focus { outline: none; border-color: #3182ce; box-shadow: 0 0 0 3px rgba(66,153,225,0.5); }
        button { background-color: #3182ce; color: white; border: none; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background-color: #2b6cb0; }
        .platform-card { background: #fff; border: 1px solid #e2e8f0; border-left: 6px solid #3182ce; padding: 20px; margin-bottom: 15px; border-radius: 4px; text-align: left; }
        .platform-name { font-size: 18px; font-weight: bold; color: #2d3748; }
        .platform-desc { font-size: 14px; color: #4a5568; margin: 8px 0 12px 0; }
        .apply-btn { display: inline-block; padding: 12px 24px; background: #3182ce; color: white; text-decoration: none; border-radius: 4px; font-size: 15px; font-weight: bold; text-align: center; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #3182ce; text-decoration: none; font-weight: bold; }
        @media(min-width: 480px) { .search-box { flex-direction: row; } input { flex: 2; } button { flex: 1; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="lang-picker">
            <a href="?lang=ro{% if cautat %}&q={{ q }}&l={{ l }}{% endif %}" class="lang-btn {% if lang == 'ro' %}active{% endif %}">RO</a>
            <a href="?lang=en{% if cautat %}&q={{ q }}&l={{ l }}{% endif %}" class="lang-btn {% if lang == 'en' %}active{% endif %}">EN</a>
            <a href="?lang=hu{% if cautat %}&q={{ q }}&l={{ l }}{% endif %}" class="lang-btn {% if lang == 'hu' %}active{% endif %}">HU</a>
        </div>

        {% if cautat %}
            <a href="/?lang={{ lang }}" class="back-link">{{ t.back }}</a>
            <h1>{{ t.results_for }} "{{ q if q else 'Toate joburile' }}" {{ t.in }} {{ l if l else "România" }}</h1>
            <p class="sub-text" style="text-align: left; font-weight: bold; margin-top: 20px;">{{ t.click_to_see }}</p>

            <div style="margin-top: 15px;">
                {% for p in platforme %}
                    <div class="platform-card">
                        <div class="platform-name">{{ p.nume }}</div>
                        <div class="platform-desc">{{ p.desc }}</div>
                        <a href="{{ p.url }}" rel="external" target="_system" class="apply-btn">Deschide Anunțurile Reale →</a>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <h1>{{ t.title }}</h1>
            <p class="sub-text">{{ t.sub }}</p>
            
            <form action="/" method="GET" class="search-box">
                <input type="hidden" name="lang" value="{{ lang }}">
                <input type="text" name="q" value="{{ q }}" placeholder="{{ t.placeholder_q }}">
                <input type="text" name="l" value="{{ l }}" placeholder="{{ t.placeholder_l }}">
                <button type="submit">{{ t.search_btn }}</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

def genereaza_linkuri_realetime(q, l):
    q_curat = str(q).strip().lower() if q else ""
    l_curat = str(l).strip().lower() if l else ""
    
    q_encoded = urllib.parse.quote(q_curat)
    l_encoded = urllib.parse.quote(l_curat)
    
    # STRUCTURA REPARATĂ: Adăugat explicit '/' după domeniu pentru a preveni lipirea cuvintelor
    if l_curat:
        url_olx = f"https://olx.ro{l_encoded}/q-{q_encoded}/"
        url_ejobs = f"https://ejobs.ro{l_encoded}/{q_encoded}/"
        url_bestjobs = f"https://bestjobs.eu{q_encoded}&location={l_encoded}"
        url_publi24 = f"https://publi24.ro{l_encoded}/?q={q_encoded}"
    else:
        url_olx = f"https://olx.roq-{q_encoded}/"
        url_ejobs = f"https://ejobs.ro{q_encoded}/"
        url_bestjobs = f"https://bestjobs.eu{q_encoded}"
        url_publi24 = f"https://publi24.ro?q={q_encoded}"

    return [
        {"nume": "OLX Locuri de Muncă (Toate Paginile)", "url": url_olx, "desc": "Deschide direct pe OLX zecile de pagini cu anunțuri reale."},
        {"nume": "eJobs România (Live)", "url": url_ejobs, "desc": "Baza completă de date eJobs sortată instant."},
        {"nume": "BestJobs", "url": url_bestjobs, "desc": "Anunțuri de angajare în timp real din rețeaua BestJobs."},
        {"nume": "Publi24 Jobs", "url": url_publi24, "desc": "Locuri de muncă adăugate direct de angajatori."}
    ]

@app.route('/')
def home():
    lang = request.args.get('lang', 'ro')
    if lang not in TRANSLATIONS:
        lang = 'ro'
        
    cuvant_cheie = request.args.get('q', '')
    locatie = request.args.get('l', '')
    
    if 'q' in request.args or 'l' in request.args:
        platforme = genereaza_linkuri_realetime(cuvant_cheie, locatie)
        return render_template_string(HTML_TEMPLATE, t=TRANSLATIONS[lang], lang=lang, cautat=True, q=cuvant_cheie, l=locatie, platforme=platforme)
        
    return render_template_string(HTML_TEMPLATE, t=TRANSLATIONS[lang], lang=lang, cautat=False, q="", l="")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
