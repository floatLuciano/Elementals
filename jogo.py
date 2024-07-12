from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *
import pygame

class Jogo:
    def __init__(self, j1, j2):
        self.janela = Window(800, 400)
        self.janela.set_title("Elementals")
        self.teclado = Keyboard()
        self.fundo = GameImage("./Assets/fundo.jpg")
        self.plataforma1 = Sprite("./Assets/plataforma1_principal.png")
        self.plataforma1.set_position(self.janela.width / 2 - 140, self.janela.height - 110)
        self.plataforma2 = Sprite("./Assets/plataforma1_menor.png")
        self.plataforma2.set_position(30, self.janela.height / 2)

        self.personagem1 = Sprite(j1, frames=52)
        self.personagem1.set_position(self.plataforma1.x, self.plataforma1.y - self.personagem1.height)

        self.personagem1.set_curr_frame(0)

        self.personagem2 = Sprite(j2, frames=52)
        self.personagem2.set_position(self.plataforma1.x + 200, self.plataforma1.y - self.personagem2.height)
        self.personagem2.set_curr_frame(0)

        self.velocidade = 100
        self.gravidade = 1000
        self.velocidade_pulo = -400

        self.inicializar_variaveis_personagem1()
        self.inicializar_variaveis_personagem2()

        self.teclas_personagem1 = {
            "left": "A",
            "right": "D",
            "jump": "W",
            "attack": "N"
        }

        self.teclas_personagem2 = {
            "left": "LEFT",
            "right": "RIGHT",
            "jump": "UP",
            "attack": "Z"
        }

    def inicializar_variaveis_personagem1(self):
        self.virado1 = None
        self.direcao1 = None
        self.atacando1 = False
        self.tempo_recarga1 = 0
        self.velocidade_y1 = 0
        self.no_chao1 = True
        self.vidas1 = 3
        self.porcentagem1 = 0
        self.golpe_contado1 = False
        self.pulo_duplo_disponivel1 = 2
        self.pulou_antes1 = False
        self.danificado1 = False
        self.knockback_timer1 = 0

    def inicializar_variaveis_personagem2(self):
        self.virado2 = None
        self.direcao2 = None
        self.atacando2 = False
        self.tempo_recarga2 = 0
        self.velocidade_y2 = 0
        self.no_chao2 = True
        self.vidas2 = 3
        self.porcentagem2 = 0
        self.golpe_contado2 = False
        self.pulo_duplo_disponivel2 = 2
        self.pulou_antes2 = False
        self.danificado2 = False
        self.knockback_timer2 = 0

    def create_sword_hitbox(self, personagem, virado):
        sword_hitbox = None
        if virado == "RIGHT":
            sword_hitbox = [personagem.x + personagem.width / 2, personagem.y + personagem.height / 2, personagem.width / 4 - 4, personagem.height / 2]
        elif virado == "LEFT":
            sword_hitbox = [personagem.x + personagem.width / 4 + 4, personagem.y + personagem.height / 2, personagem.width / 4 - 4, personagem.height / 2]
        return pygame.Rect(sword_hitbox)

    def get_personagem_hitbox(self, personagem):
        return pygame.Rect([personagem.x + personagem.width / 2 - 10, personagem.y + 2 * personagem.height / 3, 22, personagem.height / 3])

    def is_attack_frame(self, personagem, attack_frames):
        curr_frame = personagem.get_curr_frame()
        return curr_frame in attack_frames

    def aplicar_knockback(self, personagem, virado, knockback_force):
        if virado == "RIGHT":
            personagem.move_y(-knockback_force)
            personagem.move_x(knockback_force)
        
        elif virado == "LEFT":
            personagem.move_y(-knockback_force)
            personagem.move_x(-knockback_force)


    def controlar_personagem(self, personagem, teclado, keys, virado, direcao, atacando, tempo_recarga, velocidade_y, no_chao, delta_time, opponent, vidas, porcentagem, golpe_contado, pulo_duplo_disponivel, pulou_antes, danificado, knockback_timer, opponent_porcentagem):
        andou = False
        estado_anterior_no_chao = no_chao

        if not personagem.collided_perfect(self.plataforma1) and not personagem.collided_perfect(self.plataforma2):
            no_chao = False
        else:
            no_chao = True

        if personagem.y >= 165 and personagem.x <= 103:
            no_chao = False

        if no_chao:
            pulo_duplo_disponivel = 2

        if teclado.key_pressed(keys["right"]) and not atacando:
            personagem.move_x(self.velocidade * delta_time)
            if direcao != "RIGHT":
                personagem.set_sequence(0, 7, True)
                personagem.set_total_duration(1500)
                personagem.play()
                direcao = "RIGHT"
                virado = "RIGHT"
            andou = True
        elif teclado.key_pressed(keys["left"]) and not atacando:
            personagem.move_x(-self.velocidade * delta_time)
            if direcao != "LEFT":
                personagem.set_sequence(8, 15, True)
                personagem.set_total_duration(1500)
                personagem.play()
                direcao = "LEFT"
                virado = "LEFT"
            andou = True
        elif teclado.key_pressed(keys["attack"]) and not atacando and tempo_recarga <= 0:
            atacando = True
            golpe_contado = False  # Resetando o golpe ao iniciar o ataque
            if virado == "RIGHT":
                personagem.set_sequence(25, 29, False)
            elif virado == "LEFT":
                personagem.set_sequence(30, 34, False)
            personagem.set_total_duration(1500)
            personagem.play()
            tempo_recarga = 0.5  # 0.5 segundos de recarga
        else:
            if not atacando:
                if virado == "RIGHT":
                    personagem.set_curr_frame(0)
                elif virado == "LEFT":
                    personagem.set_curr_frame(8)
                direcao = None

        if teclado.key_pressed(keys["jump"]) and not pulou_antes:
            if no_chao or pulo_duplo_disponivel > 0:
                if velocidade_y == 0 or pulo_duplo_disponivel == 2:
                    velocidade_y = self.velocidade_pulo * (1 - porcentagem / 100 *0.5)  # Aplicar o multiplicador da porcentagem
                else:
                    velocidade_y = self.velocidade_pulo * (1 - porcentagem / 100* 0.5)  # Dar o segundo pulo com o multiplicador
                no_chao = False
                pulo_duplo_disponivel -= 1
                print(f"Pulo duplo disponível: {pulo_duplo_disponivel}") 
                pulou_antes = True

        if not teclado.key_pressed(keys["jump"]):
            pulou_antes = False

        if not no_chao:
            velocidade_y += self.gravidade * delta_time
            personagem.move_y(velocidade_y * delta_time)
            if velocidade_y < 0:  # Subindo
                if virado == "RIGHT":
                    personagem.set_sequence(17, 18, False)
                elif virado == "LEFT":
                    personagem.set_sequence(21, 22, False)
            else:  # Descendo
                if virado == "RIGHT":
                    personagem.set_sequence(19, 20, False)
                elif virado == "LEFT":
                    personagem.set_sequence(23, 24, False)

        if atacando:
            personagem.update()
            if personagem.get_curr_frame() in [28, 33]:
                atacando = False
                if direcao == "RIGHT":
                    personagem.set_sequence(0, 7, True)
                elif direcao == "LEFT":
                    personagem.set_sequence(8, 15, True)
                personagem.set_total_duration(500)
                personagem.play()
            else:
                attack_frames_right = [26, 27]
                attack_frames_left = [32, 33]
                if virado == "RIGHT" and self.is_attack_frame(personagem, attack_frames_right) and not golpe_contado:
                    sword_hitbox = self.create_sword_hitbox(personagem, virado)
                    opponent_hitbox = self.get_personagem_hitbox(opponent)
                    if sword_hitbox.colliderect(opponent_hitbox):
                        if not danificado:
                            opponent.set_sequence(45, 49, False)  # Animação para golpe pela esquerda
                            opponent.set_total_duration(1000)
                            opponent_porcentagem += 10  # Aumentar a porcentagem do oponente
                            danificado = True
                            knockback_timer = 0.2  # Aplicar knockback por 0.2 segundos
                            self.aplicar_knockback(opponent, virado, 10 + opponent_porcentagem * 0.1)
                        print("Acertou o oponente com a espada!")
                        golpe_contado = True
                elif virado == "LEFT" and self.is_attack_frame(personagem, attack_frames_left) and not golpe_contado:
                    sword_hitbox = self.create_sword_hitbox(personagem, virado)
                    opponent_hitbox = self.get_personagem_hitbox(opponent)
                    if sword_hitbox.colliderect(opponent_hitbox):
                        if not danificado:
                            opponent.set_sequence(49, 52, False)  # Animação para golpe pela direita
                            opponent.set_total_duration(1000)
                            opponent_porcentagem += 10  # Aumentar a porcentagem do oponente
                            danificado = True
                            knockback_timer = 0.2  # Aplicar knockback por 0.2 segundos
                            self.aplicar_knockback(opponent, virado, 10 + opponent_porcentagem * 0.1)
                        print("Acertou o oponente com a espada!")
                        golpe_contado = True
        else:
            if andou:
                personagem.update()

        if knockback_timer > 0:
            knockback_timer -= delta_time

        if danificado and knockback_timer <= 0:
            danificado = False

        if no_chao and not estado_anterior_no_chao:
            if virado == "RIGHT":
                personagem.set_curr_frame(0)
            elif virado == "LEFT":
                personagem.set_curr_frame(8)
            if teclado.key_pressed(keys["right"]) and not atacando:
                personagem.set_sequence(0, 7, True)
                personagem.set_total_duration(1500)
                personagem.play()
            elif teclado.key_pressed(keys["left"]) and not atacando:
                personagem.set_sequence(8, 15, True)
                personagem.set_total_duration(1500)
                personagem.play()

        # Verificar se o personagem saiu da tela
        if personagem.x < -100 or personagem.x > self.janela.width + 100 or personagem.y < -100 or personagem.y > self.janela.height + 100:
            personagem.set_position(self.janela.width / 2 - personagem.width / 2, self.janela.height / 2 - personagem.height / 2)
            vidas -= 1
            porcentagem = 0

        tempo_recarga -= delta_time

        return virado, direcao, atacando, tempo_recarga, velocidade_y, no_chao, vidas, porcentagem, golpe_contado, pulo_duplo_disponivel, pulou_antes, danificado, knockback_timer, opponent_porcentagem

    def draw_text(self, text, x, y, size, color):
         self.janela.draw_text(text, x, y, size=size, color=color, font_name="Arial", bold=True)


    def get_percentage_color(self, percentage):
        if 0 <= percentage <= 19:
            return "white"
        elif 20 <= percentage <= 29:
            return "beige"
        elif 30 <= percentage <= 69:
            return "yellow"
        elif 70 <= percentage <= 99:
            return "orange"
        elif 100 <= percentage <= 150:
            return "red"
        else:
            return "white"

    def run(self):
        while True:
            delta_time = self.janela.delta_time()
            self.janela.update()
            self.fundo.draw()
            self.plataforma1.draw()
            self.plataforma2.draw()
            self.personagem1.draw()
            self.personagem2.draw()

            self.virado1, self.direcao1, self.atacando1, self.tempo_recarga1, self.velocidade_y1, self.no_chao1, self.vidas1, self.porcentagem1, self.golpe_contado1, self.pulo_duplo_disponivel1, self.pulou_antes1, self.danificado1, self.knockback_timer1, self.porcentagem2 = self.controlar_personagem(
                self.personagem1, self.teclado, self.teclas_personagem1, self.virado1, self.direcao1, self.atacando1, self.tempo_recarga1, self.velocidade_y1, self.no_chao1, delta_time, self.personagem2, self.vidas1, self.porcentagem1, self.golpe_contado1, self.pulo_duplo_disponivel1, self.pulou_antes1, self.danificado1, self.knockback_timer1, self.porcentagem2)

            self.virado2, self.direcao2, self.atacando2, self.tempo_recarga2, self.velocidade_y2, self.no_chao2, self.vidas2, self.porcentagem2, self.golpe_contado2, self.pulo_duplo_disponivel2, self.pulou_antes2, self.danificado2, self.knockback_timer2, self.porcentagem1 = self.controlar_personagem(
                self.personagem2, self.teclado, self.teclas_personagem2, self.virado2, self.direcao2, self.atacando2, self.tempo_recarga2, self.velocidade_y2, self.no_chao2, delta_time, self.personagem1, self.vidas2, self.porcentagem2, self.golpe_contado2, self.pulo_duplo_disponivel2, self.pulou_antes2, self.danificado2, self.knockback_timer2, self.porcentagem1)

            self.draw_text(f"Vidas: {self.vidas1}", 10, 10, 20, "white")
            self.draw_text(f"{self.porcentagem1}%", 10, 30, 30, self.get_percentage_color(self.porcentagem1))
            self.draw_text(f"Vidas: {self.vidas2}", self.janela.width - 100, 10, 20, "white")

            self.draw_text(f"{self.porcentagem2}%", self.janela.width - 100, 30, 30, self.get_percentage_color(self.porcentagem2))

            
            if self.teclado.key_pressed("ESC"):
                break
            self.janela.update()
        self.janela.close()

if __name__ == "__main__":
    jogo = Jogo("./Assets/bg1.jpg", "./Assets/personagens/Elemental_fire.png", "./Assets/personagens/Elemental_water.png")
    jogo.run()
