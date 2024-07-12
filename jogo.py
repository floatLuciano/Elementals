from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *

def create_sword_hitbox(personagem, virado):
    sword_hitbox = None
    if virado == "RIGHT":
        sword_hitbox = [personagem.x + 40, personagem.y + 10, 20, 10]
    elif virado == "LEFT":
        sword_hitbox = [personagem.x - 20, personagem.y + 10, 20, 10]
    return sword_hitbox

def is_attack_frame(personagem, attack_frames):
    curr_frame = personagem.get_curr_frame()
    return curr_frame in attack_frames

def hitbox_collided(hitbox1, hitbox2):
    x1, y1, w1, h1 = hitbox1
    x2, y2, w2, h2 = hitbox2
    return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2)

def aplicar_knockback(personagem, virado, knockback_force):
    if virado == "RIGHT":
        personagem.move_x(knockback_force)
    elif virado == "LEFT":
        personagem.move_x(-knockback_force)

def controlar_personagem(personagem, teclado, keys, virado, direcao, atacando, tempo_recarga, velocidade_y, no_chao, delta_time, opponent, vidas, porcentagem, golpe_contado, pulo_duplo_disponivel, pulou_antes, danificado, knockback_timer, opponent_porcentagem):
    andou = False
    estado_anterior_no_chao = no_chao

    if (personagem.collided_perfect(plataforma1) == False) and (personagem.collided_perfect(plataforma2) == False):
        no_chao = False
    else:
        no_chao = True

    if personagem.y >= 165 and personagem.x <= 103:
        no_chao = False

    if no_chao:
        pulo_duplo_disponivel = 2

    if teclado.key_pressed(keys["right"]) and not atacando:
        personagem.move_x(velocidade * delta_time)
        if direcao != "RIGHT":
            personagem.set_sequence(0, 7, True)
            personagem.set_total_duration(1500)
            personagem.play()
            direcao = "RIGHT"
            virado = "RIGHT"
        andou = True
    elif teclado.key_pressed(keys["left"]) and not atacando:
        personagem.move_x(-velocidade * delta_time)
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
                velocidade_y = velocidade_pulo * (1 - porcentagem / 100)  # Aplicar o multiplicador da porcentagem
            else:
                velocidade_y = velocidade_pulo * (1 - porcentagem / 100)  # Dar o segundo pulo com o multiplicador
            no_chao = False
            pulo_duplo_disponivel -= 1
            print(f"Pulo duplo disponível: {pulo_duplo_disponivel}")  # Print de depuração
            pulou_antes = True

    if not teclado.key_pressed(keys["jump"]):
        pulou_antes = False

    if no_chao == False:
        velocidade_y += gravidade * delta_time
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
        if (personagem.get_curr_frame() == 28) or (personagem.get_curr_frame() == 33):
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
            if virado == "RIGHT" and is_attack_frame(personagem, attack_frames_right) and not golpe_contado:
                sword_hitbox = create_sword_hitbox(personagem, virado)
                opponent_hitbox = [opponent.x, opponent.y, opponent.width, opponent.height]
                if hitbox_collided(sword_hitbox, opponent_hitbox):
                    if not danificado:
                        opponent.set_sequence(45, 49, False)  # Animação para golpe pela esquerda
                        opponent.set_total_duration(1000)
                        opponent_porcentagem += 10  # Aumentar a porcentagem do oponente
                        danificado = True
                        knockback_timer = 0.2  # Aplicar knockback por 0.2 segundos
                        aplicar_knockback(opponent, virado, 10 + opponent_porcentagem * 0.1)
                    print("Acertou o oponente com a espada!")
                    golpe_contado = True
            elif virado == "LEFT" and is_attack_frame(personagem, attack_frames_left) and not golpe_contado:
                sword_hitbox = create_sword_hitbox(personagem, virado)
                opponent_hitbox = [opponent.x, opponent.y, opponent.width, opponent.height]
                if hitbox_collided(sword_hitbox, opponent_hitbox):
                    if not danificado:
                        opponent.set_sequence(49, 52, False)  # Animação para golpe pela direita
                        opponent.set_total_duration(1000)
                        opponent_porcentagem += 10  # Aumentar a porcentagem do oponente
                        danificado = True
                        knockback_timer = 0.2  # Aplicar knockback por 0.2 segundos
                        aplicar_knockback(opponent, virado, 10 + opponent_porcentagem * 0.1)
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
    if personagem.x < -100 or personagem.x > janela.width + 100 or personagem.y < -100 or personagem.y > janela.height + 100:
        personagem.set_position(janela.width / 2 - personagem.width / 2, janela.height / 2 - personagem.height / 2)
        vidas -= 1
        porcentagem = 0

    tempo_recarga -= delta_time

    return virado, direcao, atacando, tempo_recarga, velocidade_y, no_chao, vidas, porcentagem, golpe_contado, pulo_duplo_disponivel, pulou_antes, danificado, knockback_timer, opponent_porcentagem

def draw_text(text, x, y, size, color, janela):
    janela.draw_text(text, x, y, size=size, color=color, font_name="Arial", bold=True)

def get_percentage_color(percentage):
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

janela = Window(800, 400)
janela.set_title("Elementals")
teclado = Keyboard()
fundo = GameImage("./Assets/bg1.jpg")
plataforma1 = Sprite("./Assets/plataforma1_principal.png")
plataforma1.set_position(janela.width / 2 - 140, janela.height - 110)
plataforma2 = Sprite("./Assets/plataforma1_menor.png")
plataforma2.set_position(30, janela.height / 2)

personagem1 = Sprite("./Assets/personagens/Elemental_fire.png", frames=52)
personagem1.set_position(plataforma1.x, janela.height - plataforma1.y - 60)
personagem1.set_curr_frame(0)

personagem2 = Sprite("./Assets/personagens/Elemental_water.png", frames=52)
personagem2.set_position(janela.width / 2 + 100, janela.height - plataforma1.y - 60)
personagem2.set_curr_frame(0)

velocidade = 100
gravidade = 1000
velocidade_pulo = -400

virado1 = None
direcao1 = None
atacando1 = False
tempo_recarga1 = 0
velocidade_y1 = 0
no_chao1 = True
vidas1 = 3
porcentagem1 = 0
golpe_contado1 = False
pulo_duplo_disponivel1 = 2
pulou_antes1 = False
danificado1 = False
knockback_timer1 = 0

virado2 = None
direcao2 = None
atacando2 = False
tempo_recarga2 = 0
velocidade_y2 = 0
no_chao2 = True
vidas2 = 3
porcentagem2 = 0
golpe_contado2 = False
pulo_duplo_disponivel2 = 2
pulou_antes2 = False
danificado2 = False
knockback_timer2 = 0

teclas_personagem1 = {
    "left": "A",
    "right": "D",
    "jump": "W",
    "attack": "N"
}

teclas_personagem2 = {
    "left": "LEFT",
    "right": "RIGHT",
    "jump": "UP",
    "attack": "Z"
}

while True:
    delta_time = janela.delta_time()
    janela.update()
    fundo.draw()
    plataforma1.draw()
    plataforma2.draw()

    virado1, direcao1, atacando1, tempo_recarga1, velocidade_y1, no_chao1, vidas1, porcentagem1, golpe_contado1, pulo_duplo_disponivel1, pulou_antes1, danificado1, knockback_timer1, porcentagem2 = controlar_personagem(
        personagem1, teclado, teclas_personagem1, virado1, direcao1, atacando1, tempo_recarga1, velocidade_y1, no_chao1, delta_time, personagem2, vidas1, porcentagem1, golpe_contado1, pulo_duplo_disponivel1, pulou_antes1, danificado1, knockback_timer1, porcentagem2)

    virado2, direcao2, atacando2, tempo_recarga2, velocidade_y2, no_chao2, vidas2, porcentagem2, golpe_contado2, pulo_duplo_disponivel2, pulou_antes2, danificado2, knockback_timer2, porcentagem1 = controlar_personagem(
        personagem2, teclado, teclas_personagem2, virado2, direcao2, atacando2, tempo_recarga2, velocidade_y2, no_chao2, delta_time, personagem1, vidas2, porcentagem2, golpe_contado2, pulo_duplo_disponivel2, pulou_antes2, danificado2, knockback_timer2, porcentagem1)

    draw_text(f"Vidas: {vidas1}", 10, 10, 20, "white", janela)
    draw_text(f"    {porcentagem1}%", 10, 30, 30, get_percentage_color(porcentagem1), janela)

    draw_text(f"Vidas: {vidas2}", janela.width - 100, 10, 20, "white", janela)
    draw_text(f"    {porcentagem2}%", janela.width - 100, 30, 30, get_percentage_color(porcentagem2), janela)

    personagem1.draw()
    personagem2.draw()

    if teclado.key_pressed("ESC"):
        break

janela.close()
