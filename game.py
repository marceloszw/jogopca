import re
import sys, pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

screen_width = 1000
screen_height = 800

RED = (255, 100, 0)

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super(Jogador, self).__init__()
        self.surf = pygame.image.load("imagens/arvore.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.vidas_restantes = 7

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -9)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 9)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-9, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(9, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super(Inimigo, self).__init__()
        #self.surf = pygame.Surface((20, 35))
        #self.surf.fill((0, 0, 0))
        self.surf = pygame.image.load("imagens/inimigo.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )
        self.speed = random.randint(5, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

pygame.init()

pygame.mixer.music.load("music/pirates.mid")
pygame.mixer.music.play()

bg = pygame.image.load("imagens/field.jpg")

screen = pygame.display.set_mode((screen_width, screen_height))

sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 48)

img = font.render('Vidas: 7', True, RED)
rect = img.get_rect()
rect.topleft = (800, 20)

img_game_over = font.render('GAME OVER', True, RED)
rect_img_game_over = img_game_over.get_rect()
rect_img_game_over.topleft = (400, 300)

adicionar_inimigo = pygame.USEREVENT + 1
pygame.time.set_timer(adicionar_inimigo, 400)

jogador = Jogador()

inimigos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)

game_over = False

rodando = True
while rodando:
    while game_over == False:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    rodando = False

            elif event.type == pygame.QUIT:
                rodando = False

            elif event.type == adicionar_inimigo:
                novo_inimigo = Inimigo()
                inimigos.add(novo_inimigo)
                all_sprites.add(novo_inimigo)
        
        pressed_keys = pygame.key.get_pressed()

        jogador.update(pressed_keys)

        inimigos.update()

        #screen.fill((255, 255, 255))
        screen.blit(bg, (0,0))
        screen.blit(img, rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollide(jogador, inimigos, True):
            if jogador.vidas_restantes > 1:
                jogador.vidas_restantes -= 1
                img = font.render('Vidas: '+str(jogador.vidas_restantes), True, RED)
                print(jogador.vidas_restantes)
                screen.blit(img, rect)
            
            else:
                game_over = True

            

        pygame.display.flip()

        clock = pygame.time.Clock()
        clock.tick(20)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                rodando = False

        elif event.type == pygame.QUIT:
            rodando = False

                
        pressed_keys = pygame.key.get_pressed()
    
    screen.fill((0,0,0))
    screen.blit(img_game_over, rect_img_game_over)
    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(20)


pygame.quit()