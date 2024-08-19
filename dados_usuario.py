import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk

def tirar_dados():
    # Cierra la ventana principal al iniciar esta función
    root.destroy()

    def mostrar_resultado(event=None):
        try:
            # Obtiene el texto ingresado en la entrada y lo convierte a entero
            cantidad = int(entrada.get())
            
            # Genera una serie de números aleatorios entre 1 y 9
            dados = pd.Series(np.random.randint(1, 9, cantidad))
            
            # Convierte la serie a una cadena separada por comas
            dadosstr = ", ".join(map(str, dados))
            
            # Actualiza el texto del Label con el resultado
            resultado_label.config(text=f"Has ingresado: {dadosstr}")

            # Crea un botón que llama a la función contar_veces cuando se presiona
            contar_button = tk.Button(root_dados, text="Contar", command=lambda: contar_veces(dados))
            contar_button.pack(pady=10)
            
        except ValueError:
            # Maneja el caso donde la entrada no puede ser convertida a entero
            resultado_label.config(text="Por favor, ingrese un número válido.")
    
    def contar_veces(dados):
        # Esta función contará las veces que aparece cada número en la serie 'dados'
        conteo = dados.value_counts().sort_index().to_string()
        conteo_label.config(text=f"Conteo de resultados:\n{conteo}")
        
        # Crea un botón que llama a la función mostrar_dataframe cuando se presiona
        hacer_tabla_button = tk.Button(root_dados, text="Hacer tabla", command=lambda: mostrar_dataframe(dados))
        hacer_tabla_button.pack(pady=10)

    def mostrar_dataframe(dados):
        # Convierte el conteo de valores a un DataFrame
        conteo_df = pd.DataFrame({'Número': dados.value_counts().index, 'Cantidad': dados.value_counts().values})

        # Cierra la ventana de los dados
        root_dados.destroy()

        # Crea una nueva ventana para mostrar el DataFrame
        Tabla = tk.Tk()
        Tabla.title("Resultado del Conteo")

        # Muestra el DataFrame en un Label en la nueva ventana
        tabla_label = tk.Label(Tabla, text=conteo_df.to_string(index=False))
        tabla_label.pack(pady=10)

        # Añade un botón para cerrar la nueva ventana
        close_button = tk.Button(Tabla, text="Cerrar", command=Tabla.destroy)
        close_button.pack(pady=10)

        # Añade un botón para generar el gráfico de barras
        hacer_plot_button = tk.Button(Tabla, text="Hacer gráfico", command=lambda: make_barplot(conteo_df))
        hacer_plot_button.pack(pady=10)

        Tabla.mainloop()
    
    # Crea la ventana para el proceso de tirar dados
    root_dados = tk.Tk()
    root_dados.title("Tirar Dados")

    # Etiqueta para solicitar la cantidad
    tk.Label(root_dados, text="¿Cuántas veces?").pack(pady=10)
    
    # Entrada de texto para que el usuario ingrese la cantidad
    entrada = tk.Entry(root_dados)
    entrada.pack(pady=10)
    entrada.focus_set()  # Coloca el foco en la entrada de texto

    # Vincula la tecla "Enter" para obtener la respuesta
    entrada.bind("<Return>", mostrar_resultado)
    
    # Etiqueta para mostrar el resultado
    resultado_label = tk.Label(root_dados, text="")
    resultado_label.pack(pady=10)

    # Etiqueta para mostrar el conteo después de presionar el botón "Contar"
    conteo_label = tk.Label(root_dados, text="")
    conteo_label.pack(pady=10)

    root_dados.mainloop()


def make_barplot(dadosdf):
    ax = sns.barplot(x="Número", y="Cantidad", data=dadosdf, palette="cool")

    plt.title("Veces que salió cada número")
    plt.xlabel("Número")
    plt.ylabel("Veces que salió")
    ax.set(yticks=[])  # Oculta las etiquetas del eje y

    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'),
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),  # Desplazamiento de las etiquetas
                    textcoords='offset points')

    plt.show()

# Crea una ventana principal
root = tk.Tk()

# Opcional: Configura la ventana (título, tamaño, etc.)
root.title("Dados")

# Añade widgets (botones, etiquetas, cuadros de texto, etc.)
lanzar_dados = tk.Button(root, text="Lanzar dados", command=tirar_dados)
lanzar_dados.pack(pady=10)

# Inicia el bucle principal de eventos
root.mainloop()
