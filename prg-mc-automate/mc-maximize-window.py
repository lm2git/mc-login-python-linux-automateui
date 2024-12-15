import os
import time

# Funzione per elencare tutte le finestre aperte
def list_windows():
    windows = os.popen("wmctrl -l").read().strip().split("\n")
    window_list = []
    for win in windows:
        parts = win.split(maxsplit=3)
        if len(parts) == 4:
            window_list.append((parts[0], parts[3]))  # Ottieni l'ID e il titolo della finestra
    return window_list

# Funzione per forzare lo stato e massimizzare una finestra
def maximize_window(window_title):
    try:
        # Trova l'ID della finestra corrispondente
        windows = os.popen("wmctrl -l").read().strip().split("\n")
        for win in windows:
            parts = win.split(maxsplit=3)
            if len(parts) == 4 and window_title in parts[3]:
                window_id = parts[0]

                # Rimuove eventuale stato full-screen
                os.system(f"wmctrl -i -r {window_id} -b remove,fullscreen")
                time.sleep(0.1)

                # Porta la finestra in primo piano
                os.system(f"wmctrl -i -a {window_id}")
                time.sleep(0.1)

                # Massimizza la finestra
                os.system(f"wmctrl -i -r {window_id} -b add,maximized_vert,maximized_horz")
                print(f"Finestra '{window_title}' massimizzata.")
                return window_id
        print(f"Finestra con titolo '{window_title}' non trovata.")
    except Exception as e:
        print(f"Errore: {e}")
        return None

if __name__ == "__main__":
    print("Finestre aperte:")
    windows = list_windows()

    # Cerca una finestra che contiene 'Minecraft' nel nome
    found_minecraft = False
    for window_id, title in windows:
        if "Minecraft" in title:
            found_minecraft = True
            print(f"Finestra trovata: {title}")
            maximize_window(title)  # Massimizza la finestra di Minecraft
            break

    if not found_minecraft:
        print("Finestra con il nome 'Minecraft' non trovata.")