import math

import pygame

imageList = [pygame.image.load("Assets/img/j1.png"), pygame.image.load("Assets/img/j2.png")]
nameList = ["PLAYER 1", "PLAYER 2"]


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, playerId):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.playerId = playerId
        self.name = nameList[self.playerId - 1]
        self.playerImage = pygame.transform.scale(imageList[self.playerId - 1], (100, 100))
        self.rotatedImage = pygame.transform.scale(imageList[self.playerId - 1], (100, 100))
        # self.explosionImage = pygame.image.load("Assets/img/explosion.jpg")
        self.rect = self.playerImage.get_rect()
        if playerId == 1:
            self.rect.centerx = self.width * 0.25
        elif playerId == 2:
            self.rect.centerx = self.width * 0.75
        self.rect.centery = self.height - 150
        self.hp = 3
        self.bulletList = []
        self.bullet_sound = pygame.mixer.Sound("Assets/audio/shoot.wav")
        self.lateralSpeed = 10
        self.verticalSpeed = 7
        self.shotCD = 20
        self.direction = 0
        self.alive = True

    def inputHandler(self):
        if self.alive:
            self.shotCD -= 1
            keys = pygame.key.get_pressed()
            if self.playerId == 1:
                if keys[pygame.K_a]:
                    self.__moveLeft()
                if keys[pygame.K_d]:
                    self.__moveRight()
                if keys[pygame.K_w]:
                    self.__moveUp()
                if keys[pygame.K_s]:
                    self.__moveDown()
                if keys[pygame.K_SPACE]:
                    self.__shoot()
            elif self.playerId == 2:
                if keys[pygame.K_LEFT]:
                    self.__moveLeft()
                if keys[pygame.K_RIGHT]:
                    self.__moveRight()
                if keys[pygame.K_UP]:
                    self.__moveUp()
                if keys[pygame.K_DOWN]:
                    self.__moveDown()
                if keys[pygame.K_RCTRL]:
                    self.__shoot()

    def __moveRight(self):
        self.rect.right += self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 270)
        self.__move()
        self.direction = 1

    def __moveLeft(self):
        self.rect.left -= self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 90)
        self.__move()
        self.direction = 3

    def __moveUp(self):
        self.rect.top -= self.verticalSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 0)
        self.__move()
        self.direction = 0

    def __moveDown(self):
        self.rect.bottom += self.lateralSpeed
        self.rotatedImage = pygame.transform.rotate(self.playerImage, 180)
        self.__move()
        self.direction = 2

    def __move(self):
        if self.hp:
            if self.rect.left <= 100:
                self.rect.left = 100
            elif self.rect.right >= self.width - 100:
                self.rect.right = self.width - 100
            if self.rect.top <= 100:
                self.rect.top = 100
            elif self.rect.bottom >= self.height - 100:
                self.rect.bottom = self.height - 100

    def __shoot(self):
        if self.shotCD <= 0:
            pygame.mixer.Sound.play(self.bullet_sound)
            if self.direction == 0:
                self.bulletList.append([[self.rect.centerx + 20, self.rect.top], 0])
            if self.direction == 1:
                self.bulletList.append([[self.rect.right, self.rect.centery + 20], 1])
            if self.direction == 2:
                self.bulletList.append([[self.rect.centerx - 20, self.rect.bottom], 2])
            if self.direction == 3:
                self.bulletList.append([[self.rect.left, self.rect.centery - 20], 3])
            self.shotCD = 20

    def __moveBullets(self):
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

    def draw(self, screen):
        if self.alive:
            screen.blit(self.rotatedImage, self.rect)
            self.__moveBullets()
            self.__drawBullets(screen)

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
