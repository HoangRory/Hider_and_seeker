import pygame
import sys
from button import Button
import os

HEITGH = 600
WIDTH = 800

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEITGH))
menuBG = pygame.image.load("assets/MenuBG.png")

def menu():
    pygame.display.set_caption("Hide and seek")
    
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        menuText = pygame.font.Font(None, 100).render("HIDE AND SEEK", True, (255, 255, 255))
        menuRect = menuText.get_rect(center=(WIDTH/2, HEITGH/2 - 200))
        subtitleText = pygame.font.Font(None, 35).render("(But you're not playing)", True, (255, 255, 255))
        subtitleRect = subtitleText.get_rect(center=(WIDTH/2, HEITGH/2 - 125))
        
        startButton = Button(image = None, pos = (WIDTH/2, HEITGH/2), text = "Start", font = pygame.font.Font(None, 75), textColor = "White", hoverColor = "Green")
        
        screen.blit(menuText, menuRect)
        screen.blit(subtitleText, subtitleRect)
        
        for button in [startButton]:
            button.changeColor(mousePos)
            button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.checkInput(mousePos):
                    start()
                    
        pygame.display.update()
        
def start():
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        promptText = pygame.font.Font(None, 75).render("Choose a level", True, (255, 255, 255))
        promptRect = promptText.get_rect(center=(WIDTH/2, HEITGH/2 - 200))
        
        screen.blit(promptText, promptRect)
        
        level1Button = Button(image = None, pos = (WIDTH/2, HEITGH/2), text = "Level 1", font = pygame.font.Font(None, 50), textColor = "White", hoverColor = "Green")
        level2Button = Button(image = None, pos = (WIDTH/2, HEITGH/2 + 50), text = "Level 2", font = pygame.font.Font(None, 50), textColor = "White", hoverColor = "Green")
        level3Button = Button(image = None, pos = (WIDTH/2, HEITGH/2 + 100), text = "Level 3", font = pygame.font.Font(None, 50), textColor = "White", hoverColor = "Green")
        
        for button in [level1Button, level2Button, level3Button]:
            button.changeColor(mousePos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1Button.checkInput(mousePos):
                    level1()
                elif level2Button.checkInput(mousePos):
                    level2()
                elif level3Button.checkInput(mousePos):
                    level3()

        pygame.display.update()
        
def level1():
    os.system("python Level1/main.py")
def level2():
    os.system("python Level2/main.py")
def level3():
    os.system("python Level3/main.py")
        
        
menu()