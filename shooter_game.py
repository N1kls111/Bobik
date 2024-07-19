#код кака, кака и еще раз кака
from random import randint
from pygame import *

WIN_W = 700
WIN_H = 500

lost = 0
killed = 0

window = display.set_mode((WIN_W, WIN_H))
display.set_caption("Bobik228")

background = transform.scale(image.load("bobik.jpg"), (WIN_W, WIN_H))

clock = time.Clock()
FPS = 60

x1 = 315
y1 = 435

speed1 = 1
speed2 = 2

class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_img, player_x, player_y, player_speed):
        super().__init__(player_img, player_x, player_y, player_speed)

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= speed2
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += speed2

class Enemy(GameSprite):
    def __init__(self, player_img, player_x, player_y, player_speed):
        super().__init__(player_img, player_x, player_y, player_speed)

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= WIN_H:
            self.rect.x = randint(80, WIN_W - 80)
            self.rect.y = 0
            lost += 1

class Meteor(GameSprite):
    def __init__(self, player_img, player_x, player_y, player_speed):
        super().__init__(player_img, player_x, player_y, player_speed)

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= WIN_H:
            self.rect.x = randint(80, WIN_W - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()

font.init()
my_font = font.Font(None, 70)
my_text = 'Бобик фасссс'
my_color = (123, 104, 238)
question = my_font.render(my_text, True, my_color)

win_txt = my_font.render('YOU WIN!', True, (0, 0, 0))
lose_txt = my_font.render('YOU LOSE!', True, (0, 0, 0))

bobik1 = Player('rocket.png', x1, y1, speed2)

popokaka = sprite.Group()
bobik3 = sprite.Group()
meteors = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, WIN_W - 50), 0, speed1)
    popokaka.add(enemy)

for i in range(3):
    meteor = Meteor('asteroid.png', randint(0, WIN_W - 50), 0, speed2)
    meteors.add(meteor)

mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play(-1, 0.0)

ammo = 30
reload_time = 1000
last_shot_time = 0

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and ammo > 0 and not finish:
                current_time = time.get_ticks()
                if current_time - last_shot_time > reload_time:
                    bullet = Bullet('bullet.png', bobik1.rect.x + 15, bobik1.rect.y, 7)
                    bobik3.add(bullet)
                    ammo -= 1
                    last_shot_time = current_time

    if not finish:
        collides = sprite.groupcollide(bobik3, popokaka, True, True)
        for c in collides:
            killed += 1
            enemy = Enemy('ufo.png', randint(0, WIN_W - 50), 0, speed1)
            popokaka.add(enemy)

        if sprite.spritecollide(bobik1, popokaka, False) or sprite.spritecollide(bobik1, meteors, False) or lost >= 5:
            window.blit(lose_txt, (WIN_W // 2 - 100, WIN_H // 2))
            display.update()
            time.delay(1000)
            finish = True
        if killed >= 1:
            window.blit(win_txt, (WIN_W // 2 - 100, WIN_H // 2))
            display.update()
            time.delay(1000)
            finish = True

        window.blit(background, (0, 0))
        
        bobik1.reset()
        bobik1.update()

        bobik3.draw(window)
        bobik3.update()

        popokaka.draw(window)
        popokaka.update()

        meteors.draw(window)
        meteors.update()

        window.blit(question, (150, 0))
        display.update()
        clock.tick(FPS)
display.update()