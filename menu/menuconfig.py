# --- valorant_skin_changer.py ---
# DECOY: Fake Valorant Skin Changer
# This is a visual facade. It does NOT modify game memory.
# Compile with: pyinstaller --onefile --noconsole valorant_skin_changer.py

import os
import sys
import json
import time
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Fake "encrypted" config
_CONFIG = {
    "version": "v4.2.1 By Saturn",
    "build": "2026.06.28-r7",
    "api_endpoint": "https://api.valorant-skins.internal/v2/swap",
    "auth_token": "eyJhbGciOiJIUzI1NiIs...",
    "skin_db_revision": "rev_2026_06_28_8847",
    "injection_method": "KernelAPC-Hybrid",
    "driver_loaded": False,
    "vanguard_bypass": "Ring0-Shadow",
    "cache_dir": os.path.join(os.environ.get("LOCALAPPDATA", "."), "ValorantSkinChanger", "cache"),
    "log_file": os.path.join(os.environ.get("LOCALAPPDATA", "."), "ValorantSkinChanger", "runtime.log"),
}

_WEAPON_SKINS = {
    "Vandal": ["Prime Vandal", "Reaver Vandal", "Glitchpop Vandal", "Champions 2023", "Sentinels of Light", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite", "Evori Dreamwings"],
    "Phantom": ["Prime Phantom", "Reaver Phantom", "Glitchpop Phantom", "Champions 2022", "Sentinels of Light", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite", "Evori Dreamwings"],
    "Operator": ["Prime Operator", "Reaver Operator", "Glitchpop Operator", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Sheriff": ["Prime Sheriff", "Reaver Sheriff", "Glitchpop Sheriff", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Classic": ["Prime Classic", "Reaver Classic", "Glitchpop Classic", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Ghost": ["Prime Ghost", "Reaver Ghost", "Glitchpop Ghost", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Spectre": ["Prime Spectre", "Reaver Spectre", "Glitchpop Spectre", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Judge": ["Prime Judge", "Reaver Judge", "Glitchpop Judge", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Bulldog": ["Prime Bulldog", "Reaver Bulldog", "Glitchpop Bulldog", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Guardian": ["Prime Guardian", "Reaver Guardian", "Glitchpop Guardian", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Marshal": ["Prime Marshal", "Reaver Marshal", "Glitchpop Marshal", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Bucky": ["Prime Bucky", "Reaver Bucky", "Glitchpop Bucky", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Frenzy": ["Prime Frenzy", "Reaver Frenzy", "Glitchpop Frenzy", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Shorty": ["Prime Shorty", "Reaver Shorty", "Glitchpop Shorty", "Elderflame", "Sovereign", "Oni", "Ego", "Forsaken", "Gaia's Vengeance", "ChronoVoid", "Prelude to Chaos", "Magepunk", "Neptune", "RGX 11z Pro", "BlastX", "Origin", "Spectrum", "Tigris", "Luna", "Abyssal", "Araxys", "Kuronami", "Mystbloom", "Ignite"],
    "Knife": ["Prime Axe", "Reaver Knife", "Glitchpop Dagger", "Elderflame Dagger", "Sovereign Sword", "Oni Claw", "Ego Knife", "Forsaken Ritual Blade", "Gaia's Wrath", "ChronoVoid Sword", "Prelude to Chaos Blade", "Magepunk Electroblade", "Neptune Anchor", "RGX 11z Pro Blade", "BlastX Polymer Knife", "Origin Crescent Blade", "Spectrum Waveform", "Tigris Fang", "Luna's Descent", "Abyssal Scythe", "Araxys Bio-Collector", "Kuronami Kunai", "Mystbloom Petal Wand", "Ignite Fan", "Evori Dreamwings Staff"],
}

_KNIFE_VARIANTS = {
    "Prime Axe": ["Default", "Gold", "Green", "Orange"],
    "Reaver Knife": ["Default", "Red", "Black", "White"],
    "Glitchpop Dagger": ["Default", "Blue", "Gold", "Red"],
    "Elderflame Dagger": ["Default", "Blue", "Dark", "Red"],
    "Oni Claw": ["Default", "Black", "Green", "White"],
    "RGX 11z Pro Blade": ["Default", "Red", "Blue", "Yellow", "Green"],
    "Champions 2022": ["Default", "Gold"],
    "Champions 2023": ["Default", "Gold"],
}

_RARITY_COLORS = {
    "Select": "#b0b0b0",
    "Deluxe": "#3a8c3a",
    "Premium": "#3a7cc4",
    "Exclusive": "#d44fd4",
    "Ultra": "#e6a817",
    "Melee": "#ff4444",
}

def _log_event(msg: str):
    os.makedirs(os.path.dirname(_CONFIG["log_file"]), exist_ok=True)
    with open(_CONFIG["log_file"], "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def _fake_scan_processes():
    """Simulate process scanning for Vanguard."""
    processes = ["vgc.exe", "vgk.sys", "VALORANT-Win64-Shipping.exe", "RiotGamesApi.exe"]
    for proc in processes:
        time.sleep(random.uniform(0.1, 0.4))
        _log_event(f"SCAN: {proc} -> signature_valid={random.choice([True, True, True, False])}")
    return True

def _fake_inject_driver():
    """Simulate kernel driver injection sequence."""
    steps = [
        ("Allocating non-paged pool memory...", 0.3),
        ("Mapping driver image to kernel space...", 0.5),
        ("Patching DriverObject dispatch table...", 0.4),
        ("Hooking NtCreateFile via SSDT shadow...", 0.6),
        ("Bypassing PatchGuard integrity check...", 0.8),
        ("Establishing APC queue for user-mode callback...", 0.4),
        ("Driver loaded. Handle: 0x%08X" % random.randint(0x1000, 0xFFFF), 0.2),
    ]
    return steps

class SkinChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Valorant Skin Changer {_CONFIG['version']}")
        self.root.geometry("900x650")
        self.root.configure(bg="#0f0f0f")
        self.root.resizable(False, False)
        
        self.selected_weapon = tk.StringVar(value="Vandal")
        self.selected_skin = tk.StringVar()
        self.selected_variant = tk.StringVar(value="Default")
        self.injection_active = False
        
        self._build_ui()
        _log_event("UI initialized")
    
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#0f0f0f", height=60)
        header.pack(fill="x", padx=10, pady=5)
        
        tk.Label(header, text="VALORANT", font=("Arial Black", 24), fg="#ff4655", bg="#0f0f0f").pack(side="left")
        tk.Label(header, text=f"SKIN CHANGER  {_CONFIG['version']}", font=("Arial", 14), fg="#ffffff", bg="#0f0f0f").pack(side="left", padx=10)
        
        status_frame = tk.Frame(header, bg="#0f0f0f")
        status_frame.pack(side="right")
        
        self.status_dot = tk.Canvas(status_frame, width=12, height=12, bg="#0f0f0f", highlightthickness=0)
        self.status_dot.pack(side="left")
        self.status_dot.create_oval(2, 2, 10, 10, fill="#ff4444", tags="dot")
        
        self.status_label = tk.Label(status_frame, text="OFFLINE", font=("Consolas", 10), fg="#ff4444", bg="#0f0f0f")
        self.status_label.pack(side="left", padx=5)
        
        # Main content
        content = tk.Frame(self.root, bg="#0f0f0f")
        content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel: Weapon list
        left = tk.Frame(content, bg="#1a1a1a", width=200)
        left.pack(side="left", fill="y", padx=5)
        left.pack_propagate(False)
        
        tk.Label(left, text="WEAPONS", font=("Arial Black", 12), fg="#ff4655", bg="#1a1a1a").pack(pady=10)
        
        weapon_list = tk.Listbox(left, bg="#1a1a1a", fg="#ffffff", font=("Consolas", 11),
                                  selectbackground="#ff4655", selectforeground="#ffffff",
                                  borderwidth=0, highlightthickness=0)
        for weapon in _WEAPON_SKINS.keys():
            weapon_list.insert("end", f"  {weapon}")
        weapon_list.pack(fill="both", expand=True, padx=5, pady=5)
        weapon_list.bind("<<ListboxSelect>>", self._on_weapon_select)
        self.weapon_list = weapon_list
        
        # Center panel: Skin grid
        center = tk.Frame(content, bg="#1a1a1a")
        center.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(center, text="AVAILABLE SKINS", font=("Arial Black", 12), fg="#ff4655", bg="#1a1a1a").pack(pady=10)
        
        self.skin_canvas = tk.Canvas(center, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(center, orient="vertical", command=self.skin_canvas.yview)
        self.skin_frame = tk.Frame(self.skin_canvas, bg="#1a1a1a")
        
        self.skin_frame.bind("<Configure>", lambda e: self.skin_canvas.configure(scrollregion=self.skin_canvas.bbox("all")))
        self.skin_canvas.create_window((0, 0), window=self.skin_frame, anchor="nw")
        self.skin_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.skin_canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        # Right panel: Controls
        right = tk.Frame(content, bg="#1a1a1a", width=220)
        right.pack(side="right", fill="y", padx=5)
        right.pack_propagate(False)
        
        tk.Label(right, text="CONTROLS", font=("Arial Black", 12), fg="#ff4655", bg="#1a1a1a").pack(pady=10)
        
        # Selected skin display
        self.preview_frame = tk.Frame(right, bg="#0f0f0f", height=120)
        self.preview_frame.pack(fill="x", padx=10, pady=5)
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = tk.Label(self.preview_frame, text="No skin selected", 
                                       font=("Consolas", 10), fg="#888888", bg="#0f0f0f", wraplength=180)
        self.preview_label.pack(expand=True)
        
        # Variant selector
        tk.Label(right, text="VARIANT", font=("Arial Black", 10), fg="#ffffff", bg="#1a1a1a").pack(pady=(15, 5))
        self.variant_combo = ttk.Combobox(right, textvariable=self.selected_variant, 
                                          state="readonly", font=("Consolas", 10))
        self.variant_combo.pack(fill="x", padx=10)
        
        # Action buttons
        btn_style = {"font": ("Arial Black", 11), "fg": "#ffffff", "borderwidth": 0, 
                     "highlightthickness": 0, "cursor": "hand2"}
        
        self.inject_btn = tk.Button(right, text="INJECT SKIN", bg="#ff4655", 
                                    command=self._inject_skin, **btn_style)
        self.inject_btn.pack(fill="x", padx=10, pady=(20, 5), ipady=8)
        
        self.bypass_btn = tk.Button(right, text="BYPASS VANGUARD", bg="#444444",
                                    command=self._bypass_vanguard, **btn_style)
        self.bypass_btn.pack(fill="x", padx=10, pady=5, ipady=8)
        
        self.refresh_btn = tk.Button(right, text="REFRESH SKIN DB", bg="#2a2a2a",
                                     command=self._refresh_db, **btn_style)
        self.refresh_btn.pack(fill="x", padx=10, pady=5, ipady=8)
        
        # Console output
        tk.Label(right, text="CONSOLE", font=("Arial Black", 10), fg="#ffffff", bg="#1a1a1a").pack(pady=(15, 5))
        self.console = tk.Text(right, bg="#0f0f0f", fg="#00ff00", font=("Consolas", 8),
                               height=10, borderwidth=0, highlightthickness=0, state="disabled")
        self.console.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Footer
        footer = tk.Frame(self.root, bg="#0f0f0f", height=30)
        footer.pack(fill="x", padx=10, pady=5)
        
        self.footer_label = tk.Label(footer, text=f"Build: {_CONFIG['build']} | Skin DB: {_CONFIG['skin_db_revision']}", 
                                      font=("Consolas", 8), fg="#555555", bg="#0f0f0f")
        self.footer_label.pack(side="left")
        
        self.prog_label = tk.Label(footer, text="", font=("Consolas", 8), fg="#ff4655", bg="#0f0f0f")
        self.prog_label.pack(side="right")
        
        # Initialize with Vandal skins
        self._populate_skins("Vandal")
    
    def _console_log(self, msg: str):
        self.console.configure(state="normal")
        self.console.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")
        _log_event(msg)
    
    def _on_weapon_select(self, event):
        selection = self.weapon_list.curselection()
        if selection:
            weapon = self.weapon_list.get(selection[0]).strip()
            self.selected_weapon.set(weapon)
            self._populate_skins(weapon)
            self._console_log(f"Selected weapon: {weapon}")
    
    def _populate_skins(self, weapon: str):
        for widget in self.skin_frame.winfo_children():
            widget.destroy()
        
        skins = _WEAPON_SKINS.get(weapon, [])
        for i, skin in enumerate(skins):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(self.skin_frame, text=skin, font=("Consolas", 9),
                           bg="#2a2a2a", fg="#ffffff", borderwidth=0,
                           highlightthickness=0, width=18, height=2,
                           command=lambda s=skin: self._select_skin(s))
            btn.grid(row=row, column=col, padx=3, pady=3)
            
            # Fake rarity indicator
            rarity = random.choice(list(_RARITY_COLORS.keys()))
            btn.configure(fg=_RARITY_COLORS[rarity])
    
    def _select_skin(self, skin: str):
        self.selected_skin.set(skin)
        self.preview_label.configure(text=f"{self.selected_weapon.get()}\n{skin}", fg="#ffffff")
        
        # Populate variants
        variants = _KNIFE_VARIANTS.get(skin, ["Default"])
        self.variant_combo.configure(values=variants)
        self.selected_variant.set(variants[0])
        
        self._console_log(f"Skin selected: {skin} ({self.selected_variant.get()})")
    
    def _inject_skin(self):
        if not self.selected_skin.get():
            messagebox.showwarning("No Selection", "Select a skin first.")
            return
        
        if self.injection_active:
            messagebox.showwarning("Busy", "Injection already in progress.")
            return
        
        self.injection_active = True
        self.inject_btn.configure(bg="#888888", text="INJECTING...")
        self._console_log("Starting skin injection sequence...")
        
        def inject_thread():
            steps = [
                ("Initializing Vanguard bypass module...", 0.8),
                ("Scanning for VALORANT-Win64-Shipping.exe...", 1.2),
                ("Process found. PID: %d" % random.randint(4000, 9000), 0.5),
                ("Allocating memory in target process...", 0.6),
                ("Writing skin swap payload...", 0.7),
                ("Patching weapon ID in entity array...", 0.9),
                ("Verifying checksum integrity...", 0.4),
                ("Skin applied successfully.", 0.3),
            ]
            
            for msg, delay in steps:
                self.root.after(0, lambda m=msg: self._console_log(m))
                self.root.after(0, lambda m=msg: self.prog_label.configure(text=m))
                time.sleep(delay)
            
            self.root.after(0, self._injection_complete)
        
        threading.Thread(target=inject_thread, daemon=True).start()
    
    def _injection_complete(self):
        self.injection_active = False
        self.inject_btn.configure(bg="#ff4655", text="INJECT SKIN")
        self.prog_label.configure(text="READY")
        self._console_log("Injection complete. Skin active in-game.")
        messagebox.showinfo("Success", f"Applied {self.selected_skin.get()} to {self.selected_weapon.get()}")
    
    def _bypass_vanguard(self):
        self.bypass_btn.configure(bg="#888888", text="BYPASSING...")
        self._console_log("Initiating Vanguard bypass sequence...")
        
        def bypass_thread():
            _fake_scan_processes()
            
            steps = _fake_inject_driver()
            for msg, delay in steps:
                self.root.after(0, lambda m=msg: self._console_log(m))
                time.sleep(delay)
            
            self.root.after(0, lambda: self.status_dot.itemconfig("dot", fill="#00ff00"))
            self.root.after(0, lambda: self.status_label.configure(text="VANGUARD BYPASSED", fg="#00ff00"))
            self.root.after(0, lambda: self.bypass_btn.configure(bg="#444444", text="BYPASS VANGUARD"))
            self.root.after(0, lambda: self._console_log("Vanguard bypass active. Kernel driver loaded."))
            self.root.after(0, lambda: messagebox.showinfo("Bypass Active", "Vanguard kernel hooks disabled.\nSkin injection enabled."))
        
        threading.Thread(target=bypass_thread, daemon=True).start()
    
    def _refresh_db(self):
        self._console_log("Fetching latest skin database from API...")
        self.refresh_btn.configure(bg="#888888", text="REFRESHING...")
        
        def refresh_thread():
            time.sleep(2.5)
            _CONFIG["skin_db_revision"] = f"rev_{datetime.now().strftime('%Y_%m_%d_%H%M')}"
            self.root.after(0, lambda: self.footer_label.configure(
                text=f"Build: {_CONFIG['build']} | Skin DB: {_CONFIG['skin_db_revision']}"))
            self.root.after(0, lambda: self.refresh_btn.configure(bg="#2a2a2a", text="REFRESH SKIN DB"))
            self.root.after(0, lambda: self._console_log(f"Skin DB updated. {_CONFIG['skin_db_revision']}"))
        
        threading.Thread(target=refresh_thread, daemon=True).start()


def main():
    os.makedirs(_CONFIG["cache_dir"], exist_ok=True)
    _log_event("=" * 50)
    _log_event("Valorant Skin Changer started")
    _log_event(f"Version: {_CONFIG['version']}")
    _log_event(f"Build: {_CONFIG['build']}")
    _log_event(f"Injection method: {_CONFIG['injection_method']}")
    _log_event(f"Vanguard bypass: {_CONFIG['vanguard_bypass']}")
    _log_event("=" * 50)
    
    root = tk.Tk()
    app = SkinChangerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()