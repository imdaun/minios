import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import datetime
import webbrowser
import subprocess
import os
import sys
import random
import winsound
import market  # Наш магазин игр

# Опциональные библиотеки (если их нет, ОС всё равно запустится)
try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False

try:
    import minecraft_launcher_lib as mll
    HAS_MLL = True
except ImportError:
    HAS_MLL = False


class MiniOS:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniOS — Arch Edition v2.0")
        self.root.geometry("1100x720")
        
        # Настройки по умолчанию
        self.bg_color = "#0a0e14"
        self.fg_color = "#1793d1"
        self.text_color = "#ccc"
        self.sound_enabled = True
        
        self.apply_theme()

        # Рабочий стол
        self.desktop = tk.Canvas(root, bg=self.bg_color, highlightthickness=0)
        self.desktop.pack(fill="both", expand=True)

        # Панель задач снизу
        self.panel = tk.Frame(root, bg="#11161d", height=44)
        self.panel.pack(side="bottom", fill="x")
        self.panel.pack_propagate(False)

        # Кнопка "Пуск" (меню)
        self.start_btn = tk.Button(self.panel, text="🐧 Меню", bg="#1793d1", fg="#fff", 
                                   font=("Segoe UI", 10, "bold"), relief="flat", 
                                   command=self.show_start_menu)
        self.start_btn.pack(side="left", padx=5)

        # Иконки
        self.draw_icons()

        # Часы
        self.clock = tk.Label(self.panel, bg="#11161d", fg="#888", font=("Segoe UI", 10))
        self.clock.pack(side="right", padx=15)
        self.update_clock()

    def apply_theme(self):
        self.root.configure(bg=self.bg_color)

    def draw_icons(self):
        self.desktop.delete("all")
        
        self.create_icon("🖥️", "Терминал", 20, self.open_terminal)
        self.create_icon("🌐", "Браузер", 130, self.open_browser)
        self.create_icon("🧮", "Калькулятор", 240, self.open_calc)
        self.create_icon("📝", "Заметки", 350, self.open_notes)
        self.create_icon("⛏️", "Minecraft", 460, self.open_mc_launcher)
        self.create_icon("🐧", "Пингвинчик", 570, self.open_penguin)
        self.create_icon("⚙️", "Настройки", 680, self.open_settings)
        self.create_icon("🎮", "Магазин", 790, self.open_market)

    def create_icon(self, glyph, label, x, command):
        frame = tk.Frame(self.desktop, bg=self.bg_color, cursor="hand2")
        frame.place(x=x, y=20, width=90, height=90)
        lbl = tk.Label(frame, text=glyph, font=("Segoe UI", 28), bg=self.bg_color, fg=self.fg_color)
        lbl.pack()
        txt = tk.Label(frame, text=label, font=("Segoe UI", 9), bg=self.bg_color, fg=self.text_color)
        txt.pack()
        for w in (frame, lbl, txt):
            w.bind("<Button-1>", lambda e: self.click_and_run(command))
            w.bind("<Enter>", lambda e: frame.configure(bg=self.fg_color))
            w.bind("<Leave>", lambda e: frame.configure(bg=self.bg_color))

    def click_and_run(self, command):
        if self.sound_enabled:
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                pass
        command()

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S · %d.%m.%Y")
        self.clock.config(text=now)
        self.root.after(1000, self.update_clock)

    # ---------- Меню Пуск ----------
    def show_start_menu(self):
        menu = tk.Menu(self.root, tearoff=0, bg="#11161d", fg="#fff", font=("Segoe UI", 10))
        menu.add_command(label="🖥️ Терминал", command=self.open_terminal)
        menu.add_command(label="🌐 Браузер", command=self.open_browser)
        menu.add_command(label="🧮 Калькулятор", command=self.open_calc)
        menu.add_command(label="📝 Заметки", command=self.open_notes)
        menu.add_command(label="⛏️ Minecraft", command=self.open_mc_launcher)
        menu.add_command(label="🐧 Пингвинчик", command=self.open_penguin)
        menu.add_command(label="🎮 Магазин игр", command=self.open_market)
        menu.add_separator()
        menu.add_command(label="⚙️ Настройки", command=self.open_settings)
        menu.add_separator()
        menu.add_command(label="❌ Выключить ОС", command=self.root.destroy)
        
        x = self.start_btn.winfo_rootx()
        y = self.start_btn.winfo_rooty() - 250
        menu.post(x, y)

    # ---------- Настройки ----------
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Настройки")
        win.geometry("400x350")
        win.configure(bg=self.bg_color)

        tk.Label(win, text="Настройки MiniOS", bg=self.bg_color, fg=self.fg_color, 
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        def toggle_theme():
            if self.bg_color == "#0a0e14":
                self.bg_color = "#f0f0f0"
                self.fg_color = "#0078d7"
                self.text_color = "#333"
            else:
                self.bg_color = "#0a0e14"
                self.fg_color = "#1793d1"
                self.text_color = "#ccc"
            
            win.configure(bg=self.bg_color)
            self.apply_theme()
            self.desktop.configure(bg=self.bg_color)
            self.draw_icons()

        tk.Button(win, text="🌓 Сменить тему", command=toggle_theme,
                  bg=self.fg_color, fg="#fff", font=("Segoe UI", 10)).pack(pady=10)

        self.sound_var = tk.BooleanVar(value=self.sound_enabled)
        def toggle_sound():
            self.sound_enabled = self.sound_var.get()
            if self.sound_enabled:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)

        tk.Checkbutton(win, text="🔊 Звуки кликов", variable=self.sound_var,
                       command=toggle_sound, bg=self.bg_color, fg=self.text_color,
                       selectcolor=self.bg_color, font=("Segoe UI", 10)).pack(pady=10)

        tk.Label(win, text="MiniOS v2.0 (Python Edition)\nРазработчик: Ты!", 
                 bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 9)).pack(pady=20)

    # ---------- Внешние модули ----------
    def open_market(self):
        market.open_store(self.root)

    # ---------- Приложения ----------
    def open_terminal(self):
        win = tk.Toplevel(self.root)
        win.title("Терминал")
        win.geometry("640x400")
        win.configure(bg="#000")
        
        out = scrolledtext.ScrolledText(win, bg="#000", fg="#0f0", insertbackground="#0f0",
                                        font=("Courier New", 11))
        out.pack(fill="both", expand=True, padx=5, pady=5)
        out.insert("end", "MiniOS v2.0\nВведите help\n\n")
        
        inp_frame = tk.Frame(win, bg="#000")
        inp_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(inp_frame, text="[user@mini-os ~]$", bg="#000", fg="#1793d1",
                 font=("Courier New", 11)).pack(side="left")
        
        inp = tk.Entry(inp_frame, bg="#000", fg="#0f0", insertbackground="#0f0",
                       font=("Courier New", 11))
        inp.pack(side="left", fill="x", expand=True)
        inp.focus()

        def run_cmd(e=None):
            cmd = inp.get().strip()
            inp.delete(0, "end")
            out.insert("end", f"[user@mini-os ~]$ {cmd}\n")
            
            if cmd == "help":
                out.insert("end", "Команды: help, neofetch, date, clear, echo <text>\n")
            elif cmd == "neofetch":
                out.insert("end", "   .--.\n  |o_o |   OS: MiniOS v2.0\n  |:_/ |   Shell: tk-sh\n //   \\ \\\n(|     | )\n/'\\_   _/`\\\n\\___)=(___/\n")
            elif cmd == "date":
                out.insert("end", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
            elif cmd == "clear":
                out.delete("1.0", "end")
            elif cmd.startswith("echo "):
                out.insert("end", cmd[5:] + "\n")
            elif cmd:
                out.insert("end", f"{cmd}: команда не найдена\n")
            out.see("end")

        inp.bind("<Return>", run_cmd)

    def open_browser(self):
        win = tk.Toplevel(self.root)
        win.title("Браузер")
        win.geometry("520x260")
        win.configure(bg="#11161d")

        tk.Label(win, text="Введите URL:", bg="#11161d", fg="#ccc",
                 font=("Segoe UI", 11)).pack(pady=10)
        url = tk.Entry(win, font=("Segoe UI", 11), width=55)
        url.pack(pady=5)
        url.insert(0, "https://www.google.com")

        status = tk.Label(win, text="", bg="#11161d", fg="#7aff7a", font=("Segoe UI", 9))
        status.pack(pady=5)

        def go_external():
            link = url.get().strip()
            if not link.startswith("http"):
                link = "https://" + link
            webbrowser.open(link)
            status.config(text=f"Открыто в браузере")

        tk.Button(win, text="🌐 Открыть", command=go_external,
                  bg="#1793d1", fg="#fff", font=("Segoe UI", 11),
                  width=32).pack(pady=5)

    def open_calc(self):
        win = tk.Toplevel(self.root)
        win.title("Калькулятор")
        win.geometry("300x400")
        win.configure(bg="#11161d")
        
        display = tk.Entry(win, font=("Courier New", 18), bg="#0a0e14", fg="#1793d1",
                           justify="right", bd=0)
        display.pack(fill="x", padx=10, pady=10, ipady=10)

        def press(k):
            if k == "C":
                display.delete(0, "end")
            elif k == "=":
                try:
                    expr = display.get()
                    display.delete(0, "end")
                    display.insert(0, str(eval(expr or "0")))
                except Exception:
                    display.delete(0, "end")
                    display.insert(0, "Ошибка")
            else:
                display.insert("end", k)

        grid = tk.Frame(win, bg="#11161d")
        grid.pack(fill="both", expand=True, padx=10, pady=10)
        keys = [["C", "±", "%", "/"], ["7", "8", "9", "*"],
                ["4", "5", "6", "-"], ["1", "2", "3", "+"],
                ["0", ".", "=", ""]]
        
        for r, row in enumerate(keys):
            for c, k in enumerate(row):
                if not k:
                    continue
                tk.Button(grid, text=k, font=("Segoe UI", 14), bg="#1a2332", fg="#ddd",
                          command=lambda k=k: press(k)).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
        
        for i in range(4):
            grid.columnconfigure(i, weight=1)
        for i in range(5):
            grid.rowconfigure(i, weight=1)

    def open_notes(self):
        win = tk.Toplevel(self.root)
        win.title("Заметки")
        win.geometry("480x360")
        
        text = tk.Text(win, bg="#1a1f2b", fg="#ddd", font=("Segoe UI", 11), wrap="word")
        text.pack(fill="both", expand=True, padx=5, pady=5)
        
        notes_file = "notes.txt"
        try:
            with open(notes_file, "r", encoding="utf-8") as f:
                text.insert("1.0", f.read())
        except FileNotFoundError:
            pass

        def save(e=None):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
                
        text.bind("<KeyRelease>", save)

    def open_mc_launcher(self):
        win = tk.Toplevel(self.root)
        win.title("Лаунчер Minecraft")
        win.geometry("480x320")
        win.configure(bg="#11161d")

        if not HAS_MLL:
            tk.Label(win, text="Установите:\npip install minecraft_launcher_lib",
                     bg="#11161d", fg="#e05555", font=("Segoe UI", 10)).pack(pady=20)
            return

        mc_dir = mll.utils.get_minecraft_directory()
        try:
            versions = mll.utils.get_installed_versions(mc_dir)
            version_ids = [v["id"] for v in versions] if versions else []
        except Exception:
            version_ids = []

        tk.Label(win, text="Версия:", bg="#11161d", fg="#ccc").pack(pady=5)
        ver_var = tk.StringVar(value=version_ids[0] if version_ids else "1.20.1")
        ttk.Combobox(win, textvariable=ver_var, values=version_ids, width=30).pack()

        tk.Label(win, text="Ник:", bg="#11161d", fg="#ccc").pack(pady=5)
        name_entry = tk.Entry(win, width=30)
        name_entry.insert(0, "Player")
        name_entry.pack()

        status = tk.Label(win, text="", bg="#11161d", fg="#7aff7a", font=("Segoe UI", 9))
        status.pack(pady=10)

        def install_and_launch():
            version = ver_var.get().strip()
            username = name_entry.get().strip() or "Player"
            if not version:
                status.config(text="Укажите версию")
                return
            status.config(text=f"Установка/проверка {version}...")
            win.update()
            try:
                if version not in version_ids:
                    mll.install.install_minecraft_version(version, mc_dir)
                status.config(text="Запуск Minecraft...")
                win.update()
                options = {"username": username}
                cmd = mll.command.get_minecraft_command(version, mc_dir, options)
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                status.config(text="Minecraft запущен в отдельном окне!")
            except Exception as e:
                status.config(text=f"Ошибка: {e}")

        tk.Button(win, text="⛏️ Установить и запустить", command=install_and_launch,
                  bg="#1793d1", fg="#fff", font=("Segoe UI", 11)).pack(pady=10)

    def open_penguin(self):
        win = tk.Toplevel(self.root)
        win.title("Пингвинчик 🐧")
        win.geometry("360x420")
        win.configure(bg="#0a0e14")
        
        phrases = [
            "I use Arch, btw.",
            "Linux — это свобода.",
            "Бойся терминала!",
            "sudo make me a sandwich",
            "sudo dowland me firefoks",
            "I use kall btw",
            "Все мы немножко пингвины 🐧",
        ]
        phrase = random.choice(phrases)

        art = r"""
       .--.
      |o_o |
      |:_/ |
     //   \ \
    (|     | )
   /'\_   _/`\
   \___)=(___/
"""
        tk.Label(win, text=art, bg="#0a0e14", fg="#1793d1",
                 font=("Courier New", 11), justify="left").pack(pady=10)
        tk.Label(win, text="Tux", bg="#0a0e14", fg="#7aff7a",
                 font=("Segoe UI", 14, "bold")).pack()
        tk.Label(win, text=f'"{phrase}"', bg="#0a0e14", fg="#ccc",
                 font=("Segoe UI", 10, "italic")).pack(pady=5)

        def get_firefox():
            webbrowser.open("https://www.mozilla.org/ru/firefox/new/")

        tk.Button(win, text="🦊 Скачать Firefox", command=get_firefox,
                  bg="#ff7139", fg="#fff", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=2).pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    MiniOS(root)
    root.mainloop()
