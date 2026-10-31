import tkinter as tk
from tkinter import messagebox
import winsound

def open_settings(root, os_instance):
    win = tk.Toplevel(root)
    win.title("Настройки")
    win.geometry("400x350")
    win.configure(bg=os_instance.bg_color)

    tk.Label(win, text="Настройки MiniOS", bg=os_instance.bg_color, fg=os_instance.fg_color, font=("Segoe UI", 14, "bold")).pack(pady=15)

    def toggle_theme():
        if os_instance.bg_color == "#0a0e14":
            os_instance.bg_color = "#f0f0f0"
            os_instance.fg_color = "#0078d7"
            os_instance.text_color = "#333"
        else:
            os_instance.bg_color = "#0a0e14"
            os_instance.fg_color = "#1793d1"
            os_instance.text_color = "#ccc"
        win.configure(bg=os_instance.bg_color)
        os_instance.apply_theme()
        os_instance.desktop.configure(bg=os_instance.bg_color)
        os_instance.draw_icons()

    tk.Button(win, text="🌓 Сменить тему", command=toggle_theme, bg=os_instance.fg_color, fg="#fff").pack(pady=10)

    def toggle_sound():
        os_instance.sound_enabled = not os_instance.sound_enabled
        if os_instance.sound_enabled:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

    tk.Button(win, text="🔊 Переключить звук", command=toggle_sound, bg=os_instance.fg_color, fg="#fff").pack(pady=10)
