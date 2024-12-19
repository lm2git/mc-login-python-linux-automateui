import os
import time
from datetime import datetime
import pyautogui

# Path al file di log di Minecraft-
user_home = os.path.expanduser("~")
log_file_path = os.path.join(user_home, ".minecraft", "logs", "latest.log")

# Path al file di debug
debug_log_path = "disconnections.log"

# Funzione per scrivere i log con livello
def log_message(level, message):
    """Scrive un messaggio con timestamp, livello e messaggio su disconnections.log"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(debug_log_path, "a") as debug_log:
        debug_log.write(f"{timestamp} {level}: {message}\n")

# Funzione per loggare un messaggio di info
def log_info(message):
    log_message("INFO", message)

# Funzione per loggare un messaggio di successo
def log_success(message):
    log_message("SUCCESS", message)

# Funzione per loggare un messaggio di errore
def log_error(message):
    log_message("ERROR", message)

def list_windows():
    """Elenca tutte le finestre aperte"""
    windows = os.popen("wmctrl -l").read().strip().split("\n")
    window_list = []
    for win in windows:
        parts = win.split(maxsplit=3)
        if len(parts) == 4:
            window_list.append((parts[0], parts[3]))  # Ottieni l'ID e il titolo della finestra
    return window_list

def maximize_window(window_title):
    """Forza lo stato e massimizza una finestra"""
    try:
        windows = os.popen("wmctrl -l").read().strip().split("\n")
        for win in windows:
            parts = win.split(maxsplit=3)
            if len(parts) == 4 and window_title in parts[3]:
                window_id = parts[0]
                
                # Se la finestra è minimizzata, la ripristina
                os.system(f"wmctrl -i -r {window_id} -b remove,minimized")
                os.system(f"wmctrl -i -a {window_id}")  # Porta la finestra in primo piano

                os.system(f"wmctrl -i -r {window_id} -b add,maximized_vert,maximized_horz")
                time.sleep(1)
                log_success(f"Finestra '{window_title}' massimizzata.")
                return window_id
        log_error(f"Finestra con titolo '{window_title}' non trovata.")
    except Exception as e:
        log_error(f"Errore durante la gestione della finestra: {e}")
        return None

def is_minecraft_window_in_focus(window_title):
    """Verifica se la finestra di Minecraft è in focus"""
    windows = os.popen("wmctrl -l").read().strip().split("\n")
    for win in windows:
        parts = win.split(maxsplit=3)
        if len(parts) == 4 and window_title in parts[3]:
            # Controlla se la finestra è in focus (di solito indicato con un * accanto al titolo)
            if '*' in parts[3]:
                return True
    return False

def perform_additional_actions():
    """Esegue le azioni successive con tentativi multipli e ritardi robusti."""
    try:
        success = False
        
        for attempt in range(3):  # Massimo 3 tentativi
            log_info(f"Tentativo {attempt + 1} per aprire la chat e inviare il login...")
            time.sleep(2)  # Attesa per sicurezza

            # Verifica e assicura che Minecraft sia in focus e massimizzato
            windows = list_windows()
            for window_id, title in windows:
                if "Minecraft" in title:
                    if not is_minecraft_window_in_focus(title):
                        log_info(f"Finestra '{title}' non in focus, la massimizzando...")
                        maximize_window(title)
                    break
            
            # Sposta mouse al centro dello schermo
            width, height = pyautogui.size()

            # Calcola il centro dello schermo
            center_x = width // 2
            center_y = height // 2

            # Sposta il mouse al centro dello schermo
            pyautogui.moveTo(center_x, center_y)
            
            # Simula click per garantire focus sulla finestra
            pyautogui.click()
            time.sleep(5)
            
            # Apri la chat con "t"
            pyautogui.press("t")
            time.sleep(3)  # Attendi per essere sicuri che la chat si apra
            
            # Cancellare il carattere "t" se è stato scritto per errore
            pyautogui.press("backspace")
            time.sleep(2)  # Breve attesa per assicurarsi che il carattere venga rimosso
            
            # Digita il comando "/login Poppi1971"
            pyautogui.keyDown("shift")  # Per il simbolo "/"
            pyautogui.press("7")        # Tasto 7 con Shift dà "/"
            pyautogui.keyUp("shift")
            time.sleep(2)
            
            pyautogui.write("login Poppi1971", interval=0.2)  # Scrive la password lentamente
            time.sleep(2)
            pyautogui.press("enter")  # Invio per confermare
            
            # Aggiungi un breve controllo temporale
            log_info("Comando di login inviato. Attendo riscontro...")
            time.sleep(5)  # Attendi qualche secondo per verificare il risultato
            
            # Tentativo di interazione successiva (slot e click destro)
            pyautogui.press("5")  # Seleziona lo slot 5
            time.sleep(2)
            pyautogui.click(button="right")  # Click destro per interagire
            time.sleep(2)
            
            # Muovi il cursore alle coordinate specificate e clicca
            pyautogui.moveTo(960, 572)  # Posizione specifica
            time.sleep(1)
            pyautogui.click(button="left")  # Click sinistro
            time.sleep(1)
            
            log_success("Movimento e click completati. Azioni eseguite con successo.")
            success = True
            break  # Esce dal ciclo se tutte le azioni sono completate
            
        if not success:
            log_error("Azioni fallite dopo 3 tentativi.")
        else:
            log_success("Azioni successive completate con successo.")
            
    except Exception as e:
        log_error(f"Errore durante l'esecuzione delle azioni: {e}")

def monitor_log_file():
    """Monitora il file di log per disconnessioni"""
    try:
        if not os.path.exists(log_file_path):
            log_error(f"File non trovato: {log_file_path}")
            return

        last_file_size = os.path.getsize(log_file_path)
        last_disconnection_logged = False

        while True:
            current_file_size = os.path.getsize(log_file_path)

            if current_file_size != last_file_size:
                with open(log_file_path, "r") as log_file:
                    log_file.seek(last_file_size)
                    new_lines = log_file.readlines()

                    disconnection_found = False

                    for line in new_lines:
                        if "Per favore, esegui l'autenticazione con il comando: /login" in line:
                            disconnection_found = True
                            break

                    if disconnection_found and not last_disconnection_logged:
                        log_info("Disconnessione rilevata")
                        last_disconnection_logged = True

                        # Trova la finestra di Minecraft e avvia le azioni
                        windows = list_windows()
                        for window_id, title in windows:
                            if "Minecraft" in title:
                                log_info(f"Finestra trovata: {title}")
                                maximize_window(title)
                                time.sleep(5)
                                perform_additional_actions()
                                break

                    elif not disconnection_found:
                        last_disconnection_logged = False

                last_file_size = current_file_size

            time.sleep(10)
            # Effettua un piccolo jiggling del mouse
            x, y = pyautogui.position()  # Ottieni posizione corrente
            pyautogui.moveTo(x + 1, y)  # Sposta di 1 pixel a destra
            pyautogui.moveTo(x, y)      # Riporta alla posizione originale

    except Exception as e:
        log_error(f"Errore durante il monitoraggio del log: {e}")

if __name__ == "__main__":
    monitor_log_file()
