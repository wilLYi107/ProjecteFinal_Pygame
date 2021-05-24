import pygame, sys
from pygame import *
import pygame_gui
import player
import enemy

class Main:
    def __init__(self):
        pygame.init()
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h

        self.introManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")
        self.gameManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")

        self.clock = pygame.time.Clock()
        self.time = 0
        self.state = "intro"
        self.font = pygame.font.SysFont("Arial", 30)

        self.screen = pygame.display.set_mode((self.width, self.height))

        # self.background = pygame.image.load("Assets/img/bg.jpg")
        # self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.doublePlayer = False
        self.enemyNumber = 1
        self.enemy1 = enemy.Enemy(self.width, self.height, 1)
        self.enemy2 = enemy.Enemy(self.width, self.height, 2)

        self.startBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 50, self.height * 0.67), (100, 50)),
            text='START GAME',
            manager=self.introManager)
        self.menuExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 50, 20), (30, 30)),
            text='X',
            manager=self.introManager,
            object_id='exitButton')
        self.gameExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 50, 20), (30, 30)),
            text='X',
            manager=self.gameManager,
            object_id='exitButton')

        self.onePlayerBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.45) - 50, self.height * 0.45), (100, 50)),
            text='1 PLAYER',
            manager=self.introManager)
        self.onePlayerBtn.select()
        self.twoPlayerBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.55) - 50, self.height * 0.45), (100, 50)),
            text='2 PLAYERS',
            manager=self.introManager)

        self.noEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.4) - 50, self.height * 0.55), (100, 50)),
            text='NO ENEMIES',
            manager=self.introManager)
        self.noEnemyBtn.disable()
        self.oneEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 50, self.height * 0.55), (100, 50)),
            text='1 ENEMY',
            manager=self.introManager)
        self.oneEnemyBtn.select()
        self.twoEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.6) - 50, self.height * 0.55), (100, 50)),
            text='2 ENEMIES',
            manager=self.introManager)

    def draw(self):
        # self.screen.blit(self.background, (0, 0))
        self.screen.fill((255, 255, 255))
        self.gameManager.draw_ui(self.screen)
        if self.doublePlayer:
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
        else:
            self.player1.draw(self.screen)
        if self.enemyNumber == 1:
            self.enemy1.draw(self.screen)
        elif self.enemyNumber == 2:
            self.enemy1.draw(self.screen)
            self.enemy2.draw(self.screen)
        pygame.display.flip()

    def inputHandler(self):
        input = pygame.event.get()
        for ev in input:
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.gameManager.process_events(ev)
            if ev.type == pygame.USEREVENT:
                if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.gameExitBtn:
                        pygame.quit()
                        sys.exit()
        if not self.doublePlayer:
            self.player1.inputHandler(input)
        else:
            self.player1.inputHandler(input)
            self.player2.inputHandler(input)

    def __intro(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            self.introManager.process_events(ev)
            if ev.type == pygame.USEREVENT:
                if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.startBtn:
                        self.state = "main_game"
                        if not self.doublePlayer:
                            self.player1 = player.Player(self.width, self.height, 1)
                        else:
                            self.player1 = player.Player(self.width, self.height, 1)
                            self.player2 = player.Player(self.width, self.height, 2)
                    if ev.ui_element == self.menuExitBtn:
                        pygame.quit()
                        sys.exit()
                    if ev.ui_element == self.onePlayerBtn:
                        self.doublePlayer = False
                        self.onePlayerBtn.select()
                        self.twoPlayerBtn.unselect()
                        self.noEnemyBtn.disable()
                        if self.enemyNumber == 0:
                            self.enemyNumber = 1
                            self.oneEnemyBtn.select()
                    if ev.ui_element == self.twoPlayerBtn:
                        self.doublePlayer = True
                        self.onePlayerBtn.unselect()
                        self.twoPlayerBtn.select()
                        self.noEnemyBtn.enable()
                    if ev.ui_element == self.noEnemyBtn:
                        self.enemyNumber = 0
                        self.noEnemyBtn.select()
                        self.oneEnemyBtn.unselect()
                        self.twoEnemyBtn.unselect()
                    if ev.ui_element == self.oneEnemyBtn:
                        self.enemyNumber = 1
                        self.noEnemyBtn.unselect()
                        self.oneEnemyBtn.select()
                        self.twoEnemyBtn.unselect()
                    if ev.ui_element == self.twoEnemyBtn:
                        self.enemyNumber = 2
                        self.noEnemyBtn.unselect()
                        self.oneEnemyBtn.unselect()
                        self.twoEnemyBtn.select()
        self.introManager.update(self.time)
        self.screen.fill((30, 30, 30))
        self.introManager.draw_ui(self.screen)
        pygame.display.update()

    def __main_game(self):
        self.draw()
        self.inputHandler()
        self.gameManager.update(self.time)
        self.gameManager.draw_ui(self.screen)

    def stateChange(self):
        if self.state == "intro":
            self.__intro()
        elif self.state == "main_game":
            self.__main_game()

    def play(self):
        while True:
            self.time = self.clock.tick(60) / 1000.0
            self.stateChange()

run = Main()
run.play()
