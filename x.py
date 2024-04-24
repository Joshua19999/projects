import pyautogui
import time
def obtener_posicion_mouse():
    try:
        while True:
            x, y = pyautogui.position()
            print(f'Posición del mouse - X: {x}, Y: {y}', end='\r')
    except KeyboardInterrupt:
        print('\n¡Script detenido!')

def mouse():
    pyautogui.click(418,7429)
    time.sleep(1)
    pyautogui.click(486,6716)
    time.sleep(1)

    try:
            while True:
                pyautogui.click(79,46127)
                time.sleep(1)
    except KeyboardInterrupt:
            print('\n¡Script detenido!')

mouse()