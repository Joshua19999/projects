import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser
import subprocess
import sys

class GeneradorInterfaz:
    def __init__(self, ventana): 
        self.ventana = ventana
        ventana.title("Inicio")
        ventana.geometry("300x400+400+100")

        tk.Button(ventana, text="Nuevo", width=15, height=2, command=self.configurar_ventana).place(x=24, y=8)
        tk.Button(ventana, text="Abrir", width=15, height=2,command=self.seleccionar_programa).place(x=176, y=9)

    def configurar_ventana(self):
        self.ventana.destroy()
        root=tk.Tk()
        self.root = root
        self.root.title("Generador de Interfaz Gráfica")
        self.seleccionado = None  # Para almacenar el widget seleccionado

        # Frame para la configuración
        self.config_frame = tk.Frame(root)
        self.config_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entradas para el nombre y título de la ventana
        tk.Label(self.config_frame, text="Nombre de la ventana:").grid(row=0, column=0, pady=5, sticky=tk.W)
        self.nombre_ventana_entry = tk.Entry(self.config_frame, width=40)
        self.nombre_ventana_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.config_frame, text="Título de la ventana:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.titulo_ventana_entry = tk.Entry(self.config_frame, width=40)
        self.titulo_ventana_entry.grid(row=1, column=1, pady=5)

        # Entrada para el número de botones
        tk.Label(self.config_frame, text="Número de botones:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.num_botones_entry = tk.Entry(self.config_frame, width=10)
        self.num_botones_entry.grid(row=2, column=1, pady=5)

        # Entrada para la geometría de la ventana (ancho x alto + x_pos + y_pos)
        tk.Label(self.config_frame, text="Ancho de la ventana:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.ancho_entry = tk.Entry(self.config_frame, width=10)
        self.ancho_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.config_frame, text="Alto de la ventana:").grid(row=4, column=0, pady=5, sticky=tk.W)
        self.alto_entry = tk.Entry(self.config_frame, width=10)
        self.alto_entry.grid(row=4, column=1, pady=5)

        tk.Label(self.config_frame, text="Posición X:").grid(row=5, column=0, pady=5, sticky=tk.W)
        self.pos_x_entry = tk.Entry(self.config_frame, width=10)
        self.pos_x_entry.grid(row=5, column=1, pady=5)

        tk.Label(self.config_frame, text="Posición Y:").grid(row=6, column=0, pady=5, sticky=tk.W)
        self.pos_y_entry = tk.Entry(self.config_frame, width=10)
        self.pos_y_entry.grid(row=6, column=1, pady=5)

        # Botón para configurar los botones
        tk.Button(self.config_frame, text="Configurar Botones", command=self.configurar_botones).grid(row=7, column=0, columnspan=2, pady=10)

        self.botones_frame = tk.Frame(self.root)
        self.botones_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def configurar_botones(self):
        # Obtener datos de entrada
        nombre_ventana = self.nombre_ventana_entry.get().strip()
        titulo_ventana = self.titulo_ventana_entry.get().strip()
        num_botones = self.num_botones_entry.get().strip()
        ancho = self.ancho_entry.get().strip()
        alto = self.alto_entry.get().strip()
        pos_x = self.pos_x_entry.get().strip()
        pos_y = self.pos_y_entry.get().strip()

        # Validar entradas
        if not nombre_ventana or not titulo_ventana or not num_botones.isdigit() or not ancho.isdigit() or not alto.isdigit() or not pos_x.isdigit() or not pos_y.isdigit():
            messagebox.showerror("Error", "Por favor, completa todos los campos correctamente.")
            return

        self.num_botones = int(num_botones)

        # Limpiar la sección de configuración de botones
        for widget in self.botones_frame.winfo_children():
            widget.destroy()

        # Configurar cada botón con texto o mensaje
        self.texto_botones = []
        self.mensaje_botones = []

        for i in range(self.num_botones):
            tk.Label(self.botones_frame, text=f"Texto del botón {i+1}:").grid(row=i, column=0, pady=5, sticky=tk.W)
            texto_entry = tk.Entry(self.botones_frame, width=40)
            texto_entry.grid(row=i, column=1, pady=5)
            self.texto_botones.append(texto_entry)

            tk.Label(self.botones_frame, text=f"Mensaje al hacer clic (opcional):").grid(row=i, column=2, pady=5, sticky=tk.W)
            mensaje_entry = tk.Entry(self.botones_frame, width=40)
            mensaje_entry.grid(row=i, column=3, pady=5)
            self.mensaje_botones.append(mensaje_entry)

        tk.Button(self.botones_frame, text="Generar Interfaz", command=self.generar_interfaz).grid(row=self.num_botones, column=0, columnspan=4, pady=10)

    def generar_interfaz(self):
        # Obtener los datos
        nombre_ventana = self.nombre_ventana_entry.get().strip()
        titulo_ventana = self.titulo_ventana_entry.get().strip()
        ancho = self.ancho_entry.get().strip()
        alto = self.alto_entry.get().strip()
        pos_x = self.pos_x_entry.get().strip()
        pos_y = self.pos_y_entry.get().strip()

        geometria = f"{ancho}x{alto}+{pos_x}+{pos_y}"

        botones = [(self.texto_botones[i].get(), self.mensaje_botones[i].get()) for i in range(self.num_botones)]

        # Cerrar ventana actual y abrir el editor gráfico
        self.root.destroy()
        self.abrir_editor_grafico(titulo_ventana, geometria, botones)

    def abrir_editor_grafico(self, titulo_ventana, geometria, botones):
        """
        Abre una nueva ventana con un editor gráfico donde el usuario puede insertar o eliminar botones.
        Los botones no podrán salir de los límites de la ventana.
        """
        self.nueva_ventana = tk.Tk()
        self.nueva_ventana.title(titulo_ventana)
        self.nueva_ventana.geometry(geometria)

        # Crear los botones en la ventana generada
        self.crear_botones(self.nueva_ventana, botones)

        # Abrir la ventana del editor
        self.abrir_ventana_editor()

    def seleccionar_programa(self):
        """Abre un cuadro de diálogo para seleccionar un archivo .py y habilita el botón de ejecutar."""
        self.archivo_seleccionado = filedialog.askopenfilename(
            title="Selecciona un script Python",
            filetypes=(("Archivos Python", "*.py"), ("Todos los archivos", "*.*"))
        )
        
        if self.archivo_seleccionado:
            self.boton_ejecutar.config(state=tk.NORMAL)
            messagebox.showinfo("Archivo seleccionado", f"Script seleccionado: {self.archivo_seleccionado}")
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

    def ejecutar_programa(self):
        """Ejecuta el script Python seleccionado."""
        if self.archivo_seleccionado:
            try:
                # Ejecuta el archivo .py con el mismo intérprete de Python que está ejecutando este script
                subprocess.run([sys.executable, self.archivo_seleccionado], check=True)
                messagebox.showinfo("Éxito", "El script se ejecutó correctamente.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"El script devolvió un error:\n{e}")
            except FileNotFoundError:
                messagebox.showerror("Error", "El archivo no se encontró.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al ejecutar el script:\n{e}")
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo para ejecutar.")

    def crear_botones(self, ventana, botones):
        """ Crear los botones especificados en la ventana generada. """
        for texto, mensaje in botones:
            boton = tk.Button(ventana, text=texto, width=15, height=2)
            boton.place(x=10, y=10)  # Colocar los botones inicialmente en la esquina superior izquierda
            boton.bind("<ButtonPress-1>", self.seleccionar_widget)
            boton.bind("<Double-1>", self.editar_texto_widget)
            boton.bind("<B1-Motion>", self.on_drag)

    def seleccionar_widget(self, event):
        """ Seleccionar un widget para posibles acciones como eliminar. """
        self.seleccionado = event.widget
        

    def editar_texto_widget(self, event):
        """ Editar el texto de un widget con doble clic. """
        widget = event.widget
        nuevo_texto = simpledialog.askstring("Editar texto", "Ingrese el nuevo texto:", initialvalue=widget.cget("text"))
        if nuevo_texto:
            widget.config(text=nuevo_texto)

    def start_drag(self, event):
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def on_drag(self, event):
        widget = event.widget
        ventana = widget.winfo_toplevel()

        # Obtener el tamaño actual de la ventana
        ancho_ventana = ventana.winfo_width()
        alto_ventana = ventana.winfo_height()

        # Obtener el tamaño del widget
        ancho_widget = widget.winfo_width()
        alto_widget = widget.winfo_height()

        # Obtener la nueva posición del widget
        new_x = widget.winfo_x() + event.x - widget.winfo_width() // 2
        new_y = widget.winfo_y() + event.y - widget.winfo_height() // 2

        # Limitar el movimiento para que el widget no salga de la ventana
        new_x = max(0, min(new_x, ancho_ventana - ancho_widget))
        new_y = max(0, min(new_y, alto_ventana - alto_widget))

        # Colocar el widget en la nueva posición
        widget.place(x=new_x, y=new_y)

    def abrir_ventana_editor(self):
        """ Abre la ventana del editor donde se pueden agregar o eliminar botones o textos. """
        editor = tk.Toplevel(self.nueva_ventana)
        editor.title("Editor de Interfaz")
        editor.geometry("300x300")

        tk.Button(editor, text="Insertar Botón", command=self.insertar_boton).pack(pady=10)
        tk.Button(editor, text="Insertar Texto", command=self.insertar_texto).pack(pady=10)
        tk.Button(editor, text="Eliminar Selección", command=self.eliminar_seleccion).pack(pady=10)
              # Selector de colores
        tk.Button(editor, text="Cambiar Color de Fondo", command=self.cambiar_color_fondo).pack(pady=10)
        tk.Button(editor, text="Cambiar Color de Texto", command=self.cambiar_color_texto).pack(pady=10)
        tk.Button(editor, text="Generar Código", command=self.generar_codigo).pack(pady=10)

    def insertar_boton(self):
        """ Inserta un nuevo botón en la ventana generada. """
        nuevo_boton = tk.Button(self.nueva_ventana, text="Nuevo Botón", width=15, height=2)
        nuevo_boton.place(x=50, y=50)
        nuevo_boton.bind("<ButtonPress-1>", self.seleccionar_widget)
        nuevo_boton.bind("<Double-1>", self.editar_texto_widget)
        nuevo_boton.bind("<B1-Motion>", self.on_drag)

    def insertar_texto(self):
        """ Inserta un nuevo texto en la ventana generada. """
        nuevo_texto = tk.Label(self.nueva_ventana, text="Nuevo Texto", font=("Arial", 14))
        nuevo_texto.place(x=50, y=100)
        nuevo_texto.bind("<ButtonPress-1>", self.seleccionar_widget)
        nuevo_texto.bind("<Double-1>", self.editar_texto_widget)
        nuevo_texto.bind("<B1-Motion>", self.on_drag)


    def eliminar_seleccion(self):
        """ Elimina el widget seleccionado de la ventana generada. """
        if self.seleccionado:
            self.seleccionado.destroy()
            self.seleccionado = None
        else:
            messagebox.showerror("Error", "No hay selección para eliminar.")

    def generar_codigo(self):
        """Genera el código de la ventana y lo guarda en un archivo, incluyendo texto, posición, tamaño y configuraciones de cada objeto (sin fuente)."""
        if not hasattr(self, 'nueva_ventana'):
            messagebox.showerror("Error", "No hay una ventana abierta para generar el código.")
            return

        widgets = self.nueva_ventana.winfo_children()
        codigo = 'import tkinter as tk\nfrom tkinter import messagebox\n\n'
        codigo += f'def crear_ventana():\n'
        codigo += f'    ventana = tk.Tk()\n'
        codigo += f'    ventana.title("{self.nueva_ventana.title()}")\n'
        codigo += f'    ventana.geometry("{self.nueva_ventana.geometry()}")\n\n'

        for widget in widgets:
            if isinstance(widget, tk.Button):
                # Obtener configuración del botón
                texto_boton = widget.cget("text")
                ancho_boton = widget.cget("width")
                alto_boton = widget.cget("height")
                color_fondo = widget.cget("bg")
                color_texto = widget.cget("fg")

                # Verificar si el botón tiene un comando asociado (mensaje)
                if widget.cget("command"):
                    codigo += (
                        f'    tk.Button(ventana, text="{texto_boton}", width={ancho_boton}, height={alto_boton}, '
                        f'bg="{color_fondo}", fg="{color_texto}", '
                        f'command=lambda: messagebox.showinfo("Mensaje", "{texto_boton}")).place(x={widget.winfo_x()}, y={widget.winfo_y()})\n'
                    )
                else:
                    codigo += (
                        f'    tk.Button(ventana, text="{texto_boton}", width={ancho_boton}, height={alto_boton}, '
                        f'bg="{color_fondo}", fg="{color_texto}").place(x={widget.winfo_x()}, y={widget.winfo_y()})\n'
                    )

            elif isinstance(widget, tk.Label):
                # Obtener configuración de la etiqueta (sin fuente)
                texto_etiqueta = widget.cget("text")
                color_fondo = widget.cget("bg")
                color_texto = widget.cget("fg")

                codigo += (
                    f'    tk.Label(ventana, text="{texto_etiqueta}", '
                    f'bg="{color_fondo}", fg="{color_texto}").place(x={widget.winfo_x()}, y={widget.winfo_y()})\n'
                )

        # Cierre de la función
        codigo += '\n    ventana.mainloop()\n\n'
        codigo += 'if __name__ == "__main__":\n'
        codigo += '    crear_ventana()\n'

        # Guardar el código en un archivo
        archivo = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if archivo:
            with open(archivo, "w") as file:
                file.write(codigo)
            messagebox.showinfo("Éxito", "Código generado y guardado exitosamente.")


    def cambiar_color_fondo(self):
        color = colorchooser.askcolor(title="Seleccionar color de fondo")
        if color[1] and self.seleccionado:
            self.seleccionado.config(bg=color[1])

    def cambiar_color_texto(self):
        color = colorchooser.askcolor(title="Seleccionar color de texto")
        if color[1] and self.seleccionado:
            self.seleccionado.config(fg=color[1])


# Crear la ventana principal
if __name__ == "__main__":
    ventana = tk.Tk()
    app = GeneradorInterfaz(ventana)
    ventana.mainloop()
