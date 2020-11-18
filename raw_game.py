import pygame
import os
import random

pygame.init()

# global constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DEAD_DINO = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))
DINO_RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
DINO_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DINO_DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DINO_DUCKING
        self.run_img = DINO_RUNNING
        self.jump_img = DINO_JUMPING
        self.dead_img = DEAD_DINO

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS


    def update(self, user_input):
        if (self.dino_duck):
            self.duck()
        if (self.dino_run):
            self.run()
        if (self.dino_jump):
            self.jump()
        
        if (self.step_index >= 10):
            self.step_index = 0
        
        if ((user_input[pygame.K_UP]) and (not (self.dino_jump))):
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif ((user_input[pygame.K_DOWN]) and (not (self.dino_jump))):
            self.dino_jump = False
            self.dino_duck = True
            self.dino_run = False
        elif (not ((self.dino_jump) or  (user_input[pygame.K_DOWN]))):
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img
        if (self.dino_jump):
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if (self.jump_vel < (-self.JUMP_VEL)):
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def die(self):
        self.dino_duck = False
        self.dino_run = False
        self.dino_jump = False
        self.image = self.dead_img

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if (self.x < -self.width):
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if (self.rect.x < (-self.rect.width)):
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    game_is_running = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    
    def score():
        global points, game_speed
        points += 1
        if (points % 100 == 0):  # increment the speed every 100points milestone
            game_speed += 1
        
        
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        SCREEN.blit(text, text_rect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
        if (x_pos_bg <= -image_width):
            SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while game_is_running:
        for event in pygame.event.get():  # iterate trough all pygame events
            if (event.type == pygame.QUIT):
                game_is_running = False

        SCREEN.fill((255, 255, 255))  # fills the screen with white color
        user_input = pygame.key.get_pressed()

        player.draw(SCREEN)  # draws the dino on the screen
        player.update(user_input)


        if (len(obstacles) == 0):
            choice = random.randint(0,1)

            if (choice == 0):
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif (choice == 1):
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if (player.dino_rect.colliderect(obstacle.rect)):
                player.die()
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)


        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    game_is_running = True
    while (game_is_running):
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if (death_count == 0):
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your score: " + str(points), True, (0, 0, 0))
            score_rect = score.get_rect()
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, score_rect)
        
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(DINO_RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                game_is_running = False
                pygame.quit()
            if (event.type == pygame.KEYDOWN):
                main()


menu(death_count=0)
