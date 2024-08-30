import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk

def calcular_interes_compuesto(event=None):
    # Obtiene los valores de las entradas y realiza el cálculo del interés compuesto
    try:
        cantidad_valor = float(cantidad_entry.get())  # Cambiado el nombre de la variable para evitar conflicto
        importe_anual_valor = float(importe_anual_entry.get())
        años_valor = int(años_entry.get())
        interes_valor = float(interes_entry.get()) / 100  # Dividir por 100 para obtener el porcentaje

        cantidades = [cantidad_valor]
        añosl = [0]
        for año in np.arange(1, años_valor + 1):
            cantidad_valor += cantidad_valor * interes_valor + importe_anual_valor
            cantidad_valor = round(cantidad_valor)
            cantidades.append(cantidad_valor)
            añosl.append(año)

        incom_df = pd.DataFrame({"Años": añosl, "Cantidad": cantidades})
        root.destroy()

        # Configuración del gráfico
        fig, ax = plt.subplots(figsize=(20, 8))

        # Crear el gráfico de barras
        sns.barplot(data=incom_df, x="Años", y="Cantidad", palette="bright", ax=ax)

        # Ajustar las etiquetas y el título del gráfico
        ax.set_title("Gráfico de Barras Interactivo")
        ax.set_xlabel("Años")
        ax.set_ylabel("Cantidad")
        ax.set(yticks=[], xticks=[])

        # Inicializar la variable para almacenar el texto de anotación actual
        current_annotation = None

        def on_click(event):
            nonlocal current_annotation  # Para modificar la variable definida en el contexto exterior

            # Limpiar cualquier anotación existente
            if current_annotation is not None:
                current_annotation.remove()
                current_annotation = None

            # Buscar las barras en el gráfico
            for bar in ax.patches:
                # Comprueba si el clic está dentro de los límites de la barra
                if bar.contains(event)[0]:
                    # Obtiene la altura de la barra (valor de y)
                    height = bar.get_height()
                    # Obtiene la ubicación de la barra en el eje x (centro de la barra)
                    x_loc = bar.get_x() + bar.get_width() / 2

                    # Añadir un texto en la gráfica con la altura y la ubicación en x
                    current_annotation = ax.text(x_loc, height, f'Cantidad: {height:.0f}\nAño: {x_loc:.0f}', 
                                                 ha='center', va='bottom', color='black', fontsize=12)

                    # Refrescar el gráfico para mostrar el texto
                    plt.draw()

        # Conectar el evento de clic con la figura
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    except ValueError:
        resultado_label.config(text="Por favor, ingrese valores numéricos válidos.")

root = tk.Tk()

# Configura la ventana
root.title("Calculadora de interés compuesto")

# Crea etiquetas y campos de entrada
tk.Label(root, text="Cantidad:").pack(pady=5)
cantidad_entry = tk.Entry(root)  # Cambiado el nombre de la variable para evitar conflicto
cantidad_entry.pack(pady=5)

tk.Label(root, text="Importe anual:").pack(pady=5)
importe_anual_entry = tk.Entry(root)
importe_anual_entry.pack(pady=5)

tk.Label(root, text="Años:").pack(pady=5)
años_entry = tk.Entry(root)
años_entry.pack(pady=5)

tk.Label(root, text="Interés (%):").pack(pady=5)
interes_entry = tk.Entry(root)
interes_entry.pack(pady=5)

# Crea un botón de cálculo
boton_calcular = tk.Button(root, text="Calcular", command=calcular_interes_compuesto)
boton_calcular.pack(pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=10)

# Vincula la tecla Enter al botón de cálculo
root.bind("<Return>", calcular_interes_compuesto)

# Coloca el foco inicial en el primer campo de entrada
cantidad_entry.focus_set()

# Inicia el bucle principal de eventos
root.mainloop()
