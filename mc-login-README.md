# mc-login.py

## Descrizione

`mc-login.py` è uno script Python progettato per monitorare i file di log di Minecraft e automatizzare la procedura di autenticazione nel gioco. Quando il server richiede l'autenticazione con il comando `/login`, lo script rileva la richiesta, mette a fuoco la finestra di gioco, apre la chat e inserisce automaticamente il comando per autenticarsi.

---

## Requisiti

- **Sistema operativo**: Linux (richiede il comando `wmctrl` per la gestione delle finestre)
- **Python**: Versione 3.7 o successiva
- **Dipendenze aggiuntive**:
  - `pyautogui` per il controllo del mouse e della tastiera

Per installare le dipendenze, esegui:

```bash
pip install pyautogui
```

---

## Installazione

1. Clona o scarica questo repository.
2. Assicurati che il comando `wmctrl` sia installato sul tuo sistema. Puoi installarlo con il seguente comando:
   ```bash
   sudo apt-get install wmctrl
   ```
3. Verifica che il percorso dei file di log di Minecraft sia corretto. Lo script assume che i log si trovino nella directory `~/.minecraft/logs/latest.log`.

---

## Configurazione

1. Modifica la variabile `debug_log_path` per specificare il percorso del file di debug, se necessario.
2. Personalizza il comando di login nella funzione `perform_additional_actions`. Lo script usa il comando:
   ```
   /login Poppi1971
   ```
   Cambia `Poppi1971` con la tua password o un valore appropriato.

---

## Utilizzo

Esegui lo script dalla riga di comando:

```bash
python3 mc-login.py
```

Lo script:

1. Monitorerà il file `latest.log` per rilevare eventuali richieste di login.
2. Metterà a fuoco e massimizzerà la finestra di Minecraft.
3. Inserirà automaticamente il comando di login e completerà altre azioni specifiche.

---

## Debugging

I messaggi di log vengono salvati nel file `disconnections.log`. Puoi utilizzarli per diagnosticare eventuali problemi. Ogni messaggio include:

- Timestamp
- Livello del log (INFO, SUCCESS, ERROR)
- Descrizione dell'evento

---

## Limitazioni

- Lo script è progettato per ambienti Linux e potrebbe non funzionare correttamente su altri sistemi operativi.
- Lo script dipende dal nome della finestra di Minecraft. Assicurati che contenga la parola "Minecraft".
- Non è consigliabile includere una password direttamente nel codice per motivi di sicurezza.

---

## Contributi

Contributi e miglioramenti sono benvenuti! Invia una pull request o apri un'issue per segnalare problemi o suggerire nuove funzionalità.

---

## Note Legali

L'utilizzo di questo script deve essere conforme ai termini di servizio del server Minecraft su cui viene utilizzato. L'autore declina ogni responsabilità per eventuali violazioni o danni causati dall'uso dello script.

per quanto riguarda i prerequisiti genera uno script apposito che installa tutto quello che serve per far girare tutto python incluso e rigenera la doc 

