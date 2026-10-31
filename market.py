import tkinter as tk
import os
import subprocess
import zipfile
import requests

# Наш "каталог" игр
GAMES_CATALOG = [
    {
        "name": "Mindustry",
        "desc": "Стратегия/Башни. Защищай ядро.",
        "url": "https://github.com/Anuken/Mindustry/releases/download/v146/Mindustry-Desktop.jar"
    },
    {
        "name": "VVVVVV (Clone)",
        "desc": "Платформер.",
        "url": "https://github.com/TerryCavanagh/VVVVVV/releases/download/2.4.2/VVVVVV.zip" 
    }
]

def open_store(root):
    """Открывает окно магазина."""
    win = tk.Toplevel(root)
    win.title("Магазин игр (GitHub)")
    win.geometry("600x450")
    win.configure(bg="#11161d")

    tk.Label(win, text="🎮 Бесплатные игры с GitHub", bg="#11161d", fg="#1793d1",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    list_frame = tk.Frame(win, bg="#11161d")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    status_label = tk.Label(win, text="", bg="#11161d", fg="#7aff7a", font=("Segoe UI", 10))
    status_label.pack(pady=5)

    def download_game(game):
        games_dir = "games"
        if not os.path.exists(games_dir):
            os.makedirs(games_dir)

        filename = game["name"].replace(" ", "_") + ".zip"
        filepath = os.path.join(games_dir, filename)
        
        status_label.config(text=f"Скачивание {game['name']}...")
        win.update()

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(game["url"], stream=True, headers=headers, allow_redirects=True)
            r.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            status_label.config(text=f"Распаковка {game['name']}...")
            win.update()

            extract_path = os.path.join(games_dir, game["name"].replace(" ", "_"))
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)

            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            os.remove(filepath)
            status_label.config(text=f"Готово! Игра в папке: {extract_path}")
            
            exe_found = None
            for r_dir, dirs, files in os.walk(extract_path):
                for file in files:
                    if file.endswith(".exe"):
                        exe_found = os.path.join(r_dir, file)
                        break
                if exe_found:
                    break

            if exe_found:
                status_label.config(text=f"Запуск {os.path.basename(exe_found)}...")
                win.update()
                subprocess.Popen([exe_found], cwd=os.path.dirname(exe_found))
            else:
                status_label.config(text=f"Игра скачана. Проверь папку: {extract_path}")

        except Exception as e:
            status_label.config(text=f"Ошибка: {e}")

    for game in GAMES_CATALOG:
        row = tk.Frame(list_frame, bg="#1a2332", pady=10, padx=10)
        row.pack(fill="x", pady=5)

        info_frame = tk.Frame(row, bg="#1a2332")
        info_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(info_frame, text=game["name"], bg="#1a2332", fg="#fff",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(info_frame, text=game["desc"], bg="#1a2332", fg="#aaa",
                 font=("Segoe UI", 9)).pack(anchor="w")

        btn = tk.Button(row, text="Скачать", bg="#1793d1", fg="#fff",
                        command=lambda g=game: download_game(g))
        btn.pack(side="right", padx=10)
