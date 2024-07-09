import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Define a classe 'cube', que representa um bloco da cobra ou do snack
class cube(object):
    rows = 20  # Número de linhas no grid
    w = 500    # Largura da janela do jogo
    
    def __init__(self, start, dirnx=1, dirny=0, color=(0, 255, 0)):
        self.pos = start  # Posição inicial do cubo
        self.dirnx = dirnx  # Direção no eixo x
        self.dirny = dirny  # Direção no eixo y
        self.color = color  # Cor do cubo

    # Método para mover o cubo na direção especificada
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # Método para desenhar o cubo na superfície do jogo
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:  # Desenhar olhos no cubo (cabeça da cobra)
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Define a classe 'snake', que representa a cobra
class snake(object):
    body = []  # Corpo da cobra
    turns = {}  # Dicionário de voltas da cobra

    def __init__(self, color, pos):
        self.color = color  # Cor da cobra
        self.head = cube(pos)  # Cabeça da cobra
        self.body.append(self.head)  # Adiciona a cabeça ao corpo
        self.dirnx = 0  # Direção no eixo x
        self.dirny = 1  # Direção no eixo y

    # Método para mover a cobra
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Encerra o jogo se a janela for fechada
                pygame.quit()
                pygame.mixer.music.stop()
                return

            keys = pygame.key.get_pressed()  # Verifica quais teclas estão pressionadas

            # Define a direção da cobra com base nas teclas pressionadas
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Verifica se a cobra bateu nas bordas do grid
                if c.dirnx == -1 and c.pos[0] <= 0 or c.dirnx == 1 and c.pos[0] >= c.rows - 1 or c.dirny == 1 and c.pos[1] >= c.rows - 1 or c.dirny == -1 and c.pos[1] <= 0:
                    message_box('Você perdeu!', 'Bateu na borda.')
                    pygame.mixer.music.stop()  # Para a música quando a cobra bate nas bordas
                    self.reset((10, 10))
                    return
                else:
                    c.move(c.dirnx, c.dirny)

    # Método para resetar a cobra (após perder)
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # Método para adicionar um cubo ao corpo da cobra
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    # Método para desenhar a cobra na superfície do jogo
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # Desenha a cabeça da cobra com olhos
            else:
                c.draw(surface)

# Função para desenhar o grid na superfície do jogo
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# Função para atualizar a janela do jogo
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

# Função para gerar uma posição aleatória para o snack
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

# Função para exibir uma mensagem de alerta usando tkinter
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# Função principal que inicializa e executa o jogo
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((width, width))
    s = snake((0, 255, 0), (10, 10))  # Inicializa a cobra com a cor verde
    snack = cube(randomSnack(rows, s), color=(255, 0, 0))  # Inicializa o snack com a cor vermelha
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box('Você perdeu!', 'Bateu em si mesma.')
                pygame.mixer.music.stop()  # Para a música quando a cobra colide consigo mesma
                s.reset((10, 10))
                flag = False  # Encerra o loop do jogo

        redrawWindow(win)

    pygame.mixer.music.load('./music/Music_Apoxode_-_Electric_1.mp3')  # Carrega o arquivo de música
    pygame.mixer.music.play(-1)  # Reproduz a música em loop

main()
