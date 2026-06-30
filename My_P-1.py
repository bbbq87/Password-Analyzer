import re
import tkinter as tk
from tkinter import ttk

# ---------- Logic ----------

def password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'\d', password): score += 1
    if re.search(r'[@$!%*?&#^()_+=\-{}\[\]|:;"\'<>,./~`]', password): score += 1

    if password == "":
        return "—", 0
    if score <= 2:
        return "Weak", score
    elif score <= 4:
        return "Medium", score
    return "Strong", score


def check_strength(event=None):
    pwd = entry.get()
    strength, score = password_strength(pwd)
    strength_label.config(text=f"Strength: {strength}")

    progress['value'] = score

    colors = {
        "—": ("#888899", "grey.Horizontal.TProgressbar"),
        "Weak": ("#FF5C7A", "red.Horizontal.TProgressbar"),
        "Medium": ("#FFB454", "orange.Horizontal.TProgressbar"),
        "Strong": ("#3DDC97", "green.Horizontal.TProgressbar"),
    }
    color, bar_style = colors[strength]
    strength_label.config(fg=color)
    progress.configure(style=bar_style)

    # Animate the hint text/checklist
    update_checklist(pwd)


def update_checklist(pwd):
    checks = [
        (len_check, len(pwd) >= 8),
        (upper_check, bool(re.search(r'[A-Z]', pwd))),
        (lower_check, bool(re.search(r'[a-z]', pwd))),
        (digit_check, bool(re.search(r'\d', pwd))),
        (symbol_check, bool(re.search(r'[@$!%*?&#^()_+=\-{}\[\]|:;"\'<>,./~`]', pwd))),
    ]
    for label, ok in checks:
        if ok:
            label.config(fg="#3DDC97", text=label.cget("text").replace("○", "●"))
        else:
            base = label.cget("text").replace("●", "○")
            label.config(fg="#6B6B7B", text=base)


def toggle_password():
    if entry.cget("show") == "*":
        entry.config(show="")
        toggle_btn.config(text="🙈")
    else:
        entry.config(show="*")
        toggle_btn.config(text="👁")


# ---------- GUI setup ----------

root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("460x520")
root.configure(bg="#15151F")
root.resizable(False, False)

BG = "#15151F"
CARD_BG = "#1C1C2A"
ACCENT = "#00E5FF"
PURPLE = "#C77DFF"

# Outer card frame for a "panel" look
card = tk.Frame(root, bg=CARD_BG, highlightbackground="#2A2A3D", highlightthickness=1)
card.pack(padx=24, pady=24, fill="both", expand=True)

title_label = tk.Label(
    card, text="🔐 Password Strength Checker",
    font=("Helvetica", 18, "bold"), bg=CARD_BG, fg=ACCENT
)
title_label.pack(pady=(24, 18))

subtitle = tk.Label(
    card, text="Enter Password", font=("Arial", 13, "bold"),
    bg=CARD_BG, fg=PURPLE
)
subtitle.pack(pady=(0, 10))

# Entry + show/hide toggle in a pill-shaped row
entry_frame = tk.Frame(card, bg="#2A2A3D", highlightbackground="#3A3A52", highlightthickness=1)
entry_frame.pack(pady=6, padx=30, fill="x")

entry = tk.Entry(
    entry_frame, show="*", font=("Arial", 14),
    bg="#2A2A3D", fg="white", insertbackground=ACCENT,
    relief="flat", bd=0
)
entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(14, 0))
entry.bind("<KeyRelease>", check_strength)

toggle_btn = tk.Button(
    entry_frame, text="👁", command=toggle_password,
    bg="#2A2A3D", fg="white", relief="flat", bd=0,
    activebackground="#2A2A3D", font=("Arial", 12), cursor="hand2"
)
toggle_btn.pack(side="right", padx=8)

# Strength label
strength_label = tk.Label(
    card, text="Strength: —", font=("Arial", 14, "bold"),
    bg=CARD_BG, fg="#888899"
)
strength_label.pack(pady=(22, 8))

# Progress bar styling
style = ttk.Style()
style.theme_use("clam")
for name, color in [
    ("grey", "#444455"),
    ("red", "#FF5C7A"),
    ("orange", "#FFB454"),
    ("green", "#3DDC97"),
]:
    style.configure(
        f"{name}.Horizontal.TProgressbar",
        troughcolor="#2A2A3D", background=color,
        thickness=14, bordercolor="#2A2A3D", lightcolor=color, darkcolor=color
    )

progress = ttk.Progressbar(card, length=360, maximum=6, style="grey.Horizontal.TProgressbar")
progress.pack(pady=(0, 24))

# Checklist of requirements
checklist_frame = tk.Frame(card, bg=CARD_BG)
checklist_frame.pack(pady=(0, 20), padx=30, fill="x")

checklist_title = tk.Label(
    checklist_frame, text="Requirements", font=("Arial", 11, "bold"),
    bg=CARD_BG, fg="#888899"
)
checklist_title.pack(anchor="w", pady=(0, 6))

def make_check_label(text):
    lbl = tk.Label(
        checklist_frame, text=f"○  {text}", font=("Arial", 11),
        bg=CARD_BG, fg="#6B6B7B", anchor="w"
    )
    lbl.pack(anchor="w", pady=2)
    return lbl

len_check = make_check_label("At least 8 characters")
upper_check = make_check_label("Contains uppercase letter")
lower_check = make_check_label("Contains lowercase letter")
digit_check = make_check_label("Contains a number")
symbol_check = make_check_label("Contains a symbol")

footer = tk.Label(
    card, text="Tip: longer + varied passwords are stronger 💡",
    font=("Arial", 9, "italic"), bg=CARD_BG, fg="#555566"
)
footer.pack(side="bottom", pady=(0, 16))

root.mainloop()