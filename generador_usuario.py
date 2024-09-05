import tkinter as tk
from tkinter import messagebox
import re

def mostrar_instrucciones(operacion):
    instrucciones = ""
    if operacion == 'potencia':
        instrucciones = "Para la operación de potencia, ingresa dos números separados por una coma. Ejemplo: 2, 3 donde la función calcula 2 ** 3."
    elif operacion == 'raiz':
        instrucciones = "Para la operación de raíz, ingresa dos números separados por una coma. Ejemplo: 16, 2 donde la función calcula 16 ** (1 / 2)."
    elif operacion == 'bucle':
        instrucciones = "Para la operación de bucle, el argumento será 'ciclos'. La función generará un bucle que itera sobre el rango especificado por el argumento ciclos."
    else:
        instrucciones = "Ingresa números separados por comas para realizar la operación seleccionada."
        
    instrucciones_label.config(text=instrucciones)

def validar_nombre_funcion(nombre):
    # Verificar que el nombre de la función comience con una letra o un guion bajo
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', nombre):
        return True
    return False

def validar_argumentos(argumentos, operacion):
    # Validar los argumentos según la operación
    if operacion in ['suma', 'resta', 'multiplicacion', 'division']:
        if not all(arg.strip().replace('.', '', 1).isdigit() for arg in argumentos):
            messagebox.showerror("Error", "Todos los argumentos deben ser números válidos.")
            return False
    elif operacion == 'potencia':
        if len(argumentos) < 2 or not all(arg.strip().replace('.', '', 1).isdigit() for arg in argumentos[:2]):
            messagebox.showerror("Error", "Para potencia se requieren dos números válidos.")
            return False
    elif operacion == 'raiz':
        if len(argumentos) < 2 or not all(arg.strip().replace('.', '', 1).isdigit() for arg in argumentos[:2]):
            messagebox.showerror("Error", "Para raíz se requieren dos números válidos.")
            return False
    elif operacion == 'bucle':
        if len(argumentos) != 1 or not argumentos[0].strip().isdigit():
            messagebox.showerror("Error", "Para bucle se requiere un número válido.")
            return False
    return True

def generar_funcion(nombre_funcion, argumentos, operacion, codigo_bucle=None, condicion=None):
    if not validar_nombre_funcion(nombre_funcion):
        messagebox.showerror("Error", "El nombre de la función no es válido. Debe comenzar con una letra o guion bajo y solo puede contener letras, números y guiones bajos.")
        return None

    if not validar_argumentos(argumentos, operacion):
        return None

    # Definir la función sin argumentos para operaciones numéricas
    codigo_funcion = f"def {nombre_funcion}():\n"
    
    # Generar el cuerpo de la función basado en la operación seleccionada
    if operacion == 'suma':
        codigo_funcion += f"    return {' + '.join(argumentos)}\n"
    elif operacion == 'resta':
        codigo_funcion += f"    return {' - '.join(argumentos)}\n"
    elif operacion == 'multiplicacion':
        codigo_funcion += f"    return {' * '.join(argumentos)}\n"
    elif operacion == 'division':
        codigo_funcion += f"    return {' / '.join(argumentos)}\n"
    elif operacion == 'potencia':
        if len(argumentos) >= 2:
            codigo_funcion += f"    return {argumentos[0]} ** {argumentos[1]}\n"
    elif operacion == 'raiz':
        if len(argumentos) >= 2:
            codigo_funcion += f"    return {argumentos[0]} ** (1 / {argumentos[1]})\n"
    elif operacion == 'condicional':
        if condicion:
            codigo_funcion += f"    if {condicion}:\n"
            codigo_funcion += f"        return 'Condición verdadera'\n"
            codigo_funcion += f"    else:\n"
            codigo_funcion += f"        return 'Condición falsa'\n"
    elif operacion == 'bucle':
        if len(argumentos) == 1 and argumentos[0].isdigit():
            ciclos = argumentos[0]
            codigo_funcion += f"    for ciclo in range({ciclos}):\n"
            if codigo_bucle:
                codigo_funcion += f"        {codigo_bucle}\n"
            else:
                codigo_funcion += f"        pass  # Código dentro del bucle\n"
    else:
        codigo_funcion += f"    pass  # Operación no definida\n"
    
    return codigo_funcion

def generar_codigo():
    nombre_funcion = nombre_entry.get()
    argumentos = argumentos_entry.get().split(',')
    operacion = operacion_var.get()
    condicion = condicion_entry.get().strip() if operacion == 'condicional' else None

    if not nombre_funcion or not operacion:
        messagebox.showerror("Error", "Por favor, completa todos los campos")
        return

    # Limpiar los argumentos y asegurarse de que son números
    argumentos = [arg.strip() for arg in argumentos]

    if operacion == 'bucle':
        if not (len(argumentos) == 1 and argumentos[0].isdigit()):
            messagebox.showerror("Error", "Para bucle se requiere un número válido.")
            return
        
        root.withdraw()  # Oculta la ventana principal
        abrir_ventana_bucle(nombre_funcion, argumentos)
        return

    codigo_generado = generar_funcion(nombre_funcion, argumentos, operacion, condicion=condicion)

    if codigo_generado is not None:
        # Mostrar el código generado en el cuadro de texto
        codigo_text.delete(1.0, tk.END)
        codigo_text.insert(tk.END, codigo_generado)

        # Guardar el código generado en un archivo .py
        with open(f"{nombre_funcion}.py", "w") as archivo:
            archivo.write(codigo_generado)

        messagebox.showinfo("Éxito", f"Código generado y guardado en {nombre_funcion}.py")

def abrir_ventana_bucle(nombre_funcion, argumentos):
    ventana_bucle = tk.Toplevel(root)
    ventana_bucle.title("Configuración del Bucle")

    tk.Label(ventana_bucle, text="Código dentro del bucle (opcional):").pack(pady=5)
    
    # Menú desplegable para seleccionar acción común dentro del bucle
    tk.Label(ventana_bucle, text="Selecciona una acción:").pack(pady=5)
    accion_var = tk.StringVar(value="print('Hola Mundo')")  # Valor por defecto
    
    acciones = [
        "print('Hola Mundo')",
        "print(ciclo)",
        "print('El ciclo actual es:', ciclo)"
    ]
    
    accion_menu = tk.OptionMenu(ventana_bucle, accion_var, *acciones)
    accion_menu.pack(pady=5)
    
    # Campo de entrada para código personalizado dentro del bucle
    tk.Label(ventana_bucle, text="O ingresa código personalizado:").pack(pady=5)
    bucle_entry = tk.Entry(ventana_bucle, width=60)
    bucle_entry.pack(pady=5)

    def generar_bucle_codigo():
        num_ciclos = argumentos[0]  # Tomar el número de ciclos desde los argumentos
        codigo_bucle = bucle_entry.get().strip() or accion_var.get().strip()
        
        if not num_ciclos.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese un número válido de ciclos.")
            return

        if not codigo_bucle:
            messagebox.showerror("Error", "Por favor, ingrese el código para dentro del bucle.")
            return

        codigo_generado = generar_funcion(nombre_funcion, [num_ciclos], 'bucle', codigo_bucle)

        if codigo_generado:
            # Mostrar el código generado en el cuadro de texto
            codigo_text.delete(1.0, tk.END)
            codigo_text.insert(tk.END, codigo_generado)

            # Guardar el código generado en un archivo .py
            with open(f"{nombre_funcion}.py", "w") as archivo:
                archivo.write(codigo_generado)

            messagebox.showinfo("Éxito", f"Código generado y guardado en {nombre_funcion}.py")

    tk.Button(ventana_bucle, text="Generar Código de Bucle", command=generar_bucle_codigo).pack(pady=10)
    tk.Button(ventana_bucle, text="Anterior", command=lambda: (ventana_bucle.destroy(), root.deiconify())).pack(pady=5)

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Código Python")

# Etiqueta y campo de entrada para el nombre de la función
tk.Label(root, text="Nombre de la función:").pack(pady=5)
nombre_entry = tk.Entry(root, width=40)
nombre_entry.pack(pady=5)

# Etiqueta y campo de entrada para los argumentos de la función
tk.Label(root, text="Argumentos (separados por comas):").pack(pady=5)
argumentos_entry = tk.Entry(root, width=40)
argumentos_entry.pack(pady=5)

# Etiqueta y campo de entrada para la condición (opcional, para condicionales)
tk.Label(root, text="Condición (para condicionales):").pack(pady=5)
condicion_entry = tk.Entry(root, width=40)
condicion_entry.pack(pady=5)

# Etiqueta para instrucciones
instrucciones_label = tk.Label(root, text="")
instrucciones_label.pack(pady=10)

# Etiqueta y opciones para seleccionar la operación
tk.Label(root, text="Operación:").pack(pady=5)
operacion_var = tk.StringVar()
operacion_var.set("suma")  # Valor por defecto

# Botones de radio para elegir la operación
tk.Radiobutton(root, text="Suma", variable=operacion_var, value="suma", command=lambda: mostrar_instrucciones("")).pack(pady=5)
tk.Radiobutton(root, text="Resta", variable=operacion_var, value="resta", command=lambda: mostrar_instrucciones("")).pack(pady=5)
tk.Radiobutton(root, text="Multiplicación", variable=operacion_var, value="multiplicacion", command=lambda: mostrar_instrucciones("")).pack(pady=5)
tk.Radiobutton(root, text="División", variable=operacion_var, value="division", command=lambda: mostrar_instrucciones("")).pack(pady=5)
tk.Radiobutton(root, text="Potencia", variable=operacion_var, value="potencia", command=lambda: mostrar_instrucciones("potencia")).pack(pady=5)
tk.Radiobutton(root, text="Raíz", variable=operacion_var, value="raiz", command=lambda: mostrar_instrucciones("raiz")).pack(pady=5)
tk.Radiobutton(root, text="Condicional", variable=operacion_var, value="condicional", command=lambda: mostrar_instrucciones("")).pack(pady=5)
tk.Radiobutton(root, text="Bucle", variable=operacion_var, value="bucle", command=lambda: mostrar_instrucciones("bucle")).pack(pady=5)

# Botón para generar el código
tk.Button(root, text="Generar Código", command=generar_codigo).pack(pady=10)

# Cuadro de texto para mostrar el código generado
tk.Label(root, text="Código Generado:").pack(pady=5)
codigo_text = tk.Text(root, height=10, width=60)
codigo_text.pack(pady=5)

# Iniciar el bucle principal de la interfaz
root.mainloop()
