import pygame
import bullet

imageList = [pygame.image.load("Assets/img/j3.png"), pygame.image.load("Assets/img/j4.png")]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, enemyNum):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.enemyNum = enemyNum
        self.enemyImage = pygame.transform.scale(imageList[self.enemyNum - 1], (100, 100))
        self.rotatedImage = pygame.transform.scale(imageList[self.enemyNum - 1], (100, 100))
        self.rotatedImage = pygame.transform.rotate(self.rotatedImage, 180)
        self.rect = self.enemyImage.get_rect()
        if enemyNum == 1:
            self.rect.centerx = self.width * 0.25
        elif enemyNum == 2:
            self.rect.centerx = self.width * 0.75
        self.rect.centery = 100
        self.bulletList = []
        self.lateralSpeed = 1
        self.animationTime = 1
        self.shotRange = 1
        self.win = False
        self.right = True
        self.count = 0
        self.maxDown = self.rect.top + 10

    def change(self, time):
        if not self.win:
            self.__movement()
            self.__attack()
            if self.animationTime == time:
                self.position += 1
                self.animationTime += 1
                if self.position > len(imageList) - 1:
                    self.position = 0

    def __movement(self):
        if self.count < 3:
            self.__lateralMovement()
        else:
            self.__verticalMovement()

    def __lateralMovement(self):
        if self.right:
            self.rect.left += self.lateralSpeed
            if self.rect.left > self.limitR:
                self.right = False
                self.count += 0.33
        else:
            self.rect.left -= self.lateralSpeed
            if self.rect.left < self.limitL:
                self.right = True
                self.count += 0.66

    def __verticalMovement(self):
        if self.maxDown == self.rect.top:
            self.count = 0
            self.maxDown = self.rect.top + 40
        else:
            self.rect.top += 1

    def draw(self, surface):
        surface.blit(self.rotatedImage, self.rect)

    def __attack(self):
        pass
        # if randint(0, 1000) < self.shotRange:
        #     self.__shoot()

    def __shoot(self):
        x, y = self.rect.center
        newBullet = bullet.Bullet(x, y, "Assets/img/disparob.jpg", False)
        self.bulletList.append(newBullet)