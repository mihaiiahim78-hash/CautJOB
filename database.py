import sqlite3

DB_NAME = "cautjob_nou.db"

def initializeaza_baza_de_date():
    """Creează tabelul de joburi adaptat cu noua coloană de sursă globală."""
    conexiune = sqlite3.connect(DB_NAME)
    cursor = conexiune.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS joburi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT NOT NULL,
            companie TEXT,
            locatie TEXT,
            job_type TEXT,
            skills TEXT,
            description TEXT,
            published_at TEXT,
            is_verified INTEGER DEFAULT 0,
            salary INTEGER,
            sursa TEXT,
            cheie_unica TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recenzii (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            companie TEXT NOT NULL,
            comentariu TEXT NOT NULL,
            autor TEXT DEFAULT 'Anonim',
            status TEXT DEFAULT 'Aprobat'
        )
    """)
    
    conexiune.commit()
    conexiune.close()

def salveaza_joburi_in_tabel(lista_joburi):
    """Salvează joburile în siguranță."""
    conexiune = sqlite3.connect(DB_NAME)
    cursor = conexiune.cursor()
    
    numar_salvate = 0
    for j in lista_joburi:
        cheie = f"{j['companie'].lower()}_{j['titlu'].lower()[:12]}_{j['location'].lower()}".replace(" ", "")
        try:
            cursor.execute("""
                INSERT INTO joburi (titlu, companie, locatie, job_type, skills, description, published_at, is_verified, salary, sursa, cheie_unica)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                j['titlu'], j['companie'], j['location'], j['job_type'], 
                j['skills'], j['description'], j['published_at'], 
                j['is_verified'], j['salary'], j.get('sursa', 'Web'), cheie
            ))
            numar_salvate += 1
        except sqlite3.IntegrityError:
            continue
            
    conexiune.commit()
    conexiune.close()
    return numar_salvate

def extrage_toate_joburile(cuvant_cheie="", locatie="Toate", tip_job="Toate"):
    """Extrage joburile ca dicționare perfect curate pentru interfață."""
    conexiune = sqlite3.connect(DB_NAME)
    conexiune.row_factory = sqlite3.Row
    cursor = conexiune.cursor()
    
    interogare = "SELECT titlu, companie, locatie, job_type, skills, description, published_at, is_verified, salary, sursa FROM joburi WHERE 1=1"
    parametrii = []
    
    if cuvant_cheie and cuvant_cheie.lower() not in ["manager", "sofer", "general"]:
        interogare += " AND (titlu LIKE ? OR description LIKE ?)"
        parametrii.extend([f"%{cuvant_cheie}%", f"%{cuvant_cheie}%"])
        
    if locatie != "Toate" and locatie.strip() != "":
        interogare += " AND locatie LIKE ?"
        parametrii.append(f"%{locatie}%")
        
    if tip_job != "Toate":
        interogare += " AND job_type = ?"
        parametrii.append(tip_job)
        
    interogare += " ORDER BY id DESC"
    
    cursor.execute(interogare, parametrii)
    randuri = cursor.fetchall()
    conexiune.close()
    
    rezultate = []
    for r in randuri:
        rezultate.append({
            "titlu": r["titlu"], 
            "companie": r["companie"], 
            "location": r["locatie"],
            "job_type": r["job_type"], 
            "skills": r["skills"], 
            "description": r["description"], 
            "published_at": r["published_at"], 
            "is_verified": r["is_verified"], 
            "salary": r["salary"], 
            "sursa": r["sursa"]
        })
    return rezultate

def extrage_recenzii_admin():
    conexiune = sqlite3.connect(DB_NAME)
    conexiune.row_factory = sqlite3.Row
    cursor = conexiune.cursor()
    cursor.execute("SELECT id, companie, comentariu, autor, status FROM recenzii")
    randuri = cursor.fetchall()
    conexiune.close()
    return [dict(r) for r in randuri]

def schimba_status_recenzie(recenzie_id, noul_status):
    conexiune = sqlite3.connect(DB_NAME)
    cursor = conexiune.cursor()
    cursor.execute("UPDATE recenzii SET status = ? WHERE id = ?", (noul_status, recenzie_id))
    conexiune.commit()
    conexiune.close()

def sterge_recenzie_baza(recenzie_id):
    conexiune = sqlite3.connect(DB_NAME)
    cursor = conexiune.cursor()
    cursor.execute("DELETE FROM recenzii WHERE id = ?", (recenzie_id,))
    conexiune.commit()
    conexiune.close()
