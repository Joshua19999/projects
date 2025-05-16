import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import subprocess
import shlex

# Lista de instrucciones para autocompletar
instrucciones_disponibles = [
    "listar archivos",
    "mostrar directorio actual",
    "cambiar de directorio",
    "crear una carpeta",
    "eliminar una carpeta",
    "ver contenido de un archivo",
    "copiar archivo",
    "mover archivo",
    "borrar archivo",
    "descargar archivo",
    "ver procesos",
    "buscar archivo",
    "ver uso del disco",
    "ver configuración de red",
    "ver interfaces de red",
    "hacer ping",
    "ver tabla de enrutamiento",
    "mostrar puertos abiertos",
    "ver dirección ip"
]

# Diccionario de comandos con placeholders
comandos = {
    "listar archivos": "ls",
    "mostrar directorio actual": "pwd",
    "cambiar de directorio": "cd {nombre_directorio} && ls",
    "crear una carpeta": "mkdir {nombre_carpeta}",
    "eliminar una carpeta": "rm -r {nombre_carpeta}",
    "ver contenido de un archivo": "cat {archivo}",
    "copiar archivo": "cp {origen} {destino}",
    "mover archivo": "mv {origen} {destino}",
    "borrar archivo": "rm {archivo}",
    "descargar archivo": "wget {url}",
    "ver procesos": "ps aux",
    "buscar archivo": "find . -name {archivo}",
    "ver uso del disco": "df -h",
    "ver configuración de red": "ifconfig || ip addr",
    "ver interfaces de red": "ip link show",
    "hacer ping": "ping -c 4 {host}",
    "ver tabla de enrutamiento": "netstat -rn || ip route",
    "mostrar puertos abiertos": "ss -tuln || netstat -tuln",
    "ver dirección ip": "hostname -I"
}

historial = []

def traducir_a_linux(entrada):
    for clave, plantilla in comandos.items():
        if clave in entrada.lower():
            placeholders = [word.strip("{}") for word in plantilla.split() if word.startswith("{")]
            if placeholders:
                valores = {}
                for campo in placeholders:
                    valor = simpledialog.askstring("Entrada requerida", f"Ingrese {campo.replace('_', ' ')}:")
                    if not valor:
                        return None, "❌ Acción cancelada."
                    valores[campo] = valor
                try:
                    comando = plantilla.format(**valores)
                    return comando, None
                except KeyError as e:
                    return None, f"❌ Faltó un valor para: {e}"
            else:
                return plantilla, None
    return None, "❌ No se encontró un comando equivalente."

def ejecutar_comando(comando):
    try:
        resultado = subprocess.check_output(["wsl"] + shlex.split(comando), stderr=subprocess.STDOUT)
        return resultado.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"⚠️ Error al ejecutar el comando:\n{e.output.decode('utf-8')}"

def procesar_instruccion(event=None):
    entrada = entrada_texto.get()
    if not entrada.strip():
        messagebox.showwarning("Atención", "Escribe una instrucción.")
        return
    comando, error = traducir_a_linux(entrada)
    if error:
        salida_texto.insert(tk.END, f"{error}\n\n")
        salida_texto.yview(tk.END)
        return
    historial.append(comando)
    salida_texto.insert(tk.END, f">>> {comando}\n")
    resultado = ejecutar_comando(comando)
    salida_texto.insert(tk.END, f"{resultado}\n\n")
    salida_texto.yview(tk.END)
    entrada_texto.delete(0, tk.END)

def mostrar_historial():
    if historial:
        hist = "\n".join(historial)
        messagebox.showinfo("Historial de comandos", hist)
    else:
        messagebox.showinfo("Historial vacío", "Aún no has ejecutado ningún comando.")

def mostrar_ayuda():
    ayuda = "\nComandos disponibles:\n" + "-" * 30 + "\n"
    for clave in comandos.keys():
        ayuda += f"• {clave}\n"
    messagebox.showinfo("Ayuda", ayuda)

def autocompletar(event):
    texto = entrada_texto.get()
    coincidencias = [i for i in instrucciones_disponibles if i.startswith(texto)]
    if len(coincidencias) == 1:
        entrada_texto.delete(0, tk.END)
        entrada_texto.insert(0, coincidencias[0])
        return "break"
    elif len(coincidencias) > 1:
        salida_texto.insert(tk.END, f"🔍 Coincidencias: {', '.join(coincidencias)}\n")
        salida_texto.yview(tk.END)
        return "break"

# Interfaz gráfica
root = tk.Tk()
root.title("Traductor a Comandos Linux")
root.geometry("700x500")

tk.Label(root, text="Instrucción en lenguaje natural:").pack(pady=5)

entrada_texto = tk.Entry(root, width=80)
entrada_texto.pack(pady=5)
entrada_texto.bind("<Tab>", autocompletar)
entrada_texto.bind("<Return>", procesar_instruccion)  # Ejecuta con Enter

frame_botones = tk.Frame(root)
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Traducir y Ejecutar", command=procesar_instruccion).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Ayuda", command=mostrar_ayuda).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Historial", command=mostrar_historial).pack(side=tk.LEFT, padx=5)

salida_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=20)
salida_texto.pack(pady=10)

root.mainloop()
