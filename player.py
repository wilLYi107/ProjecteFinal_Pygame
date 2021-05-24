import pygame
import bullet

imageList = [pygame.image.load("Assets/img/j1.png"), pygame.image.load("Assets/img/j2.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, playerId):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.playerId = playerId
        self.playerImage = pygame.transform.scale(imageList[self.playerId - 1], (100, 100))
        self.rotatedImage = pygame.transform.scale(imageList[self.playerId - 1], (100, 100))
        # self.explosionImage = pygame.image.load("Assets/img/explosion.jpg")
        self.rect = self.playerImage.get_rect()
        if playerId == 1:
            self.rect.centerx = self.width * 0.25
        elif playerId == 2:
            self.rect.centerx = self.width * 0.75
        self.rect.centery = self.height - 100
        self.hp = 100
        self.bulletList = []
        self.lateralSpeed = 10
        self.verticalSpeed = 7

    def inputHandler(self, input):
        for event in input:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.bulletList.append([self.rect.centerx, self.rect.top])
                    # pygame.mixer.Sound.play(self.bullet_sound)
        keys = pygame.key.get_pressed()
        if self.playerId == 1:
            if keys[pygame.K_a]:
                self.moveLeft()
            if keys[pygame.K_d]:
                self.moveRight()
            if keys[pygame.K_w]:
                self.moveUp()
            if keys[pygame.K_s]:
                self.moveDown()
            if keys[pygame.K_SPACE]:
                # self.shoot(0, 0)
                print("Player 1 shoots")
        elif self.playerId == 2:
            if keys[pygame.K_LEFT]:
                self.moveLeft()
            if keys[pygame.K_RIGHT]:
                self.moveRight()
            if keys[pygame.K_UP]:
                self.moveUp()
            if keys[pygame.K_DOWN]:
                self.moveDown()
            if keys[pygame.K_RCTRL]:
                # self.shoot(0, 0)
                print("Player 2 shoots")

    def moveRight(self):
        self.rect.right += self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 270)
        self.__move()

    def moveLeft(self):
        self.rect.left -= self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 90)
        self.__move()

    def moveUp(self):
        self.rect.top -= self.verticalSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 0)
        self.__move()

    def moveDown(self):
        self.rect.bottom += self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 180)
        self.__move()

    def __move(self):
        if self.hp:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right >= self.width:
                self.rect.right = self.width
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= self.height:
                self.rect.bottom = self.height

    def shoot(self, x, y):
        newBullet = bullet.Bullet(x, y, "Assets/disparoa.jpg", True)
        self.bulletList.append(newBullet)

    def draw(self, screen):
        screen.blit(self.rotatedImage, self.rect)

    def destruct(self):
        self.hp = False
        self.lateralSpeed = 0
        # self.playerImage = self.explosionImage