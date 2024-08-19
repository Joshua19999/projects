import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicializar Pygame
pygame.init()

# Crear ventana y OpenGL context
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
glViewport(0, 0, 800, 600)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (800/600), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

# Cargar modelo 3D
vertices = [|
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
]
edges = [
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
]

# Bucle principal de juego
running = True
while running:
    # Manejar eventos de entrada
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar pantalla y dibujar modelo 3D
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(pygame.time.get_ticks() / 10, 1, 1, 1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Actualizar pantalla
    pygame.display.flip()

# Finalizar Pygame
pygame.quit()
