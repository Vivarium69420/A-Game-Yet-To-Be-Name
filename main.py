import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')

bulletSound = pygame.mixer.Sound('Game/Game_bullet.mp3')
hitSound = pygame.mixer.Sound('Game/Game_hit.mp3')
music = pygame.mixer.music.load('Game/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
score = 0


class Enemy:
    walkRight = [pygame.image.load('Game/R1E.png'), pygame.image.load('Game/R2E.png'), pygame.image.load('Game/R3E.png'), pygame.image.load('Game/R4E.png'), pygame.image.load('Game/R5E.png'), pygame.image.load('Game/R6E.png'), pygame.image.load('Game/R7E.png'), pygame.image.load('Game/R8E.png'), pygame.image.load('Game/R9E.png'), pygame.image.load('Game/R10E.png'), pygame.image.load('Game/R11E.png')]
    walkLeft = [pygame.image.load('Game/L1E.png'), pygame.image.load('Game/L2E.png'), pygame.image.load('Game/L3E.png'), pygame.image.load('Game/L4E.png'), pygame.image.load('Game/L5E.png'), pygame.image.load('Game/L6E.png'), pygame.image.load('Game/L7E.png'), pygame.image.load('Game/L8E.png'), pygame.image.load('Game/L9E.png'), pygame.image.load('Game/L10E.png'), pygame.image.load('Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:  # 3 fps, we have 11 pictures -> 33
                self.walkCount = 0

            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:  # going right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', True, (255, 0, 0))
        text_width = text.get_width()/2
        win.blit(text, (250 - text_width, 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Projectile:
    def __init__(self, x, y, radius, color, facingg):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facingg
        self.vel = 8 * facingg

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), True, (0, 0, 0))
    win.blit(text, (300, 10))
    man.draw(win)
    goblin.draw(win)
    for bullett in bullets:
        bullett.draw(win)

    pygame.display.update()


# main loop
font = pygame.font.SysFont('comicsans', 30, True, True)

run = True
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
shot = 0
bullets = []
while run:
    clock.tick(27)  # frame-rate
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
    if shot > 0:
        shot += 1
    if shot > 3:
        shot = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shot == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))
        shot = 1
    # if the box is at x = 0, if x > 0, we can still move -vel to the left
    if keys[pygame.K_RIGHT] and man.x < 500 - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_LEFT] and man.x >= man.vel:
        man.x -= man.vel
        man.standing = False
        man.left = True
        man.right = False
    else:  # reset everything if character stand-still
        man.standing = True
        man.walkCount = 0
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1  # The initial jump going up
            if man.jumpCount < 0:  # after 10 jump step, we will move downward by neg = -1
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redraw_game_window()
pygame.quit()
