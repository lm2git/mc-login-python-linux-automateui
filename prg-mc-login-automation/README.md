# mc-login.py

## Descrizione

`mc-login.py` è un semplice script Python progettato per monitorare i file di log di Minecraft che è in esecuzione su ubuntu  e automatizzare la procedura di autenticazione nel gioco. (che prevede autenticazione secondo quanto descritto nel plugin -> https://www.spigotmc.org/resources/authmereloaded.6269/ 
Quando il server richiede l'autenticazione con il comando `/login`, lo script dopo qualche secondo rileva la richiesta, massimizza la finestra di gioco, apre la chat e inserisce automaticamente il comando per autenticarsi.

---

## Requisiti

- **Sistema operativo**: Linux Ubuntu (richiede il comando `wmctrl` per la gestione delle finestre)
- **Python**: Versione 3.7 o successiva
- **Dipendenze aggiuntive**:
  - `pyautogui` per il controllo del mouse e della tastiera

Per installare le dipendenze creato uno script apposito da lanciare solo la prima volta, esegui:

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

---

## Installazione

1. Clona o scarica questo repository.
2. Assicurarsi di avviare Minecraft e  lasciare che la finestra di minecraft sia in primo piano (non in pausa!) sulla schermata di login 

---

## Configurazione e personalizzazioni 

1. Personalizza il comando di login nella funzione `perform_additional_actions`. Lo script usa il comando:
   ```
   /login Poppi1971
   ```
   Cambia `Poppi1971` con la tua password o un valore appropriato.

---

## Utilizzo

Esegui lo script dalla riga di comando e lasciare il terminale attivo:

```bash
python3 mc-login.py
```

Lasciare la finestra di minecraft in primo piano (non in pausa)

Lo script:

1. Monitorerà il file `latest.log` per rilevare eventuali richieste di login.
2. Se il gioco non è in pausa e nella schermata iniziale in cui viene indicato il messaggio "Per favore, esegui l'autenticazione con il comando: /login"  Metterà a fuoco e massimizzerà la finestra di Minecraft.
3. Inserirà automaticamente il comando di login e completerà altre azioni specifiche.

---

## Debugging

I messaggi di log vengono salvati nel file `disconnections.log`. Puoi utilizzarli per diagnosticare eventuali problemi. Ogni messaggio include:

- Timestamp
- Livello del log (INFO, SUCCESS, ERROR)
- Descrizione dell'evento

---

## Limitazioni e Note 

- Lo script è progettato per ambienti Linux e potrebbe non funzionare correttamente su altri sistemi operativi.
- Lo script dipende dal nome della finestra di Minecraft. Assicurati che contenga la parola "Minecraft" e una volta avviato su un terminale lasciar e la finestra di gioco non in pausa (non viene gestito il caso in cui la finestra si trova in una schermata diversa da quella in cui viene richiesto "Per favore, esegui l'autenticazione con il comando: /login" )
- Lo script assume come fatto che eventuali mod di autoreconnect portano il gioco nella schermata in cui viene richiesto  "Per favore, esegui l'autenticazione con il comando: /login" 
- Lo script potrebbe ulteriormente essere migliorato per gestire fasi e situazioni particolari con controlli di robustezza e  ulteriori implementazioni  (che vanno fuori dallo scope del flusso concordato in questo script)
---




