aria-travel-ai-
Documentazione Tecnica: Aria Travel AI
Descrizione del Progetto
Aria Travel AI è un'applicazione web full-stack sviluppata con l'obiettivo di fornire un assistente virtuale intelligente per la pianificazione in ambito turistico. Il sistema è progettato per simulare un'interazione naturale e continuativa, supportando l'utente nella ricerca di voli, nella strutturazione di itinerari e nella stima dei budget. L'applicativo si fonda sull'integrazione di modelli di intelligenza artificiale generativa all'interno di un'architettura client-server reattiva e scalabile.

Architettura e Funzionalità
L'applicazione integra un sistema di autenticazione e gestione degli accessi, vincolando la registrazione a criteri di sicurezza specifici per la validazione delle password. Una volta effettuato l'accesso, ogni utente dispone di un'area di lavoro personale in cui i singoli "progetti di viaggio" sono archiviati in modo persistente.

Il cuore logico del sistema risiede nella gestione del modulo di chat. A differenza dei chatbot stateless tradizionali, l'architettura implementa una memoria contestuale (Context Memory): l'intera cronologia della conversazione viene immagazzinata ed elaborata a ogni iterazione, garantendo che l'intelligenza artificiale mantenga la coerenza logica e argomentativa senza necessitare di continue presentazioni.

Per l'interfaccia grafica, il sistema implementa una logica di rendering visivo dinamico. L'applicativo analizza le risposte dell'intelligenza artificiale estraendo specifiche entità geografiche attraverso l'uso di tag XML imposti via prompt. Qualora la destinazione rientri in un elenco di mete prestabilite, il sistema carica risorse fotografiche ad alta risoluzione in modo statico; in caso contrario, si interfaccia con API esterne per la generazione e il recupero in tempo reale di immagini pertinenti al contesto geografico richiesto.

Stack Tecnologico e Gestione dei Dati
L'infrastruttura di back-end è stata sviluppata in linguaggio Python 3. L'esposizione delle interfacce di programmazione (API) è gestita tramite il framework FastAPI, affiancato dal server ASGI Uvicorn, al fine di garantire l'elaborazione asincrona delle richieste HTTP. La validazione e la serializzazione dei dati in ingresso e in uscita sono affidate alla libreria Pydantic.

La persistenza dei dati è gestita tramite SQLite3, un database relazionale leggero che viene inizializzato automaticamente al primo avvio. Il database si articola in tre tabelle principali: una per la gestione delle credenziali degli utenti, una per il salvataggio dei progetti di viaggio e un'ultima dedicata all'archiviazione granulare dei messaggi, fondamentale per il ripristino delle sessioni di chat precedenti. Il front-end è stato realizzato utilizzando HTML5 e JavaScript (Vanilla), adottando il framework Tailwind CSS per l'implementazione di un'interfaccia utente moderna e completamente responsiva. Il motore di generazione dei testi si affida alle API di Google Gemini.

Istruzioni per l'Installazione e l'Esecuzione
Per testare e avviare l'applicazione in ambiente locale, è necessario disporre di un'installazione di Python 3.8 o superiore. Si richiede innanzitutto la clonazione del repository all'interno della propria macchina e la successiva installazione delle dipendenze necessarie.

Tramite l'interfaccia a riga di comando, eseguire: pip install fastapi uvicorn pydantic

Per ragioni di sicurezza legate alla gestione delle credenziali, la chiave API di Google Gemini non è stata inclusa nel codice sorgente. Prima dell'avvio, è strettamente necessario aprire il file HTML principale e inserire la propria chiave di autenticazione in corrispondenza della costante dedicata all'interno dello script JavaScript.

Una volta soddisfatti i prerequisiti, il server può essere inizializzato eseguendo il modulo principale: python app.py

L'applicativo sarà conseguentemente accessibile e operativo tramite qualsiasi browser web all'indirizzo di rete locale (localhost) sulla porta 8000.
