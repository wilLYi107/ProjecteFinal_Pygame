import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, posX, posY, img, shooter):
        pygame.sprite.Sprite.__init__(self)
        self.bulletImage = pygame.image.load(img)
        self.rect = self.bulletImage.get_rect()
        self.rect.centerx = posX
        self.rect.centery = posY
        self.bulletSpeed = 1
        self.shooter = shooter

    def direction(self):
        if self.shooter:
            self.rect.top -= self.bulletSpeed
        else:
            self.rect.top += self.bulletSpeed

    def draw(self, surface):
        surface.blit(self.bulletImage, self.rect)