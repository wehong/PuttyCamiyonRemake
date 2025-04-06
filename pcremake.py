import pygame
import random
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.size = (self.image.get_width(), self.image.get_height())
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
    def reloc(self, rx, ry):
        self.x = rx
        self.y = ry
        self.vy = -3

    def move_lef(self):
        self.x -= 4
        if self.x <= 0:
            self.x = 0
    def move_right(self):
        self.x += 4
        if self.x > 640:
            self.x = 640
    def bounce_up(self):
        self.vy = -150
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
        
    def set_crash_image(self):
        self.image = pygame.image.load("crash.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.size = (self.image.get_width(), self.image.get_height())
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_normal_image(self):
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.size = (self.image.get_width(), self.image.get_height())
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(self.x, self.y))

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

    def reloc(self, rx, ry):
        self.x = rx
        self.y = ry
        self.vx = -1*random.randrange(3, 8)

def main():

    pygame.init()
    pygame.font.init()
    screen_width = 640
    screen_height = 480
    pygame.display.set_icon(pygame.image.load("player.png"))
    pygame.display.set_caption("Putty Camiyon Remake")
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    score = hiscore = 0
    sc_tick = 0
    sc_font = pygame.font.Font(None, 30)
    sc_text = sc_font.render(f'Score: {score}     Hi-Score: {hiscore}', True, (200, 200, 100))
    sc_text_rect = sc_text.get_rect(center = (320, 20))

    go_font = pygame.font.Font(None, 36)
    go_text = go_font.render('Game Over', True, (255, 10, 10))
    go_text_rect = go_text.get_rect(center = (320, 240))

    player = Player((180, 80))
    player_sprite = pygame.sprite.Group(player)

    balloons = [
        Balloon((600, 190)),
        Balloon((600, 280)),
        Balloon((600, 400))
    ]
    balloon_group = pygame.sprite.RenderPlain(*balloons)
    
    bounce_sound = pygame.mixer.Sound("bounce.ogg")
    crash_sound = pygame.mixer.Sound("crash.ogg")

    while True:

        play_again = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play_again = False
                    running = False
                    pygame.quit()
                    sys.exit()
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                player.move_lef()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if player.check_crash() == True:
                player.set_crash_image()
                crash_sound.play()
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
            sc_tick += 1
            if sc_tick == 60:
                score += 1
                sc_tick = 0

            screen.fill("black")
            pygame.draw.line(screen, (0,255, 0), [0, 475], [640,475], 10)
            player_sprite.draw(screen)
            balloon_group.draw(screen)
            sc_text = sc_font.render(f'Score: {score}     Hi-Score: {hiscore}', True, (200, 200, 100))
            screen.blit(sc_text, sc_text_rect) #(220, 10))

            pygame.display.flip()
            
            clock.tick(60)
        
        screen.blit(go_text, go_text_rect)
        pygame.display.flip()
        while play_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    play_again = False
        if score > hiscore:
            hiscore = score
        
        score = 0    
        player.set_normal_image()
        player.reloc(180, 80)
        balloons[0].reloc(600, 190)
        balloons[1].reloc(600, 280)
        balloons[2].reloc(500, 400)


if __name__ == '__main__':
    main()
