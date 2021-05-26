import pygame
import pygame_gui
import sys
from pygame import *

import enemy
import player


class Main:
    def __init__(self):
        pygame.init()
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h

        self.introManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")
        self.gameManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")
        self.pauseManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")
        self.controlsManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")
        self.endedManager = pygame_gui.UIManager((self.width, self.height), "Assets/themes/theme.json")

        self.clock = pygame.time.Clock()
        self.time = 0
        self.state = "intro"
        self.font = pygame.font.SysFont("Arial", 72, True)
        self.livesFont = pygame.font.SysFont("Arial", 30, True)
        self.pauseText = self.font.render("GAME PAUSED!", False, (0, 0, 0))
        pygame.mixer.music.load('Assets/audio/BackGround.mp3')
        pygame.mixer.music.play(-1)
        self.victorySound = pygame.mixer.Sound("Assets/audio/winsound.ogg")

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.movement = 360

        self.background = pygame.image.load("Assets/img/bg.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.controls = pygame.image.load("Assets/img/controls.jpg")
        self.controls = pygame.transform.scale(self.controls, (self.width, self.height))
        self.menuBg = pygame.image.load("Assets/img/bg.jpg").convert(24)
        self.menuBg = pygame.transform.scale(self.menuBg, (self.width, self.height))
        self.menuBg.set_alpha(128)
        self.titleImg = pygame.image.load("Assets/img/title.png")

        self.doublePlayer = False
        self.enemyNumber = 1

        self.startBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 100, self.height * 0.7), (200, 80)),
            text='START GAME',
            manager=self.introManager,
            object_id='startButton')
        self.menuExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 70, 20), (50, 50)),
            text='X',
            manager=self.introManager,
            object_id='exitButton')
        self.gameExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 70, 20), (50, 50)),
            text='X',
            manager=self.gameManager,
            object_id='exitButton')
        self.pausedExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 70, 20), (50, 50)),
            text='X',
            manager=self.pauseManager,
            object_id='exitButton')
        self.endedExitBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 70, 20), (50, 50)),
            text='X',
            manager=self.endedManager,
            object_id='exitButton')
        self.pauseGameBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 140, 20), (50, 50)),
            text='||',
            manager=self.gameManager,
            object_id='normalButton')
        self.unpauseGameBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width - 140, 20), (50, 50)),
            text='||',
            manager=self.pauseManager,
            object_id='normalButton')
        self.resumeGameBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 75, self.height * 0.6), (150, 50)),
            text='RESUME GAME',
            manager=self.pauseManager,
            object_id='normalButton')
        self.backToMenuBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 75, self.height * 0.68), (150, 50)),
            text='BACK TO MENU',
            manager=self.pauseManager,
            object_id='normalButton')
        self.gameEndedBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 75, self.height * 0.68), (150, 50)),
            text='BACK TO MENU',
            manager=self.endedManager,
            object_id='normalButton')
        self.continueToGameBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 100, self.height * 0.8), (200, 70)),
            text='UNDERSTOOD!',
            manager=self.controlsManager,
            object_id='normalButton')

        self.onePlayerBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.45) - 50, self.height * 0.45), (100, 50)),
            text='1 PLAYER',
            manager=self.introManager,
            object_id='menuButton')
        self.onePlayerBtn.select()
        self.twoPlayerBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.55) - 50, self.height * 0.45), (100, 50)),
            text='2 PLAYERS',
            manager=self.introManager,
            object_id='menuButton')

        self.noEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.4) - 50, self.height * 0.55), (100, 50)),
            text='NO ENEMIES',
            manager=self.introManager,
            object_id='menuButton')
        self.noEnemyBtn.disable()
        self.oneEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.5) - 50, self.height * 0.55), (100, 50)),
            text='1 ENEMY',
            manager=self.introManager,
            object_id='menuButton')
        self.oneEnemyBtn.select()
        self.twoEnemyBtn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.width * 0.6) - 50, self.height * 0.55), (100, 50)),
            text='2 ENEMIES',
            manager=self.introManager,
            object_id='menuButton')

    def reset(self):
        self.clock = pygame.time.Clock()
        self.time = 0
        self.state = "intro"
        self.movement = 360
        self.doublePlayer = False
        self.enemyNumber = 1
        self.enemy1 = enemy.Enemy(self.width, self.height, 1)
        self.enemy2 = enemy.Enemy(self.width, self.height, 2)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.gameManager.draw_ui(self.screen)
        if not self.doublePlayer:
            self.p1Lives = self.livesFont.render("P1: " + str(self.player1.hp) + " HP", False, (0, 0, 0))
        else:
            self.p1Lives = self.livesFont.render("P1: " + str(self.player1.hp) + " HP", False, (0, 0, 0))
            self.p2Lives = self.livesFont.render("P2: " + str(self.player2.hp) + " HP", False, (0, 0, 0))
        if self.enemyNumber == 1:
            self.e1Lives = self.livesFont.render("E1: " + str(self.enemy1.hp) + " HP", False, (0, 0, 0))
        elif self.enemyNumber == 2:
            self.e1Lives = self.livesFont.render("E1: " + str(self.enemy1.hp) + " HP", False, (0, 0, 0))
            self.e2Lives = self.livesFont.render("E2: " + str(self.enemy2.hp) + " HP", False, (0, 0, 0))
        if self.doublePlayer:
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.screen.blit(self.p1Lives, (40, 20))
            self.screen.blit(self.p2Lives, (40, 70))
        else:
            self.player1.draw(self.screen)
            self.screen.blit(self.p1Lives, (40, 20))
        if self.enemyNumber == 1:
            self.enemy1.draw(self.screen)
            self.screen.blit(self.e1Lives, (200, 20))
        elif self.enemyNumber == 2:
            self.enemy1.draw(self.screen)
            self.enemy2.draw(self.screen)
            self.screen.blit(self.e1Lives, (200, 20))
            self.screen.blit(self.e2Lives, (200, 70))
        pygame.display.flip()

    def inputHandler(self):
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.gameManager.process_events(ev)
            if ev.type == pygame.USEREVENT:
                if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.gameExitBtn:
                        pygame.quit()
                        sys.exit()
                    if ev.ui_element == self.pauseGameBtn:
                        self.__pause()
        if not self.doublePlayer:
            self.player1.inputHandler()
        else:
            self.player1.inputHandler()
            self.player2.inputHandler()

    def enemyShoot(self):
        if self.enemyNumber == 1 and self.doublePlayer:
            self.enemy1.shoot([self.player1.rect.center, self.player2.rect.center])
        elif self.enemyNumber == 1 and not self.doublePlayer:
            self.enemy1.shoot([self.player1.rect.center])
        elif self.enemyNumber == 2 and self.doublePlayer:
            self.enemy1.shoot([self.player1.rect.center, self.player2.rect.center])
            self.enemy2.shoot([self.player1.rect.center, self.player2.rect.center])
        elif self.enemyNumber == 2 and not self.doublePlayer:
            self.enemy1.shoot([self.player1.rect.center])
            self.enemy2.shoot([self.player1.rect.center])

    def drawEnemyBullets(self):
        if self.enemyNumber == 1:
            self.enemy1.moveBullets()
        elif self.enemyNumber == 2:
            self.enemy1.moveBullets()
            self.enemy2.moveBullets()

    def moveEnemies(self):
        if self.enemyNumber == 1:
            self.movement -= 1
            if self.movement > 270:
                self.enemy1.moveRight()
            elif self.movement > 180:
                self.enemy1.moveDown()
            elif self.movement > 90:
                self.enemy1.moveLeft()
            elif self.movement > 0:
                self.enemy1.moveUp()
            else:
                self.movement = 360
        if self.enemyNumber == 2:
            self.movement -= 1
            if self.movement > 270:
                self.enemy1.moveRight()
                self.enemy2.moveDown()
            elif self.movement > 180:
                self.enemy1.moveDown()
                self.enemy2.moveLeft()
            elif self.movement > 90:
                self.enemy1.moveLeft()
                self.enemy2.moveUp()
            elif self.movement > 0:
                self.enemy1.moveUp()
                self.enemy2.moveRight()
            else:
                self.movement = 360

    def checkCollision(self):
        if self.enemyNumber == 1 and self.doublePlayer:
            self.player1.collided([self.enemy1.bulletList, self.player2.bulletList])
            self.player2.collided([self.enemy1.bulletList, self.player1.bulletList])
            self.enemy1.collided([self.player1.bulletList, self.player2.bulletList])
        elif self.enemyNumber == 1 and not self.doublePlayer:
            self.player1.collided([self.enemy1.bulletList])
            self.enemy1.collided([self.player1.bulletList])
        elif self.enemyNumber == 0 and self.doublePlayer:
            self.player1.collided([self.player2.bulletList])
            self.player2.collided([self.player1.bulletList])
        elif self.enemyNumber == 2 and self.doublePlayer:
            self.player1.collided([self.enemy1.bulletList, self.enemy2.bulletList, self.player2.bulletList])
            self.player2.collided([self.enemy1.bulletList, self.enemy2.bulletList, self.player1.bulletList])
            self.enemy1.collided([self.player1.bulletList, self.player2.bulletList, self.enemy2.bulletList])
            self.enemy2.collided([self.player1.bulletList, self.player2.bulletList, self.enemy1.bulletList])
        elif self.enemyNumber == 2 and not self.doublePlayer:
            self.player1.collided([self.enemy1.bulletList, self.enemy2.bulletList])
            self.enemy1.collided([self.player1.bulletList, self.enemy2.bulletList])
            self.enemy2.collided([self.player1.bulletList, self.enemy1.bulletList])

    def win(self):
        if self.enemyNumber == 1 and self.doublePlayer:
            if not self.player1.alive and not self.player2.alive:
                self.__gameEnded(self.enemy1.name)
            elif not self.enemy1.alive and not self.player2.alive:
                self.__gameEnded(self.player1.name)
            elif not self.player1.alive and not self.enemy1.alive:
                self.__gameEnded(self.player2.name)
        elif self.enemyNumber == 1 and not self.doublePlayer:
            if not self.player1.alive:
                self.__gameEnded(self.enemy1.name)
            elif not self.enemy1.alive:
                self.__gameEnded(self.player1.name)
        elif self.enemyNumber == 0 and self.doublePlayer:
            if not self.player1.alive:
                self.__gameEnded(self.player2.name)
            elif not self.player2.alive:
                self.__gameEnded(self.player1.name)
        elif self.enemyNumber == 2 and self.doublePlayer:
            if not self.player1.alive and not self.player2.alive and not self.enemy1.alive:
                self.__gameEnded(self.enemy2.name)
            elif not self.enemy1.alive and not self.player2.alive and not self.enemy2.alive:
                self.__gameEnded(self.player1.name)
            elif not self.player1.alive and not self.enemy1.alive and not self.enemy2.alive:
                self.__gameEnded(self.player2.name)
            elif not self.player1.alive and not self.player2.alive and not self.enemy2.alive:
                self.__gameEnded(self.enemy1.name)
        elif self.enemyNumber == 2 and not self.doublePlayer:
            if not self.player1.alive and not self.enemy2.alive:
                self.__gameEnded(self.enemy1.name)
            elif not self.enemy1.alive and not self.enemy2.alive:
                self.__gameEnded(self.player1.name)
            elif not self.player1.alive and not self.enemy1.alive:
                self.__gameEnded(self.enemy2.name)

    def __intro(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            self.introManager.process_events(ev)
            if ev.type == pygame.USEREVENT:
                if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.startBtn:
                        self.state = "control"
                        if not self.doublePlayer:
                            self.player1 = player.Player(self.width, self.height, 1)
                        else:
                            self.player1 = player.Player(self.width, self.height, 1)
                            self.player2 = player.Player(self.width, self.height, 2)
                        if self.enemyNumber == 1:
                            self.enemy1 = enemy.Enemy(self.width, self.height, 1)
                        elif self.enemyNumber == 2:
                            self.enemy1 = enemy.Enemy(self.width, self.height, 1)
                            self.enemy2 = enemy.Enemy(self.width, self.height, 2)
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
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.menuBg, (0, 0))
        self.screen.blit(self.titleImg, ((self.width / 2) - 350, 100))
        self.introManager.draw_ui(self.screen)
        pygame.display.update()

    def __main_game(self):
        self.draw()
        self.inputHandler()
        self.enemyShoot()
        self.drawEnemyBullets()
        self.moveEnemies()
        self.checkCollision()
        self.win()
        self.gameManager.update(self.time)
        self.gameManager.draw_ui(self.screen)

    def __pause(self):
        paused = True
        pygame.mixer.music.pause()
        while paused:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.pauseManager.process_events(ev)
                if ev.type == pygame.USEREVENT:
                    if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if ev.ui_element == self.resumeGameBtn or ev.ui_element == self.unpauseGameBtn:
                            paused = False
                            pygame.mixer.music.unpause()
                        if ev.ui_element == self.backToMenuBtn:
                            self.reset()
                            paused = False
                            pygame.mixer.music.rewind()
                            pygame.mixer.music.play(-1)
                        if ev.ui_element == self.pausedExitBtn:
                            pygame.quit()
                            sys.exit()
            self.screen.blit(self.pauseText, ((self.width / 2) - 270, 300))
            self.pauseManager.update(self.time)
            self.pauseManager.draw_ui(self.screen)
            pygame.display.update()

    def __gameEnded(self, winner):
        ended = True
        pygame.mixer.Sound.play(self.victorySound)
        while ended:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.endedManager.process_events(ev)
                if ev.type == pygame.USEREVENT:
                    if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if ev.ui_element == self.gameEndedBtn:
                            self.reset()
                            ended = False
                            pygame.mixer.music.rewind()
                            pygame.mixer.music.play(-1)
                        if ev.ui_element == self.endedExitBtn:
                            pygame.quit()
                            sys.exit()
            self.screen.blit(self.font.render(winner + " WON!!", False, (0, 0, 0)), ((self.width / 2) - 270, 300))
            self.endedManager.update(self.time)
            self.endedManager.draw_ui(self.screen)
            pygame.display.update()

    def __controlKeys(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            self.controlsManager.process_events(ev)
            if ev.type == pygame.USEREVENT:
                if ev.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == self.continueToGameBtn:
                        self.state = "main_game"
        self.controlsManager.update(self.time)
        self.screen.blit(self.controls, (0, 0))
        self.controlsManager.draw_ui(self.screen)
        pygame.display.update()

    def stateChange(self):
        if self.state == "intro":
            self.__intro()
        elif self.state == "control":
            self.__controlKeys()
        elif self.state == "main_game":
            self.__main_game()

    def play(self):
        while True:
            self.time = self.clock.tick(60) / 1000.0
            self.stateChange()


run = Main()
run.play()
