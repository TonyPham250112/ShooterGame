from pygame import *
from random import randint
from time import time as timer



font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win_text = font1.render('YOU WIN', True, (55,226,21))
lose_text = font1.render('YOU LOSE', True, (255,0,0))
life_text = font2.render("Life: ", True, (76, 153, 0))
life_color = (0, 255, 0)
score = 0
lost = 0

#background music
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#image
img_back = "galaxy.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

#Supper class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)



asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)




life = 3
goal = 20
finish = False
run = True
reload_time = False
reload_second = 2
number_fire = 5
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if number_fire > 0 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    number_fire -= 1


            if number_fire <= 0 and reload_time == False:
                last_time = timer()
                reload_time = True


    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))


        if life == 2:
            life_color = (255,255,0)
        if life == 1:
            life_color = (255,0,0)

        life_text = font2.render(str(life), True, life_color)
        window.blit(life_text, (650, 10))



        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for is_collide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        collides_2 = sprite.groupcollide(asteroids, bullets, True, True)
        for is_collides in collides_2:
            score = score + 1
            asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1

        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))


        if life == 0:
            finish = True
            window.blit(lose_text, (200, 200))


        if lost >= 3:
            finish = True
            window.blit(lose_text, (200, 200))


        if reload_time == True:
            now_time = timer()

            if now_time - last_time < reload_second:
                reload = font2.render("Reloading....", 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                number_fire = 5
                reload_time = False

        display.update()
    else:
        finish = False
        lost = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()




        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 4):
            asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)



    time.delay(50)