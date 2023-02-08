import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')

clock = pygame.time.Clock()


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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


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
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# main loop
run = True
man = Player(300, 410, 64, 64)
bullets = []
while run:

    clock.tick(27)  # frame-rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))
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
