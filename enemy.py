import math

import pygame

imageList = [pygame.image.load("Assets/img/j3.png"), pygame.image.load("Assets/img/j4.png")]
nameList = ["ENEMY 1", "ENEMY 2"]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, enemyNum):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.enemyNum = enemyNum
        self.name = nameList[self.enemyNum - 1]
        self.enemyImage = pygame.transform.scale(imageList[self.enemyNum - 1], (100, 100))
        self.rotatedImage = pygame.transform.scale(imageList[self.enemyNum - 1], (100, 100))
        self.rotatedImage = pygame.transform.rotate(self.rotatedImage, 180)
        self.rect = self.enemyImage.get_rect()
        self.direction = 2
        if enemyNum == 1:
            self.rect.centerx = self.width * 0.25
        elif enemyNum == 2:
            self.rect.centerx = self.width * 0.75
        self.rect.centery = 150
        self.bulletList = []
        self.bullet_sound = pygame.mixer.Sound("Assets/audio/shoot.wav")
        self.shotCD = 100
        self.lateralSpeed = 10
        self.verticalSpeed = 5
        self.hp = 3
        self.alive = True

    def draw(self, surface):
        if self.alive:
            surface.blit(self.rotatedImage, self.rect)
            self.__drawBullets(surface)

    def shoot(self, playerPos):
        if self.alive:
            self.shotCD -= 1
            if len(playerPos) == 1:
                if (abs(self.rect.centerx - playerPos[0][0]) < 100 or abs(self.rect.centery - playerPos[0][1]) < 100) and self.shotCD <= 0:
                    if self.direction == 0:
                        self.bulletList.append([[self.rect.centerx + 20, self.rect.top], 0])
                    if self.direction == 1:
                        self.bulletList.append([[self.rect.right, self.rect.centery + 20], 1])
                    if self.direction == 2:
                        self.bulletList.append([[self.rect.centerx - 20, self.rect.bottom], 2])
                    if self.direction == 3:
                        self.bulletList.append([[self.rect.left, self.rect.centery - 20], 3])
                    pygame.mixer.Sound.play(self.bullet_sound)
                    self.shotCD = 100
            else:
                if ((abs(self.rect.centerx - playerPos[0][0]) < 100 or abs(self.rect.centerx - playerPos[1][0]) < 100) or (abs(self.rect.centery - playerPos[0][1]) < 100 or abs(self.rect.centery - playerPos[1][1]) < 100)) and self.shotCD <= 0:
                    if self.direction == 0:
                        self.bulletList.append([[self.rect.centerx + 20, self.rect.top], 0])
                    if self.direction == 1:
                        self.bulletList.append([[self.rect.right, self.rect.centery + 20], 1])
                    if self.direction == 2:
                        self.bulletList.append([[self.rect.centerx - 20, self.rect.bottom], 2])
                    if self.direction == 3:
                        self.bulletList.append([[self.rect.left, self.rect.centery - 20], 3])
                    pygame.mixer.Sound.play(self.bullet_sound)
                    self.shotCD = 100

    def moveBullets(self):
        if self.alive:
            if len(self.bulletList) > 0:
                for x in self.bulletList:
                    if x[1] == 0:
                        x[0][1] -= 20
                    if x[1] == 1:
                        x[0][0] += 20
                    if x[1] == 2:
                        x[0][1] += 20
                    if x[1] == 3:
                        x[0][0] -= 20

    def __drawBullets(self, screen):
        if self.alive:
            if len(self.bulletList) > 0:
                for x in self.bulletList:
                    pygame.draw.circle(screen, (0, 0, 0), x[0], 10)

    def moveRight(self):
        if self.alive:
            self.rect.right += self.lateralSpeed
            self.rotatedImage = pygame.transform.rotate(self.enemyImage, 270)
            self.__move()
            self.direction = 1

    def moveLeft(self):
        if self.alive:
            self.rect.left -= self.lateralSpeed
            self.rotatedImage = pygame.transform.rotate(self.enemyImage, 90)
            self.__move()
            self.direction = 3

    def moveUp(self):
        if self.alive:
            self.rect.top -= self.verticalSpeed
            self.rotatedImage = pygame.transform.rotate(self.enemyImage, 0)
            self.__move()
            self.direction = 0

    def moveDown(self):
        if self.alive:
            self.rect.bottom += self.verticalSpeed
            self.rotatedImage = pygame.transform.rotate(self.enemyImage, 180)
            self.__move()
            self.direction = 2

    def __move(self):
        if self.alive:
            if self.rect.left <= 100:
                self.rect.left = 100
            elif self.rect.right >= self.width - 100:
                self.rect.right = self.width - 100
            if self.rect.top <= 100:
                self.rect.top = 100
            elif self.rect.bottom >= self.height - 100:
                self.rect.bottom = self.height - 100

    def collided(self, bullets):
        if self.alive:
            if len(bullets) == 1:
                for x in bullets[0]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[0].remove(x)
                    if self.hp <= 0:
                        self.__destruct()
            elif len(bullets) == 2:
                for x in bullets[0]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[0].remove(x)
                    if self.hp <= 0:
                        self.__destruct()
                for x in bullets[1]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[1].remove(x)
                    if self.hp <= 0:
                        self.__destruct()
            elif len(bullets) == 3:
                for x in bullets[0]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[0].remove(x)
                    if self.hp <= 0:
                        self.__destruct()
                for x in bullets[1]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[1].remove(x)
                    if self.hp <= 0:
                        self.__destruct()
                for x in bullets[2]:
                    distance = self.__listsub(self.rect.center, x[0])
                    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                    if distance <= 50:
                        self.hp -= 1
                        bullets[2].remove(x)
                    if self.hp <= 0:
                        self.__destruct()

    def __destruct(self):
        self.alive = False

    def __listsub(self, list1, list2):
        list3 = []
        for x in range(len(list1)):
            list3.append(list1[x] - list2[x])
        return list3
