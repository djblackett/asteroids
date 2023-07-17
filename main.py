import random
import pygame
from pygame.sprite import Sprite, RenderUpdates, spritecollide

class Robot(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load("src/robot.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Rock(Sprite):
    def __init__(self, x, y,  x_velocity, y_velocity):
        Sprite.__init__(self)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.image = pygame.image.load("src/rock.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_x_velocity(self, x):
        self.x_velocity = x

    def set_y_velocity(self,y):
        self.y_velocity = y

    def increment_x(self, increment):
        self.rect.x += increment

    def increment_y(self, increment):
        self.rect.y += increment

    def update(self):
        self.increment_y(self.y_velocity)
        pygame.sprite.Sprite.update(self)


class Game:
    def __init__(self):
        self.points = 0
        self.game_over = False
        self.rock_group = RenderUpdates()

    def new_game(self):
        self.points = 0
        self.game_over = False
        self.rock_group.empty()

pygame.init()


window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Asteroids!")
game_font = pygame.font.SysFont("Arial", 24)

pygame.mixer.init()
pygame.mixer.music.load("src/Chiptune(2).ogg")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

plink = pygame.mixer.Sound("src/plink.wav")
impact = pygame.mixer.Sound("src/impact.wav")
impact.set_volume(0.5)
bonus = pygame.mixer.Sound("src/bonus.wav")
bonus.set_volume(0.4)
rock_sprite = pygame.image.load("src/rock.png")
rock_width = rock_sprite.get_width()
rock_height = rock_sprite.get_height()
robot_height = pygame.image.load("src/robot.png").get_height()
robot = Robot(320, 480 - robot_height)

players = RenderUpdates()

players.add(robot)

start_velocity = 1
rocks = []
clock = pygame.time.Clock()


to_right = False
to_left = False
to_top = False
to_bottom = False

game = Game()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_UP:
                to_top = True
            if event.key == pygame.K_DOWN:
                to_bottom = True
            if event.key == pygame.K_F2 and game.game_over:
                game.new_game()
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
            if event.key == pygame.K_UP:
                to_top = False
            if event.key == pygame.K_DOWN:
                to_bottom = False



    if to_right and robot.rect.x + robot.image.get_width() <= 640 and not game.game_over:
        robot.rect.x += 10
    if to_left and robot.rect.x >= 0 and not game.game_over:
        robot.rect.x -= 10

    if not game.game_over and random.randint(0, 120) == 60:
        x_coordinate = random.randint(0, 640 - rock_width)
        new_rock = Rock(x_coordinate, 0, 0, start_velocity)
        game.rock_group.add(new_rock)

    window.fill((0, 0, 0))


    players.draw(window)
    game.rock_group.draw(window)

    collision_list = spritecollide(robot, game.rock_group, True)

    for rock in collision_list:
        game.points += 1
        if game.points % 10 != 0:
            plink.play()
        else:
            bonus.play()


    for rock in game.rock_group:
        if not game.game_over:
            rock.increment_y(rock.y_velocity)
        if rock.rect.y >= 480 - rock_height:
            game.game_over = True
            pygame.mixer.music.stop()
            impact.play()
            break

    if game.game_over:
        text = game_font.render("Game Over!", True, (255, 0, 0))
        restart = game_font.render("Press F2 to start over", True, (255, 0, 0))
        window.blit(text, (280, 240))
        window.blit(restart, (20, 10,))
        game.rock_group.empty()


    game.rock_group.update()
    text = game_font.render("Points: " + str(game.points), True, (255, 0, 0))
    window.blit(text, (520, 10))

    pygame.display.flip()
    clock.tick(60)
