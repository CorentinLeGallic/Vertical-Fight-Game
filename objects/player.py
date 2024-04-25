import pygame
from objects.bullet import Bullet
from objects.weapons import Weapon

class Player(pygame.sprite.Sprite):

    def __init__(self, game, name, color, number):

        # initialisation de la super-classe Sprite
        super().__init__()

        # définir les attributs du joueur
        self.name = name
        self.number = number
        self.game = game
        self.speed = 2
        self.vertical_speed = 4
        self.initial_vertical_speed = 6
        self.progress = 1.9
        self.defense = 0

        # définir la position et le skin du joueur
        self.image = pygame.image.load(f'./assets/players/{color}_player.png')
        self.image = pygame.transform.scale(self.image, (44, 56.25))
        self.rect = self.image.get_rect()
        self.rect.x = spawn_position[str(f'player_{self.number}')][0]
        self.rect.y = spawn_position[str(f'player_{self.number}')][1] - self.image.get_height()
        self.initial_position = spawn_position[str(f'player_{self.number}')][1] - self.image.get_height()
        
        if self.number == 1:
            self.direction = "right"
        elif self.number == 2:
            self.direction = "left"

        # différents côtés du joueur
        self.left_side = pygame.Rect(self.rect.x, self.rect.y + 2, 1, self.image.get_height()- 4)
        self.right_side = pygame.Rect(self.rect.x + self.image.get_width(), self.rect.y + 2, 1, self.image.get_height() - 4)
        self.bottom_side = pygame.Rect(self.rect.x + 2, self.rect.y + self.image.get_height(), self.image.get_width() - 4, 1)
        self.top_side = pygame.Rect(self.rect.x + 2, self.rect.y, self.image.get_width() - 4, 1)

        self.is_jumping = False
        self.jump_counter = 0
        self.is_falling = False
        self.fall_counter = 0

        # gérer les armes
        self.weapons = {
            "Knife": Weapon("knife", 5, False, self, False),
            "Shuriken": Weapon("shuriken", 5, False, self, 5),
            "Desert Eagle": Weapon("desert_eagle", 0, 25, self, 5),
            "AK47": Weapon("ak47", 15, 15, self, 5),
            "Rocket Launcher": Weapon("rocket_launcher", 20, 5, self, 3)
        }

        self.all_weapons = [self.weapons['Knife']]
        self.weapon = self.all_weapons[len(self.all_weapons) - 1]

        # gérer les projectiles
        self.all_bullets = pygame.sprite.Group()

        # gérer la vie
        self.health = 100
        self.max_health = 100

    def update_health_bar(self):
        pygame.draw.rect(self.game.screen, (219, 0, 0), [self.rect.x + 50, self.rect.y + 13, self.max_health, 7])
        pygame.draw.rect(self.game.screen, (0, 219, 15), [self.rect.x + 50, self.rect.y + 13, self.health, 7])

    def collide_side(self, side):
        if side.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def rect_y_regulate(self):
        for i in range(-8, 8):
            if (self.rect.y + self.image.get_height() + i) % 48 == 0:
                self.rect.y += i
    def fall(self):
        if self.jump_counter > 0:
            self.jump_counter -= int(self.vertical_speed)
            self.vertical_speed = 6*(1-(self.jump_counter/self.progress)/100)
            self.jump_counter = int(self.jump_counter)
            self.rect.y += int(self.vertical_speed)
        else:
            if self.jump_counter < 0:
                self.jump_counter = 0
            self.rect.y += int(self.vertical_speed)

    def update(self):
        self.left_side = pygame.Rect(self.rect.x, self.rect.y + 2, 1, self.image.get_height()- 4)
        self.right_side = pygame.Rect(self.rect.x + self.image.get_width(), self.rect.y + 2, 1, self.image.get_height() - 4)
        self.bottom_side = pygame.Rect(self.rect.x + 2, self.rect.y + self.image.get_height(), self.image.get_width() - 4, 1)
        self.top_side = pygame.Rect(self.rect.x + 2, self.rect.y, self.image.get_width() - 4, 1)

    def move_right(self):
        if not self.collide_side(self.right_side):
            self.rect.x += self.speed
            self.update()

    def move_left(self):
        if not self.collide_side(self.left_side):
            self.rect.x -= self.speed
            self.update()

    def jump(self):
        self.jump_counter += self.vertical_speed
        self.jump_counter = int(self.jump_counter)
        self.vertical_speed = 6*(1-(self.jump_counter/self.progress)/100)
        self.rect.y -= int(self.vertical_speed)

    def equip_weapon(self, weapon):
        self.all_weapons.append(self.weapons[weapon])
        self.weapon = self.all_weapons[len(self.all_weapons) - 1]

    def unequip_weapon(self, weapon):
        self.all_weapons.remove(weapon)
        self.weapon = self.all_weapons[len(self.all_weapons) - 1]

    def shoot(self):
        if self.weapon.ammos > 0:
            bullet = Bullet(self.game, self, self.weapon)
            self.all_bullets.add(bullet)
            self.weapon.ammos -= 1
        else:
            self.unequip_weapon(self.weapon)

    def damage(self, damages):
        self.health -= damages

spawn_position = {
    "player_1":(192, 576), 
    "player_2":(1056, 576)
}


