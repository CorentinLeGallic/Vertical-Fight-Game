import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, damages, ammos, player, ammo_speed):
        super().__init__()
        self.name = name
        self.damages = damages
        self.ammos = ammos
        self.player = player
        self.ammo_speed = ammo_speed
        self.image = pygame.image.load(f'./assets/weapons/{self.name}.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x + weapons_rect[self.name][0]
        self.rect.y = self.player.rect.y + weapons_rect[self.name][1]

    def update_sprite(self):
        self.rect.x = self.player.rect.x + weapons_rect[self.name][0]
        self.rect.y = self.player.rect.y + weapons_rect[self.name][1]
        
weapons_rect = {
    "knife": (35, 15),
    "shuriken": (35, 25),
    "desert_eagle": (35, 25),
    "ak47": (25, 25),
    "rocket_launcher": (25, 25)
}