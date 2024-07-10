import pygame


class ImageButton:
    def __init__(self, x, y, width, height, text, image_before, image_after=None, sound_path=None):
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image_before), (width, height))
        if image_after:
            self.image_after = pygame.transform.scale(pygame.image.load(image_after), (width, height))
        else:
            self.image_after = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        else:
            self.sound = None
        self.mouse_pointed = False

    def draw(self, screen):

        current_image = self.image
        if self.mouse_pointed:
            current_image = self.image_after

        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pointed):
        self.mouse_pointed = self.rect.collidepoint(mouse_pointed)

    def event_mous(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mouse_pointed:
            if self.sound:
                self.sound.play()
                return True
        return False
