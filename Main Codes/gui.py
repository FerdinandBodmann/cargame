import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random


class App:
    def __init__(self, root):
        self.root = root
        self.s = 0
        self._p = 0
        self.streak = 0
        self.done = False
        self.fuel = 100
        self.max_fuel = 100

        root.title("drive")
        root.configure(bg="#0d0d0d")
        root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#0d0d0d", foreground="#cccccc",
                        fieldbackground="#1a1a1a", troughcolor="#1a1a1a")
        style.configure("TLabel", background="#0d0d0d", foreground="#cccccc")
        style.configure("TFrame", background="#0d0d0d")
        style.configure("TButton", background="#1a1a1a", foreground="#cccccc",
                        bordercolor="#333", lightcolor="#1a1a1a", darkcolor="#1a1a1a",
                        focuscolor="#0d0d0d", padding=(16, 6))
        style.map("TButton", background=[("active", "#2a2a2a")])
        style.configure("TScale", background="#0d0d0d", troughcolor="#1a1a1a",
                        slidercolor="#4ec9b0")
        style.configure("Fuel.Horizontal.TProgressbar",
                        background="#f0a030", troughcolor="#1a1a1a", bordercolor="#1a1a1a")

        main = ttk.Frame(root, padding=28)
        main.pack()

        ttk.Label(main, text="drive",
                 font=("Arial", 13, "bold"), foreground="#e0e0e0").pack(anchor="w")

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(10, 20))

        mid = ttk.Frame(main)
        mid.pack(fill="x")

        # -- Progress tile --
        bar_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222",
                           highlightthickness=1, padx=24, pady=20)
        bar_tile.pack(side=tk.LEFT, padx=(0, 8))

        self.canvas = tk.Canvas(bar_tile, width=36, height=200,
                                bg="#111", highlightthickness=0)
        self.canvas.pack()
        self.bar = self.canvas.create_rectangle(0, 200, 36, 200,
                                                fill="#4ec9b0", width=0)

        self.pct = ttk.Label(bar_tile, text="0 / 10",
                            font=("Arial", 11), foreground="#666", width=7)
        self.pct.pack(pady=(6, 0))

        self.fuel_bar = ttk.Progressbar(bar_tile, length=100, mode="determinate",
                                        maximum=self.max_fuel,
                                        style="Fuel.Horizontal.TProgressbar")
        self.fuel_bar.pack(pady=(4, 0))
        self.fuel_lbl = ttk.Label(bar_tile, text="fuel: 100",
                                  font=("Arial", 9), foreground="#f0a030")
        self.fuel_lbl.pack()

        self.streak_lbl = ttk.Label(bar_tile, text="streak: 0",
                                    font=("Arial", 9), foreground="#555")
        self.streak_lbl.pack()

        # -- Speed tile --
        speed_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222",
                              highlightthickness=1, padx=24, pady=20)
        speed_tile.pack(side=tk.LEFT, padx=4, fill="both", expand=True)

        self.speed_val = tk.DoubleVar(value=1)
        self.kmh_lbl = tk.Label(speed_tile, text="10 km/h",
                                font=("Arial", 24, "bold"), fg="#4ec9b0",
                                bg="#151515")
        self.kmh_lbl.pack(pady=(10, 5))

        self.risk_lbl = tk.Label(speed_tile, text="risk: 0%  |  +1/go",
                                 font=("Arial", 10), fg="#555",
                                 bg="#151515")
        self.risk_lbl.pack()

        self.slider = tk.Scale(speed_tile, from_=1, to=10,
                               orient="horizontal", length=160,
                               variable=self.speed_val, showvalue=False,
                               bg="#151515", fg="#ccc", troughcolor="#222",
                               highlightthickness=0, bd=0,
                               activebackground="#4ec9b0",
                               sliderrelief="flat", sliderlength=24,
                               command=self.on_speed_change)
        self.slider.pack(pady=(4, 10))

        self.go_btn = tk.Button(speed_tile, text="Go", command=self.on_go,
                                width=12, bg="#1a1a1a", fg="#4ec9b0", bd=0,
                                activebackground="#2a2a2a", activeforeground="#4ec9b0",
                                font=("Arial", 12, "bold"), cursor="hand2",
                                highlightthickness=1, highlightbackground="#333",
                                state="disabled")
        self.go_btn.pack(pady=(4, 6))

        # -- Terminal tile --
        term_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222",
                             highlightthickness=1, padx=0, pady=0)
        term_tile.pack(side=tk.LEFT, padx=(8, 0), fill="both", expand=True)

        self.term = tk.Text(term_tile, width=34, height=10,
                           bg="#0d0d0d", fg="#ccc",
                           font=("Consolas", 10),
                           bd=0, highlightthickness=0,
                           state="disabled", wrap="none")
        self.term.pack(side=tk.LEFT, fill="both", expand=True, padx=1, pady=1)
        scroll = tk.Scrollbar(term_tile, command=self.term.yview, bg="#1a1a1a",
                             troughcolor="#111", bd=0, highlightthickness=0)
        scroll.pack(side=tk.RIGHT, fill="y")
        self.term.config(yscrollcommand=scroll.set)
        self.log("idle", "#555")

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(20, 14))

        bf = ttk.Frame(main)
        bf.pack()
        self.start_btn = ttk.Button(bf, text="Start", command=self.start, width=10)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = ttk.Button(bf, text="Stop", command=self.stop, width=10)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="Exit", command=root.quit, width=10).pack(side=tk.LEFT, padx=4)

        self.on_speed_change()
        root.update()
        w = root.winfo_reqwidth() + 40
        h = root.winfo_reqheight() + 20
        root.minsize(w, h)
        root.geometry(f"{w}x{h}")

    def speed_progress(self, s):
        if s <= 2:
            return 1, 0
        elif s <= 4:
            return 2, 5
        elif s <= 6:
            return 3, 15
        elif s <= 8:
            return 4, 30
        else:
            return 5, 50

    def speed_fuel_cost(self, s):
        return s * 2

    def speed_color(self, s):
        if s <= 3:
            return "#4ec9b0"
        elif s <= 6:
            return "#d4d44a"
        else:
            return "#e06c75"

    def on_speed_change(self, _=None):
        s = int(self.speed_val.get())
        kmh = s * 10
        steps, risk = self.speed_progress(s)
        cost = self.speed_fuel_cost(s)
        c = self.speed_color(s)
        self.kmh_lbl.config(text=f"{kmh} km/h", fg=c)
        self.risk_lbl.config(text=f"risk: {risk}%  |  +{steps}/go  |  -{cost} fuel", fg=c)

    def update_bar(self):
        max_h = 200
        h = int(max_h * (self._p / 10))
        y = max_h - h
        s = int(self.speed_val.get())
        c = self.speed_color(s)
        self.canvas.itemconfig(self.bar, fill=c)
        self.canvas.coords(self.bar, 0, y, 36, max_h)

    def crash_bar(self):
        self.canvas.itemconfig(self.bar, fill="#ff4444")
        self.canvas.coords(self.bar, 0, 200, 36, 200)

    def update_fuel(self):
        self.fuel_bar["value"] = self.fuel
        self.fuel_lbl.config(text=f"fuel: {self.fuel}")

    def log(self, msg, color="#ccc"):
        ts = datetime.now().strftime("%H:%M:%S")
        tag = f"c{len(self.term.get('1.0', 'end-1c'))}"
        self.term.tag_configure(tag, foreground=color)
        self.term.config(state="normal")
        self.term.insert("end", f"[{ts}] {msg}\n", tag)
        self.term.see("end")
        self.term.config(state="disabled")

    def start(self):
        if self.s == 1:
            self.log("already running", "#e06c75")
            return
        self.s = 1
        self._p = 0
        self.done = False
        self.streak = 0
        self.fuel = self.max_fuel
        self.streak_lbl.config(text="streak: 0")
        self.go_btn.config(state="normal", fg=self.speed_color(int(self.speed_val.get())))
        self.pct.config(text="0 / 10")
        self.update_fuel()
        self.log("driving — tank full", "#4ec9b0")
        self.update_bar()

    def on_go(self):
        if self.s != 1 or self.done:
            return

        if self.fuel <= 0:
            self.s = 0
            self.done = True
            self.go_btn.config(state="disabled", fg="#555")
            self.log("out of fuel! press Start to refuel", "#f0a030")
            return

        s = int(self.speed_val.get())
        steps, risk = self.speed_progress(s)
        cost = self.speed_fuel_cost(s)
        c = self.speed_color(s)

        if risk > 0 and random.randint(1, 100) <= risk:
            self.s = 0
            self.done = True
            self.go_btn.config(state="disabled", fg="#555")
            self.crash_bar()
            self.pct.config(text="💥")
            self.log(f"CRASH! Engine blew at {s*10} km/h", "#ff4444")
            self.log("press Start to repair", "#ff4444")
            return

        self.fuel = max(self.fuel - cost, 0)
        self.update_fuel()

        old = self._p
        self._p = min(self._p + steps, 10)
        self.streak += self._p - old
        self.streak_lbl.config(text=f"streak: {self.streak}")
        self.pct.config(text=f"{self._p} / 10")
        self.update_bar()
        self.log(f"step {self._p}  ({s*10} km/h, -{cost} fuel)", c)

        if self.fuel <= 0:
            self.s = 0
            self.done = True
            self.go_btn.config(state="disabled", fg="#555")
            self.log("out of fuel! press Start to refuel", "#f0a030")
            return

        if self._p >= 10:
            self.s = 0
            self.done = True
            self.go_btn.config(state="disabled", fg="#555")
            self.log("FINISH!", "#4ec9b0")

    def stop(self):
        if self.done:
            self.log("already done, press Start to go again", "#555")
            return
        if self.s == 0:
            self.log("already stopped", "#e06c75")
        else:
            self.s = 0
            self.go_btn.config(state="disabled", fg="#555")
            self._p = 0
            self.pct.config(text="0 / 10")
            self.canvas.coords(self.bar, 0, 200, 36, 200)
            self.log(f"stopped (streak: {self.streak})", "#e06c75")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
