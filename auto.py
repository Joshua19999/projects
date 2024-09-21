import tkinter as tk
import pyautogui
import time

class Automatizador:
    def __init__(self):
        ventana = tk.Tk()
        ventana.title("Auto")
        ventana.geometry("200x400+765+169")

        # Lista para guardar las posiciones apuntadas
        self.posiciones_apuntadas = []

        # Botones
        tk.Button(ventana, text="Ejecutar", width=15, height=2, bg="#bbffbb", fg="SystemButtonText",command=self.bot).place(x=41, y=11)
        tk.Button(ventana, text="Cerrar", width=15, height=2, bg="#ff9d9d", fg="SystemButtonText", command=ventana.quit).place(x=38, y=121)
        tk.Button(ventana, text="Apuntar posición", width=15, height=2, command=self.apuntar_posicion).place(x=41, y=71)

        # Etiquetas
        self.apuntes = tk.Label(ventana, text="Apuntes:")
        self.apuntes.place(x=10, y=250)

        self.posicion = tk.Label(ventana, text="Posición del mouse - X: , Y: ")
        self.posicion.place(x=10, y=200)

        # Actualizar la posición del mouse periódicamente
        self.actualizar_posicion_mouse()

        # Bind para ejecutar "apuntar_posicion" cuando se presione Enter
        ventana.bind('<Return>', lambda event: self.apuntar_posicion())

        ventana.mainloop()

    def actualizar_posicion_mouse(self):
        x, y = pyautogui.position()
        self.posicion.config(text=f'Posición del mouse - X: {x}, Y: {y}')
        # Actualiza cada 100ms
        self.posicion.after(100, self.actualizar_posicion_mouse)

    def apuntar_posicion(self):
        x, y = pyautogui.position()
        self.posiciones_apuntadas.append(f'X: {x}, Y: {y}')
        self.apuntes.config(text="Apuntes:\n" + "\n".join(self.posiciones_apuntadas))

    def bot(self):
        pyautogui.click(538,112)
        time.sleep(5)
        pyautogui.click(613,119)
        pyautogui.click(289,157)
        pyautogui.click(452,104)


if __name__ == "__main__":
    app = Automatizador()
