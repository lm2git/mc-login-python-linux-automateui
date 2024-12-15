import time
import os

# Ottieni il nome dell'utente corrente
user_home = os.path.expanduser("~")

# Path al file latest.log
log_file_path = os.path.join(user_home, ".minecraft", "logs", "latest.log")

def monitor_log_file():
    try:
        # Verifica se il file esiste prima di tentare di aprirlo
        if not os.path.exists(log_file_path):
            print(f"File non trovato: {log_file_path}")
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

                    # Filtra le righe per il pattern richiesto
                    for line in new_lines:
                        if "Client disconnected with reason: Proxy shutting down." in line:
                            print(f"Disconnessione rilevata: {line.strip()}")

                # Aggiorna la dimensione del file per il prossimo controllo
                last_file_size = current_file_size

            # Attendi un po' prima di controllare di nuovo
            time.sleep(1)

    except Exception as e:
        print(f"Errore durante il monitoraggio del log: {e}")

# Avvia il monitoraggio
monitor_log_file()
