import pygame

pygame.init()

win = pygame.display.set_mode((700, 480))
pygame.display.set_caption("1v1 Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
clock = pygame.time.Clock()
blastSound = pygame.mixer.Sound('blastsounds.wav')
hitSound = pygame.mixer.Sound('hitsounds.wav')
score = 0

class player():
    def __init__(self,x,y,width,height):
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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 350
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('timesnewroman', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (350 - (text.get_width()/2), 220))
        pygame.display.update()
        i = 0
        while i < 301:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 300
                    pygame.quit()

class blasts():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 7
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //4], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
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
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('You have hit the enemy')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 250))
    win.blit(text, (10, 10))
    person.draw(win)
    villain.draw(win)
    for blast in ki_blasts:
        blast.draw(win)

    pygame.display.update()


#mainloop
font = pygame.font.SysFont('timesnewroman', 30)
person = player(200, 410, 64, 64)
villain = enemy(100, 410, 64, 64, 650)
ki_blasts = []
shooting = 0
run = True
while run:
    clock.tick(27)

    if villain.visible == True:
        if person.hitbox[1] < villain.hitbox[1] + villain.hitbox[3] and person.hitbox[1] + person.hitbox[3] > villain.hitbox[1]:
            if person.hitbox[0] + person.hitbox[2] > villain.hitbox[0] and person.hitbox[0] < villain.hitbox[0] + villain.hitbox[2]:
                person.hit()
                score -= 5
    #else:
        #if villain.visible == False:
            #print('You have defeated the villain and have won the game')
    if shooting > 0:
        shooting += 1
    if shooting > 3:
        shooting = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for blast in ki_blasts:
        if blast.y - blast.radius < villain.hitbox[1] + villain.hitbox[3] and blast.y + blast.radius > villain.hitbox[1]:
            if blast.x + blast.radius > villain.hitbox[0] and blast.x - blast.radius < villain.hitbox[0] + villain.hitbox[2]:
                hitSound.play()
                villain.hit()
                ki_blasts.pop(ki_blasts.index(blast))
                score += 1

        if blast.x < 700 and blast.x > 0:
            blast.x += blast.vel
        else:
            ki_blasts.pop(ki_blasts.index(blast))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shooting == 0:
        blastSound.play()
        if person.left:
            facing = -1
        else:
            facing = 1
        if len(ki_blasts) < 5:
            ki_blasts.append(blasts(round(person.x + person.width //2), round(person.y + person.height//2), 6, (255, 160, 122, 255), facing))
            shooting = 1

    if keys[pygame.K_a] and person.x > person.vel:
        person.x -= person.vel
        person.left = True
        person.right = False
        person.standing = False
    elif keys[pygame.K_d] and person.x < 700 - person.width - person.vel:
        person.x += person.vel
        person.right = True
        person.left = False
        person.standing = False
    else:
        person.standing = True
        person.walkCount = 0

    if not (person.isJump):
        if keys[pygame.K_w]:
            person.isJump = True
            person.right = False
            person.left = False
            person.walkCount = 0
    else:
        if person.jumpCount >= -10:
            neg = 1
            if person.jumpCount < 0:
                neg = -1
            person.y -= (person.jumpCount ** 2) * 0.5 * neg
            person.jumpCount -= 1
        else:
            person.isJump = False
            person.jumpCount = 10

    redrawGameWindow()

pygame.quit()
