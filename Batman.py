import json
import os
import random
import textwrap
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


# ------------------------------------------------------------
# Batman: Advanced Project
# ------------------------------------------------------------
# Features
# - Sistema de vida/salud para Batman y villanos
# - Sistema de misiones con varios pasos y recompensas
# - Multiguardado con ranuras múltiples (3 slots)
# - GUI moderna con Tkinter
# - ASCII Bat logo intro
# - Batcomputer villain search
# - Explore Gotham (random events)
# - Fight crime (combat with health system)
# ------------------------------------------------------------

SAVE_DIR = "batman_saves"
MAX_SLOTS = 3


@dataclass
class Villain:
    name: str
    threat: int
    hint: str
    max_health: int
    current_health: int
    
    def is_alive(self) -> bool:
        return self.current_health > 0
    
    def take_damage(self, damage: int):
        self.current_health = max(0, self.current_health - damage)
    
    def heal(self, amount: int):
        self.current_health = min(self.max_health, self.current_health + amount)


VILLAINS_DATA = [
    {"name": "Joker", "threat": 9, "hint": "Ríe cuando el caos reina.", "max_health": 100},
    {"name": "Harley Quinn", "threat": 6, "hint": "Acompaña al caos con un mazo.", "max_health": 70},
    {"name": "Two-Face", "threat": 7, "hint": "Todo depende de una moneda.", "max_health": 80},
    {"name": "Riddler", "threat": 8, "hint": "Ama los acertijos, odia las respuestas simples.", "max_health": 75},
    {"name": "Penguin", "threat": 5, "hint": "Sombrilla hoy, crimen mañana.", "max_health": 65},
    {"name": "Bane", "threat": 10, "hint": "El veneno corre por sus venas.", "max_health": 120},
    {"name": "Scarecrow", "threat": 7, "hint": "El miedo es su arma.", "max_health": 60},
]

GADGETS_CATALOG = [
    "Batarang",
    "Grapnel Gun",
    "Smoke Bomb",
    "Explosive Gel",
    "Cryptographic Sequencer",
    "Remote Hacking Device",
    "Line Launcher",
    "Disruptor",
]


@dataclass
class Mission:
    id: str
    name: str
    description: str
    steps: List[str]
    current_step: int = 0
    completed: bool = False
    reward_reputation: int = 5
    reward_gadget: Optional[str] = None
    
    def is_completed(self) -> bool:
        return self.completed
    
    def advance_step(self) -> bool:
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return False
        else:
            self.completed = True
            return True
    
    def get_current_step_description(self) -> str:
        if self.completed:
            return "Misión completada"
        return self.steps[self.current_step]


MISSIONS_DATA = [
    {
        "id": "mission_1",
        "name": "El Caos del Joker",
        "description": "El Joker ha escapado de Arkham y planea un ataque en Gotham.",
        "steps": [
            "Investiga el escape de Arkham Asylum",
            "Rastrea las pistas en el distrito financiero",
            "Intercepta el plan del Joker en el teatro abandonado",
            "Derrota al Joker y sus secuaces"
        ],
        "reward_reputation": 10,
        "reward_gadget": "Remote Hacking Device"
    },
    {
        "id": "mission_2",
        "name": "El Enigma de Riddler",
        "description": "Riddler ha dejado acertijos por toda la ciudad.",
        "steps": [
            "Resuelve el primer acertijo en el reloj de la ciudad",
            "Encuentra la segunda pista en la biblioteca",
            "Descifra el código en el museo",
            "Confronta a Riddler en su guarida"
        ],
        "reward_reputation": 8,
        "reward_gadget": "Cryptographic Sequencer"
    },
    {
        "id": "mission_3",
        "name": "La Moneda de Two-Face",
        "description": "Two-Face está extorsionando a los bancos de Gotham.",
        "steps": [
            "Investiga el primer robo bancario",
            "Protege el segundo banco objetivo",
            "Rastrea a Two-Face hasta su escondite",
            "Detén a Two-Face antes de que escape"
        ],
        "reward_reputation": 7,
        "reward_gadget": "Line Launcher"
    },
]


@dataclass
class Batman:
    name: str = "Batman"
    max_health: int = 100
    current_health: int = 100
    gadgets: List[str] = field(default_factory=lambda: ["Batarang", "Grapnel Gun"])
    reputation: int = 0
    missions: List[Dict[str, Any]] = field(default_factory=list)
    
    def is_alive(self) -> bool:
        return self.current_health > 0
    
    def take_damage(self, damage: int):
        self.current_health = max(0, self.current_health - damage)
    
    def heal(self, amount: int):
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        for m_data in self.missions:
            if m_data.get("id") == mission_id:
                return Mission(**m_data)
        return None
    
    def update_mission(self, mission: Mission):
        for i, m_data in enumerate(self.missions):
            if m_data.get("id") == mission.id:
                self.missions[i] = asdict(mission)
                return
        self.missions.append(asdict(mission))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "max_health": self.max_health,
            "current_health": self.current_health,
            "gadgets": self.gadgets,
            "reputation": self.reputation,
            "missions": self.missions
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Batman":
        return Batman(
            name=data.get("name", "Batman"),
            max_health=data.get("max_health", 100),
            current_health=data.get("current_health", 100),
            gadgets=list(data.get("gadgets", ["Batarang", "Grapnel Gun"])),
            reputation=int(data.get("reputation", 0)),
            missions=list(data.get("missions", []))
        )


# ============================================================
# Funciones de guardado/carga con múltiples ranuras
# ============================================================

def ensure_save_dir():
    """Crea el directorio de guardado si no existe"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def get_slot_path(slot: int) -> str:
    """Obtiene la ruta del archivo de guardado para una ranura"""
    return os.path.join(SAVE_DIR, f"slot_{slot}.json")


def save_game(batman: Batman, slot: int):
    """Guarda el juego en una ranura específica"""
    ensure_save_dir()
    path = get_slot_path(slot)
    save_data = {
        "batman": batman.to_dict(),
        "timestamp": time.time(),
        "slot": slot
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)


def load_game(slot: int) -> Optional[Batman]:
    """Carga el juego desde una ranura específica"""
    path = get_slot_path(slot)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Batman.from_dict(data["batman"])
    except Exception:
        return None


def get_save_info(slot: int) -> Optional[Dict[str, Any]]:
    """Obtiene información sobre un guardado sin cargarlo completamente"""
    path = get_slot_path(slot)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        batman_data = data["batman"]
        return {
            "slot": slot,
            "name": batman_data.get("name", "Batman"),
            "reputation": batman_data.get("reputation", 0),
            "health": f"{batman_data.get('current_health', 100)}/{batman_data.get('max_health', 100)}",
            "timestamp": data.get("timestamp", 0)
        }
    except Exception:
        return None


def delete_save(slot: int):
    """Elimina un guardado de una ranura"""
    path = get_slot_path(slot)
    if os.path.exists(path):
        os.remove(path)


# ============================================================
# Funciones de consola (para modo terminal)
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def bat_logo():
    logo = r"""
          _==/          i     i          \==_
        /XX/            |\___/|            \XX\
      /XXXX\            |XXXXX|            /XXXX\
     |XXXXXX\_         _XXXXXXX_         _/XXXXXX|
    XXXXXXXXXXXxxxxxxxXXXXXXXXXXXxxxxxxxXXXXXXXXXXX
    |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
    XXXXXX__/\_______________________/\__XXXXXXXXX
          \/  \                     /  \/
               \        /\        /
                \______/_ \______/ 
    """
    print(logo)


def header(title: str):
    clear()
    bat_logo()
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60 + "\n")


def pause(msg: str = "Presiona Enter para continuar..."):
    input(f"\n{msg}")


def choose_from_list(options: List[str], prompt: str = "Elige una opción:") -> int | None:
    for i, opt in enumerate(options, 1):
        print(f"[{i}] {opt}")
    choice = input(f"\n{prompt} ")
    if not choice.isdigit():
        return None
    idx = int(choice)
    if 1 <= idx <= len(options):
        return idx - 1
    return None


def view_profile(batman: Batman):
    header("Perfil del Caballero de la Noche")
    print(f"Identidad: {batman.name}")
    print(f"Reputación: {batman.reputation}")
    print("Gadgets:")
    for g in batman.gadgets:
        print(f" - {g}")
    pause()


# ============================================================
# GUI Simple con Tkinter
# ============================================================

class BatmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🦇 Batman: Gotham Defender")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        self.batman: Optional[Batman] = None
        self.current_slot: int = 1
        
        self.show_main_menu()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True)
        
        tk.Label(frame, text="🦇 BATMAN 🦇", font=("Arial", 28, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=30)
        
        tk.Button(frame, text="Nueva Partida", font=("Arial", 14), bg="#ffd700", 
                  width=20, height=2, command=self.new_game).pack(pady=10)
        tk.Button(frame, text="Cargar Partida", font=("Arial", 14), bg="#4a90e2", 
                  fg="white", width=20, height=2, command=self.load_menu).pack(pady=10)
        tk.Button(frame, text="Salir", font=("Arial", 14), bg="#2d2d2d", 
                  fg="white", width=20, height=2, command=self.root.quit).pack(pady=10)
    
    def new_game(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True)
        
        tk.Label(frame, text="Nueva Partida", font=("Arial", 20, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=20)
        tk.Label(frame, text="Nombre:", font=("Arial", 12), 
                 bg="#1a1a1a", fg="white").pack()
        
        name_entry = tk.Entry(frame, font=("Arial", 14), width=25)
        name_entry.insert(0, "Batman")
        name_entry.pack(pady=10)
        
        def create():
            self.batman = Batman(name=name_entry.get() or "Batman")
            save_game(self.batman, self.current_slot)
            self.show_hub()
        
        tk.Button(frame, text="Crear", font=("Arial", 12), bg="#ffd700", 
                  width=15, command=create).pack(pady=20)
        tk.Button(frame, text="Volver", font=("Arial", 12), bg="#2d2d2d", 
                  fg="white", width=15, command=self.show_main_menu).pack()
    
    def load_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True)
        
        tk.Label(frame, text="Cargar Partida", font=("Arial", 20, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=20)
        
        for i in range(1, MAX_SLOTS + 1):
            info = get_save_info(i)
            if info:
                text = f"Slot {i}: {info['name']} (Rep: {info['reputation']}, HP: {info['health']})"
                cmd = lambda s=i: self.load_slot(s)
                tk.Button(frame, text=text, font=("Arial", 11), bg="#4a90e2", 
                          fg="white", width=50, command=cmd).pack(pady=5)
        
        tk.Button(frame, text="Volver", font=("Arial", 12), bg="#2d2d2d", 
                  fg="white", width=15, command=self.show_main_menu).pack(pady=20)
    
    def load_slot(self, slot):
        loaded = load_game(slot)
        if loaded:
            self.batman = loaded
            self.current_slot = slot
            self.show_hub()
        else:
            messagebox.showerror("Error", "No se pudo cargar")
    
    def show_hub(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Stats
        stats = tk.Frame(frame, bg="#2d2d2d", relief="ridge", bd=2)
        stats.pack(fill="x", pady=5)
        tk.Label(stats, text=f"🦇 {self.batman.name} | ❤️ {self.batman.current_health}/{self.batman.max_health} | ⭐ {self.batman.reputation}", 
                 font=("Arial", 12), bg="#2d2d2d", fg="white").pack(pady=5)
        
        tk.Label(frame, text="BATICUEVA", font=("Arial", 18, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=15)
        
        # Botones
        buttons = [
            ("👤 Perfil", self.show_profile),
            ("💻 Batcomputadora", self.show_batcomputer),
            ("🔧 Gadgets", self.show_gadgets),
            ("🏙️ Explorar", self.explore),
            ("⚔️ Combate", self.combat),
            ("📋 Misiones", self.show_missions),
            ("💾 Guardar", self.save),
            ("🚪 Salir", self.show_main_menu),
        ]
        
        grid = tk.Frame(frame, bg="#1a1a1a")
        grid.pack(expand=True)
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(grid, text=text, font=("Arial", 12, "bold"), bg="#4a90e2", 
                      fg="white", width=18, height=2, command=cmd).grid(
                      row=i//2, column=i%2, padx=10, pady=10)
    
    def show_profile(self):
        info = f"Identidad: {self.batman.name}\nSalud: {self.batman.current_health}/{self.batman.max_health}\nReputación: {self.batman.reputation}\n\nGadgets:\n"
        info += "\n".join(f"• {g}" for g in self.batman.gadgets)
        messagebox.showinfo("Perfil", info)
    
    def show_batcomputer(self):
        info = "VILLANOS DE GOTHAM:\n\n"
        for v in VILLAINS_DATA:
            info += f"{v['name']} - Amenaza: {v['threat']}/10\n{v['hint']}\n\n"
        messagebox.showinfo("Batcomputadora", info)
    
    def show_gadgets(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True)
        
        tk.Label(frame, text="🔧 GADGETS", font=("Arial", 18, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=20)
        
        for gadget in GADGETS_CATALOG:
            equipped = gadget in self.batman.gadgets
            bg = "#2d2d2d" if equipped else "#4a90e2"
            text = f"✓ {gadget}" if equipped else gadget
            
            def equip(g=gadget):
                if g not in self.batman.gadgets:
                    self.batman.gadgets.append(g)
                    save_game(self.batman, self.current_slot)
                    self.show_gadgets()
            
            tk.Button(frame, text=text, font=("Arial", 11), bg=bg, fg="white", 
                      width=30, command=equip).pack(pady=3)
        
        tk.Button(frame, text="Volver", font=("Arial", 12), bg="#2d2d2d", 
                  fg="white", width=15, command=self.show_hub).pack(pady=20)
    
    def explore(self):
        events = [
            "Te deslizas entre azoteas bajo la lluvia.",
            "Encuentras una pista del Joker.",
            "La Batseñal ilumina el cielo.",
            "Catwoman cruza tu camino.",
        ]
        msg = random.choice(events)
        
        if random.random() < 0.3:
            self.batman.reputation += 1
            msg += "\n\n+1 Reputación"
        if random.random() < 0.2:
            heal = random.randint(5, 15)
            self.batman.heal(heal)
            msg += f"\n+{heal} Salud"
        
        save_game(self.batman, self.current_slot)
        messagebox.showinfo("Exploración", msg)
        self.show_hub()
    
    def combat(self):
        v_data = random.choice(VILLAINS_DATA)
        villain = Villain(v_data["name"], v_data["threat"], v_data["hint"], 
                         v_data["max_health"], v_data["max_health"])
        
        while self.batman.is_alive() and villain.is_alive():
            # Batman ataca
            dmg = random.randint(10, 25) + len(self.batman.gadgets)
            villain.take_damage(dmg)
            
            if not villain.is_alive():
                self.batman.reputation += villain.threat
                save_game(self.batman, self.current_slot)
                messagebox.showinfo("Victoria", f"¡Derrotaste a {villain.name}!\n+{villain.threat} Reputación")
                self.show_hub()
                return
            
            # Villano ataca
            dmg = random.randint(5, 15) + villain.threat
            self.batman.take_damage(dmg)
            
            if not self.batman.is_alive():
                self.batman.current_health = self.batman.max_health // 2
                save_game(self.batman, self.current_slot)
                messagebox.showwarning("Derrota", "Has sido derrotado...")
                self.show_hub()
                return
            
            # Mostrar estado
            if messagebox.askyesno("Combate", 
                f"Tu salud: {self.batman.current_health}/{self.batman.max_health}\n"
                f"{villain.name}: {villain.current_health}/{villain.max_health}\n\n"
                "¿Continuar atacando?"):
                continue
            else:
                self.show_hub()
                return
    
    def show_missions(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(frame, text="📋 MISIONES", font=("Arial", 18, "bold"), 
                 bg="#1a1a1a", fg="#ffd700").pack(pady=20)
        
        for m_data in MISSIONS_DATA:
            mission = self.batman.get_mission_by_id(m_data["id"]) or Mission(**m_data)
            
            mf = tk.Frame(frame, bg="#2d2d2d", relief="ridge", bd=2)
            mf.pack(fill="x", pady=5)
            
            status = "✓" if mission.completed else f"{mission.current_step+1}/{len(mission.steps)}"
            tk.Label(mf, text=f"{mission.name} [{status}]", font=("Arial", 11, "bold"), 
                     bg="#2d2d2d", fg="#ffd700").pack(anchor="w", padx=10, pady=5)
            tk.Label(mf, text=mission.description, font=("Arial", 9), 
                     bg="#2d2d2d", fg="white").pack(anchor="w", padx=10)
            
            if not mission.completed:
                def advance(m=mission):
                    done = m.advance_step()
                    if done:
                        self.batman.reputation += m.reward_reputation
                        if m.reward_gadget and m.reward_gadget not in self.batman.gadgets:
                            self.batman.gadgets.append(m.reward_gadget)
                        messagebox.showinfo("¡Completada!", 
                            f"{m.name}\n+{m.reward_reputation} Rep\n{m.reward_gadget or ''}")
                    self.batman.update_mission(m)
                    save_game(self.batman, self.current_slot)
                    self.show_missions()
                
                tk.Button(mf, text="Avanzar", font=("Arial", 9), bg="#4a90e2", 
                          fg="white", command=advance).pack(anchor="w", padx=10, pady=5)
        
        tk.Button(frame, text="Volver", font=("Arial", 12), bg="#2d2d2d", 
                  fg="white", width=15, command=self.show_hub).pack(pady=20)
    
    def save(self):
        save_game(self.batman, self.current_slot)
        messagebox.showinfo("Guardado", f"Partida guardada en Slot {self.current_slot}")


def main():
    root = tk.Tk()
    app = BatmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

