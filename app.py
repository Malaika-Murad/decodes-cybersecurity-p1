import tkinter as tk
from tkinter import ttk
from core.gatekeeper import GatekeeperValidator

def on_input_change(*args):
    raw_pass = pass_var.get()
    strength, entropy, tips = GatekeeperValidator.evaluate(raw_pass)

    config_map = {
        "None": ("#888888", 0, "No Input"),
        "Weak": ("#E74C3C", 33, "Weak Password"),
        "Medium": ("#F39C12", 66, "Medium Strength"),
        "Strong": ("#27AE60", 100, "Gatekeeper Verified (Strong)")
    }
    color, progress, label_text = config_map[strength]

    status_label.config(text=label_text, fg=color)
    entropy_label.config(text=f"Calculated Entropy: {entropy} bits")
    progress_bar["value"] = progress

    feedback_box.config(state="normal")
    feedback_box.delete("1.0", tk.END)
    if raw_pass:
        feedback_box.insert(tk.END, "\n".join(tips))
    feedback_box.config(state="disabled")


root = tk.Tk()
root.title("Password Strength Evaluator - Defensive Security Gatekeeper")
root.geometry("460x480")
root.resizable(False, False)
root.configure(bg="#1E222A")

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", thickness=8, troughcolor="#2D3139", background="#27AE60")

tk.Label(root, text="DEFENSIVE SECURITY GATEKEEPER", font=("Segoe UI", 12, "bold"), bg="#1E222A", fg="#61AFEF").pack(pady=(20, 5))
tk.Label(root, text="Password Strength Evaluator", font=("Segoe UI", 9), bg="#1E222A", fg="#ABB2BF").pack(pady=(0, 15))

frame = tk.Frame(root, bg="#1E222A")
frame.pack(padx=30, fill="x")

tk.Label(frame, text="Enter Target Password:", font=("Segoe UI", 9, "bold"), bg="#1E222A", fg="#DCDFE4").pack(anchor="w")

pass_var = tk.StringVar()
pass_var.trace_add("write", on_input_change)

pass_entry = tk.Entry(frame, textvariable=pass_var, show="•", font=("Segoe UI", 12), bg="#282C34", fg="#FFFFFF", insertbackground="white", relief="flat", bd=4)
pass_entry.pack(fill="x", pady=6)

status_label = tk.Label(root, text="No Input", font=("Segoe UI", 11, "bold"), bg="#1E222A", fg="#888888")
status_label.pack(pady=(10, 2))

entropy_label = tk.Label(root, text="Calculated Entropy: 0.0 bits", font=("Consolas", 9), bg="#1E222A", fg="#98C379")
entropy_label.pack(pady=(0, 8))

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=5)

diag_frame = tk.Frame(root, bg="#1E222A")
diag_frame.pack(padx=30, pady=15, fill="both", expand=True)

tk.Label(diag_frame, text="Security Audit Diagnostic:", font=("Segoe UI", 9, "bold"), bg="#1E222A", fg="#DCDFE4").pack(anchor="w")

feedback_box = tk.Text(diag_frame, height=5, font=("Consolas", 9), bg="#282C34", fg="#E06C75", relief="flat", bd=4, state="disabled")
feedback_box.pack(fill="both", expand=True, pady=6)

root.mainloop()