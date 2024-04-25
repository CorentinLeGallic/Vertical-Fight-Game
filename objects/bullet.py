from contextlib import suppress
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, player, weapon):
        super().__init__()

        self.weapon = weapon
        self.player = player
        self.game = game

        self.image = pygame.image.load(f'./assets/bullets/{self.weapon.name}_bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 5))
        self.rect = self.image.get_rect()
        self.rect.x = self.weapon.rect.x + self.weapon.image.get_width()
        self.rect.y = self.weapon.rect.y + self.weapon.image.get_height()/2

    def remove(self):
        self.player.all_bullets.remove(self)        

    def collide_walls(self):
        if self.rect.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def collide_player(self):
        for player in self.game.all_players:
            if self.rect.colliderect(player.rect) and player != self.player:
                return player
            else: return False

    def move(self):
        if self.collide_walls():
            self.remove()
        elif self.collide_player() != False:
            self.collide_player().damage(self.weapon.damages)
            self.remove()
        elif self.player.direction == "left":
            self.rect.x -= self.weapon.ammo_speed
        elif self.player.direction == "right":
            self.rect.x += self.weapon.ammo_speed