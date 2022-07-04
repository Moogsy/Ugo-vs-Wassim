import pygame

from player import Player
from monster import Monster
from comet import Comet


class Game:

    def __init__(self):

        # joueur
        self.all_player = pygame.sprite.Group()
        self.player = Player(self)
        self.all_player.add(self.player)
        self.pressed = {}

        self.is_playing = False
        self.score = 0
        self.all_monster = pygame.sprite.Group()
        self.all_comet = pygame.sprite.Group()

    def summon_commet(self):
        self.commet = Comet(self)
        self.all_comet.add(self.commet)

    def summon_monster(self):
        monster = Monster(self)
        self.all_monster.add(monster)

    def movement(self, t):

        if self.pressed.get(pygame.K_q) and self.player.rect.x > -50:
            self.player.move_left()
        if self.pressed.get(pygame.K_d) and self.player.rect.x < 930:
            self.player.move_right()
        if self.pressed.get(pygame.K_z) or self.player.rect.y != 500:
            self.player.jump(t)
            t += 0.03
        return t

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def game_over(self):
        self.player.hp = self.player.max_hp
        self.player.rect.x = 200
        self.is_playing = False
        self.all_monster = pygame.sprite.Group()
        self.all_comet = pygame.sprite.Group()
        self.pressed = {}
        print(self.score)
        self.score = 0

    def start(self):
        self.is_playing = True
        self.summon_monster()
        self.summon_monster()
        self.summon_monster()

        self.summon_commet()
        self.summon_commet()

    def update(self, surface, img):

        surface.blit(img, (0, -200))

        surface.blit(self.player.image, self.player.rect)
        self.player.update_hp_bar(surface)

        # projectile

        self.player.all_projectiles.draw(surface)
        for projectile in self.player.all_projectiles:
            projectile.move()

        # monster
        self.all_monster.draw(surface)
        for monster_el in self.all_monster:
            monster_el.forward()
            monster_el.update_hp_bar(surface)

        # comet

        self.all_comet.draw(surface)
        for comet in self.all_comet:
            comet.move_bot()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True

                if event.key == pygame.K_SPACE:
                    self.player.launch_proj()

            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False
