from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *

def create_sword_hitbox(personagem, virado):
    # Definir uma hitbox específica para a espada baseada na posição e direção do personagem
    sword_hitbox = None
    if virado == "RIGHT":
        sword_hitbox = [personagem.x + 40, personagem.y + 10, 20, 10]  # Ajuste essas dimensões conforme necessário
    elif virado == "LEFT":
        sword_hitbox = [personagem.x - 20, personagem.y + 10, 20, 10]  # Ajuste essas dimensões conforme necessário
    return sword_hitbox

def is_attack_frame(personagem, attack_frames):
    curr_frame = personagem.get_curr_frame()
    return curr_frame in attack_frames

def hitbox_collided(hitbox1, hitbox2):
    # Verifica a colisão entre duas hitboxes (x, y, largura, altura)
    x1, y1, w1, h1 = hitbox1
    x2, y2, w2, h2 = hitbox2
    return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2)

def controlar_personagem(personagem, teclado, keys, virado, direcao, atacando, velocidade_y, no_chao, delta_time, opponent):
    andou = False
    estado_anterior_no_chao = no_chao

    # Verificação de colisão com a plataforma
    if (personagem.collided_perfect(plataforma1) == False) and (personagem.collided_perfect(plataforma2) == False):
        no_chao = False
    else:
        no_chao = True

    # Verificação adicional de coordenadas
    if personagem.y >= 165 and personagem.x <= 103:
        no_chao = False

    # Controle do movimento horizontal e ataque
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
    elif teclado.key_pressed(keys["attack"]) and not atacando:
        atacando = True
        if virado == "RIGHT":
            personagem.set_sequence(25, 29, False)
        elif virado == "LEFT":
            personagem.set_sequence(30, 34, False)
        personagem.set_total_duration(1500)
        personagem.play()
    else:
        if not atacando:
            if virado == "RIGHT":
                personagem.set_curr_frame(0)
            elif virado == "LEFT":
                personagem.set_curr_frame(8)
            direcao = None

    if teclado.key_pressed(keys["jump"]) and no_chao:
        velocidade_y = velocidade_pulo
        no_chao = False

    # Aplicação da gravidade e ajuste das sequências de frames
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

    # Verifica se a animação de ataque terminou
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
        if andou:
            personagem.update()

    # Ajusta a animação quando o personagem aterrissa
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

    # Verificação de colisão durante os frames de ataque
    if atacando:
        attack_frames_right = [26, 27]
        attack_frames_left = [32, 33]
        if virado == "RIGHT" and is_attack_frame(personagem, attack_frames_right):
            sword_hitbox = create_sword_hitbox(personagem, virado)
            opponent_hitbox = [opponent.x, opponent.y, opponent.width, opponent.height]
            if hitbox_collided(sword_hitbox, opponent_hitbox):
                print("Acertou o oponente com a espada!")
        elif virado == "LEFT" and is_attack_frame(personagem, attack_frames_left):
            sword_hitbox = create_sword_hitbox(personagem, virado)
            opponent_hitbox = [opponent.x, opponent.y, opponent.width, opponent.height]
            if hitbox_collided(sword_hitbox, opponent_hitbox):
                print("Acertou o oponente com a espada!")

    return virado, direcao, atacando, velocidade_y, no_chao

janela = Window(800, 400)
janela.set_title("Elementals")
teclado = Keyboard()
fundo = GameImage("./Assets/bg1.jpg")
plataforma1 = Sprite("./Assets/plataforma1_principal.png")
plataforma1.set_position(janela.width / 2 - 140, janela.height - 110)
plataforma2 = Sprite ("./Assets/plataforma1_menor.png")
plataforma2.set_position(30, janela.height/2)

# Configuração do primeiro personagem
personagem1 = Sprite("./Assets/personagens/Elemental_fire.png", frames=52)
personagem1.set_position(plataforma1.x, janela.height - plataforma1.y-60)
personagem1.set_curr_frame(0)

# Configuração do segundo personagem
personagem2 = Sprite("./Assets/personagens/Elemental_water.png", frames=52)
personagem2.set_position(janela.width / 2 + 100, janela.height - plataforma1.y - 60)
personagem2.set_curr_frame(0)

velocidade = 100
gravidade = 1000
velocidade_pulo = -400

# Variáveis para o primeiro personagem
virado1 = None
direcao1 = None
atacando1 = False
velocidade_y1 = 0
no_chao1 = True
vida1=3
porcentagem2=0
# Variáveis para o segundo personagem
virado2 = None
direcao2 = None
atacando2 = False
velocidade_y2 = 0
no_chao2 = True
vida2=3
porcentagem2=0
# Teclas de controle para cada personagem
keys_personagem1 = {"right": "RIGHT", "left": "LEFT", "attack": "Z", "jump": "UP"}
keys_personagem2 = {"right": "D", "left": "A", "attack": "N", "jump": "W"}

while True:
    delta_time = janela.delta_time()

    # Controle do primeiro personagem
    virado1, direcao1, atacando1, velocidade_y1, no_chao1 = controlar_personagem(
        personagem1, teclado, keys_personagem1, virado1, direcao1, atacando1, velocidade_y1, no_chao1, delta_time, personagem2
    )

    # Controle do segundo personagem
    virado2, direcao2, atacando2, velocidade_y2, no_chao2 = controlar_personagem(
        personagem2, teclado, keys_personagem2, virado2, direcao2, atacando2, velocidade_y2, no_chao2, delta_time, personagem1
    )

    fundo.draw()
    plataforma1.draw()
    plataforma2.draw()
    personagem1.draw()
    personagem2.draw()

    janela.update()
