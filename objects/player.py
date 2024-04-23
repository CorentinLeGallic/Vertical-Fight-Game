import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, game, name, color, number):

        # initialisation de la super-classe Sprite
        super().__init__()

        # définir les attributs du joueur
        self.name = name
        self.number = number
        # self.coins = 0
        self.game = game
        # self.max_health = 100
        # self.health = 100
        # self.start_attack = 10
        # self.attack = 10
        self.speed = 2
        self.vertical_speed = 4
        # self.start_defense = 100
        # self.defense = 100
        self.image = pygame.image.load(f'./assets/players/{color}_player.png')
        self.image = pygame.transform.scale(self.image, (44, 56.25))
        self.rect = self.image.get_rect()
        self.rect.x = spawn_position[str(f'player_{self.number}')][0]
        self.rect.y = spawn_position[str(f'player_{self.number}')][1] - self.image.get_height()
        # self.weapon = None
        # self.armor = []

        # différents côtés du joueur
        self.left_side = pygame.Rect(self.rect.x, self.rect.y + 2, 1, self.image.get_height()- 4)
        self.right_side = pygame.Rect(self.rect.x + self.image.get_width(), self.rect.y + 2, 1, self.image.get_height() - 4)
        self.bottom_side = pygame.Rect(self.rect.x + 2, self.rect.y + self.image.get_height(), self.image.get_width() - 4, 1)
        self.top_side = pygame.Rect(self.rect.x + 2, self.rect.y, self.image.get_width() - 4, 1)

        self.is_jumping = False
        self.jump_counter = 0
        self.is_falling = False
        self.fall_counter = 0

    def fall(self):
        self.rect.y += self.vertical_speed
        self.fall_counter += self.vertical_speed

    def collide_bottom(self):
        if self.bottom_side.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def collide_top(self):
        if self.top_side.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def collide_left(self):
        if self.left_side.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def collide_right(self):
        if self.right_side.collidelist(self.game.walls) > -1:
            return True
        else:
            return False

    def update(self):
        self.left_side = pygame.Rect(self.rect.x, self.rect.y + 2, 1, self.image.get_height()- 4)
        self.right_side = pygame.Rect(self.rect.x + self.image.get_width(), self.rect.y + 2, 1, self.image.get_height() - 4)
        self.bottom_side = pygame.Rect(self.rect.x + 2, self.rect.y + self.image.get_height(), self.image.get_width() - 4, 1)
        self.top_side = pygame.Rect(self.rect.x + 2, self.rect.y, self.image.get_width() - 4, 1)

    def move_right(self):
        if not self.collide_right():
            self.rect.x += self.speed
            self.update()

    def move_left(self):
        if not self.collide_left():
            self.rect.x -= self.speed
            self.update()

    def jump(self):
        if not self.top_side.collidelist(self.game.walls) > -1:
            self.rect.y -= self.vertical_speed
            self.jump_counter += self.vertical_speed
        else:
            self.is_falling = True

spawn_position = {
    "player_1":(192, 576), 
    "player_2":(1056, 576)
}


