from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
import time
screen = Window(1920, 1050)
screen.set_title("MENU")
screen.set_background_color((0, 0, 70))
mouse = mouse.Mouse()
key = keyboard.Keyboard()
bg = GameImage('assets/bg1.jpg')
x=0
d=1

def sele_perso(mapa):
    screen = Window(1920, 1050)
    screen.set_title("MENU")
    screen.set_background_color((0, 0, 70))
    bg = GameImage(mapa)
    x=0
    d=1
    y=0
    p=0
    while True:
        bg.draw()
        bg.set_position(x, 0)
        if x > 1:
            d = 1
        elif x < (-780):
            d = 0
        if d == 1:
            x -= 0.2
        elif d == 0:
            x += 0.2

        pe1 = Sprite("assets/fire_knight.png", frames=1)
        pe1.set_position(511, 250)
        if mouse.is_over_object(pe1):
            sqr1 = Sprite("assets/selec.png", frames=1)
            y = "assets/fire_knight.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2

        else:
            sqr1 = Sprite("assets/quad.png", frames=1)
        sqr1.set_position(500, 250)

        pe2 = Sprite("assets/ground_monk.png", frames=1)
        pe2.set_position(831, 250)
        if mouse.is_over_object(pe2):
            sqr2 = Sprite("assets/selec.png", frames=1)
            y = "assets/ground_monk.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2
        else:
            sqr2 = Sprite("assets/quad.png", frames=1)
        sqr2.set_position(820, 250)

        pe3 = Sprite("assets/leaf_ranger.png", frames=1)
        pe3.set_position(1151, 250)
        if mouse.is_over_object(pe3):
            sqr3 = Sprite("assets/selec.png", frames=1)
            y = "assets/leaf_ranger.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2
        else:
            sqr3 = Sprite("assets/quad.png", frames=1)
        sqr3.set_position(1140, 250)

        pe4 = Sprite("assets/metal_bladekeeper.png", frames=1)
        pe4.set_position(511, 558)
        if mouse.is_over_object(pe4):
            sqr4 = Sprite("assets/selec.png", frames=1)
            y = "assets/metal_bladekeeper.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2
        else:
            sqr4 = Sprite("assets/quad.png", frames=1)
        sqr4.set_position(500, 558)

        pe5 = Sprite("assets/water_priestess.png", frames=1)
        pe5.set_position(831, 558)
        if mouse.is_over_object(pe5):
            sqr5 = Sprite("assets/selec.png", frames=1)
            y = "assets/water_priestess.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2
        else:
            sqr5 = Sprite("assets/quad.png", frames=1)
        sqr5.set_position(820, 558)

        pe6 = Sprite("assets/wind_hashashin.png", frames=1)
        pe6.set_position(1151, 558)
        if mouse.is_over_object(pe6):
            sqr6 = Sprite("assets/selec.png", frames=1)
            y = "assets/wind_hashashin.png"
            if p==0 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                p=1
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                time.sleep(0.2)
                j2=y
                p=2
        else:
            sqr6 = Sprite("assets/quad.png", frames=1)
        sqr6.set_position(1140, 558)

        sqr7 = Sprite("assets/selec.png", frames=1)
        sqr8 = Sprite("assets/selec.png", frames=1)
        sqr7.set_position(150, 210)
        sqr8.set_position(1490, 210)

        sqr1.draw()
        sqr2.draw()
        sqr3.draw()
        sqr4.draw()
        sqr5.draw()
        sqr6.draw()
        sqr7.draw()
        sqr8.draw()

        pe1.draw()
        pe2.draw()
        pe3.draw()
        pe4.draw()
        pe5.draw()
        pe6.draw()

        if p==0 and y!=0:
            p1 = Sprite(y, frames=1)
            p1.set_position(161,210)
            p1.draw()

        elif p==1:
            p1 = Sprite(j, frames=1)
            p1.set_position(161, 210)
            p1.draw()
            p2 = Sprite(y, frames=1)
            p2.set_position(1501, 210)
            p2.draw()

        elif p==2:
            p1 = Sprite(j, frames=1)
            p1.set_position(161, 210)
            p1.draw()
            p2 = Sprite(j2, frames=1)
            p2.set_position(1501, 210)
            p2.draw()
            jogar = Sprite("assets/bloco.png", frames=1)
            jogar.set_position(screen.width / 2 - 210, 880)
            jogar.draw()
            screen.draw_text("Começar!", screen.width / 2 - 90, 950, 40, (0, 0, 0), "Courier New", True, False)
            if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
                time.sleep(1)
                jogo(mapa,j,j2)
# o jogo aqui é para chamar a função do jogo, já com o mapa escolhido, o personagem do jogador 1 e do jogador 2.

        screen.draw_text("Selecione Seu Personagem", screen.width / 2 - 250, 90, 40, (0, 0, 0), "Courier New", True, False)
        screen.draw_text("Jogador 1", 191, 480, 40, (0, 0, 0), "Courier New", True, False)
        screen.draw_text("Jogador 2", 1531, 480, 40, (0, 0, 0), "Courier New", True, False)

        screen.update()



def sele_mapa():
    screen = Window(1920, 1050)
    screen.set_title("MENU")
    screen.set_background_color((0, 0, 70))
    x=0
    d=1
    while True:
        bg.draw()
        bg.set_position(x, 0)
        if x > 1:
            d = 1
        elif x < (-780):
            d = 0
        if d == 1:
            x -= 0.2
        elif d == 0:
            x += 0.2

        map1 = Sprite("assets/map1.jpg", frames=1)
        map1.set_position(screen.width / 2 - 350, 150)

        map2 = Sprite("assets/map2.jpg", frames=1)
        map2.set_position(screen.width / 2 - 350, 450)

        map3 = Sprite("assets/map3.jpg", 1)
        map3.set_position(screen.width / 2 - 350, 750)

        if mouse.is_over_object(map1):
            re1 = Sprite("assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                time.sleep(0.2)
                sele_perso('assets/bg1.jpg')
        else:
            re1 = Sprite("assets/retângulo.png", frames=1)

        if mouse.is_over_object(map2):
            re2 = Sprite("assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                time.sleep(0.2)
                sele_perso('assets/bg2.jpg')
        else:
            re2 = Sprite("assets/retângulo.png", frames=1)

        if mouse.is_over_object(map3):
            re3 = Sprite("assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                time.sleep(0.2)
                sele_perso('assets/bg3.jpg')
        else:
            re3 = Sprite("assets/retângulo.png", frames=1)

        re1.set_position(screen.width / 2 - 359, 137)
        re2.set_position(screen.width / 2 - 359, 437)
        re3.set_position(screen.width / 2 - 359, 737)
        re1.draw()
        re2.draw()
        re3.draw()

        map1.draw()
        map2.draw()
        map3.draw()

        screen.update()


while True:
    bg.draw()
    bg.set_position(x,0)
    if x>1:
        d=1
    elif x<(-780):
        d=0
    if d==1:
        x-=0.2
    elif d==0:
        x+=0.2
    tit = Sprite("assets/bloco grande.png", frames=1)
    tit.set_position(screen.width / 2 - 215, 20)
    tit.draw()

    ret = Sprite("assets/bloco.png", frames=1)
    ret.set_position(screen.width/2-210, 320)
    ret.draw()
    screen.draw_text("Jogar", screen.width/2-70, 390, 40, (0, 0, 0), "Courier New", True, False)

    ret2 = Sprite("assets/bloco.png", frames=1)
    ret2.set_position(screen.width/2-210, 490)
    ret2.draw()
    screen.draw_text("Configurações", screen.width/2-150, 560, 40, (0, 0, 0), "Courier New", True, False)

    ret3 = Sprite("assets/bloco.png", frames=1)
    ret3.set_position(screen.width/2-210, 660)
    ret3.draw()
    screen.draw_text("Créditos", screen.width/2-85, 730, 40, (0, 0, 0), "Courier New", True, False)

    ret4 = Sprite("assets/bloco.png", 1)
    ret4.set_position(screen.width/2-210, 830)
    ret4.draw()
    screen.draw_text("Sair", screen.width/2-60, 900, 40, (0, 0, 0), "Courier New", True, False)

    if mouse.is_over_object(ret) and mouse.is_button_pressed(1):
        time.sleep(0.2)
        sele_mapa()

    if mouse.is_over_object(ret2) and mouse.is_button_pressed(1):
        time.sleep(0.2)

    if mouse.is_over_object(ret3) and mouse.is_button_pressed(1):
        time.sleep(0.2)

    if mouse.is_over_object(ret4) and mouse.is_button_pressed(1):
        time.sleep(0.2)
        break

    screen.update()