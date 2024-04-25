import pygame
import pytmx
import pyscroll

from objects.player import Player

class Game:
    
    def __init__(self):

        # gérer les FPS
        self.clock = pygame.time.Clock()
        self.FPS = 70

        # dictionnaire des events (touches)
        self.pressed = {}

        # groupe des joueurs
        self.all_players = pygame.sprite.Group()

        # créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((1200, 760))
        pygame.display.set_caption("VFG - Vertical Fight Game")

        # charger la map
        tmx_data = pytmx.util_pygame.load_pygame('./maps/dirt_map_1/map/dirt_map_1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size(), None, True)

        # définir la liste contenant les zones de collisions
        self.walls = [(object.x, object.y, object.width, object.height) for object in tmx_data.objects if object.Collisions]

        self.type = "Menu"

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # designer le menu
        self.start_button = pygame.image.load('./assets/buttons/start_button.png')
        self.start_button = pygame.transform.scale(self.start_button, (472,96))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = self.screen.get_width()/2 - self.start_button.get_width()/2
        self.start_button_rect.y = 200

        self.shop_button = pygame.image.load('./assets/buttons/shop_button.png')
        self.shop_button = pygame.transform.scale(self.shop_button, (472,96))
        self.shop_button_rect = self.shop_button.get_rect()
        self.shop_button_rect.x = self.screen.get_width()/2 - self.shop_button.get_width()/2
        self.shop_button_rect.y = self.start_button_rect.y + self.start_button.get_height() + 50

        # designer la boutique
        self.shuriken_button = pygame.image.load('./assets/buttons/shuriken_button.png')
        self.shuriken_button = pygame.transform.scale(self.shuriken_button, (275,451))
        self.shuriken_button_rect = self.shuriken_button.get_rect()
        self.shuriken_button_rect.x = 20
        self.shuriken_button_rect.y = 100

        self.desert_eagle_button = pygame.image.load('./assets/buttons/desert_eagle_button.png')
        self.desert_eagle_button = pygame.transform.scale(self.desert_eagle_button, (275,451))
        self.desert_eagle_button_rect = self.desert_eagle_button.get_rect()
        self.desert_eagle_button_rect.x = self.shuriken_button_rect.x + self.shuriken_button.get_width() + 20
        self.desert_eagle_button_rect.y = 100

        self.ak47_button = pygame.image.load('./assets/buttons/ak47_button.png')
        self.ak47_button = pygame.transform.scale(self.ak47_button, (275,451))
        self.ak47_button_rect = self.ak47_button.get_rect()
        self.ak47_button_rect.x = self.desert_eagle_button_rect.x + self.desert_eagle_button.get_width() + 20
        self.ak47_button_rect.y = 100

        self.rocket_launcher_button = pygame.image.load('./assets/buttons/rocket_launcher_button.png')
        self.rocket_launcher_button = pygame.transform.scale(self.rocket_launcher_button, (275,451))
        self.rocket_launcher_button_rect = self.rocket_launcher_button.get_rect()
        self.rocket_launcher_button_rect.x = self.ak47_button_rect.x + self.ak47_button.get_width() + 20
        self.rocket_launcher_button_rect.y = 100

        self.back_to_menu_button = pygame.image.load('./assets/buttons/back_to_menu_button.png')
        self.back_to_menu_button = pygame.transform.scale(self.back_to_menu_button, (472,96))
        self.back_to_menu_button_rect = self.back_to_menu_button.get_rect()
        self.back_to_menu_button_rect.x = self.screen.get_width()/2 - self.back_to_menu_button.get_width()/2
        self.back_to_menu_button_rect.y = self.screen.get_height() - self.back_to_menu_button.get_height() - 10
        
    # clear l'écran
    def clear_screen(self):
        pygame.draw.rect(self.screen, (0, 0, 0), [0, 0, self.screen.get_width(), self.screen.get_height()])
    
    # faire apparaitre le menu
    def show_menu(self):
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.shop_button, self.shop_button_rect)

    # charger les joueurs
    def load_players(self):
        self.player_1 = Player(self, "Corentin", "red", 1)
        self.all_players.add(self.player_1)
        self.player_2 = Player(self, "Lucas", "blue", 2)
        self.all_players.add(self.player_2)

    # démarrer le jeu
    def start(self):
        self.type = "Playing"
        self.load_players()

    # arrêter le jeu
    def stop(self):
        self.type = "Menu"

    def show_shop(self):
        self.screen.blit(self.shuriken_button, self.shuriken_button_rect)
        self.screen.blit(self.desert_eagle_button, self.desert_eagle_button_rect)
        self.screen.blit(self.ak47_button, self.ak47_button_rect)
        self.screen.blit(self.rocket_launcher_button, self.rocket_launcher_button_rect)
        self.screen.blit(self.back_to_menu_button, self.back_to_menu_button_rect)

    # update le jeu
    def update(self):
            # afficher les éléments sur l'écran
            pygame.draw.rect(self.screen, (65, 155, 180), [0, 0, self.screen.get_width(), self.screen.get_height() - 40])
            self.group.draw(self.screen)

            # afficher les joueurs
            self.screen.blit(self.player_1.image, self.player_1.rect)
            self.screen.blit(self.player_2.image, self.player_2.rect)

            # afficher les armes
            self.screen.blit(self.player_1.weapon.image, self.player_1.weapon.rect)
            self.screen.blit(self.player_2.weapon.image, self.player_2.weapon.rect)

            for player in self.all_players:
                if player.is_jumping:
                    if player.collide_side(player.top_side):
                        player.is_jumping = False
                    else:
                        if player.jump_counter >= 150:
                            player.rect_y_regulate()
                            player.is_jumping = False
                            if player.collide_side(player.bottom_side):
                                player.jump_counter = 0
                        else:
                            player.jump()
                            player.update()
            
                if not player.collide_side(player.bottom_side) and not player.is_jumping:
                    player.is_falling = True
                elif player.collide_side(player.bottom_side) and player.vertical_speed != player.initial_vertical_speed:
                    player.vertical_speed = player.initial_vertical_speed
                    
                if player.is_falling:
                    if not player.collide_side(player.bottom_side):
                        player.fall()
                        player.update()
                    else:
                        player.rect_y_regulate()
                        player.jump_counter = 0
                        player.is_falling = False
                        player.vertical_speed = player.initial_vertical_speed
                        player.update()

                # update la position des armes
                player.weapon.update_sprite()

                # update la position des projectiles
                for bullet in player.all_bullets:
                    bullet.move()
                    self.screen.blit(bullet.image, bullet.rect)

                # update la vie des joueurs
                player.update_health_bar()

            # gérer les déplacements du premier joueur
            if self.pressed.get(pygame.K_q):
                self.player_1.move_left()
            elif self.pressed.get(pygame.K_d):
                self.player_1.move_right()

            # gérer les déplacements du second joueur
            if self.pressed.get(pygame.K_LEFT):
                self.player_2.move_left()
            elif self.pressed.get(pygame.K_RIGHT):
                self.player_2.move_right()

    def run(self):

        # boucle du jeu
        running = True

        while running:

            if self.type == "Menu":
                self.show_menu()
            elif self.type == "Playing":
                # update le jeu
                self.update()
            elif self.type == "Shop":
                self.show_shop()

            # actualiser l'affichage
            pygame.display.flip()

            # vérifier les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                    if self.type == "Playing":
                        if event.key == pygame.K_z and not self.player_1.is_jumping and not self.player_1.is_falling:
                            self.player_1.is_jumping = True
                        if event.key == pygame.K_UP and not self.player_2.is_jumping and not self.player_2.is_falling:
                            self.player_2.is_jumping = True
                        if event.key == pygame.K_l:
                            self.player_1.equip_weapon("Rocket Launcher")
                        if event.key == pygame.K_s:
                            self.player_1.shoot()
                        if event.key == pygame.K_DOWN:
                            self.player_1.shoot()
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.type == "Menu":
                        if self.start_button_rect.collidepoint(event.pos):
                            self.clear_screen()
                            self.start()
                        elif self.shop_button_rect.collidepoint(event.pos):
                            self.clear_screen()
                            self.type = "Shop"
                    if self.type == "Shop":
                        if self.back_to_menu_button_rect.collidepoint(event.pos):
                            self.clear_screen()
                            self.type = "Menu"
            self.clock.tick(self.FPS)

        pygame.quit()