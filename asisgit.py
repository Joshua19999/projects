import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import os
import threading
from datetime import datetime

class AsistenteGitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Git/GitHub")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        if not self.verificar_git():
            messagebox.showerror("Error", "Git no está instalado.\nInstala desde: https://git-scm.com/downloads")
            self.root.destroy()
            return
        
        self.crear_interfaz()
        self.actualizar_directorio_actual()
        self.mostrar_bienvenida()
    
    def verificar_git(self):
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def crear_interfaz(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=6, relief="flat", background="#4a90e2")
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(2, weight=1)
        
        titulo = tk.Label(main_frame, text="🚀 ASISTENTE GIT/GITHUB", 
                         font=('Arial', 18, 'bold'), bg='#2b2b2b', fg='#4a90e2')
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, text="📁 Directorio:").grid(row=0, column=0, padx=5)
        self.dir_label = tk.Label(dir_frame, text="", bg='#3a3a3a', fg='white', 
                                  anchor='w', padx=5, pady=5, relief='sunken')
        self.dir_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(dir_frame, text="Cambiar", command=self.cambiar_directorio).grid(row=0, column=2, padx=5)
        
        # Frame izquierdo para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(0, 5))
        
        self.crear_tab_basico()
        self.crear_tab_ramas()
        self.crear_tab_remoto()
        self.crear_tab_utilidades()
        
        # Frame derecho para consola
        console_container = ttk.Frame(main_frame)
        console_container.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(5, 0))
        console_container.columnconfigure(0, weight=1)
        console_container.rowconfigure(0, weight=1)
        
        output_frame = ttk.LabelFrame(console_container, text="📋 Consola de Comandos Git", padding="5")
        output_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=60,
                                                     bg='#1e1e1e', fg='#00ff00',
                                                     font=('Consolas', 9), wrap=tk.WORD,
                                                     insertbackground='white')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags para colores
        self.output_text.tag_config('comando', foreground='#00d4ff', font=('Consolas', 9, 'bold'))
        self.output_text.tag_config('exito', foreground='#00ff00')
        self.output_text.tag_config('error', foreground='#ff4444')
        self.output_text.tag_config('advertencia', foreground='#ffaa00')
        self.output_text.tag_config('info', foreground='#aaaaaa')
        self.output_text.tag_config('timestamp', foreground='#888888', font=('Consolas', 8))
        
        # Botones debajo de la consola
        btn_frame = ttk.Frame(console_container)
        btn_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text="🔄 Actualizar Estado", 
                  command=self.actualizar_estado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Limpiar", 
                  command=self.limpiar_salida).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Salir", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def crear_tab_basico(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Básico")
        
        canvas = tk.Canvas(tab, bg='#2b2b2b', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        config_frame = ttk.LabelFrame(scrollable_frame, text="⚙️ Configuración", padding="10")
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(config_frame, text="Configurar Usuario y Email", 
                  command=self.configurar_usuario, width=30).pack(pady=3)
        ttk.Button(config_frame, text="Ver Configuración", 
                  command=lambda: self.ejecutar_comando('git config --list'), width=30).pack(pady=3)
        
        repo_frame = ttk.LabelFrame(scrollable_frame, text="📁 Repositorio", padding="10")
        repo_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(repo_frame, text="Inicializar (git init)", 
                  command=lambda: self.ejecutar_comando('git init'), width=30).pack(pady=3)
        ttk.Button(repo_frame, text="Ver Estado (git status)", 
                  command=lambda: self.ejecutar_comando('git status'), width=30).pack(pady=3)
        
        add_frame = ttk.LabelFrame(scrollable_frame, text="➕ Agregar", padding="10")
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(add_frame, text="Agregar Todos (git add .)", 
                  command=lambda: self.ejecutar_comando('git add .'), width=30).pack(pady=3)
        ttk.Button(add_frame, text="Agregar Archivo Específico", 
                  command=self.agregar_archivo_especifico, width=30).pack(pady=3)
        
        commit_frame = ttk.LabelFrame(scrollable_frame, text="💾 Commit", padding="10")
        commit_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(commit_frame, text="Mensaje:").pack(anchor='w')
        self.commit_entry = ttk.Entry(commit_frame, width=40)
        self.commit_entry.pack(fill=tk.X, pady=3)
        ttk.Button(commit_frame, text="Hacer Commit", command=self.hacer_commit, width=30).pack(pady=3)
        
        log_frame = ttk.LabelFrame(scrollable_frame, text="📜 Historial", padding="10")
        log_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(log_frame, text="Ver Historial", 
                  command=lambda: self.ejecutar_comando('git log --oneline --graph --all -20'), 
                  width=30).pack(pady=3)
    
    def crear_tab_ramas(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🌿 Ramas")
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="Ver Ramas", 
                  command=lambda: self.ejecutar_comando('git branch -a'), width=35).pack(pady=5)
        
        crear_frame = ttk.LabelFrame(frame, text="Crear Rama", padding="10")
        crear_frame.pack(fill=tk.X, pady=10)
        ttk.Label(crear_frame, text="Nombre:").pack(anchor='w')
        self.rama_entry = ttk.Entry(crear_frame, width=40)
        self.rama_entry.pack(fill=tk.X, pady=3)
        ttk.Button(crear_frame, text="Crear", command=self.crear_rama, width=30).pack(pady=3)
        
        cambiar_frame = ttk.LabelFrame(frame, text="Cambiar Rama", padding="10")
        cambiar_frame.pack(fill=tk.X, pady=10)
        ttk.Label(cambiar_frame, text="Nombre:").pack(anchor='w')
        self.cambiar_rama_entry = ttk.Entry(cambiar_frame, width=40)
        self.cambiar_rama_entry.pack(fill=tk.X, pady=3)
        ttk.Button(cambiar_frame, text="Cambiar", command=self.cambiar_rama, width=30).pack(pady=3)
        
        merge_frame = ttk.LabelFrame(frame, text="Fusionar", padding="10")
        merge_frame.pack(fill=tk.X, pady=10)
        ttk.Label(merge_frame, text="Rama a fusionar:").pack(anchor='w')
        self.merge_entry = ttk.Entry(merge_frame, width=40)
        self.merge_entry.pack(fill=tk.X, pady=3)
        ttk.Button(merge_frame, text="Merge", command=self.fusionar_rama, width=30).pack(pady=3)
    
    def crear_tab_remoto(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🌐 Remoto")
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frame, text="Ver Remotos", 
                  command=lambda: self.ejecutar_comando('git remote -v'), width=35).pack(pady=5)
        
        clonar_frame = ttk.LabelFrame(frame, text="Clonar", padding="10")
        clonar_frame.pack(fill=tk.X, pady=10)
        ttk.Label(clonar_frame, text="URL:").pack(anchor='w')
        self.clone_entry = ttk.Entry(clonar_frame, width=50)
        self.clone_entry.pack(fill=tk.X, pady=3)
        ttk.Button(clonar_frame, text="Clonar", command=self.clonar_repo, width=30).pack(pady=3)
        
        remoto_frame = ttk.LabelFrame(frame, text="Agregar Remoto", padding="10")
        remoto_frame.pack(fill=tk.X, pady=10)
        ttk.Label(remoto_frame, text="Nombre:").pack(anchor='w')
        self.remoto_nombre_entry = ttk.Entry(remoto_frame, width=50)
        self.remoto_nombre_entry.insert(0, "origin")
        self.remoto_nombre_entry.pack(fill=tk.X, pady=3)
        ttk.Label(remoto_frame, text="URL:").pack(anchor='w')
        self.remoto_url_entry = ttk.Entry(remoto_frame, width=50)
        self.remoto_url_entry.pack(fill=tk.X, pady=3)
        ttk.Button(remoto_frame, text="Agregar", command=self.agregar_remoto, width=30).pack(pady=3)
        
        push_frame = ttk.LabelFrame(frame, text="Push", padding="10")
        push_frame.pack(fill=tk.X, pady=10)
        push_inner = ttk.Frame(push_frame)
        push_inner.pack(fill=tk.X)
        ttk.Label(push_inner, text="Remoto:").grid(row=0, column=0, sticky='w')
        self.push_remoto_entry = ttk.Entry(push_inner, width=15)
        self.push_remoto_entry.insert(0, "origin")
        self.push_remoto_entry.grid(row=0, column=1, padx=5)
        ttk.Label(push_inner, text="Rama:").grid(row=0, column=2, sticky='w')
        self.push_rama_entry = ttk.Entry(push_inner, width=15)
        self.push_rama_entry.insert(0, "main")
        self.push_rama_entry.grid(row=0, column=3, padx=5)
        ttk.Button(push_frame, text="Push", command=self.push, width=30).pack(pady=3)
        
        pull_frame = ttk.LabelFrame(frame, text="Pull", padding="10")
        pull_frame.pack(fill=tk.X, pady=10)
        pull_inner = ttk.Frame(pull_frame)
        pull_inner.pack(fill=tk.X)
        ttk.Label(pull_inner, text="Remoto:").grid(row=0, column=0, sticky='w')
        self.pull_remoto_entry = ttk.Entry(pull_inner, width=15)
        self.pull_remoto_entry.insert(0, "origin")
        self.pull_remoto_entry.grid(row=0, column=1, padx=5)
        ttk.Label(pull_inner, text="Rama:").grid(row=0, column=2, sticky='w')
        self.pull_rama_entry = ttk.Entry(pull_inner, width=15)
        self.pull_rama_entry.insert(0, "main")
        self.pull_rama_entry.grid(row=0, column=3, padx=5)
        ttk.Button(pull_frame, text="Pull", command=self.pull, width=30).pack(pady=3)
    
    def crear_tab_utilidades(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Utilidades")
        frame = ttk.Frame(tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        diff_frame = ttk.LabelFrame(frame, text="Diferencias", padding="10")
        diff_frame.pack(fill=tk.X, pady=10)
        ttk.Button(diff_frame, text="Ver Diferencias", 
                  command=lambda: self.ejecutar_comando('git diff'), width=35).pack(pady=3)
        ttk.Button(diff_frame, text="Diferencias Staging", 
                  command=lambda: self.ejecutar_comando('git diff --staged'), width=35).pack(pady=3)
        
        deshacer_frame = ttk.LabelFrame(frame, text="Deshacer", padding="10")
        deshacer_frame.pack(fill=tk.X, pady=10)
        ttk.Button(deshacer_frame, text="Reset (quitar del staging)", 
                  command=lambda: self.ejecutar_comando('git reset'), width=35).pack(pady=3)
        ttk.Button(deshacer_frame, text="Deshacer Último Commit", 
                  command=lambda: self.ejecutar_comando('git reset --soft HEAD~1'), width=35).pack(pady=3)
        
        gitignore_frame = ttk.LabelFrame(frame, text=".gitignore", padding="10")
        gitignore_frame.pack(fill=tk.X, pady=10)
        ttk.Button(gitignore_frame, text="Crear .gitignore", 
                  command=self.crear_gitignore, width=35).pack(pady=3)
        
        ayuda_frame = ttk.LabelFrame(frame, text="Ayuda", padding="10")
        ayuda_frame.pack(fill=tk.X, pady=10)
        ttk.Button(ayuda_frame, text="Comandos Comunes", 
                  command=self.mostrar_ayuda, width=35).pack(pady=3)
    
    def actualizar_directorio_actual(self):
        self.dir_label.config(text=os.getcwd())
    
    def mostrar_bienvenida(self):
        """Muestra mensaje de bienvenida en la consola"""
        bienvenida = f"""{'═' * 60}
🚀 ASISTENTE GIT/GITHUB - CONSOLA INICIADA
{'═' * 60}

📁 Directorio actual: {os.getcwd()}
⏰ Hora de inicio: {datetime.now().strftime('%H:%M:%S')}

💡 Todos los comandos Git se mostrarán aquí en tiempo real.
   Usa los botones de las pestañas para ejecutar operaciones.

{'═' * 60}

"""
        self.escribir_salida(bienvenida, 'info')
    
    def cambiar_directorio(self):
        directorio = filedialog.askdirectory(title="Seleccionar Directorio")
        if directorio:
            os.chdir(directorio)
            self.actualizar_directorio_actual()
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.escribir_salida(f"\n[{timestamp}] ", 'timestamp')
            self.escribir_salida(f"📁 Directorio cambiado a:\n", 'info')
            self.escribir_salida(f"   {directorio}\n", 'exito')
    
    def ejecutar_comando(self, comando):
        def ejecutar():
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.escribir_salida(f"\n[{timestamp}] ", 'timestamp')
            self.escribir_salida(f"$ {comando}\n", 'comando')
            self.escribir_salida("─" * 60 + "\n", 'info')
            
            try:
                resultado = subprocess.run(comando, shell=True, capture_output=True, 
                                         text=True, encoding='utf-8', errors='replace', cwd=os.getcwd())
                
                if resultado.stdout:
                    self.escribir_salida(resultado.stdout, 'exito')
                
                if resultado.stderr:
                    # Git a veces envía información normal por stderr
                    if resultado.returncode == 0:
                        self.escribir_salida(resultado.stderr, 'advertencia')
                    else:
                        self.escribir_salida(resultado.stderr, 'error')
                
                if resultado.returncode != 0:
                    self.escribir_salida(f"\n❌ Error: El comando terminó con código {resultado.returncode}\n", 'error')
                else:
                    self.escribir_salida("\n✅ Comando ejecutado correctamente\n", 'exito')
                    
            except Exception as e:
                self.escribir_salida(f"\n❌ Excepción: {str(e)}\n", 'error')
            
            self.escribir_salida("═" * 60 + "\n\n", 'info')
            
        threading.Thread(target=ejecutar, daemon=True).start()
    
    def escribir_salida(self, texto, tag=None):
        if tag:
            self.output_text.insert(tk.END, texto, tag)
        else:
            self.output_text.insert(tk.END, texto)
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def limpiar_salida(self):
        self.output_text.delete(1.0, tk.END)
    
    def actualizar_estado(self):
        self.ejecutar_comando('git status')
    
    def configurar_usuario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Configurar Usuario")
        ventana.geometry("400x180")
        ventana.configure(bg='#2b2b2b')
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nombre:").pack(anchor='w', pady=5)
        nombre_entry = ttk.Entry(frame, width=40)
        nombre_entry.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="Email:").pack(anchor='w', pady=5)
        email_entry = ttk.Entry(frame, width=40)
        email_entry.pack(fill=tk.X, pady=5)
        
        def guardar():
            if nombre_entry.get() and email_entry.get():
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.escribir_salida(f"\n[{timestamp}] ", 'timestamp')
                self.escribir_salida("⚙️ Configurando usuario Git...\n", 'info')
                self.ejecutar_comando(f'git config --global user.name "{nombre_entry.get()}"')
                self.ejecutar_comando(f'git config --global user.email "{email_entry.get()}"')
                ventana.destroy()
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=10)
    
    def agregar_archivo_especifico(self):
        archivo = filedialog.askopenfilename(title="Seleccionar Archivo")
        if archivo:
            try:
                rel_path = os.path.relpath(archivo, os.getcwd())
                self.ejecutar_comando(f'git add "{rel_path}"')
            except:
                self.ejecutar_comando(f'git add "{archivo}"')
    
    def hacer_commit(self):
        mensaje = self.commit_entry.get()
        if mensaje:
            self.ejecutar_comando(f'git commit -m "{mensaje}"')
            self.commit_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Ingresa un mensaje")
    
    def crear_rama(self):
        if self.rama_entry.get():
            self.ejecutar_comando(f'git branch {self.rama_entry.get()}')
            self.rama_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Ingresa un nombre")
    
    def cambiar_rama(self):
        if self.cambiar_rama_entry.get():
            self.ejecutar_comando(f'git checkout {self.cambiar_rama_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre de la rama")
    
    def fusionar_rama(self):
        if self.merge_entry.get():
            if messagebox.askyesno("Confirmar", f"¿Fusionar '{self.merge_entry.get()}'?"):
                self.ejecutar_comando(f'git merge {self.merge_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Ingresa el nombre")
    
    def clonar_repo(self):
        if self.clone_entry.get():
            self.ejecutar_comando(f'git clone {self.clone_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Ingresa la URL")
    
    def agregar_remoto(self):
        if self.remoto_nombre_entry.get() and self.remoto_url_entry.get():
            self.ejecutar_comando(f'git remote add {self.remoto_nombre_entry.get()} {self.remoto_url_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
    
    def push(self):
        if self.push_remoto_entry.get() and self.push_rama_entry.get():
            self.ejecutar_comando(f'git push {self.push_remoto_entry.get()} {self.push_rama_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Completa los campos")
    
    def pull(self):
        if self.pull_remoto_entry.get() and self.pull_rama_entry.get():
            self.ejecutar_comando(f'git pull {self.pull_remoto_entry.get()} {self.pull_rama_entry.get()}')
        else:
            messagebox.showwarning("Advertencia", "Completa los campos")
    
    def crear_gitignore(self):
        contenido = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDEs
.vscode/
.idea/
*.swp

# Sistema
.DS_Store
Thumbs.db

# Logs
*.log
"""
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(contenido)
            messagebox.showinfo("Éxito", ".gitignore creado")
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.escribir_salida(f"\n[{timestamp}] ", 'timestamp')
            self.escribir_salida("✅ Archivo .gitignore creado correctamente\n", 'exito')
            self.escribir_salida(f"   Ubicación: {os.path.join(os.getcwd(), '.gitignore')}\n", 'info')
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            self.escribir_salida(f"❌ Error al crear .gitignore: {e}\n", 'error')
    
    def mostrar_ayuda(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Ayuda Git")
        ventana.geometry("650x550")
        ventana.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(ventana, bg='#1e1e1e', fg='white', 
                                        font=('Consolas', 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ayuda = """COMANDOS GIT MÁS COMUNES

📋 CONFIGURACIÓN:
  git config --global user.name "Nombre"
  git config --global user.email "email@ejemplo.com"
  git config --list

📁 BÁSICOS:
  git init                    - Inicializar repositorio
  git status                  - Ver estado
  git add <archivo>           - Agregar archivo
  git add .                   - Agregar todos
  git commit -m "mensaje"     - Hacer commit
  git log                     - Ver historial
  git log --oneline           - Historial resumido

🌿 RAMAS:
  git branch                  - Ver ramas
  git branch <nombre>         - Crear rama
  git checkout <rama>         - Cambiar de rama
  git checkout -b <rama>      - Crear y cambiar
  git merge <rama>            - Fusionar rama
  git branch -d <rama>        - Eliminar rama

🌐 REMOTO (GitHub):
  git clone <url>             - Clonar repositorio
  git remote add origin <url> - Agregar remoto
  git remote -v               - Ver remotos
  git push origin <rama>      - Subir cambios
  git pull origin <rama>      - Descargar cambios
  git fetch                   - Obtener sin fusionar

🔧 UTILIDADES:
  git diff                    - Ver diferencias
  git diff --staged           - Diferencias staging
  git reset                   - Quitar del staging
  git reset --soft HEAD~1     - Deshacer último commit
  git stash                   - Guardar cambios temporalmente
  git stash pop               - Recuperar cambios

💡 FLUJO BÁSICO:
  1. git add .
  2. git commit -m "mensaje"
  3. git push origin main

🔗 PRIMER PUSH A GITHUB:
  1. Crear repo en GitHub
  2. git remote add origin <url>
  3. git branch -M main
  4. git push -u origin main
"""
        text.insert(1.0, ayuda)
        text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenteGitGUI(root)
    root.mainloop()
