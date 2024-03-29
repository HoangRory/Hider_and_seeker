class Button():
    def __init__(self, pos, image, text, font, textColor, hoverColor):
        self.pos = pos
        self.image = image
        self.font = font
        self.text = text
        self.textImage = self.font.render(self.text, True, textColor)
        self.hoverColor = hoverColor
        if self.image is None:
            self.image = self.textImage
        self.textColor = textColor
        self.rect = self.image.get_rect(center = (self.pos[0], self.pos[1]))
        self.textRect = self.textImage.get_rect(center = (self.pos[0], self.pos[1]))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)
        
    def checkInput(self, mousePos):
        if (mousePos[0] > self.rect.left and mousePos[0] < self.rect.right 
            and mousePos[1] > self.rect.top and mousePos[1] < self.rect.bottom):
            return True
        return False
    
    def changeColor(self, mousePos):
        if (mousePos[0] > self.rect.left and mousePos[0] < self.rect.right 
            and mousePos[1] > self.rect.top and mousePos[1] < self.rect.bottom):
            self.text = self.font.render(self.text, True, self.hoverColor)
        else:
            self.text = self.font.render(self.text, True, self.textColor)