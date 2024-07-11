from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *

def create_sword_hitbox(personagem, virado):
    #to do: melhorar hitbox
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

def controlar_personagem(personagem, teclado, keys, virado, direcao, atacando, velocidade_y, no_chao, delta_time, opponent, janela, vidas, porcentagem):
    andou = False
    estado_anterior_no_chao = no_chao

    if (personagem.collided_perfect(plataforma1) == False) and (personagem.collided_perfect(plataforma2) == False):
        no_chao = False
    else:
        no_chao = True

    if personagem.y >= 165 and personagem.x <= 103:
        no_chao = False

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
        if andou:
            personagem.update()

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

    # Verificar se o personagem saiu da tela
    if personagem.x < -100 or personagem.x > janela.width + 100 or personagem.y < -100 or personagem.y > janela.height + 100:
        personagem.set_position(janela.width / 2 - personagem.width / 2, janela.height / 2 - personagem.height / 2)
        vidas -= 1
        porcentagem = 0

    return virado, direcao, atacando, velocidade_y, no_chao, vidas, porcentagem

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
plataforma2 = Sprite ("./Assets/plataforma1_menor.png")
plataforma2.set_position(30, janela.height/2)

personagem1 = Sprite("./Assets/personagens/Elemental_fire.png", frames=52)
personagem1.set_position(plataforma1.x, janela.height - plataforma1.y-60)
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
velocidade_y1 = 0
no_chao1 = True
vida1 = 3
porcentagem1 = 0

virado2 = None
direcao2 = None
atacando2 = False
velocidade_y2 = 0
no_chao2 = True
vida2 = 3
porcentagem2 = 0

keys_personagem1 = {"right": "RIGHT", "left": "LEFT", "attack": "Z", "jump": "UP"}
keys_personagem2 = {"right": "D", "left": "A", "attack": "N", "jump": "W"}

while True:
    delta_time = janela.delta_time()

    virado1, direcao1, atacando1, velocidade_y1, no_chao1, vida1, porcentagem1 = controlar_personagem(
        personagem1, teclado, keys_personagem1, virado1, direcao1, atacando1, velocidade_y1, no_chao1, delta_time, personagem2, janela, vida1, porcentagem1
    )

    virado2, direcao2, atacando2, velocidade_y2, no_chao2, vida2, porcentagem2 = controlar_personagem(
        personagem2, teclado, keys_personagem2, virado2, direcao2, atacando2, velocidade_y2, no_chao2, delta_time, personagem1, janela, vida2, porcentagem2
    )

    fundo.draw()
    plataforma1.draw()
    plataforma2.draw()
    personagem1.draw()
    personagem2.draw()

    draw_text(f"Vidas: {vida1}", 10, 10, 24, "white", janela)
    draw_text(f"  {porcentagem1}%", 10, 40, 30, get_percentage_color(porcentagem1), janela)
    
    draw_text(f"Vidas: {vida2}", janela.width - 150, 10, 24, "white", janela)
    draw_text(f"  {porcentagem2}%", janela.width - 150, 40, 30, get_percentage_color(porcentagem2), janela)

    janela.update()
