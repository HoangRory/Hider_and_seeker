import pygame
class Button():
    def __init__(self, pos, image, text, fontSize, textColor, hoverSize):
        self.pos = pos
        self.image = image
        self.fontSize = fontSize
        self.font = pygame.font.Font(None, fontSize)
        self.text = text
        self.textImage = self.font.render(self.text, True, textColor)
        if self.image is None:
            self.image = self.textImage
        self.textColor = textColor
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        self.textRect = self.textImage.get_rect(center = (self.pos[0], self.pos[1]))
        self.hoverSize = hoverSize
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.textImage, self.textRect)
        
    def checkInput(self, mousePos):
        if (mousePos[0] > self.rect.left and mousePos[0] < self.rect.right 
            and mousePos[1] > self.rect.top and mousePos[1] < self.rect.bottom):
            return True
        return False
    
    def changeSize(self, mousePos):
        if (mousePos[0] > self.rect.left and mousePos[0] < self.rect.right 
            and mousePos[1] > self.rect.top and mousePos[1] < self.rect.bottom):
            self.image = pygame.transform.scale(self.image, self.hoverSize)
            self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
            self.font = pygame.font.Font(None, self.fontSize + 3)
        else:
            self.image = pygame.transform.scale(self.image, self.rect.size)
            self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
            self.font = pygame.font.Font(None, self.fontSize)
            
        self.textImage = self.font.render(self.text, True, self.textColor)
        self.textRect = self.textImage.get_rect(center = (self.pos[0], self.pos[1]))