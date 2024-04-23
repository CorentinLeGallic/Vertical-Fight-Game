from msilib.schema import Class
import pygame
import pytmx
import pyscroll

from objects.player import Player

class Game:
    
    def __init__(self):

        # gérer les FPS
        self.clock = pygame.time.Clock()
        self.FPS = 50

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

        self.is_playing = False

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    # designer le menu
    def show_menu(self):

        self.start_button = pygame.image.load('./assets/buttons/start_button.png')
        self.start_button = pygame.transform.scale(self.start_button, (472,96))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = self.screen.get_width()/2 - self.start_button.get_width()/2
        self.start_button_rect.y = 300

        self.screen.blit(self.start_button, self.start_button_rect)

    # charger les joueurs
    def load_players(self):
        self.player_1 = Player(self, "Corentin", "red", 1)
        self.all_players.add(self.player_1)
        self.player_2 = Player(self, "Lucas", "blue", 2)
        self.all_players.add(self.player_2)

    # démarrer le jeu
    def start(self):
        self.is_playing = True
        self.load_players()

    # arrêter le jeu
    def stop(self):
        self.is_playing = False

    # update le jeu
    def update(self):
            # afficher les éléments sur l'écran
            pygame.draw.rect(self.screen, (65, 155, 180), [0, 0, self.screen.get_width(), self.screen.get_height() - 40])
            self.group.draw(self.screen)

            # afficher les joueurs
            self.screen.blit(self.player_1.image, self.player_1.rect)
            self.screen.blit(self.player_2.image, self.player_2.rect)

            for player in self.all_players:
                if player.is_jumping:
                    if player.collide_top():
                        # print("Collide top")
                        player.is_jumping = False
                        player.jump_counter = 0
                        player.is_falling = True
                    else:
                        if player.jump_counter >= 96:
                            player.rect.y += player.jump_counter - 96
                            player.is_jumping = False
                            player.jump_counter = 0
                        else:
                            player.jump()
                            player.update()
            
                if not player.collide_bottom() and not player.is_jumping:
                    player.is_falling = True
                    
                if player.is_falling: 
                    print(player.collide_bottom())
                    if not player.collide_bottom():
                        player.fall()
                        player.update()
                        if player.fall_counter >= 48:
                            player.rect.y -= player.fall_counter - 48
                            player.fall_counter = 0
                    else:
                        player.fall_counter = 0
                        player.is_falling = False

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

            if self.is_playing:
                # update le jeu
                self.update()
            else:
                self.show_menu()

            # actualiser l'affichage
            pygame.display.flip()

            # vérifier les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                    if event.key == pygame.K_z and self.is_playing and not self.player_1.is_jumping and not self.player_1.is_falling:
                        self.player_1.is_jumping = True
                    if event.key == pygame.K_UP and self.is_playing and not self.player_2.is_jumping and not self.player_2.is_falling:
                        self.player_2.is_jumping = True
                        print("Player 2 jump")
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    if self.start_button_rect.collidepoint(event.pos) and not self.is_playing:
                        self.start()
            self.clock.tick(self.FPS)

        pygame.quit()