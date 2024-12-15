import os
import time
import subprocess
from datetime import datetime
import pyautogui
import pygetwindow as gw

# Prerequisiti
# - sudo apt update -y
# - sudo apt install python3 -y
# - sudo apt install python3-pip xdotool wmctrl -y
# - pip install pygetwindow pyautogui python-xlib

# Costanti configurabili
PASSWORD = os.getenv("MC_PASSWORD")  # Imposta questa variabile d'ambiente con la tua password
CHAT_KEY = 't'
HOTBAR_SLOT = '5'
CLICK_POSITION = (960, 540)  # Coordinate da aggiustare

# Percorsi dei file
USER_HOME = os.path.expanduser("~")
LOG_FILE_PATH = os.path.join(USER_HOME, ".minecraft", "logs", "latest.log")
DEBUG_LOG_PATH = "disconnections.log"
TEMPFILE_PATH = os.path.join("/tmp", "latest_log_position.txt")

def check_prerequisites():
    """Verifica che i prerequisiti di sistema siano soddisfatti."""
    prerequisites = {
        "xdotool": "Strumento per gestire finestre e tastiera/mouse",
        "wmctrl": "Strumento per controllare finestre",
        "pyautogui": "Libreria Python per automazione GUI",
        "pygetwindow": "Libreria Python per gestire finestre",
    }
    missing = []

    # Verifica comandi di sistema
    for command in ["xdotool", "wmctrl"]:
        if not shutil.which(command):
            missing.append(command)

    # Verifica librerie Python
    try:
        import pyautogui
        import pygetwindow
    except ImportError as e:
        missing.append(str(e).split()[-1])  # Nome del pacchetto mancante

    if missing:
        print("Mancano i seguenti prerequisiti:")
        for m in missing:
            print(f"- {m}: {prerequisites.get(m, 'Sconosciuto')}")
        exit(1)

def log_debug_message(message):
    """Scrive un messaggio con timestamp su disconnections.log"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(DEBUG_LOG_PATH, "a") as debug_log:
        debug_log.write(f"{timestamp} {message}\n")

def focus_minecraft():
    """Porta la finestra di Minecraft in primo piano usando xdotool."""
    try:
        result = subprocess.check_output(["xdotool", "search", "--name", "Minecraft"], text=True)
        window_id = result.strip().split('\n')[0]
        subprocess.run(["xdotool", "windowactivate", window_id])
        print("Finestra di Minecraft attivata.")
        return True
    except (subprocess.CalledProcessError, IndexError) as e:
        log_debug_message(f"Errore nell'attivare la finestra di Minecraft: {e}")
        return False

def perform_actions():
    """Esegue la sequenza di azioni necessarie."""
    if not focus_minecraft():
        return
    time.sleep(3)

    # Aprire la chat
    pyautogui.press(CHAT_KEY)
    time.sleep(1)

    # Inserire il comando /login e premere Enter
    pyautogui.typewrite(f"/login {PASSWORD}")
    pyautogui.press('enter')
    time.sleep(3)

    # Selezionare il numero 5 nella hotbar
    pyautogui.press(HOTBAR_SLOT)
    time.sleep(1)

    # Tasto destro del mouse
    pyautogui.click(button='right')
    time.sleep(1)

    # Muovere il mouse e cliccare sinistro
    screen_width, screen_height = pyautogui.size()
    if not (0 <= CLICK_POSITION[0] < screen_width and 0 <= CLICK_POSITION[1] < screen_height):
        log_debug_message(f"Posizione del mouse non valida: {CLICK_POSITION}")
        return

    pyautogui.moveTo(*CLICK_POSITION)
    pyautogui.click(button='left')
    print("Sequenza completata.")

def get_last_position():
    """Legge l'ultima posizione salvata del file di log."""
    try:
        with open(TEMPFILE_PATH, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def set_last_position(position):
    """Salva la posizione attuale del file di log."""
    with open(TEMPFILE_PATH, "w") as f:
        f.write(str(position))

def monitor_log_file():
    """Monitora il file di log e reagisce alle disconnessioni."""
    try:
        if not os.path.exists(LOG_FILE_PATH):
            log_debug_message(f"File non trovato: {LOG_FILE_PATH}")
            return

        last_position = get_last_position()

        while True:
            with open(LOG_FILE_PATH, "r") as log_file:
                log_file.seek(last_position)
                new_lines = log_file.readlines()
                disconnection_found = False

                for line in new_lines:
                    if "Client disconnected with reason: Proxy shutting down." in line:
                        disconnection_found = True
                        log_debug_message("Disconnessione rilevata.")
                        perform_actions()

                if not disconnection_found:
                    log_debug_message("Nessuna disconnessione rilevata durante il check.")

                last_position = log_file.tell()
                set_last_position(last_position)

            time.sleep(1)
    except Exception as e:
        log_debug_message(f"Errore durante il monitoraggio del log: {e}")

# Main
if __name__ == "__main__":
    check_prerequisites()

    if not PASSWORD:
        print("Errore: Imposta la variabile d'ambiente MC_PASSWORD con la tua password.")
        exit(1)

    monitor_log_file()
