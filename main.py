import pygame, sys
from pygame import *
import player

class Main:
    def __init__(self):
        pygame.init()
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h - 20
        self.clock = pygame.time.Clock()
        self.state = "intro"
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Proyecto Final")
        self.font = pygame.font.SysFont("Arial", 30)
        self.background = pygame.image.load("Assets/bg.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.player1 = player.Player(self.width, self.height, 1)
        self.player2 = player.Player(self.width, self.height, 2)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        pygame.display.flip()

    def inputHandler(self):
        input = pygame.event.get()
        for ev in input:
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.player1.inputHandler(input)
        self.player2.inputHandler(input)

    def __intro(self):
        self.screen.fill((30, 30, 30))
        txt = self.font.render("MENÚ", False, (255, 255, 255))
        self.screen.blit(txt, (self.width/2 - 50, self.height/2 - 15))

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                self.state = "main_game"

        pygame.display.update()

    def __main_game(self):
        self.draw()
        self.inputHandler()

        # if ev.type == KEYDOWN:
        #     if ev.key == K_w:
        #         self.player1.moveUp()
        #     if ev.key == K_a:
        #         self.player1.moveLeft()
        #     if ev.key == K_s:
        #         self.player1.moveDown()
        #     if ev.key == K_d:
        #         self.player1.moveRight()

    def stateChange(self):
        if self.state == "intro":
            self.__intro()
        elif self.state == "main_game":
            self.__main_game()

    def play(self):
        while True:
            self.clock.tick(60)
            self.stateChange()

run = Main()
run.play()
