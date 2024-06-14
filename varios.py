from random import randrange 
import tkinter
import pygame,sys
from pygame.locals import *
import pyautogui
from tkinter import *
from tkinter import messagebox
import tkinter
from turtle import bgcolor
import hashlib
import string
from random import *
from ctypes import resize
from distutils.command.config import config
from hashlib import sha256
from time import time
import requests
import turtle
def adivinaelnumero():
    def adivinar():
        respuesta=cuadro.get()
        if int(respuesta)==numero:
            resultado.config(text="Felicidades")
        else:
            resultado.config(text="Perdiste")

    numero=randrange(11)
    print(numero)

    ventana=tkinter.Tk()
    ventana.geometry("200x300")

    instruciones=tkinter.Label(ventana,text="Pon un numero 0-10")
    instruciones.pack()

    cuadro=tkinter.Entry(ventana)
    cuadro.pack()

    jugar=tkinter.Button(ventana,text="jugar",command=adivinar)
    jugar.pack()

    resultado=tkinter.Label(ventana,text="resultado")
    resultado.pack()

    cerrar=tkinter.Button(ventana,text="cerrar",command=ventana.destroy)
    cerrar.pack(side="right",anchor="s")

    ventana.mainloop()

def myfirstgame():
    pygame.init()

    pantalla=pygame.display.set_mode((300,300))
    pygame.display.set_caption("Mi primer juego")

    while True:
        for evento in pygame.event.get():
            if evento.type ==QUIT:
                pygame.quit()
                sys.quit()
        pygame.display.update()

def mouseposition():
    print("\t",pyautogui.displayMousePosition())


def calculator_ig():
 
    class Pycalc(Frame):
 
        def __init__(self, master, *args, **kwargs):
            Frame.__init__(self, master, *args, **kwargs)
            self.parent = master
            self.grid()
            self.createWidgets()
 
        def deleteLastCharacter(self):
            textLength = len(self.display.get())
 
            if textLength >= 1:
                self.display.delete(textLength - 1, END)
            if textLength == 1:
                self.replaceText("0")
 
        def replaceText(self, text):
            self.display.delete(0, END)
            self.display.insert(0, text)
 
        def append(self, text):
            actualText = self.display.get()
            textLength = len(actualText)
            if actualText == "0":
                self.replaceText(text)
            else:
                self.display.insert(textLength, text)
 
        def evaluate(self):
            try:
                self.replaceText(eval(self.display.get()))
            except (SyntaxError, AttributeError):
                messagebox.showerror("Error", "Syntax Error")
                self.replaceText("0")
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot Divide by 0")
                self.replaceText("0")
 
        def containsSigns(self):
            operatorList = ["*", "/", "+", "-"]
            display = self.display.get()
            for c in display:
                if c in operatorList:
                    return True
            return False
 
        def changeSign(self):
            if self.containsSigns():
                self.evaluate()
            firstChar = self.display.get()[0]
            if firstChar == "0":
                pass
            elif firstChar == "-":
                self.display.delete(0)
            else:
                self.display.insert(0, "-")
 
        def inverse(self):
            self.display.insert(0, "1/(")
            self.append(")")
            self.evaluate()
 
        def createWidgets(self):
            self.display = Entry(self, font=("Arial", 24), relief=RAISED, justify=RIGHT, bg='darkblue', fg='red', borderwidth=0)
            self.display.insert(0, "0")
            self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")
 
            self.ceButton = Button(self, font=("Arial", 12), fg='red', text="CE", highlightbackground='red', command=lambda: self.replaceText("0"))
            self.ceButton.grid(row=1, column=0, sticky="nsew")
            self.inverseButton = Button(self, font=("Arial", 12), fg='red', text="1/x", highlightbackground='lightgrey', command=lambda: self.inverse())
            self.inverseButton.grid(row=1, column=2, sticky="nsew")
            self.delButton = Button(self, font=("Arial", 12), fg='#e8e8e8', text="Del", highlightbackground='red', command=lambda: self.deleteLastCharacter())
            self.delButton.grid(row=1, column=1, sticky="nsew")
            self.divButton = Button(self, font=("Arial", 12), fg='red', text="/", highlightbackground='lightgrey', command=lambda: self.append("/"))
            self.divButton.grid(row=1, column=3, sticky="nsew")
 
            self.sevenButton = Button(self, font=("Arial", 12), fg='white', text="7", highlightbackground='black', command=lambda: self.append("7"))
            self.sevenButton.grid(row=2, column=0, sticky="nsew")
            self.eightButton = Button(self, font=("Arial", 12), fg='white', text="8", highlightbackground='black', command=lambda: self.append("8"))
            self.eightButton.grid(row=2, column=1, sticky="nsew")
            self.nineButton = Button(self, font=("Arial", 12), fg='white', text="9", highlightbackground='black', command=lambda: self.append("9"))
            self.nineButton.grid(row=2, column=2, sticky="nsew")
            self.multButton = Button(self, font=("Arial", 12), fg='red', text="*", highlightbackground='lightgrey', command=lambda: self.append("*"))
            self.multButton.grid(row=2, column=3, sticky="nsew")
 
            self.fourButton = Button(self, font=("Arial", 12), fg='white', text="4", highlightbackground='black', command=lambda: self.append("4"))
            self.fourButton.grid(row=3, column=0, sticky="nsew")
            self.fiveButton = Button(self, font=("Arial", 12), fg='white', text="5", highlightbackground='black', command=lambda: self.append("5"))
            self.fiveButton.grid(row=3, column=1, sticky="nsew")
            self.sixButton = Button(self, font=("Arial", 12), fg='white', text="6", highlightbackground='black', command=lambda: self.append("6"))
            self.sixButton.grid(row=3, column=2, sticky="nsew")
            self.minusButton = Button(self, font=("Arial", 12), fg='red', text="-", highlightbackground='lightgrey', command=lambda: self.append("-"))
            self.minusButton.grid(row=3, column=3, sticky="nsew")
 
            self.oneButton = Button(self, font=("Arial", 12), fg='white', text="1", highlightbackground='black', command=lambda: self.append("1"))
            self.oneButton.grid(row=4, column=0, sticky="nsew")
            self.twoButton = Button(self, font=("Arial", 12), fg='white', text="2", highlightbackground='black', command=lambda: self.append("2"))
            self.twoButton.grid(row=4, column=1, sticky="nsew")
            self.threeButton = Button(self, font=("Arial", 12), fg='white', text="3", highlightbackground='black', command=lambda: self.append("3"))
            self.threeButton.grid(row=4, column=2, sticky="nsew")
            self.plusButton = Button(self, font=("Arial", 12), fg='red', text="+", highlightbackground='lightgrey', command=lambda: self.append("+"))
            self.plusButton.grid(row=4, column=3, sticky="nsew")
 
            self.negToggleButton = Button(self, font=("Arial", 12), fg='red', text="+/-", highlightbackground='lightgrey', command=lambda: self.changeSign())
            self.negToggleButton.grid(row=5, column=0, sticky="nsew")
            self.zeroButton = Button(self, font=("Arial", 12), fg='white', text="0", highlightbackground='black', command=lambda: self.append("0"))
            self.zeroButton.grid(row=5, column=1, sticky="nsew")
            self.decimalButton = Button(self, font=("Arial", 12), fg='white', text=".", highlightbackground='lightgrey', command=lambda: self.append("."))
            self.decimalButton.grid(row=5, column=2, sticky="nsew")
            self.equalsButton = Button(self, font=("Arial", 12), fg='red', text="=", highlightbackground='lightgrey', command=lambda: self.evaluate())
            self.equalsButton.grid(row=5, column=3, sticky="nsew")
 
 
    Calculator = Tk()
    Calculator.title("AdictoCalculator")
    Calculator.resizable(False, False)
    Calculator.config(cursor="pencil")
    root = Pycalc(Calculator).grid()
    Calculator.mainloop()

def comisiones():
    ventas_hechas=float(input("Cuantas ventas hizo? "))
    comision=ventas_hechas*13/100
    print(type(comision))
    print("Su comision es de " + str(round(comision)))
    print(type(comision))
    print(comision)

def copypeg():
    def copiar_contenido(origen, destino):
        try:
            with open(origen, 'r') as archivo_origen:
                contenido = archivo_origen.read()

            with open(destino, 'a') as archivo_destino:
                archivo_destino.write(contenido)

            print(f"El contenido se ha copiado correctamente de '{origen}' a '{destino}'.")
        except FileNotFoundError:
            print("Error: No se pudo encontrar el archivo de origen.")
        except IOError:
            print("Error: No se pudo copiar el contenido del archivo.")

# Ejemplo de uso
    archivo_origen = input('origen? ')
    archivo_destino = input('destino? ')

    copiar_contenido(archivo_origen, archivo_destino)
 
def cuenta_ig():

    def incrementar():
        cuenta = int(contador["text"])
        cuenta += 1
        contador.config(text=cuenta)


    def decrementar():
        cuenta=int(contador["text"])
        cuenta -= 1
        contador.config(text=cuenta)

    
    ventana=tkinter.Tk()
    ventana.geometry("300x300")
    ventana.config(bg="red")
    contador=tkinter.Label(ventana,text=0)
    contador.pack()

    incremetardor=tkinter.Button(ventana,text="incrementar",command=incrementar).pack()
    decrementardor=tkinter.Button(ventana, text="decrementar",command=decrementar).pack()
    cerrar=tkinter.Button(ventana, text="cerrar",command=ventana.destroy).pack(side="right",anchor="s")


    ventana.mainloop()

def encriptar():

    def encriptar_sha256(texto):
        # Codificar el texto en UTF-8 antes de encriptarlo
        texto_codificado = texto.encode('utf-8')

        # Crear un objeto de hash SHA-256
        sha256 = hashlib.sha256()

        # Actualizar el hash con el texto codificado
        sha256.update(texto_codificado)

        # Obtener el hash en formato hexadecimal
        hash_sha256 = sha256.hexdigest()

        return hash_sha256

    # Ejemplo de uso
    texto = "Hola, este es un ejemplo de encriptación en SHA-256"

    hash_encriptado = encriptar_sha256(texto)
    print("Texto original:", texto)
    print("Hash encriptado (SHA-256):", hash_encriptado)

def finanzas():

    class Gastos:
        def __init__(self, nombre, categoria, monto):
            self.nombre = nombre
            self.categoria = categoria
            self.monto = monto

    gastos = []

    ventana=tkinter.Tk()
    ventana.geometry("300x300")

    while True:
        cuadro=tkinter.Label(ventana,text="Qué acción desea realizar?")
        cuadro.pack(side="top",anchor="s")
        agregar_gasto=tkinter.Button(ventana,text="agregar gasto",command="agregar gasto").pack(side="right",anchor="n")
        ver_gastos=tkinter.Button(ventana,text="ver gastos",command="ver gastos").pack(side="top",anchor="n")
        salir=tkinter.Button(ventana,text="salir",command="salir").pack(side="left",anchor="n")

        opcion = input("¿Qué acción desea realizar? (Agregar gasto / Ver gastos / Salir): ")

        if opcion.lower() == "agregar gasto":
            nombre = input("Ingrese el nombre del gasto: ")
            categoria = input("Ingrese la categoría del gasto: ")
            monto = float(input("Ingrese el monto del gasto: "))
            gastos.append(Gastos(nombre, categoria, monto))

        elif opcion.lower() == "ver gastos":
            total_gastos = 0
            for gasto in gastos:
                print(f"{gasto.nombre} - Categoría: {gasto.categoria} - Monto: {gasto.monto}")
                total_gastos += gasto.monto
            print(f"Total de gastos: {total_gastos}")

        elif opcion.lower() == "salir":
            break

        else:

            print("Opción inválida. Por favor, elija una de las opciones válidas.")


def ing():
    
    ventana=tkinter.Tk() 
    ventana.resizable() #resistividad, true moverse y false no moverse
    ventana.iconbitmap() #icono
    ventana.title("Hola amigo")
    ventana.config(bg="blue")
    ventana.geometry("400x300")

    boton=tkinter.Button (ventana,text="Cerrar", command=ventana.destroy,bg="red",bd=30,relief="sunken").pack(side="right",anchor="s")

    ventana=tkinter.mainloop()

def metodos():
    edades=[6,7]
    edades.append(8)
    print(edades)

def minero_bitcoin():
    
    Noce_max = 10000000000
    texto = 'ABCD'

    def SHA256(texto):
        return sha256(texto.encode('ascii')).hexdigest()

    def mine(numero_bloque, transaccion, hash_anterior, prefijo_de_ceros):

        str_prefijo = '0' * prefijo_de_ceros

        for nonce in range(Noce_max):

            texto = str(numero_bloque) + transaccion + hash_anterior + str(nonce)
            hash_nuevo = SHA256(texto)

            if hash_nuevo.startswith(str_prefijo):
                print('BTC minado con éxito en el nonce ' + str(nonce))
                return hash_nuevo

        raise BaseException('No se encontró el hash')

    if __name__ == '__main__':
        transaccion = '''Manolo---Pepe (20)'''
    
        dificultad = 6
        start = time()
        hash_nuevo =mine(2,transaccion,str(sha256(texto.encode('ascii')).hexdigest()),dificultad)
        print(hash_nuevo)
        print(str(time()-start) + ' segundos')

def nombredeneegocio(): 
    x=input("De que trata el negocio? ")
    y=input("Tu nombre? ")
    print(x+" "+y)
    print("Tu nombre es "+x+ " "+y)

def navegadorweb():
   
    response = requests.get('https://deriv.com/')

    print(response.content)

def piedra_papel():
    
    respuesta=str()
    def obtener_numero():
        numero=randrange(2)
        dic={0:"piedra",1:"tijeras",2:"papel"}
        return dic[numero]


    def piedra():
        respuesta="piedra"
        if respuesta=="piedra" and numero=="tijeras":
            cuadro.config(text="Ganaste")
        elif respuesta==numero:
            cuadro.config(text="Empate")
        else:
            cuadro.config(text="Perdiste")

    def papel():
        respuesta="papel"
        if papel=="papel" and numero=="piedra":
            cuadro.config(text="Ganaste")
        elif respuesta==numero:
            cuadro.config(text="Empate")
        else:
            cuadro.config(text="Perdiste")


    def tijeras():
        respuesta="tijeras"
        if tijeras=="tijeras" and numero=="papel":
            cuadro.config(text="Ganaste")
        elif respuesta==numero:
            cuadro.config(text="Empate")
        else:
            cuadro.config(text="perdiste")

    ventana=tkinter.Tk()
    ventana.geometry("300x300")

    boton_de_piedra=tkinter.Button(ventana,text="piedra",command=piedra).pack(side="left",anchor="n")
    boton_de_papel=tkinter.Button(ventana,text="papel",command=papel).pack(side="right",anchor="n")
    boton_de_tijeras=tkinter.Button(ventana,text="tijeras",command= tijeras).pack()

    boton_de_cerrar=tkinter.Button(ventana,text="cerrar",command= ventana.destroy).pack(side="right",anchor="s")

    cuadro=tkinter.Label(ventana,text="el resultado")
    cuadro.pack(side="top",anchor="s")

    numero=obtener_numero  ()
    print(numero)

    ventana.mainloop()

def serpiente():

    cuadro=turtle.Turtle()
    cuadro.forward(100) 
    

