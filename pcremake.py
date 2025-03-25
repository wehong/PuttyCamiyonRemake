import pygame
import random

pygame.init()
screen_width = 640
screen_height = 480
pygame.display.set_caption("Putty Camiyon Remake")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.size = (self.image.get_width()*1.5, self.image.get_height()*1.5)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=position)
        
        (self.x, self.y) = position
        self.vy = -3
       
    def update(self):
        self.vy += 3
        self.y = self.y + self.vy/30
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

    def move_lef(self):
        self.x -= 4
        if self.x <= 0:
            self.x = 0
    def move_right(self):
        self.x += 4
        if self.x > 640:
            self.x = 640
    def bounce_up(self):
        self.vy = -130
    def bounce_left(self):
        self.vy = -100
        self.x -= 20
        if self.x <= 0:
            self.x = 0
    def bounce_right(self):
        self.vy = -100
        self.x += 20
        if self.x >= 640:
            self.x = 640
    def bounce_down(self):
        self.vy -= 2
        self.y += 3

    def check_crash(self):
        if self.y >= 430:
            return True
        else:
            return False

class Balloon(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("balloon.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.size = (self.image.get_width(), self.image.get_height())
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=position)
        
        (self.x, self.y) = position
        self.vx = -1*random.randrange(3, 8)

    def update(self):
        self.x += self.vx
        if self.x <= -30:
            self.x = 670
            self.vx = -1*random.randrange(3, 8)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)#self.position

def main():

    running = True
    g_over = True

    player = Player((180, 80))
    player_sprite = pygame.sprite.Group(player)

    balloons = [
        Balloon((600, 190)),
        Balloon((600, 280)),
        Balloon((600, 400))
    ]
    balloon_group = pygame.sprite.RenderPlain(*balloons)
    
    bounce_sound = pygame.mixer.Sound("bounce.ogg" )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            player.move_lef()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if player.check_crash() == True:
            running = False

        collisions = pygame.sprite.spritecollide(player, balloon_group, False)
        if collisions:
            for ball in collisions:
                diff_x = ball.x - player.get_x()
                diff_y = ball.y - player.get_y()
                if diff_y >=0 and diff_x > 20:
                    player.bounce_left()
                    bounce_sound.play()
                elif diff_y >=0 and diff_x < -20:
                    player.bounce_right()
                    bounce_sound.play()
                elif diff_y >= 0:
                    player.bounce_up()
                    bounce_sound.play()
                else:
                    player.bounce_down()
            collisions = None

        player_sprite.update()
        balloon_group.update()

        screen.fill("black")
        pygame.draw.line(screen, (0,255, 0), [0, 475], [640,475], 10)
        player_sprite.draw(screen)
        balloon_group.draw(screen)

        pygame.display.flip()
        
        clock.tick(60)

if __name__ == '__main__':
    main()
