from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import sqlite3
import uvicorn
import re 

app = FastAPI()

def prepara_database():
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute('''CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, email TEXT, password TEXT NOT NULL)''')
    cursore.execute('''CREATE TABLE IF NOT EXISTS viaggi (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, destinazione TEXT NOT NULL)''')
    cursore.execute('''CREATE TABLE IF NOT EXISTS messaggi (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, destinazione TEXT NOT NULL, mittente TEXT NOT NULL, testo TEXT NOT NULL)''')
    connessione.commit()
    connessione.close()

prepara_database()

# --- MODELLI DATI ---
class UtenteReg(BaseModel):
    username: str
    email: str
    password: str

class UtenteLog(BaseModel):
    username: str
    password: str

class Viaggio(BaseModel):
    username: str
    destinazione: str

class Messaggio(BaseModel):
    username: str
    destinazione: str
    mittente: str
    testo: str

class RinominaRequest(BaseModel):
    username: str
    vecchio_nome: str
    nuovo_nome: str

# MODELLO AGGIUNTO: Per l'eliminazione
class EliminaRequest(BaseModel):
    username: str
    destinazione: str

# --- API ---
@app.get("/")
async def carica_sito():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/registrati")
async def registrati(utente: UtenteReg):
    if len(utente.password) < 8 or not re.search(r'[A-Z]', utente.password):
        raise HTTPException(status_code=400, detail="La password deve avere almeno 8 caratteri e contenere almeno una lettera maiuscola.")
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    try:
        cursore.execute("INSERT INTO utenti (username, email, password) VALUES (?, ?, ?)", (utente.username, utente.email, utente.password))
        connessione.commit()
        return {"messaggio": "Account creato con successo!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username già in uso.")
    finally:
        connessione.close()

@app.post("/api/login")
async def login(utente: UtenteLog):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute("SELECT * FROM utenti WHERE username=? AND password=?", (utente.username, utente.password))
    user_trovato = cursore.fetchone()
    connessione.close()
    if user_trovato:
        return {"messaggio": "Login approvato!"}
    else:
        raise HTTPException(status_code=401, detail="Username o Password errati.")

@app.post("/api/salva_viaggio")
async def salva_viaggio(viaggio: Viaggio):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute("SELECT * FROM viaggi WHERE username=? AND destinazione=?", (viaggio.username, viaggio.destinazione))
    if not cursore.fetchone():
        cursore.execute("INSERT INTO viaggi (username, destinazione) VALUES (?, ?)", (viaggio.username, viaggio.destinazione))
        connessione.commit()
    connessione.close()
    return {"status": "ok"}

@app.get("/api/miei_viaggi/{username}")
async def miei_viaggi(username: str):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute("SELECT destinazione FROM viaggi WHERE username=?", (username,))
    viaggi = [row[0] for row in cursore.fetchall()]
    connessione.close()
    return {"viaggi": viaggi}

@app.post("/api/salva_messaggio")
async def salva_messaggio(msg: Messaggio):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute("INSERT INTO messaggi (username, destinazione, mittente, testo) VALUES (?, ?, ?, ?)", 
                    (msg.username, msg.destinazione, msg.mittente, msg.testo))
    connessione.commit()
    connessione.close()
    return {"status": "ok"}

@app.get("/api/cronologia_chat/{username}/{destinazione}")
async def cronologia_chat(username: str, destinazione: str):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    cursore.execute("SELECT mittente, testo FROM messaggi WHERE username=? AND destinazione=? ORDER BY id ASC", (username, destinazione))
    messaggi = [{"mittente": row[0], "testo": row[1]} for row in cursore.fetchall()]
    connessione.close()
    return {"messaggi": messaggi}

@app.post("/api/rinomina_viaggio")
async def rinomina_viaggio(rinomina: RinominaRequest):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    try:
        cursore.execute("SELECT * FROM viaggi WHERE username=? AND destinazione=?", (rinomina.username, rinomina.nuovo_nome))
        if cursore.fetchone():
            raise HTTPException(status_code=400, detail="Esiste già un viaggio con questo nome.")
        cursore.execute("UPDATE viaggi SET destinazione=? WHERE username=? AND destinazione=?", (rinomina.nuovo_nome, rinomina.username, rinomina.vecchio_nome))
        cursore.execute("UPDATE messaggi SET destinazione=? WHERE username=? AND destinazione=?", (rinomina.nuovo_nome, rinomina.username, rinomina.vecchio_nome))
        connessione.commit()
        return {"messaggio": "Viaggio rinominato."}
    except Exception as e:
        connessione.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connessione.close()

# NUOVA API: Elimina Viaggio
@app.post("/api/elimina_viaggio")
async def elimina_viaggio(req: EliminaRequest):
    connessione = sqlite3.connect('aria_travel.db')
    cursore = connessione.cursor()
    try:
        cursore.execute("DELETE FROM viaggi WHERE username=? AND destinazione=?", (req.username, req.destinazione))
        cursore.execute("DELETE FROM messaggi WHERE username=? AND destinazione=?", (req.username, req.destinazione))
        connessione.commit()
        return {"messaggio": "Viaggio eliminato."}
    except Exception as e:
        connessione.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connessione.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)