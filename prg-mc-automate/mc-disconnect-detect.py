import time
import os
from datetime import datetime

# Ottieni il nome dell'utente corrente
user_home = os.path.expanduser("~")

# Path al file latest.log
log_file_path = os.path.join(user_home, ".minecraft", "logs", "latest.log")

# Path al file di debug
debug_log_path = "disconnections.log"

def log_debug_message(message):
    """Scrive un messaggio con timestamp su disconnections.log"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(debug_log_path, "a") as debug_log:
        debug_log.write(f"{timestamp} {message}\n")

def monitor_log_file():
    try:
        # Verifica se il file esiste prima di tentare di aprirlo
        if not os.path.exists(log_file_path):
            log_debug_message(f"File non trovato: {log_file_path}")
            return
        
        last_file_size = os.path.getsize(log_file_path)  # Ottieni la dimensione iniziale del file

        while True:
            # Ottieni la dimensione attuale del file
            current_file_size = os.path.getsize(log_file_path)

            # Se la dimensione del file è cambiata, leggi le nuove righe
            if current_file_size != last_file_size:
                with open(log_file_path, "r") as log_file:
                    log_file.seek(last_file_size)  # Vai alla posizione dell'ultima lettura
                    new_lines = log_file.readlines()  # Leggi solo le nuove righe

                    # Flag per sapere se è stata rilevata una disconnessione
                    disconnection_found = False

                    # Filtra le righe per il pattern richiesto
                    for line in new_lines:
                        if "Client disconnected with reason: Proxy shutting down." in line:
                            disconnection_found = True
                            log_debug_message(f"Disconnessione rilevata---------")

                    if not disconnection_found:
                        log_debug_message("Nessuna disconnessione rilevata durante il check.")

                # Aggiorna la dimensione del file per il prossimo controllo
                last_file_size = current_file_size

            # Attendi un po' prima di controllare di nuovo
            time.sleep(1)

    except Exception as e:
        log_debug_message(f"Errore durante il monitoraggio del log: {e}")

# Avvia il monitoraggio
monitor_log_file()
