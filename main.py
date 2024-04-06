import pygame
import sys
from button import Button
import os

HEITGH = 720
WIDTH = 1280

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEITGH))
menuBG = pygame.image.load("assets/MenuBG.png")
buttonBG = pygame.image.load("assets/Button.png")
buttonBG = pygame.transform.scale(buttonBG, (250, 100))

def printText(inputText, size, color, pos):
    font = pygame.font.Font(None, size)
    text = font.render(inputText, True, color)
    textRect = text.get_rect(center=pos)
    textOutlineUp = font.render(inputText, True, (0, 0, 0))
    textRectOutlineUp = textOutlineUp.get_rect(center=(pos[0], pos[1] - 2))  # Slightly offset for outline
    screen.blit(textOutlineUp, textRectOutlineUp)

    textOutlineDown = font.render(inputText, True, (0, 0, 0))
    textRectOutlineDown = textOutlineDown.get_rect(center=(pos[0], pos[1] + 2))  # Slightly offset for outline
    screen.blit(textOutlineDown, textRectOutlineDown)

    textOutlineLeft = font.render(inputText, True, (0, 0, 0))
    textRectOutlineLeft = textOutlineLeft.get_rect(center=(pos[0] - 2, pos[1]))  # Slightly offset for outline
    screen.blit(textOutlineLeft, textRectOutlineLeft)

    textOutlineRight = font.render(inputText, True, (0, 0, 0))
    textRectOutlineRight = textOutlineRight.get_rect(center=(pos[0] + 2, pos[1]))  # Slightly offset for outline
    screen.blit(textOutlineRight, textRectOutlineRight)
    screen.blit(text, textRect)

def menu():
    pygame.display.set_caption("Hide and seek")
    
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()

        menuText = "HIDE AND SEEK"
        printText(menuText, 150, (255, 255, 255), (WIDTH/2, HEITGH/2 - 200))
        subtitleText = "But you're not playing"
        printText(subtitleText, 50, (255, 255, 255), (WIDTH/2, HEITGH/2 - 125))
        
        startButton = Button(image=buttonBG, pos=(WIDTH/2, HEITGH/2 + 50), text="START", fontSize=75, textColor="White", hoverSize=(260, 110))
        
        for button in [startButton]:
            button.changeSize(mousePos)
            button.update(screen)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.checkInput(mousePos):
                    start()
                    
        pygame.display.update()

lvButton = pygame.image.load("assets/Button.png")
lvButton = pygame.transform.scale(lvButton, (175, 80))
def start():
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        promptText = "Choose a level"
        printText(promptText, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 200))
        
        level1Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2 - 50), text="Level 1", fontSize=50, textColor="White", hoverSize=(185, 85))
        level2Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2 + 50), text="Level 2", fontSize=50, textColor="White", hoverSize=(185, 85))
        level3Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2 + 150), text="Level 3", fontSize=50, textColor="White", hoverSize=(185, 85))
        
        for button in [level1Button, level2Button, level3Button]:
            button.changeSize(mousePos)
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