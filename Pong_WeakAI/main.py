import pygame, sys, random, math

from constant import *
from Ball import Ball
from Paddle import Paddle

class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.sounds_list = {
            'paddle_hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('sounds/wall_hit.wav')
        }

        self.small_font = pygame.font.Font('./font.ttf', 24)
        self.large_font = pygame.font.Font('./font.ttf', 48)
        self.score_font = pygame.font.Font('./font.ttf', 96)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 1
        self.winning_player = 0

        self.player1 = Paddle(self.screen, 30, 90, 15, 60)
        self.player2 = Paddle(self.screen, WIDTH - 30, HEIGHT - 90, 15, 60)

        self.counter_attack =  0
        self.counter_attack_REMAINING = 1

        self.boost_ball =  0
        self.boost_ball_REMAINING = 2


        self.ball = Ball(self.screen, WIDTH/2 - 6, HEIGHT/2 - 6, 12, 12)

        self.game_state = 'start'


    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':
                        self.game_state = 'serve'
                    elif self.game_state == 'serve':
                        self.game_state = 'play'
                    elif self.game_state == 'done':
                        self.game_state = 'serve'
                        self.ball.Reset()

                        self.player1_score=0
                        self.player2_score=0
                        print(self.player1_score)
                        self.boost_ball_REMAINING = 2
                        self.counter_attack_REMAINING = 1

                        if self.winning_player == 1:
                            self.serving_player = 2
                        else:
                            self.serving_player = 1

            if self.boost_ball > 0 and self.game_state == 'play':
                self.ball.dx = self.ball.dx * 3
                self.boost_ball = 0
                self.boost_ball_REMAINING -= 1

            if self.counter_attack > 0 and self.game_state == 'play':
                self.ball.dx = -self.ball.dx * 5
                self.counter_attack = 0
                self.counter_attack_REMAINING -= 1
 

        if self.game_state == 'serve':
            self.ball.dy = random.uniform(-150, 150)
            if self.serving_player == 1:
                self.ball.dx = random.uniform(420, 600)
            else:
                self.ball.dx = -random.uniform(420, 600)

        elif self.game_state == 'play':
            if self.ball.Collides(self.player1):
                self.ball.dx = -self.ball.dx * 1.2  # reflect speed multiplier
                self.ball.rect.x = self.player1.rect.x + 15

                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)

                self.music_channel.play(self.sounds_list['paddle_hit'])

            if self.ball.Collides(self.player2):
                self.ball.dx = -self.ball.dx * 1.2
                self.ball.rect.x = self.player2.rect.x - 12
                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)

                self.music_channel.play(self.sounds_list['paddle_hit'])

            # ball hit top wall
            if self.ball.rect.y <= 0:
                self.ball.rect.y = 0
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            # ball hit bottom wall, 12 represents ball size
            if self.ball.rect.y >= HEIGHT - 12:
                self.ball.rect.y = HEIGHT - 12
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            if self.ball.rect.x < 0:
                self.serving_player = 1
                self.player2_score += 1
                self.music_channel.play(self.sounds_list['score'])
                if self.player2_score==WINNING_SCORE:
                    self.winning_player=2
                    self.game_state='done'
                else:
                    self.game_state = 'serve'
                    self.ball.Reset()

            if self.ball.rect.x > WIDTH:
                self.serving_player = 2
                self.player1_score += 1
                self.music_channel.play(self.sounds_list['score'])
                if self.player1_score==WINNING_SCORE:
                    self.winning_player=1
                    self.game_state='done'
                else:
                    self.game_state = 'serve'
                    self.ball.Reset()

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.player1.dy = -PADDLE_SPEED
        elif key[pygame.K_s]:
            self.player1.dy = PADDLE_SPEED
        elif key[pygame.K_d] and self.boost_ball_REMAINING > 0:
            self.boost_ball = 1
        elif key[pygame.K_a] and self.counter_attack_REMAINING > 0:
            self.counter_attack = 1
        else:
            self.player1.dy = 0

        if self.game_state == 'play':
            self.ball.update(dt)

        self.player1.update(dt)
        self.player2.update(dt)

    def render(self):
        self.screen.fill((40, 45, 52))

        remaining_boosts = self.small_font.render(f"Boosts Left: {self.boost_ball_REMAINING}", False, (255, 255, 255))
        self.screen.blit(remaining_boosts, (50, 20))

        remaining_boosts = self.small_font.render(f"Counter-attack Left: {self.counter_attack_REMAINING}", False, (255, 255, 255))
        self.screen.blit(remaining_boosts, (50, 40))

        if self.game_state == 'start':
            t_welcome = self.small_font.render("Welcome to Pong!", False, (255, 255, 255))
            text_rect = t_welcome.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_welcome, text_rect)

            t_press_enter_begin = self.small_font.render('Players VS Weak AI', False, (255, 255, 255))
            text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_press_enter_begin, text_rect)

            t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, (255, 255, 255))
            text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, HEIGHT - 50))
            self.screen.blit(t_press_enter_begin, text_rect)
        elif self.game_state == 'serve':
            if self.serving_player == 2 :
                t_serve = self.small_font.render("Weak AI" + "'s serve!", False, (255, 255, 255))
                text_rect = t_serve.get_rect(center=(WIDTH/2, 30))
                self.screen.blit(t_serve, text_rect)
            else:
                t_serve = self.small_font.render("player" + "'s serve!", False, (255, 255, 255))
                text_rect = t_serve.get_rect(center=(WIDTH/2, 30))
                self.screen.blit(t_serve, text_rect)

            t_enter_serve = self.small_font.render("Press Enter to serve!", False, (255, 255, 255))
            text_rect = t_enter_serve.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_enter_serve, text_rect)
        elif self.game_state == 'play':
            pass
        elif self.game_state == 'done':
            if self.serving_player == 1 :            
                t_win = self.large_font.render("Weak AI" + "'s wins!", False, (255, 255, 255))
                text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
                self.screen.blit(t_win, text_rect)
            else :
                t_win = self.large_font.render("player" "'s wins!", False, (255, 255, 255))
                text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
                self.screen.blit(t_win, text_rect)                

            t_restart = self.small_font.render("Press Enter to restart", False, (255, 255, 255))
            text_rect = t_restart.get_rect(center=(WIDTH / 2, 70))
            self.screen.blit(t_restart, text_rect)

        self.DisplayScore()

        #right paddle
        self.player2.render()

        #left paddle
        self.player1.render()

        #ball
        self.ball.render()

    def DisplayScore(self):
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (255, 255, 255))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (255, 255, 255))
        self.screen.blit(self.t_p1_score, (WIDTH/2 - 150, HEIGHT/3))
        self.screen.blit(self.t_p2_score, (WIDTH / 2 + 90, HEIGHT / 3))

if __name__ == '__main__':
    main = GameMain()

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("Pong game running with {:d} FPS".format(int(clock.get_fps())))

        # elapsed time from the last call
        dt = clock.tick(MAX_FRAME_RATE)/1000.0

        events = pygame.event.get()
        main.update(dt, events)
        main.render()

        pygame.display.update()
