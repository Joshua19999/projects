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
        pyautogui.click()  # si no hay coordenadas, clic en posición actual

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
        label_status.config(text="Screenshot guardado como captura.png")
    except Exception as e:
        label_status.config(text=f"Error al tomar screenshot: {e}")

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

# Botones y etiquetas
btn_mouse = tk.Button(ventana, text="Obtener posición del mouse", command=iniciar_mouse)
btn_mouse.pack(pady=10)

label_mouse = tk.Label(ventana, text="Posición del mouse - X: 0, Y: 0")
label_mouse.pack(pady=5)

btn_mover = tk.Button(ventana, text="Mover mouse (500,300)", command=mover_mouse)
btn_mover.pack(pady=10)

# Entradas para coordenadas
frame_coords = tk.Frame(ventana)
frame_coords.pack(pady=5)

tk.Label(frame_coords, text="X:").grid(row=0, column=0)
entry_x = tk.Entry(frame_coords, width=5)
entry_x.grid(row=0, column=1)

tk.Label(frame_coords, text="Y:").grid(row=0, column=2)
entry_y = tk.Entry(frame_coords, width=5)
entry_y.grid(row=0, column=3)

btn_click = tk.Button(ventana, text="Click en coordenadas", command=click_mouse)
btn_click.pack(pady=10)

btn_doble = tk.Button(ventana, text="Doble Click en coordenadas", command=doble_click)
btn_doble.pack(pady=10)

entrada_texto = tk.Entry(ventana, width=40)
entrada_texto.pack(pady=5)

btn_escribir = tk.Button(ventana, text="Escribir texto", command=escribir)
btn_escribir.pack(pady=10)

# Desplegable para teclas
frame_tecla = tk.Frame(ventana)
frame_tecla.pack(pady=5)

tk.Label(frame_tecla, text="Selecciona tecla:").grid(row=0, column=0)

teclas_comunes = ["enter", "esc", "tab", "space", "up", "down", "left", "right", "backspace", "delete", "shift", "ctrl", "alt"]
combo_tecla = ttk.Combobox(frame_tecla, values=teclas_comunes, width=10)
combo_tecla.grid(row=0, column=1)
combo_tecla.set("enter")  # valor por defecto

btn_tecla = tk.Button(ventana, text="Presionar tecla", command=presionar_tecla)
btn_tecla.pack(pady=10)

btn_screenshot = tk.Button(ventana, text="Tomar Screenshot", command=tomar_screenshot)
btn_screenshot.pack(pady=10)

label_status = tk.Label(ventana, text="")
label_status.pack(pady=5)

ventana.mainloop()
