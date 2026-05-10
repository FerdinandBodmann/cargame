import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import random
import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class UserDialog:
    def __init__(self, root):
        self.root = root
        self.selected = None
        self.users = load_users()

        self.win = tk.Toplevel(root)
        self.win.title("select user")
        self.win.configure(bg="#0d0d0d")
        self.win.resizable(False, False)
        self.win.transient(root)
        self.win.grab_set()

        tk.Label(self.win, text="select user",
                font=("Arial", 14, "bold"), fg="#e0e0e0",
                bg="#0d0d0d").pack(pady=(20, 16))

        self.list_frame = tk.Frame(self.win, bg="#0d0d0d")
        self.list_frame.pack(padx=30)
        self.refresh_list()

        btn_frame = tk.Frame(self.win, bg="#0d0d0d")
        btn_frame.pack(pady=(12, 20))

        tk.Button(btn_frame, text="+ New User", command=self.new_user,
                 bg="#1a1a1a", fg="#4ec9b0", bd=0,
                 activebackground="#2a2a2a", activeforeground="#4ec9b0",
                 font=("Arial", 10), cursor="hand2",
                 highlightthickness=1, highlightbackground="#333",
                 padx=12, pady=4).pack(side=tk.LEFT, padx=4)

        self.del_btn = tk.Button(btn_frame, text="Delete", command=self.delete_user,
                                bg="#1a1a1a", fg="#e06c75", bd=0,
                                activebackground="#2a2a2a", activeforeground="#e06c75",
                                font=("Arial", 10), cursor="hand2",
                                highlightthickness=1, highlightbackground="#333",
                                padx=12, pady=4)
        self.del_btn.pack(side=tk.LEFT, padx=4)

        if not self.users:
            self.del_btn.config(state="disabled", fg="#555")

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.users:
            tk.Label(self.list_frame, text="no users yet — create one",
                    font=("Arial", 10), fg="#555",
                    bg="#0d0d0d").pack(pady=10)
            return

        for name in sorted(self.users.keys()):
            data = self.users[name]
            f = tk.Frame(self.list_frame, bg="#151515",
                        highlightbackground="#333", highlightthickness=1)
            f.pack(fill="x", pady=2)

            info = f"scraps: {data.get('scraps', 0)}  |  best: {data.get('best_streak', 0)}"
            tk.Label(f, text=f"  {name}", font=("Arial", 11, "bold"),
                    fg="#ccc", bg="#151515", width=12, anchor="w").pack(side=tk.LEFT, pady=6)
            tk.Label(f, text=info, font=("Arial", 9),
                    fg="#555", bg="#151515").pack(side=tk.LEFT, padx=(4, 0))

            btn = tk.Button(f, text="Select", command=lambda n=name: self.select(n),
                           bg="#1a1a1a", fg="#4ec9b0", bd=0,
                           activebackground="#2a2a2a", activeforeground="#4ec9b0",
                           font=("Arial", 9), cursor="hand2", padx=10,
                           highlightthickness=1, highlightbackground="#333")
            btn.pack(side=tk.RIGHT, padx=6, pady=4)

    def select(self, name):
        self.selected = name
        self.win.destroy()

    def new_user(self):
        name = simpledialog.askstring("new user", "enter username:",
                                      parent=self.win)
        if not name or not name.strip():
            return
        name = name.strip()
        if name in self.users:
            messagebox.showwarning("exists", "user already exists", parent=self.win)
            return
        self.users[name] = {
            "scraps": 0,
            "best_streak": 0,
            "upg_engine": 0,
            "upg_tank": 0,
            "upg_armor": 0,
            "upg_turbo": 0,
        }
        save_users(self.users)
        self.refresh_list()

    def delete_user(self):
        if not self.users:
            return
        name = simpledialog.askstring("delete user", "enter username to delete:",
                                      parent=self.win)
        if not name or name not in self.users:
            return
        if messagebox.askyesno("confirm", f"delete '{name}'?", parent=self.win):
            del self.users[name]
            save_users(self.users)
            self.refresh_list()

    def on_close(self):
        self.root.destroy()
        self.win.destroy()


class App:
    def __init__(self, root, user_data, username):
        self.root = root
        self.username = username
        self.s = 0
        self._p = 0
        self.streak = 0
        self.best_streak = user_data.get("best_streak", 0)
        self.done = False
        self.broken = False
        self.repair_clicks = 0

        self.max_fuel = 100
        self.max_hp = 100
        self.fuel = self.max_fuel
        self.hp = self.max_hp

        self.scraps = user_data.get("scraps", 0)
        self.upg_engine = user_data.get("upg_engine", 0)
        self.upg_tank = user_data.get("upg_tank", 0)
        self.upg_armor = user_data.get("upg_armor", 0)
        self.upg_turbo = user_data.get("upg_turbo", 0)

        self.max_fuel += self.upg_tank * 25
        self.fuel = self.max_fuel

        root.title(f"drive — {username}")
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
        style.configure("HP.Horizontal.TProgressbar",
                        background="#e06c75", troughcolor="#1a1a1a", bordercolor="#1a1a1a")

        main = ttk.Frame(root, padding=28)
        main.pack()

        top = ttk.Frame(main)
        top.pack(fill="x")
        ttk.Label(top, text="drive",
                 font=("Arial", 13, "bold"), foreground="#e0e0e0").pack(side=tk.LEFT)
        tk.Button(top, text=f"@{username}  ▼", command=self.switch_user,
                 font=("Arial", 9), bg="#151515", fg="#888",
                 bd=0, cursor="hand2", padx=8, pady=2,
                 highlightthickness=1, highlightbackground="#333").pack(side=tk.RIGHT)

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
        self.pct.pack(pady=(4, 0))

        self.fuel_bar = ttk.Progressbar(bar_tile, length=100, mode="determinate",
                                        maximum=self.max_fuel,
                                        style="Fuel.Horizontal.TProgressbar")
        self.fuel_bar.pack(pady=(4, 0))
        self.fuel_lbl = ttk.Label(bar_tile, text=f"fuel: {self.fuel}",
                                  font=("Arial", 9), foreground="#f0a030")
        self.fuel_lbl.pack()

        self.hp_bar = ttk.Progressbar(bar_tile, length=100, mode="determinate",
                                      maximum=self.max_hp,
                                      style="HP.Horizontal.TProgressbar")
        self.hp_bar.pack(pady=(4, 0))
        self.hp_lbl = ttk.Label(bar_tile, text=f"hp: {self.hp}",
                                font=("Arial", 9), foreground="#e06c75")
        self.hp_lbl.pack()

        self.streak_lbl = ttk.Label(bar_tile, text=f"streak: 0  |  best: {self.best_streak}",
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

        bf = tk.Frame(speed_tile, bg="#151515")
        bf.pack()
        self.go_btn = tk.Button(bf, text="Go", command=self.on_go,
                                width=9, bg="#1a1a1a", fg="#4ec9b0", bd=0,
                                activebackground="#2a2a2a", activeforeground="#4ec9b0",
                                font=("Arial", 12, "bold"), cursor="hand2",
                                highlightthickness=1, highlightbackground="#333",
                                state="disabled")
        self.go_btn.pack(side=tk.LEFT, padx=2)
        self.nitro_btn = tk.Button(bf, text="Nitro", command=self.on_nitro,
                                   width=7, bg="#1a1a1a", fg="#e06c75", bd=0,
                                   activebackground="#2a2a2a", activeforeground="#e06c75",
                                   font=("Arial", 10, "bold"), cursor="hand2",
                                   highlightthickness=1, highlightbackground="#333",
                                   state="disabled")
        self.nitro_btn.pack(side=tk.LEFT, padx=2)

        # -- Upgrades tile --
        upg_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222",
                            highlightthickness=1, padx=16, pady=14)
        upg_tile.pack(side=tk.LEFT, padx=4, fill="both", expand=True)

        upg_header = tk.Frame(upg_tile, bg="#151515")
        upg_header.pack(fill="x")
        tk.Label(upg_header, text="upgrades", font=("Arial", 10, "bold"),
                fg="#888", bg="#151515").pack(side=tk.LEFT)
        self.scrap_lbl = tk.Label(upg_header, text=f"scraps: {self.scraps}",
                                 font=("Arial", 10, "bold"),
                                 fg="#f0a030", bg="#151515")
        self.scrap_lbl.pack(side=tk.RIGHT)

        self.upg_btns = {}
        upgs = [
            ("engine", "-10% crash risk", 3, "upg_engine"),
            ("tank", "+25 fuel cap", 2, "upg_tank"),
            ("armor", "-50% damage", 4, "upg_armor"),
            ("turbo", "+1 step/go", 5, "upg_turbo"),
        ]
        for name, desc, cost, attr in upgs:
            f = tk.Frame(upg_tile, bg="#151515")
            f.pack(fill="x", pady=3)
            tk.Label(f, text=f"{name}  ", font=("Arial", 9),
                    fg="#aaa", bg="#151515", width=7, anchor="w").pack(side=tk.LEFT)
            tk.Label(f, text=desc, font=("Arial", 8),
                    fg="#555", bg="#151515").pack(side=tk.LEFT, padx=(0, 6))
            btn = tk.Button(f, text=f"{cost}s", command=lambda a=attr, c=cost: self.buy_upgrade(a, c),
                           font=("Arial", 8), bg="#1a1a1a", fg="#888",
                           bd=0, cursor="hand2", padx=6,
                           highlightthickness=1, highlightbackground="#333")
            btn.pack(side=tk.RIGHT)
            self.upg_btns[attr] = btn

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
        ttk.Button(bf, text="Exit", command=self.on_exit, width=10).pack(side=tk.LEFT, padx=4)

        self.on_speed_change()
        self.update_upg_buttons()
        root.update()
        w = root.winfo_reqwidth() + 40
        h = root.winfo_reqheight() + 20
        root.minsize(w, h)
        root.geometry(f"{w}x{h}")

    # --- persistence ---

    def save_user_data(self):
        users = load_users()
        users[self.username] = {
            "scraps": self.scraps,
            "best_streak": self.best_streak,
            "upg_engine": self.upg_engine,
            "upg_tank": self.upg_tank,
            "upg_armor": self.upg_armor,
            "upg_turbo": self.upg_turbo,
        }
        save_users(users)

    def switch_user(self):
        self.save_user_data()
        self.root.destroy()

    def on_exit(self):
        self.save_user_data()
        self.root.quit()

    # --- mechanics ---

    def speed_data(self, s):
        if s <= 2:
            return 1, 0, False, 0
        elif s <= 4:
            return 2, 5, False, 10
        elif s <= 6:
            return 3, 15, False, 20
        elif s <= 8:
            return 4, 30, False, 30
        else:
            return 5, 50, True, 40

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
        steps, risk, instant, dmg = self.speed_data(s)
        cost = self.speed_fuel_cost(s)
        c = self.speed_color(s)
        risk_display = max(risk - (self.upg_engine * 10), 0)
        label = f"risk: {risk_display}%  |  +{steps + self.upg_turbo}/go  |  -{cost} fuel"
        if dmg > 0:
            label += f"  |  dmg: {dmg}"
        self.kmh_lbl.config(text=f"{kmh} km/h", fg=c)
        self.risk_lbl.config(text=label, fg=c)

    # --- progress bar ---

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

    # --- fuel / hp ---

    def update_fuel(self):
        self.fuel_bar.config(maximum=self.max_fuel)
        self.fuel_bar["value"] = self.fuel
        self.fuel_lbl.config(text=f"fuel: {self.fuel}")

    def update_hp(self):
        self.hp_bar.config(maximum=self.max_hp)
        self.hp_bar["value"] = self.hp
        self.hp_lbl.config(text=f"hp: {self.hp}")

    # --- log ---

    def log(self, msg, color="#ccc"):
        ts = datetime.now().strftime("%H:%M:%S")
        tag = f"c{len(self.term.get('1.0', 'end-1c'))}"
        self.term.tag_configure(tag, foreground=color)
        self.term.config(state="normal")
        self.term.insert("end", f"[{ts}] {msg}\n", tag)
        self.term.see("end")
        self.term.config(state="disabled")

    # --- upgrades ---

    def update_upg_buttons(self):
        for attr, btn in self.upg_btns.items():
            lvl = getattr(self, attr)
            if lvl >= 3:
                btn.config(text="MAX", state="disabled", fg="#555")
            else:
                btn.config(state="normal", fg="#888")

    def buy_upgrade(self, attr, cost):
        lvl = getattr(self, attr)
        if lvl >= 3:
            return
        if self.scraps < cost:
            self.log("not enough scraps", "#e06c75")
            return
        self.scraps -= cost
        setattr(self, attr, lvl + 1)
        if attr == "upg_tank":
            self.max_fuel += 25
            self.fuel = self.max_fuel
            self.update_fuel()
            self.log("tank upgraded! +25 fuel", "#4ec9b0")
        elif attr == "upg_engine":
            self.log("engine upgraded! -10% crash risk", "#4ec9b0")
        elif attr == "upg_armor":
            self.log("armor upgraded! -50% damage", "#4ec9b0")
        elif attr == "upg_turbo":
            self.log("turbo upgraded! +1 step per Go", "#4ec9b0")
        self.scrap_lbl.config(text=f"scraps: {self.scraps}")
        self.update_upg_buttons()
        self.on_speed_change()
        self.save_user_data()

    # --- start / stop / go / nitro ---

    def start(self):
        if self.broken:
            self.log("car is broken! repair it first", "#e06c75")
            return
        if self.s == 1:
            self.log("already running", "#e06c75")
            return
        self.s = 1
        self._p = 0
        self.done = False
        self.hp = self.max_hp
        self.fuel = self.max_fuel
        self.streak = 0
        self.repair_clicks = 0
        s = int(self.speed_val.get())
        c = self.speed_color(s)
        self.go_btn.config(state="normal", fg=c)
        self.nitro_btn.config(state="normal" if self.fuel >= 15 else "disabled", fg="#e06c75")
        self.pct.config(text="0 / 10")
        self.update_fuel()
        self.update_hp()
        self.update_bar()
        self.streak_lbl.config(text=f"streak: 0  |  best: {self.best_streak}")
        self.log("driving", "#4ec9b0")

    def stop(self):
        if self.done or self.broken:
            self.log("already done, press Start to go again", "#555")
            return
        if self.s == 0:
            self.log("already stopped", "#e06c75")
        else:
            self.s = 0
            self.go_btn.config(state="disabled", fg="#555")
            self.nitro_btn.config(state="disabled", fg="#555")
            self._p = 0
            self.pct.config(text="0 / 10")
            self.canvas.coords(self.bar, 0, 200, 36, 200)
            self.log(f"stopped (streak: {self.streak})", "#e06c75")

    def on_go(self):
        if self.s != 1 or self.done or self.broken:
            return
        self._drive(0)

    def on_nitro(self):
        if self.s != 1 or self.done or self.broken:
            return
        if self.fuel < 15:
            self.log("not enough fuel for nitro", "#f0a030")
            return
        self._drive(1)

    def _drive(self, nitro):
        s = int(self.speed_val.get())
        steps, risk, instant, dmg = self.speed_data(s)
        cost = self.speed_fuel_cost(s)
        extra_steps = self.upg_turbo

        if nitro:
            extra_steps += 2
            cost += 15
            if random.randint(1, 100) <= 20:
                dmg_nitro = int(30 * (0.5 if self.upg_armor else 1))
                self.hp = max(self.hp - dmg_nitro, 0)
                self.update_hp()
                self.log(f"nitro backfired! -{dmg_nitro} hp", "#ff4444")
                if self.hp <= 0:
                    self._break_car("nitro blew the engine!")
                    return

        if self.fuel < cost:
            self.log("not enough fuel!", "#f0a030")
            return

        self.fuel = max(self.fuel - cost, 0)
        self.update_fuel()
        self.nitro_btn.config(state="disabled" if self.fuel < 15 else "normal")

        c = self.speed_color(s)
        risk_actual = max(risk - (self.upg_engine * 10), 0)

        if risk_actual > 0 and random.randint(1, 100) <= risk_actual:
            if instant:
                self._break_car(f"engine exploded at {s*10} km/h!")
                return
            else:
                dmg_taken = dmg
                if self.upg_armor:
                    dmg_taken = int(dmg_taken * 0.5)
                self.hp = max(self.hp - dmg_taken, 0)
                self.update_hp()
                self.log(f"damage! -{dmg_taken} hp  ({self.hp}/{self.max_hp})", "#e06c75")
                if self.hp <= 0:
                    self._break_car("car is wrecked!")
                    return

        total_steps = steps + extra_steps
        old = self._p
        self._p = min(self._p + total_steps, 10)
        gained = self._p - old
        self.streak += gained
        if self.streak > self.best_streak:
            self.best_streak = self.streak
        self.streak_lbl.config(text=f"streak: {self.streak}  |  best: {self.best_streak}")
        self.pct.config(text=f"{self._p} / 10")
        self.update_bar()

        label = f"step {self._p}  ({s*10} km/h, -{cost} fuel)"
        if nitro:
            label += "  NITRO!"
        self.log(label, c)

        if self.fuel <= 0:
            self.log("ran out of fuel!", "#f0a030")

        if self._p >= 10:
            self._finish()
            return

        if self.fuel <= 0:
            self._stop_driving("out of fuel")

    def _finish(self):
        self.s = 0
        self.done = True
        self.go_btn.config(state="disabled", fg="#555")
        self.nitro_btn.config(state="disabled", fg="#555")
        self.scraps += 1
        self.scrap_lbl.config(text=f"scraps: {self.scraps}")
        self.log("FINISH! +1 scrap", "#4ec9b0")
        self.save_user_data()

    def _stop_driving(self, reason):
        self.s = 0
        self.done = True
        self.go_btn.config(state="disabled", fg="#555")
        self.nitro_btn.config(state="disabled", fg="#555")

    def _break_car(self, msg):
        self.s = 0
        self.broken = True
        self.done = True
        self.go_btn.config(state="disabled", fg="#555")
        self.nitro_btn.config(state="disabled", fg="#555")
        self.crash_bar()
        self.pct.config(text="💥")
        self.log(msg, "#ff4444")
        self.log("car is broken — click Repair to fix it", "#ff4444")
        self.start_btn.config(state="disabled")
        self.show_repair()

    # --- repair mini-game ---

    def show_repair(self):
        self.repair_clicks = 0
        self.repair_win = tk.Toplevel(self.root)
        self.repair_win.title("repair car")
        self.repair_win.configure(bg="#151515")
        self.repair_win.resizable(False, False)
        self.repair_win.transient(self.root)
        self.repair_win.grab_set()

        tk.Label(self.repair_win, text="REPAIR CAR",
                font=("Arial", 14, "bold"), fg="#4ec9b0",
                bg="#151515").pack(pady=(16, 8))

        tk.Label(self.repair_win, text="click the button 10 times to fix it",
                font=("Arial", 10), fg="#888",
                bg="#151515").pack()

        self.repair_prog = ttk.Progressbar(self.repair_win, length=200,
                                           mode="determinate", maximum=10)
        self.repair_prog.pack(pady=(12, 4))

        self.repair_lbl = tk.Label(self.repair_win, text="0 / 10",
                                  font=("Arial", 11), fg="#aaa",
                                  bg="#151515")
        self.repair_lbl.pack()

        self.repair_hammer = tk.Button(self.repair_win, text="🔨  HIT!",
                                      command=self.repair_click,
                                      font=("Arial", 16, "bold"),
                                      bg="#2d2d2d", fg="#e0e0e0", bd=0,
                                      activebackground="#444", activeforeground="#fff",
                                      cursor="hand2", padx=30, pady=10,
                                      highlightthickness=1, highlightbackground="#444")
        self.repair_hammer.pack(pady=(12, 16))
        self.repair_win.protocol("WM_DELETE_WINDOW", self.repair_closed)

    def repair_click(self):
        self.repair_clicks += 1
        self.repair_prog["value"] = self.repair_clicks
        self.repair_lbl.config(text=f"{self.repair_clicks} / 10")
        if self.repair_clicks >= 10:
            self.repair_win.destroy()
            self.broken = False
            self.hp = self.max_hp
            self.update_hp()
            self.start_btn.config(state="normal")
            self.pct.config(text="0 / 10")
            self.canvas.coords(self.bar, 0, 200, 36, 200)
            self.log("car repaired! ready to drive", "#4ec9b0")

    def repair_closed(self):
        self.repair_win.destroy()
        self.log("repair cancelled — car still broken", "#e06c75")


if __name__ == "__main__":
    root = tk.Tk()
    dlg = UserDialog(root)
    root.wait_window(dlg.win)
    if dlg.selected:
        for w in root.winfo_children():
            w.destroy()
        App(root, dlg.users[dlg.selected], dlg.selected)
        root.mainloop()
