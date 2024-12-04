
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((864, 936))
pygame.display.set_caption("Flappy Bird HW (with a soccer ball)")

WIDTH = 864
HEIGHT = 936

fps = 60
clock = pygame.time.Clock()

fly = False
gameOver = False
groundScroll = 0
scrollSpeed = 3
cactusGap = 225
cactusFrequency = 2000
lastCactus = pygame.time.get_ticks() - cactusFrequency
score = 0
font = pygame.font.SysFont("arial", 40)
WHITE = (255,255,255)
passCactus = False

run = True

ground = pygame.image.load("ground.png")
bg = pygame.image.load("bg.png")
restartImg = pygame.image.load("restart.png")

class Dino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f"trex{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.clicked = False
    def update(self):
        if fly == True:
            self.velocity += 0.5
            if self.velocity >= 8:
                self.velocity = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)
        if gameOver == False:
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False
            self.counter += 1
            runCooldown = 5
            if self.counter > runCooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            
class Cactus(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cactus.png")
        self.rect = self.image.get_rect()
        if pos == -1:
            self.rect.topleft = [x,y + int(cactusGap//2)]
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(cactusGap//2)]
    def update(self):
        self.rect.x -= scrollSpeed
        if self.rect.right < 0:
            self.kill()

cactusGroup = pygame.sprite.Group()
dinoGroup = pygame.sprite.Group()

dino = Dino(100, HEIGHT//2)
dinoGroup.add(dino)

while run:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    screen.blit(ground, (groundScroll, 768))
    dinoGroup.draw(screen)
    dinoGroup.update()
    cactusGroup.draw(screen)

    if len(cactusGroup) > 0:
        if dinoGroup.sprites()[0].rect.left > cactusGroup.sprites()[0].rect.left and dinoGroup.sprites()[0].rect.right < cactusGroup.sprites()[0].rect.right and passCactus == False:
            passCactus = True
        if passCactus == True:
            if dinoGroup.sprites()[0].rect.left > cactusGroup.sprites()[0].rect.right:
                score += 1
                passCactus = False
    text = font.render(str(score), True, WHITE)
    screen.blit(text, (WIDTH//2, 40))

    if dino.rect.bottom > 768:
        gameOver = True
        fly = False

    if pygame.sprite.groupcollide(dinoGroup, cactusGroup, False, False) or dino.rect.top < 0:
        gameOver = True

    if gameOver == False and fly == True:
        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35:
            groundScroll = 0
        timeNow = pygame.time.get_ticks()
        if timeNow - lastCactus > cactusFrequency:
            cactusHeight = random.randint(-100,100)
            bottomCactus = Cactus(WIDTH, int(HEIGHT//2) + cactusHeight, -1)
            topCactus = Cactus(WIDTH, int(HEIGHT//2) + cactusHeight, 1)
            cactusGroup.add(bottomCactus)
            cactusGroup.add(topCactus)
            lastCactus = timeNow
        cactusGroup.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and gameOver == False:
            fly = True
    pygame.display.update()