import tkinter as tk

def create_icon(desktop, bg_color, fg_color, glyph, label, x, command):
    frame = tk.Frame(desktop, bg=bg_color, cursor="hand2")
    frame.place(x=x, y=20, width=90, height=90)
    lbl = tk.Label(frame, text=glyph, font=("Segoe UI", 28), bg=bg_color, fg=fg_color)
    lbl.pack()
    txt = tk.Label(frame, text=label, font=("Segoe UI", 9), bg=bg_color, fg="#ccc")
    txt.pack()
    for w in (frame, lbl, txt):
        w.bind("<Button-1>", lambda e: command())
        w.bind("<Enter>", lambda e: frame.configure(bg=fg_color))
        w.bind("<Leave>", lambda e: frame.configure(bg=bg_color))
    return frame
