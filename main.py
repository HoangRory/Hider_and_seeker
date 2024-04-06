import pygame
import sys
from button import Button
from Level1.main import main as lvl1
from Level2.main import main as lvl2
from Level3.main import main as lvl3

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

waitPrompt = "Loading..."
def level1():
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        promptText = "Choose a map"
        printText(promptText, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 200))
        map1Button = Button(image=lvButton, pos=(WIDTH/2 - 200, HEITGH/2), text="Map 1", fontSize=50, textColor="White", hoverSize=(185, 85))
        map2Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2), text="Map 2", fontSize=50, textColor="White", hoverSize=(185, 85))
        map3Button = Button(image=lvButton, pos=(WIDTH/2 + 200, HEITGH/2), text="Map 3", fontSize=50, textColor="White", hoverSize=(185, 85))
        map4Button = Button(image=lvButton, pos=(WIDTH/2 - 100, HEITGH/2 + 150), text="Map 4", fontSize=50, textColor="White", hoverSize=(185, 85))
        map5Button = Button(image=lvButton, pos=(WIDTH/2 + 100, HEITGH/2 + 150), text="Map 5", fontSize=50, textColor="White", hoverSize=(185, 85))
        backButton = Button(image=lvButton, pos=(100, HEITGH - 50), text="< Back", fontSize=50, textColor="White", hoverSize=(185, 85))

        for button in [map1Button, map2Button, map3Button, map4Button, map5Button, backButton]:
            button.changeSize(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                printText(waitPrompt, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 100))
                pygame.display.update()
                if map1Button.checkInput(mousePos):
                    lvl1("map1.txt")
                elif map2Button.checkInput(mousePos):
                    lvl1("map2.txt")
                elif map3Button.checkInput(mousePos):
                    lvl1("map3.txt")
                elif map4Button.checkInput(mousePos):
                    lvl1("map4.txt")
                elif map5Button.checkInput(mousePos):
                    lvl1("map5.txt")
                elif backButton.checkInput(mousePos):
                    start()
                    break
                pygame.display.set_mode((WIDTH, HEITGH))   
        pygame.display.update()

def level2():
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        promptText = "Choose a map"
        printText(promptText, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 200))
        map1Button = Button(image=lvButton, pos=(WIDTH/2 - 200, HEITGH/2), text="Map 1", fontSize=50, textColor="White", hoverSize=(185, 85))
        map2Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2), text="Map 2", fontSize=50, textColor="White", hoverSize=(185, 85))
        map3Button = Button(image=lvButton, pos=(WIDTH/2 + 200, HEITGH/2), text="Map 3", fontSize=50, textColor="White", hoverSize=(185, 85))
        map4Button = Button(image=lvButton, pos=(WIDTH/2 - 100, HEITGH/2 + 150), text="Map 4", fontSize=50, textColor="White", hoverSize=(185, 85))
        map5Button = Button(image=lvButton, pos=(WIDTH/2 + 100, HEITGH/2 + 150), text="Map 5", fontSize=50, textColor="White", hoverSize=(185, 85))
        backButton = Button(image=lvButton, pos=(100, HEITGH - 50), text="< Back", fontSize=50, textColor="White", hoverSize=(185, 85))

        for button in [map1Button, map2Button, map3Button, map4Button, map5Button, backButton]:
            button.changeSize(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                printText(waitPrompt, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 100))
                pygame.display.update()
                if map1Button.checkInput(mousePos):
                    lvl2("map1.txt")
                elif map2Button.checkInput(mousePos):
                    lvl2("map2.txt")
                elif map3Button.checkInput(mousePos):
                    lvl2("map3.txt")
                elif map4Button.checkInput(mousePos):
                    lvl2("map4.txt")
                elif map5Button.checkInput(mousePos):
                    lvl2("map5.txt")
                elif backButton.checkInput(mousePos):
                    start()
                    break
                pygame.display.set_mode((WIDTH, HEITGH))
        pygame.display.update()
        
def level3():
    while True:
        screen.blit(menuBG, (0, 0))
        mousePos = pygame.mouse.get_pos()
        promptText = "Choose a map"
        printText(promptText, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 200))
        map1Button = Button(image=lvButton, pos=(WIDTH/2 - 200, HEITGH/2), text="Map 1", fontSize=50, textColor="White", hoverSize=(185, 85))
        map2Button = Button(image=lvButton, pos=(WIDTH/2, HEITGH/2), text="Map 2", fontSize=50, textColor="White", hoverSize=(185, 85))
        map3Button = Button(image=lvButton, pos=(WIDTH/2 + 200, HEITGH/2), text="Map 3", fontSize=50, textColor="White", hoverSize=(185, 85))
        map4Button = Button(image=lvButton, pos=(WIDTH/2 - 100, HEITGH/2 + 150), text="Map 4", fontSize=50, textColor="White", hoverSize=(185, 85))
        map5Button = Button(image=lvButton, pos=(WIDTH/2 + 100, HEITGH/2 + 150), text="Map 5", fontSize=50, textColor="White", hoverSize=(185, 85))
        backButton = Button(image=lvButton, pos=(100, HEITGH - 50), text="< Back", fontSize=50, textColor="White", hoverSize=(185, 85))

        for button in [map1Button, map2Button, map3Button, map4Button, map5Button, backButton]:
            button.changeSize(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                printText(waitPrompt, 100, (255, 255, 255), (WIDTH/2, HEITGH/2 - 100))
                pygame.display.update()
                if map1Button.checkInput(mousePos):
                    lvl3("map1.txt")
                elif map2Button.checkInput(mousePos):
                    lvl3("map2.txt")
                elif map3Button.checkInput(mousePos):
                    lvl3("map3.txt")
                elif map4Button.checkInput(mousePos):
                    lvl3("map4.txt")
                elif map5Button.checkInput(mousePos):
                    lvl3("map5.txt")
                elif backButton.checkInput(mousePos):
                    start()
                    break
                pygame.display.set_mode((WIDTH, HEITGH))        
        pygame.display.update()       
        
menu()