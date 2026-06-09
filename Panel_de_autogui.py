import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk

# --- Funciones ---
def obtener_posicion_mouse(label):
    while True:
        x, y = pyautogui.position()
        label.config(text=f"Posición del mouse - X: {x}, Y: {y}")
        time.sleep(0.1)

def mover_mouse():
    pyautogui.moveTo(500, 300, duration=1)

def click_mouse():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        pyautogui.click(x, y)
    except ValueError:
        pyautogui.click()

def doble_click():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        pyautogui.doubleClick(x, y)
    except ValueError:
        pyautogui.doubleClick()

def escribir_texto(frase):
    time.sleep(2)
    pyautogui.write(frase)

def presionar_tecla():
    tecla = combo_tecla.get()
    if tecla.strip() != "":
        pyautogui.press(tecla)
    else:
        pyautogui.press("enter")

def tomar_screenshot():
    try:
        captura = pyautogui.screenshot()
        captura.save("captura.png")
        label_status.config(text="✅ Screenshot guardado como captura.png")
    except Exception as e:
        label_status.config(text=f"❌ Error al tomar screenshot: {e}")

# --- Interfaz gráfica ---
def iniciar_mouse():
    hilo = threading.Thread(target=obtener_posicion_mouse, args=(label_mouse,))
    hilo.daemon = True
    hilo.start()

def escribir():
    frase = entrada_texto.get()
    hilo = threading.Thread(target=escribir_texto, args=(frase,))
    hilo.daemon = True
    hilo.start()

# Ventana principal
ventana = tk.Tk()
ventana.title("Panel PyAutoGUI")
ventana.geometry("400x550")

# Sección Mouse
frame_mouse = tk.LabelFrame(ventana, text="Mouse", padx=10, pady=10)
frame_mouse.pack(fill="x", expand=True, padx=10, pady=5)

btn_mouse = tk.Button(frame_mouse, text="Obtener posición del mouse", command=iniciar_mouse)
btn_mouse.pack(fill="x", pady=5)

label_mouse = tk.Label(frame_mouse, text="Posición del mouse - X: 0, Y: 0")
label_mouse.pack(fill="x", pady=5)

btn_mover = tk.Button(frame_mouse, text="Mover mouse (500,300)", command=mover_mouse)
btn_mover.pack(fill="x", pady=5)

frame_coords = tk.Frame(frame_mouse)
frame_coords.pack(fill="x", pady=5)

tk.Label(frame_coords, text="X:").grid(row=0, column=0)
entry_x = tk.Entry(frame_coords, width=5)
entry_x.grid(row=0, column=1)

tk.Label(frame_coords, text="Y:").grid(row=0, column=2)
entry_y = tk.Entry(frame_coords, width=5)
entry_y.grid(row=0, column=3)

btn_click = tk.Button(frame_mouse, text="Click en coordenadas", command=click_mouse)
btn_click.pack(fill="x", pady=5)

btn_doble = tk.Button(frame_mouse, text="Doble Click en coordenadas", command=doble_click)
btn_doble.pack(fill="x", pady=5)

# Sección Teclado
frame_teclado = tk.LabelFrame(ventana, text="Teclado", padx=10, pady=10)
frame_teclado.pack(fill="x", expand=True, padx=10, pady=5)

entrada_texto = tk.Entry(frame_teclado, width=40)
entrada_texto.pack(fill="x", pady=5)

btn_escribir = tk.Button(frame_teclado, text="Escribir texto", command=escribir)
btn_escribir.pack(fill="x", pady=5)

tk.Label(frame_teclado, text="Selecciona tecla:").pack(pady=5)
teclas_comunes = ["enter", "esc", "tab", "space", "up", "down", "left", "right", "backspace", "delete", "shift", "ctrl", "alt"]
combo_tecla = ttk.Combobox(frame_teclado, values=teclas_comunes, width=10)
combo_tecla.pack(pady=5)
combo_tecla.set("enter")

btn_tecla = tk.Button(frame_teclado, text="Presionar tecla", command=presionar_tecla)
btn_tecla.pack(fill="x", pady=5)

# Sección Screenshot
frame_ss = tk.LabelFrame(ventana, text="Captura de pantalla", padx=10, pady=10)
frame_ss.pack(fill="x", expand=True, padx=10, pady=5)

btn_screenshot = tk.Button(frame_ss, text="Tomar Screenshot", command=tomar_screenshot)
btn_screenshot.pack(fill="x", pady=5)

label_status = tk.Label(frame_ss, text="")
label_status.pack(fill="x", pady=5)

ventana.mainloop()
