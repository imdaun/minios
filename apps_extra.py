import tkinter as tk
import os
import subprocess
import zipfile
import requests
import webbrowser
import random

def open_market(root):
    win = tk.Toplevel(root)
    win.title("Магазин игр (GitHub)")
    win.geometry("600x450")
    win.configure(bg="#11161d")

    tk.Label(win, text="🎮 Бесплатные игры с GitHub", bg="#11161d", fg="#1793d1", font=("Segoe UI", 14, "bold")).pack(pady=10)
    list_frame = tk.Frame(win, bg="#11161d")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    status_label = tk.Label(win, text="", bg="#11161d", fg="#7aff7a", font=("Segoe UI", 10))
    status_label.pack(pady=5)

    games_catalog = [
        {"name": "Mindustry", "desc": "Стратегия", "url": "https://github.com/Anuken/Mindustry/releases/download/v146/Mindustry-Desktop.jar"},
        {"name": "VVVVVV", "desc": "Платформер", "url": "https://github.com/TerryCavanagh/VVVVVV/releases/download/2.4.2/VVVVVV.zip"}
    ]

    def download_game(game):
        games_dir = "games"
        if not os.path.exists(games_dir): os.makedirs(games_dir)
        filepath = os.path.join(games_dir, game["name"] + ".zip")
        status_label.config(text=f"Скачивание {game['name']}...")
        win.update()
        try:
            r = requests.get(game["url"], stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
            status_label.config(text="Распаковка...")
            win.update()
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(games_dir, game["name"]))
            os.remove(filepath)
            status_label.config(text="Готово!")
        except Exception as e:
            status_label.config(text=f"Ошибка: {e}")

    for game in games_catalog:
        row = tk.Frame(list_frame, bg="#1a2332", pady=10, padx=10)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=game["name"], bg="#1a2332", fg="#fff").pack(side="left")
        tk.Button(row, text="Скачать", bg="#1793d1", fg="#fff", command=lambda g=game: download_game(g)).pack(side="right")
