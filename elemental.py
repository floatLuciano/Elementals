from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from PPlay.sound import *
from jogo import *
import time
screen = Window(800, 400)
screen.set_title("MENU")
screen.set_background_color((0, 0, 70))
mouse = mouse.Mouse()
key = keyboard.Keyboard()
bg = GameImage('Assets/bg1.jpg')
x=0
d=1
vol=50
click = Sound("click.ogg")
click.set_volume(50)

def volume():
    global vol
    if vol>=0 and vol<=100:
        if key.key_pressed('O'):
            screen.draw_text(f"Volume {vol}", 1521, 800, 40, (0, 0, 0), "Courier New", True, False)
            vol-=1

        elif key.key_pressed('P'):
            screen.draw_text(f"Volume {vol}", 1521, 800, 40, (0, 0, 0), "Courier New", True, False)
            vol+= 1

    elif vol>100:
        vol=100
        screen.draw_text(f"Volume {vol}", 1521, 800, 40, (0, 0, 0), "Courier New", True, False)

    elif vol<0:
        vol=0
        screen.draw_text(f"Volume {vol}", 1521, 800, 40, (0, 0, 0), "Courier New", True, False)

def clicar():
    click.set_volume(vol)
    click.stop()
    click.play()
    time.sleep(0.2)
def sele_perso(mapa):
    screen = Window(800, 400)
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
        elif x < (-200):
            d = 0
        if d == 1:
            x -= 0.2
        elif d == 0:
            x += 0.2

        pe1 = Sprite("Assets/fire_knight.png", frames=1)
        pe1.set_position(110, 210)
        if mouse.is_over_object(pe1):
            sqr1 = Sprite("Assets/selec.png", frames=1)
            y = "Assets/fire_knight.png"
            if p==0 and mouse.is_button_pressed(1):
                clicar()
                p=1
                t= "./Assets/personagens/Elemental_fire.png"
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                clicar()
                j2=y
                t2= "./Assets/personagens/Elemental_fire.png"
                p=2

        else:
            sqr1 = Sprite("Assets/quad.png", frames=1)
        sqr1.set_position(105, 210)

        pe2 = Sprite("Assets/wind_hashashin.png", frames=1)
        pe2.set_position(255, 210)
        if mouse.is_over_object(pe2):
            sqr2 = Sprite("Assets/selec.png", frames=1)
            y = "Assets/wind_hashashin.png"
            if p==0 and mouse.is_button_pressed(1):
                clicar()
                p=1
                t="./Assets/personagens/Elemental_wind.png"
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                clicar()
                t2="./Assets/personagens/Elemental_wind.png"
                j2=y
                p=2
        else:
            sqr2 = Sprite("Assets/quad.png", frames=1)
        sqr2.set_position(250, 210)

        pe4 = Sprite("Assets/metal_bladekeeper.png", frames=1)
        pe4.set_position(405, 210)
        if mouse.is_over_object(pe4):
            sqr4 = Sprite("Assets/selec.png", frames=1)
            y = "Assets/metal_bladekeeper.png"
            if p==0 and mouse.is_button_pressed(1):
                clicar()
                p=1
                t="./Assets/personagens/Elemental_metal.png"
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                clicar()
                j2=y
                t2="./Assets/personagens/Elemental_metal.png"
                p=2
        else:
            sqr4 = Sprite("Assets/quad.png", frames=1)
        sqr4.set_position(400, 210)

        pe5 = Sprite("Assets/water_priestess.png", frames=1)
        pe5.set_position(555, 210)
        if mouse.is_over_object(pe5):
            sqr5 = Sprite("Assets/selec.png", frames=1)
            y = "Assets/water_priestess.png"
            if p==0 and mouse.is_button_pressed(1):
                clicar()
                p=1
                t= "./Assets/personagens/Elemental_water.png"
                j=y
            elif p==1 and mouse.is_button_pressed(1):
                clicar()
                j2=y
                t2= "./Assets/personagens/Elemental_water.png"
                p=2
        else:
            sqr5 = Sprite("Assets/quad.png", frames=1)
        sqr5.set_position(550, 210)

        sqr7 = Sprite("Assets/selec.png", frames=1)
        sqr8 = Sprite("Assets/selec.png", frames=1)
        sqr7.set_position(20, 30)
        sqr8.set_position(640, 30)

        sqr1.draw()
        sqr2.draw()
        sqr4.draw()
        sqr5.draw()
        sqr7.draw()
        sqr8.draw()

        pe1.draw()
        pe2.draw()
        pe4.draw()
        pe5.draw()

        if p==0 and y!=0:
            p1 = Sprite(y, frames=1)
            p1.set_position(25,30)
            p1.draw()

        elif p==1:
            p1 = Sprite(j, frames=1)
            p1.set_position(25, 30)
            p1.draw()
            p2 = Sprite(y, frames=1)
            p2.set_position(645, 30)
            p2.draw()

        elif p==2:
            p1 = Sprite(j, frames=1)
            p1.set_position(25, 30)
            p1.draw()
            p2 = Sprite(j2, frames=1)
            p2.set_position(645, 30)
            p2.draw()
            jogar = Sprite("Assets/bloco.png", frames=1)
            jogar.set_position(screen.width / 2 - 102, 300)
            jogar.draw()
            screen.draw_text("Começar!", screen.width / 2 - 55, 330, 24, (0, 0, 0), "Courier New", True, False)
            if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
                clicar()
                jogo=Jogo(t,t2)
                jogo.run()


# o jogo aqui é para chamar a função do jogo, já com o mapa escolhido, o personagem do jogador 1 e do jogador 2.

        cabeca = Sprite("Assets/blocomaior.png", frames=1)
        cabeca.set_position(screen.width /2 -150, 39)
        cabeca.draw()
        screen.draw_text("Escolha seu Lutador", screen.width / 2 - 120, 92, 22, (0, 0, 0), "Courier New", True, False)
        jog1 = Sprite("Assets/blocomenor.png", frames=1)
        jog1.set_position(12, 145)
        jog1.draw()
        screen.draw_text("Jogador 1", 32, 168, 20, (0, 0, 0), "Courier New", True, False)

        jog2 = Sprite("Assets/blocomenor.png", frames=1)
        jog2.set_position(632, 145)
        jog2.draw()
        screen.draw_text("Jogador 2", 652, 168, 20, (0, 0, 0), "Courier New", True, False)

        volume()

        screen.update()
        if key.key_pressed('esc'):
            break

def sele_mapa():
    screen = Window(800, 400)
    screen.set_title("MENU")
    screen.set_background_color((0, 0, 70))
    x=0
    d=1

    while True:
        bg.draw()
        bg.set_position(x, 0)
        if x > 1:
            d = 1
        elif x < (-200):
            d = 0
        if d == 1:
            x -= 0.2
        elif d == 0:
            x += 0.2

        map1 = Sprite("Assets/map1.jpg", frames=1)
        map1.set_position(90, 120)

        map2 = Sprite("Assets/map2.jpg", frames=1)
        map2.set_position(400, 120)

        map3 = Sprite("Assets/map3.jpg", 1)
        map3.set_position(screen.width / 2 - 150, 255)

        if mouse.is_over_object(map1):
            re1 = Sprite("Assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                clicar()
                sele_perso('Assets/bg1.jpg')
        else:
            re1 = Sprite("Assets/retângulo.png", frames=1)

        if mouse.is_over_object(map2):
            re2 = Sprite("Assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                clicar()
                sele_perso('Assets/bg2.jpg')
        else:
            re2 = Sprite("Assets/retângulo.png", frames=1)

        if mouse.is_over_object(map3):
            re3 = Sprite("Assets/reverso.png", frames=1)
            if mouse.is_button_pressed(1):
                clicar()
                sele_perso('Assets/bg3.jpg')
        else:
            re3 = Sprite("Assets/retângulo.png", frames=1)

        re1.set_position(85, 115)
        re2.set_position(395, 115)
        re3.set_position(screen.width / 2 - 155, 250)
        re1.draw()
        re2.draw()
        re3.draw()

        map1.draw()
        map2.draw()
        map3.draw()

        ret = Sprite("Assets/blocomaior.png", frames=1)
        ret.set_position(250, -5)
        ret.draw()
        screen.draw_text("Selecione o Mapa", 280, 45, 25, (0, 0, 0), "Courier New", True, False)

        volume()

        screen.update()
        if key.key_pressed('esc'):
            break

while True:
    bg.draw()
    bg.set_position(x,0)
    if x>1:
        d=1
    elif x<(-200):
        d=0
    if d==1:
        x-=0.2
    elif d==0:
        x+=0.2
    tit = Sprite("Assets/bloco grande.png", frames=1)
    tit.set_position(screen.width / 2 - 112, -15)
    tit.draw()

    logo = Sprite ("Assets/logo.png",frames=1)
    logo.set_position(screen.width / 2 - 85, 28)
    logo.draw()

    ret = Sprite("Assets/bloco.png", frames=1)
    ret.set_position(175, 150)
    ret.draw()
    screen.draw_text("Jogar", 245, 182, 20, (0, 0, 0), "Courier New", True, False)

    ret2 = Sprite("Assets/bloco.png", frames=1)
    ret2.set_position(175, 250)
    ret2.draw()
    screen.draw_text("Controles", 220, 282, 20, (0, 0, 0), "Courier New", True, False)

    ret3 = Sprite("Assets/bloco.png", frames=1)
    ret3.set_position(425, 150)
    ret3.draw()
    screen.draw_text("Créditos", 475, 182, 20, (0, 0, 0), "Courier New", True, False)

    ret4 = Sprite("Assets/bloco.png", 1)
    ret4.set_position(425, 250)
    ret4.draw()
    screen.draw_text("Sair", 500, 282, 20, (0, 0, 0), "Courier New", True, False)

    if mouse.is_over_object(ret) and mouse.is_button_pressed(1):
        clicar()
        sele_mapa()

    if mouse.is_over_object(ret2) and mouse.is_button_pressed(1):
        clicar()

    if mouse.is_over_object(ret3) and mouse.is_button_pressed(1):
        clicar()

    if mouse.is_over_object(ret4) and mouse.is_button_pressed(1):
        clicar()
        break

    volume()
    screen.update()