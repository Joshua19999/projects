import tkinter as tk
from random import randrange

# --- Funciones del juego ---
def make_list_of_free_fields(board):
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O','X']:
                free.append((row,col))
    return free

def victory_for(board, sgn):
    # filas y columnas
    for rc in range(3):
        if all(board[rc][c] == sgn for c in range(3)):
            highlight([(rc,0),(rc,1),(rc,2)])
            return True
        if all(board[r][rc] == sgn for r in range(3)):
            highlight([(0,rc),(1,rc),(2,rc)])
            return True
    # diagonales
    if all(board[i][i] == sgn for i in range(3)):
        highlight([(0,0),(1,1),(2,2)])
        return True
    if all(board[i][2-i] == sgn for i in range(3)):
        highlight([(0,2),(1,1),(2,0)])
        return True
    return False

def draw_move(board):
    free = make_list_of_free_fields(board)
    if free:
        row, col = free[randrange(len(free))]
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state="disabled", disabledforeground="red")
        if victory_for(board, 'X'):
            status_label.config(text="💻 ¡He ganado!")
            disable_all()

def player_move(row, col):
    if board[row][col] not in ['O','X']:
        board[row][col] = 'O'
        buttons[row][col].config(text='O', state="disabled", disabledforeground="blue")
        if victory_for(board, 'O'):
            status_label.config(text="🎉 ¡Has ganado!")
            disable_all()
        else:
            draw_move(board)
            if not make_list_of_free_fields(board) and not victory_for(board,'X'):
                status_label.config(text="🤝 ¡Empate!")

def disable_all():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state="disabled")

def highlight(cells):
    for r,c in cells:
        buttons[r][c].config(bg="yellow")

def reset_game():
    global board
    board = [[3*j+i+1 for i in range(3)] for j in range(3)]
    board[1][1] = 'X'  # jugada inicial de la máquina
    for r in range(3):
        for c in range(3):
            text = str(board[r][c]) if board[r][c] not in ['O','X'] else board[r][c]
            buttons[r][c].config(text=text, state="normal", bg="#444", fg="white")
    buttons[1][1].config(text='X', state="disabled", disabledforeground="red")
    status_label.config(text="Tu turno")

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Tres en Raya")
ventana.configure(bg="#222")

board = [[3*j+i+1 for i in range(3)] for j in range(3)]
board[1][1] = 'X'  # primer jugada de la máquina

buttons = [[None for _ in range(3)] for _ in range(3)]

frame = tk.Frame(ventana, bg="#222")
frame.pack(pady=20)

for r in range(3):
    for c in range(3):
        text = str(board[r][c]) if board[r][c] not in ['O','X'] else board[r][c]
        buttons[r][c] = tk.Button(frame, text=text, width=6, height=3,
                                  font=("Arial", 20, "bold"),
                                  bg="#444", fg="white",
                                  activebackground="#666",
                                  command=lambda r=r, c=c: player_move(r,c))
        buttons[r][c].grid(row=r, column=c, padx=5, pady=5)

# deshabilitar la jugada inicial de la máquina
buttons[1][1].config(text='X', state="disabled", disabledforeground="red")

status_label = tk.Label(ventana, text="Tu turno", font=("Arial", 16, "bold"), bg="#222", fg="white")
status_label.pack(pady=10)

reset_button = tk.Button(ventana, text="🔄 Reiniciar partida", font=("Arial", 12, "bold"),
                         bg="#555", fg="white", command=reset_game)
reset_button.pack(pady=10)

ventana.mainloop()
