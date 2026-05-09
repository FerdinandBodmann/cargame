import tkinter as tk
from tkinter import ttk
from datetime import datetime


class App:
    def __init__(self, root):
        self.root = root
        self.s = 0
        self._p = 0

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
        style.configure("Green.Vertical.TProgressbar",
                        background="#4ec9b0", troughcolor="#1a1a1a", bordercolor="#1a1a1a")

        main = ttk.Frame(root, padding=28)
        main.pack()

        ttk.Label(main, text="drive",
                 font=("Arial", 13, "bold"), foreground="#e0e0e0").pack(anchor="w")

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(10, 20))

        mid = ttk.Frame(main)
        mid.pack(fill="x")

        bar_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222", highlightthickness=1, padx=24, pady=20)
        bar_tile.pack(side=tk.LEFT, padx=(0, 8))

        self.progress = ttk.Progressbar(bar_tile, length=180, mode="determinate",
                                        maximum=10, orient="vertical",
                                        style="Green.Vertical.TProgressbar")
        self.progress.pack()
        self.pct = ttk.Label(bar_tile, text="0 / 10",
                            font=("Arial", 11), foreground="#666", width=7)
        self.pct.pack(pady=(8, 0))

        term_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222", highlightthickness=1, padx=0, pady=0)
        term_tile.pack(side=tk.LEFT, padx=4, fill="both", expand=True)

        self.term = tk.Text(term_tile, width=38, height=10,
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

        prompt_tile = tk.Frame(mid, bg="#151515", highlightbackground="#222", highlightthickness=1, padx=20, pady=20)
        prompt_tile.pack(side=tk.LEFT, padx=(8, 0))

        self.prompt_lbl = tk.Label(prompt_tile, text="waiting",
                                   font=("Arial", 11), fg="#555",
                                   bg="#151515")
        self.prompt_lbl.pack()

        pf = tk.Frame(prompt_tile, bg="#151515")
        pf.pack(pady=(10, 0))
        self.yes_btn = tk.Button(pf, text="Yes", command=self.on_yes, width=8,
                                bg="#1a1a1a", fg="#cccccc", bd=0,
                                activebackground="#2a2a2a", activeforeground="#ccc",
                                font=("Arial", 10), cursor="hand2",
                                highlightthickness=1, highlightbackground="#333")
        self.yes_btn.pack(side=tk.LEFT, padx=3)
        self.no_btn = tk.Button(pf, text="No", command=self.on_no, width=8,
                               bg="#1a1a1a", fg="#cccccc", bd=0,
                               activebackground="#2a2a2a", activeforeground="#ccc",
                               font=("Arial", 10), cursor="hand2",
                               highlightthickness=1, highlightbackground="#333")
        self.no_btn.pack(side=tk.LEFT, padx=3)

        self.prompt_lbl.config(fg="#555", text="waiting")
        self.yes_btn.config(state="disabled", fg="#555")
        self.no_btn.config(state="disabled", fg="#555")

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(20, 14))

        bf = ttk.Frame(main)
        bf.pack()
        self.start_btn = ttk.Button(bf, text="Start", command=self.start, width=10)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = ttk.Button(bf, text="Stop", command=self.stop, width=10)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        ttk.Button(bf, text="Exit", command=root.quit, width=10).pack(side=tk.LEFT, padx=4)

        self._cb = None

        root.update()
        w = root.winfo_reqwidth() + 20
        h = root.winfo_reqheight() + 20
        root.minsize(w, h)
        root.geometry(f"{w}x{h}")

    def log(self, msg, color="#ccc"):
        ts = datetime.now().strftime("%H:%M:%S")
        tag = f"c{len(self.term.get('1.0', 'end-1c'))}"
        self.term.tag_configure(tag, foreground=color)
        self.term.config(state="normal")
        self.term.insert("end", f"[{ts}] {msg}\n", tag)
        self.term.see("end")
        self.term.config(state="disabled")

    def prompt(self, text, cb):
        self._cb = cb
        self.prompt_lbl.config(text=text, fg="#cccccc")
        self.yes_btn.config(state="normal", fg="#cccccc")
        self.no_btn.config(state="normal", fg="#cccccc")

    def hide_prompt(self):
        self.prompt_lbl.config(text="waiting", fg="#555")
        self.yes_btn.config(state="disabled", fg="#555")
        self.no_btn.config(state="disabled", fg="#555")
        self._cb = None

    def on_yes(self):
        if self._cb:
            cb = self._cb
            self.hide_prompt()
            cb(True)

    def on_no(self):
        if self._cb:
            cb = self._cb
            self.hide_prompt()
            cb(False)

    def start(self):
        if self.s == 1:
            self.log("already running", "#e06c75")
            return
        self.prompt("drive?", self._on_drive)

    def _on_drive(self, yes):
        if not yes:
            self.log("idle", "#555")
            return
        self.s = 1
        self._p = 0
        self.log("driving", "#4ec9b0")
        self._step()

    def _step(self):
        if self.s != 1:
            return
        self._p += 1
        self.progress["value"] = self._p
        self.pct.config(text=f"{self._p} / 10")
        if self._p >= 10:
            self.s = 0
            self.progress["value"] = 0
            self.pct.config(text="0 / 10")
            self.log("done", "#4ec9b0")
            return
        self.prompt("continue?", self._on_cont)

    def _on_cont(self, yes):
        if yes:
            self.log(f"step {self._p + 1}", "#4ec9b0")
            self._step()
        else:
            self.s = 0
            self.progress["value"] = 0
            self.pct.config(text="0 / 10")
            self.log("stopped", "#e06c75")

    def stop(self):
        if self.s == 0:
            self.log("already stopped", "#e06c75")
        else:
            self.s = 0
            self.progress["value"] = 0
            self.pct.config(text="0 / 10")
            self.log("stopped", "#e06c75")
            self.hide_prompt()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
