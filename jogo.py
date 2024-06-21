from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *

class Personagem:
    def __init__(self, imagem, x, y, keys):
        self.sprite = Sprite(imagem, frames=52)
        self.sprite.set_position(x, y)
        self.sprite.set_curr_frame(0)
        self.direcao = None
        self.virado = None
        self.atacando = False
        self.velocidade_y = 0
        self.no_chao = True
        self.keys = keys

    def controlar(self, teclado, delta_time, gravidade, velocidade, velocidade_pulo):
        andou = False
        p = self.sprite

        if teclado.key_pressed(self.keys["right"]) and not self.atacando:
            p.move_x(velocidade * delta_time)
            if self.direcao != "RIGHT":
                p.set_sequence(0, 7, True)
                p.set_total_duration(1500)
                p.play()
                self.direcao = "RIGHT"
                self.virado = "RIGHT"
            andou = True
        elif teclado.key_pressed(self.keys["left"]) and not self.atacando:
            p.move_x(-velocidade * delta_time)
            if self.direcao != "LEFT":
                p.set_sequence(8, 15, True)
                p.set_total_duration(1500)
                p.play()
                self.direcao = "LEFT"
                self.virado = "LEFT"
            andou = True
        elif teclado.key_pressed(self.keys["attack"]) and not self.atacando:
            self.atacando = True
            if self.virado == "RIGHT":
                p.set_sequence(25, 29, False)
            elif self.virado == "LEFT":
                p.set_sequence(30, 34, False)
            p.set_total_duration(1500)
            p.play()
        else:
            if not self.atacando:
                if self.virado == "RIGHT":
                    p.set_curr_frame(0)
                elif self.virado == "LEFT":
                    p.set_curr_frame(8)
                self.direcao = None

        if teclado.key_pressed(self.keys["up"]) and self.no_chao:
            self.velocidade_y = velocidade_pulo
            self.no_chao = False

        # Aplicação da gravidade
        if not self.no_chao:
            self.velocidade_y += gravidade * delta_time
            p.move_y(self.velocidade_y * delta_time)
            if self.virado == "RIGHT":
                p.set_sequence(17, 20)
            elif self.virado == "LEFT":
                p.set_sequence(21, 24)

        # Verifica se o personagem está no chão
        if p.y >= janela.height - p.height - 30:
            p.y = janela.height - p.height - 30
            self.velocidade_y = 0
            self.no_chao = True

        # Verifica se a animação de ataque terminou
        if self.atacando:
            p.update()
            if (p.get_curr_frame() == 28) or (p.get_curr_frame() == 33):
                self.atacando = False
                if self.direcao == "RIGHT":
                    p.set_sequence(0, 7, True)
                elif self.direcao == "LEFT":
                    p.set_sequence(8, 15, True)
                p.set_total_duration(500)
                p.play()
        else:
            if andou:
                p.update()

janela = Window(800, 400)
janela.set_title("Elementals")

teclado = Keyboard()
fundo = GameImage("./Assets/tela1.jpg")

# Instanciação dos personagens
personagens = [
    Personagem("./Assets/personagens/Elemental_fire.png", janela.width / 2 - 100, janela.height - 110, {"left": "LEFT", "right": "RIGHT", "up": "UP", "attack": "Z"}),
    Personagem("./Assets/personagens/Elemental_water.png", janela.width / 2 + 100, janela.height - 110, {"left": "A", "right": "D", "up": "W", "attack": "N"})
]

velocidade = 100
gravidade = 1000
velocidade_pulo = -400

while True:
    delta_time = janela.delta_time()

    for personagem in personagens:
        personagem.controlar(teclado, delta_time, gravidade, velocidade, velocidade_pulo)

    fundo.draw()
    for personagem in personagens:
        personagem.sprite.draw()

    janela.update()
