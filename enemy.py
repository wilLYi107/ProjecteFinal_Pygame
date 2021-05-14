import pygame
import bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, posX, posY, dist, img1, img2):
        pygame.sprite.Sprite.__init__(self)
        self.imageList = [pygame.image.load(img1), pygame.image.load(img2)]
        self.position = 0
        self.enemyImage = self.imageList[self.position]

        self.rect = self.enemyImage.get_rect()
        self.rect.centerx = posX
        self.rect.centery = posY

        self.bulletList = []
        self.lateralSpeed = 1
        self.animationTime = 1
        self.shotRange = 1
        self.win = False

        self.right = True
        self.count = 0
        self.maxDown = self.rect.top + 10

        self.limitR = posX + dist
        self.limitL = posX - dist

    def change(self, time):
        if not self.win:
            self.__movement()
            self.__attack()
            if self.animationTime == time:
                self.position += 1
                self.animationTime += 1

                if self.position > len(self.imageList) - 1:
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
        self.enemyImage = self.imageList[self.position]
        surface.blit(self.enemyImage, self.rect)

    def __attack(self):
        pass
        # if randint(0, 1000) < self.shotRange:
        #     self.__shoot()

    def __shoot(self):
        x, y = self.rect.center
        newBullet = bullet.Bullet(x, y, "Assets/img/disparob.jpg", False)
        self.bulletList.append(newBullet)