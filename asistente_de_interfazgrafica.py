import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog, colorchooser, font
import subprocess
import sys
import json
from datetime import datetime


class GeneradorInterfaz:
    """Asistente mejorado para generar interfaces gráficas con Python/Tkinter"""
    
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("🎨 Asistente de Generación de Interfaces")
        ventana.geometry("500x600+400+100")
        ventana.configure(bg="#f0f0f0")
        ventana.resizable(False, False)
        
        # Título principal
        titulo = tk.Label(ventana, text="🎨 Generador de Interfaces Gráficas", 
                         font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=30)
        
        # Descripción
        desc = tk.Label(ventana, text="Crea interfaces gráficas de forma visual\ny genera código Python automáticamente",
                       font=("Arial", 11), bg="#f0f0f0", fg="#7f8c8d", justify=tk.CENTER)
        desc.pack(pady=10)
        
        # Frame para botones principales
        frame_botones = tk.Frame(ventana, bg="#f0f0f0")
        frame_botones.pack(pady=40)
        
        # Botón Nuevo Proyecto
        btn_nuevo = tk.Button(frame_botones, text="📄 Nuevo Proyecto", width=20, height=3,
                             font=("Arial", 11, "bold"), bg="#3498db", fg="white",
                             activebackground="#2980b9", cursor="hand2", relief=tk.FLAT,
                             command=self.configurar_ventana)
        btn_nuevo.grid(row=0, column=0, padx=15, pady=15)
        
        # Botón Abrir Proyecto
        btn_abrir = tk.Button(frame_botones, text="📂 Abrir Proyecto", width=20, height=3,
                             font=("Arial", 11, "bold"), bg="#2ecc71", fg="white",
                             activebackground="#27ae60", cursor="hand2", relief=tk.FLAT,
                             command=self.abrir_proyecto)
        btn_abrir.grid(row=0, column=1, padx=15, pady=15)
        
        # Botón Ejecutar Script
        btn_ejecutar = tk.Button(frame_botones, text="▶️ Ejecutar Script", width=20, height=3,
                                font=("Arial", 11, "bold"), bg="#e74c3c", fg="white",
                                activebackground="#c0392b", cursor="hand2", relief=tk.FLAT,
                                command=self.ejecutar_script)
        btn_ejecutar.grid(row=1, column=0, padx=15, pady=15)
        
        # Botón Tutorial
        btn_tutorial = tk.Button(frame_botones, text="❓ Tutorial", width=20, height=3,
                                font=("Arial", 11, "bold"), bg="#9b59b6", fg="white",
                                activebackground="#8e44ad", cursor="hand2", relief=tk.FLAT,
                                command=self.mostrar_tutorial)
        btn_tutorial.grid(row=1, column=1, padx=15, pady=15)
        
        # Footer
        footer = tk.Label(ventana, text="Versión 2.0 - Asistente Mejorado",
                         font=("Arial", 9), bg="#f0f0f0", fg="#95a5a6")
        footer.pack(side=tk.BOTTOM, pady=15)
    
    def mostrar_tutorial(self):
        """Muestra un tutorial de uso del generador."""
        tutorial = tk.Toplevel(self.ventana)
        tutorial.title("📚 Tutorial - Generador de Interfaces")
        tutorial.geometry("600x500")
        tutorial.configure(bg="white")
        tutorial.resizable(False, False)
        
        tk.Label(tutorial, text="📚 Guía de Uso Rápida", 
                font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=20)
        
        canvas = tk.Canvas(tutorial, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tutorial, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg="white")
        
        frame_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        pasos = [
            ("1️⃣ Crear Nuevo Proyecto", "Haz clic en 'Nuevo Proyecto' y configura el título y dimensiones."),
            ("2️⃣ Diseñar la Interfaz", "Usa el panel de herramientas para agregar widgets."),
            ("3️⃣ Mover Widgets", "Arrastra los widgets con el mouse para posicionarlos."),
            ("4️⃣ Editar Propiedades", "Doble clic en un widget para editar su texto."),
            ("5️⃣ Personalizar Colores", "Selecciona un widget y usa los botones de color."),
            ("6️⃣ Agregar Más Widgets", "Usa los botones del editor para insertar más elementos."),
            ("7️⃣ Generar Código", "Haz clic en 'Generar Código' para crear el archivo Python."),
            ("8️⃣ Guardar Proyecto", "Guarda tu proyecto en formato JSON para editarlo después."),
        ]
        
        for titulo_paso, desc in pasos:
            frame_paso = tk.Frame(frame_scroll, bg="#ecf0f1", relief=tk.RAISED, bd=1)
            frame_paso.pack(fill=tk.X, padx=20, pady=8)
            tk.Label(frame_paso, text=titulo_paso, font=("Arial", 11, "bold"),
                    bg="#ecf0f1", fg="#2c3e50", anchor="w").pack(fill=tk.X, padx=15, pady=(10, 5))
            tk.Label(frame_paso, text=desc, font=("Arial", 9),
                    bg="#ecf0f1", fg="#34495e", anchor="w", 
                    wraplength=520, justify=tk.LEFT).pack(fill=tk.X, padx=15, pady=(0, 10))
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        tk.Button(tutorial, text="Cerrar", command=tutorial.destroy,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 width=15, height=2, cursor="hand2").pack(pady=15)
    
    def abrir_proyecto(self):
        """Abre un proyecto guardado previamente."""
        archivo = filedialog.askopenfilename(
            title="Abrir Proyecto",
            filetypes=[("Proyectos de Interfaz", "*.json"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    proyecto = json.load(f)
                messagebox.showinfo("Éxito", "Proyecto cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el proyecto:\n{e}")
    
    def ejecutar_script(self):
        """Selecciona y ejecuta un script Python."""
        archivo = filedialog.askopenfilename(
            title="Selecciona un script Python",
            filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                subprocess.Popen([sys.executable, archivo])
                messagebox.showinfo("Éxito", f"Script ejecutado:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar el script:\n{e}")
    
    def configurar_ventana(self):
        """Configuración inicial del proyecto con asistente mejorado."""
        self.ventana.destroy()
        root = tk.Tk()
        self.root = root
        self.root.title("⚙️ Configuración del Proyecto")
        self.root.geometry("600x450")
        self.root.configure(bg="#ecf0f1")
        self.root.resizable(False, False)
        self.seleccionado = None
        
        # Encabezado
        header = tk.Frame(root, bg="#3498db", height=70)
        header.pack(fill=tk.X)
        tk.Label(header, text="⚙️ Configuración del Proyecto",
                font=("Arial", 16, "bold"), bg="#3498db", fg="white").pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Sección 1: Información básica
        seccion1 = tk.LabelFrame(main_frame, text="📋 Información Básica",
                                font=("Arial", 11, "bold"), bg="white", 
                                fg="#2c3e50", padx=15, pady=15)
        seccion1.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(seccion1, text="Título de la ventana:", bg="white",
                font=("Arial", 10)).grid(row=0, column=0, pady=10, sticky=tk.W)
        self.titulo_ventana_entry = tk.Entry(seccion1, width=35, font=("Arial", 10))
        self.titulo_ventana_entry.insert(0, "Mi Aplicación")
        self.titulo_ventana_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Sección 2: Dimensiones
        seccion2 = tk.LabelFrame(main_frame, text="📐 Dimensiones de la Ventana",
                                font=("Arial", 11, "bold"), bg="white", 
                                fg="#2c3e50", padx=15, pady=15)
        seccion2.pack(fill=tk.X, pady=(0, 15))
        
        dim_frame = tk.Frame(seccion2, bg="white")
        dim_frame.pack()
        
        tk.Label(dim_frame, text="Ancho:", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.ancho_entry = tk.Entry(dim_frame, width=10, font=("Arial", 10))
        self.ancho_entry.insert(0, "800")
        self.ancho_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dim_frame, text="Alto:", bg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.alto_entry = tk.Entry(dim_frame, width=10, font=("Arial", 10))
        self.alto_entry.insert(0, "600")
        self.alto_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(dim_frame, text="Posición X:", bg="white", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.pos_x_entry = tk.Entry(dim_frame, width=10, font=("Arial", 10))
        self.pos_x_entry.insert(0, "100")
        self.pos_x_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dim_frame, text="Posición Y:", bg="white", font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=5)
        self.pos_y_entry = tk.Entry(dim_frame, width=10, font=("Arial", 10))
        self.pos_y_entry.insert(0, "100")
        self.pos_y_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Botones de acción
        botones_frame = tk.Frame(root, bg="#ecf0f1")
        botones_frame.pack(pady=20)
        
        tk.Button(botones_frame, text="✨ Crear Proyecto", command=self.iniciar_editor,
                 bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                 width=15, height=2, cursor="hand2").grid(row=0, column=0, padx=10)
        
        tk.Button(botones_frame, text="❌ Cancelar", command=self.root.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                 width=15, height=2, cursor="hand2").grid(row=0, column=1, padx=10)
    
    def iniciar_editor(self):
        """Inicia el editor con la configuración especificada."""
        titulo = self.titulo_ventana_entry.get().strip()
        ancho = self.ancho_entry.get().strip()
        alto = self.alto_entry.get().strip()
        pos_x = self.pos_x_entry.get().strip()
        pos_y = self.pos_y_entry.get().strip()
        
        if not titulo or not ancho.isdigit() or not alto.isdigit():
            messagebox.showerror("Error", "Por favor, completa todos los campos correctamente.")
            return
        
        geometria = f"{ancho}x{alto}+{pos_x}+{pos_y}"
        self.root.destroy()
        self.abrir_editor_grafico(titulo, geometria, [])
    
    def abrir_editor_grafico(self, titulo_ventana, geometria, botones):
        """Abre el editor gráfico donde se diseña la interfaz."""
        self.nueva_ventana = tk.Tk()
        self.nueva_ventana.title(titulo_ventana)
        self.nueva_ventana.geometry(geometria)
        self.nueva_ventana.configure(bg="white")
        
        self.widgets_creados = []
        self.resize_handle = None  # Manejador de redimensionamiento
        self.resizing = False
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_start_width = 0
        self.resize_start_height = 0
        
        # Abrir panel de herramientas
        self.abrir_ventana_editor()
    
    def abrir_ventana_editor(self):
        """Abre la ventana del editor con herramientas mejoradas."""
        editor = tk.Toplevel(self.nueva_ventana)
        editor.title("🛠️ Panel de Herramientas")
        editor.geometry("280x650+50+100")
        editor.configure(bg="#34495e")
        editor.attributes('-topmost', True)
        
        # Título del panel
        tk.Label(editor, text="🛠️ Herramientas", font=("Arial", 13, "bold"),
                bg="#34495e", fg="white").pack(pady=15)
        
        # Frame para widgets
        frame_widgets = tk.LabelFrame(editor, text="Agregar Widgets", 
                                      bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        frame_widgets.pack(fill=tk.X, padx=10, pady=10)
        
        botones_widgets = [
            ("➕ Botón", self.insertar_boton, "#3498db"),
            ("📝 Etiqueta", self.insertar_texto, "#2ecc71"),
            ("✏️ Campo de Texto", self.insertar_entry, "#9b59b6"),
            ("☑️ Checkbox", self.insertar_checkbox, "#e67e22"),
            ("🔘 Radiobutton", self.insertar_radiobutton, "#1abc9c"),
        ]
        
        for texto, comando, color in botones_widgets:
            tk.Button(frame_widgets, text=texto, command=comando,
                     bg=color, fg="white", font=("Arial", 9, "bold"), 
                     width=22, cursor="hand2", relief=tk.FLAT).pack(pady=5, padx=10)
        
        # Frame para edición
        frame_edicion = tk.LabelFrame(editor, text="Edición", 
                                      bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        frame_edicion.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(frame_edicion, text="🎨 Color Fondo", command=self.cambiar_color_fondo,
                 bg="#3498db", fg="white", font=("Arial", 9, "bold"), 
                 width=22, relief=tk.FLAT).pack(pady=5, padx=10)
        tk.Button(frame_edicion, text="🖊️ Color Texto", command=self.cambiar_color_texto,
                 bg="#9b59b6", fg="white", font=("Arial", 9, "bold"), 
                 width=22, relief=tk.FLAT).pack(pady=5, padx=10)
        tk.Button(frame_edicion, text="🗑️ Eliminar", command=self.eliminar_seleccion,
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), 
                 width=22, relief=tk.FLAT).pack(pady=5, padx=10)
        
        # Instrucciones
        instrucciones = tk.Label(editor, text="💡 Arrastra para mover\n🔍 Esquina inferior derecha para redimensionar",
                                font=("Arial", 8), bg="#34495e", fg="#ecf0f1", justify=tk.CENTER)
        instrucciones.pack(pady=10)
        
        # Frame para acciones
        frame_acciones = tk.LabelFrame(editor, text="Proyecto", 
                                       bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        frame_acciones.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(frame_acciones, text="💾 Guardar Proyecto", command=self.guardar_proyecto,
                 bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), 
                 width=22, relief=tk.FLAT).pack(pady=5, padx=10)
        tk.Button(frame_acciones, text="📄 Generar Código", command=self.generar_codigo,
                 bg="#f39c12", fg="white", font=("Arial", 9, "bold"), 
                 width=22, relief=tk.FLAT).pack(pady=5, padx=10)
    
    def insertar_boton(self):
        """Inserta un nuevo botón."""
        boton = tk.Button(self.nueva_ventana, text="Nuevo Botón", width=15, height=2,
                         bg="#3498db", fg="white", font=("Arial", 9, "bold"))
        boton.place(x=50, y=50)
        self.configurar_widget(boton)
        self.widgets_creados.append(boton)
    
    def insertar_texto(self):
        """Inserta una nueva etiqueta."""
        etiqueta = tk.Label(self.nueva_ventana, text="Nueva Etiqueta", 
                           font=("Arial", 11), bg="white")
        etiqueta.place(x=50, y=100)
        self.configurar_widget(etiqueta)
        self.widgets_creados.append(etiqueta)
    
    def insertar_entry(self):
        """Inserta un nuevo campo de texto."""
        entry = tk.Entry(self.nueva_ventana, width=30, font=("Arial", 10))
        entry.place(x=50, y=150)
        self.configurar_widget(entry)
        self.widgets_creados.append(entry)
    
    def insertar_checkbox(self):
        """Inserta un nuevo checkbox."""
        checkbox = tk.Checkbutton(self.nueva_ventana, text="Opción", 
                                 font=("Arial", 9), bg="white")
        checkbox.place(x=50, y=200)
        self.configurar_widget(checkbox)
        self.widgets_creados.append(checkbox)
    
    def insertar_radiobutton(self):
        """Inserta un nuevo radiobutton."""
        radio = tk.Radiobutton(self.nueva_ventana, text="Opción", 
                              font=("Arial", 9), bg="white")
        radio.place(x=50, y=250)
        self.configurar_widget(radio)
        self.widgets_creados.append(radio)
    
    def configurar_widget(self, widget):
        """Configura los eventos de un widget."""
        widget.bind("<ButtonPress-1>", self.seleccionar_widget)
        widget.bind("<Double-1>", self.editar_texto_widget)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_release)
        widget.bind("<Motion>", self.on_motion)
    
    def seleccionar_widget(self, event):
        """Selecciona un widget."""
        widget = event.widget
        self.seleccionado = widget
        
        # Verificar si se está haciendo clic en el área de redimensionamiento
        x, y = event.x, event.y
        w_width = widget.winfo_width()
        w_height = widget.winfo_height()
        
        # Área de 10 píxeles en la esquina inferior derecha para redimensionar
        if x > w_width - 15 and y > w_height - 15:
            self.resizing = True
            self.resize_start_x = event.x_root
            self.resize_start_y = event.y_root
            try:
                self.resize_start_width = widget.cget('width')
                self.resize_start_height = widget.cget('height')
            except:
                self.resize_start_width = widget.winfo_width()
                self.resize_start_height = widget.winfo_height()
        else:
            self.resizing = False
    
    def on_release(self, event):
        """Maneja el evento de soltar el botón del ratón."""
        self.resizing = False
    
    def on_motion(self, event):
        """Cambia el cursor cuando está sobre el área de redimensionamiento."""
        widget = event.widget
        x, y = event.x, event.y
        w_width = widget.winfo_width()
        w_height = widget.winfo_height()
        
        # Cambiar cursor en la esquina inferior derecha
        if x > w_width - 15 and y > w_height - 15:
            widget.config(cursor="sizing")
        else:
            widget.config(cursor="hand2")
    
    def editar_texto_widget(self, event):
        """Edita el texto de un widget con doble clic."""
        widget = event.widget
        try:
            texto_actual = widget.cget("text")
            nuevo_texto = simpledialog.askstring("Editar texto", 
                                                "Ingrese el nuevo texto:",
                                                initialvalue=texto_actual)
            if nuevo_texto:
                widget.config(text=nuevo_texto)
        except:
            pass
    
    def on_drag(self, event):
        """Mueve o redimensiona un widget arrastrándolo."""
        widget = event.widget
        
        if self.resizing:
            # Redimensionar el widget
            delta_x = event.x_root - self.resize_start_x
            delta_y = event.y_root - self.resize_start_y
            
            tipo = widget.winfo_class()
            
            try:
                if tipo == 'Button':
                    # Para botones, ajustar width y height
                    new_width = max(5, self.resize_start_width + delta_x // 7)
                    new_height = max(1, self.resize_start_height + delta_y // 20)
                    widget.config(width=new_width, height=new_height)
                elif tipo == 'Entry':
                    # Para Entry, solo ajustar width
                    new_width = max(5, self.resize_start_width + delta_x // 7)
                    widget.config(width=new_width)
                elif tipo == 'Label':
                    # Para Label, cambiar el tamaño de fuente
                    current_font = widget.cget('font')
                    if isinstance(current_font, str):
                        font_family = current_font.split()[0] if current_font else "Arial"
                        font_size = 11
                    else:
                        font_family = current_font[0] if len(current_font) > 0 else "Arial"
                        font_size = current_font[1] if len(current_font) > 1 else 11
                    
                    new_size = max(8, font_size + delta_y // 10)
                    widget.config(font=(font_family, new_size))
            except:
                pass
        else:
            # Mover el widget
            ventana = widget.winfo_toplevel()
            
            # Obtener dimensiones
            ancho_ventana = ventana.winfo_width()
            alto_ventana = ventana.winfo_height()
            ancho_widget = widget.winfo_width()
            alto_widget = widget.winfo_height()
            
            # Calcular nueva posición
            new_x = widget.winfo_x() + event.x - widget.winfo_width() // 2
            new_y = widget.winfo_y() + event.y - widget.winfo_height() // 2
            
            # Limitar movimiento
            new_x = max(0, min(new_x, ancho_ventana - ancho_widget))
            new_y = max(0, min(new_y, alto_ventana - alto_widget))
            
            widget.place(x=new_x, y=new_y)
    
    def cambiar_color_fondo(self):
        """Cambia el color de fondo del widget seleccionado."""
        if self.seleccionado:
            color = colorchooser.askcolor(title="Seleccionar color de fondo")
            if color[1]:
                try:
                    self.seleccionado.config(bg=color[1])
                except:
                    messagebox.showwarning("Advertencia", 
                                         "Este widget no soporta cambio de color de fondo")
        else:
            messagebox.showwarning("Advertencia", "No hay ningún widget seleccionado")
    
    def cambiar_color_texto(self):
        """Cambia el color de texto del widget seleccionado."""
        if self.seleccionado:
            color = colorchooser.askcolor(title="Seleccionar color de texto")
            if color[1]:
                try:
                    self.seleccionado.config(fg=color[1])
                except:
                    messagebox.showwarning("Advertencia", 
                                         "Este widget no soporta cambio de color de texto")
        else:
            messagebox.showwarning("Advertencia", "No hay ningún widget seleccionado")
    
    def eliminar_seleccion(self):
        """Elimina el widget seleccionado."""
        if self.seleccionado:
            self.seleccionado.destroy()
            if self.seleccionado in self.widgets_creados:
                self.widgets_creados.remove(self.seleccionado)
            self.seleccionado = None
        else:
            messagebox.showwarning("Advertencia", "No hay ningún widget seleccionado")
    
    def guardar_proyecto(self):
        """Guarda el proyecto en formato JSON."""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Proyectos de Interfaz", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            proyecto = {
                'titulo': self.nueva_ventana.title(),
                'geometria': self.nueva_ventana.geometry(),
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'widgets': []
            }
            
            for widget in self.nueva_ventana.winfo_children():
                widget_data = {
                    'tipo': widget.winfo_class(),
                    'x': widget.winfo_x(),
                    'y': widget.winfo_y(),
                }
                
                try:
                    widget_data['text'] = widget.cget('text')
                except:
                    pass
                
                try:
                    widget_data['bg'] = widget.cget('bg')
                    widget_data['fg'] = widget.cget('fg')
                except:
                    pass
                
                proyecto['widgets'].append(widget_data)
            
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(proyecto, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Éxito", "Proyecto guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el proyecto:\n{e}")
    
    def generar_codigo(self):
        """Genera el código Python de la interfaz."""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        widgets = self.nueva_ventana.winfo_children()
        codigo = 'import tkinter as tk\nfrom tkinter import messagebox\n\n'
        codigo += 'def crear_ventana():\n'
        codigo += '    ventana = tk.Tk()\n'
        codigo += f'    ventana.title("{self.nueva_ventana.title()}")\n'
        codigo += f'    ventana.geometry("{self.nueva_ventana.geometry()}")\n'
        codigo += '    ventana.configure(bg="white")\n\n'
        
        for widget in widgets:
            tipo = widget.winfo_class()
            x = widget.winfo_x()
            y = widget.winfo_y()
            
            if tipo == 'Button':
                texto = widget.cget("text")
                ancho = widget.cget("width")
                alto = widget.cget("height")
                bg = widget.cget("bg")
                fg = widget.cget("fg")
                codigo += f'    tk.Button(ventana, text="{texto}", width={ancho}, height={alto}, '
                codigo += f'bg="{bg}", fg="{fg}").place(x={x}, y={y})\n'
            
            elif tipo == 'Label':
                texto = widget.cget("text")
                bg = widget.cget("bg")
                fg = widget.cget("fg")
                codigo += f'    tk.Label(ventana, text="{texto}", bg="{bg}", fg="{fg}").place(x={x}, y={y})\n'
            
            elif tipo == 'Entry':
                width = widget.cget("width")
                codigo += f'    tk.Entry(ventana, width={width}).place(x={x}, y={y})\n'
            
            elif tipo == 'Checkbutton':
                texto = widget.cget("text")
                bg = widget.cget("bg")
                codigo += f'    tk.Checkbutton(ventana, text="{texto}", bg="{bg}").place(x={x}, y={y})\n'
            
            elif tipo == 'Radiobutton':
                texto = widget.cget("text")
                bg = widget.cget("bg")
                codigo += f'    tk.Radiobutton(ventana, text="{texto}", bg="{bg}").place(x={x}, y={y})\n'
        
        codigo += '\n    ventana.mainloop()\n\n'
        codigo += 'if __name__ == "__main__":\n'
        codigo += '    crear_ventana()\n'
        
        try:
            with open(archivo, "w", encoding="utf-8") as file:
                file.write(codigo)
            messagebox.showinfo("Éxito", "Código generado y guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el código:\n{e}")


# Crear la ventana principal
if __name__ == "__main__":
    ventana = tk.Tk()
    app = GeneradorInterfaz(ventana)
    ventana.mainloop()
