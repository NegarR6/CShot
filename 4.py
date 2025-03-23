import pygame
import random
import os

class Target:
    def __init__(self, x, y, points=5, image_path=None):
        self.x = x
        self.y = y
        self.points = points
        self.active = True

        if image_path is None:
            image_path = os.path.join(os.path.dirname(__file__), "pics", "Target.png")

        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (35, 35))

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def hit(self):
        if self.active:
            self.active = False
            return self.points
        return 0

    def respawn(self):
        self.x = random.randint(0, 1165)
        self.y = random.randint(120, 615)
        self.active = True

    def check_collision(self, shot):
        return self.x <= shot[0] <= self.x + 35 and self.y <= shot[1] <= self.y + 35

class Shoot:
    def __init__(self, screen):
        self.screen = screen
        self.shot_x = random.randint(3, 1194)
        self.shot_y = random.randint(123, 644)
        self.shot_speed = 3
        self.shots = []
        self.shotsl = []

    def shooting(self, keys, up_key, down_key, left_key, right_key, shoot_key, time, bullets):
        if time <= 0 or bullets <= 0:
            return

        if keys[up_key]:
            self.shot_y -= self.shot_speed
            if self.shot_y < 123:
                self.shot_y = 123
        if keys[down_key]:
            self.shot_y += self.shot_speed
            if self.shot_y > 644:
                self.shot_y = 644
        if keys[left_key]:
            self.shot_x -= self.shot_speed
            if self.shot_x < 3:
                self.shot_x = 3
        if keys[right_key]:
            self.shot_x += self.shot_speed
            if self.shot_x > 1194:
                self.shot_x = 1194

        if keys[shoot_key]:
            self.shots.append((self.shot_x, self.shot_y))
            self.shotsl = [(self.shot_x, self.shot_y)]

class Input:
    def __init__(self, screen):
        self.player1_name = ""
        self.player2_name = ""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_input_box(self, text, x, y, active):
        input_box = pygame.Rect(x, y, 200, 40)
        color = (1, 87, 155) if active else (66, 165, 245)
        pygame.draw.rect(self.screen, color, input_box, 2)
        text_surface = self.font.render(text, True, (26, 35, 126))
        self.screen.blit(text_surface, (x + 5, y + 5))
        return input_box

    def get_player_names(self):
        player1_name = ""
        player2_name = ""
        active1 = True
        active2 = False
        error_message = ""  # پیام خطا

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_RETURN:
                            if len(player1_name) > 8:  # بررسی طول نام بازیکن اول
                                error_message = "Player 1 name must be 8 characters or less!"
                            else:
                                active1 = False
                                active2 = True
                                error_message = ""  # پاک کردن پیام خطا
                        elif event.key == pygame.K_BACKSPACE:
                            player1_name = player1_name[:-1]
                        else:
                            if len(player1_name) < 8:  # محدودیت ۸ کاراکتر
                                player1_name += event.unicode
                    elif active2:
                        if event.key == pygame.K_RETURN:
                            if len(player2_name) > 8:  # بررسی طول نام بازیکن دوم
                                error_message = "Player 2 name must be 8 characters or less!"
                            else:
                                running = False
                                error_message = ""  # پاک کردن پیام خطا
                        elif event.key == pygame.K_BACKSPACE:
                            player2_name = player2_name[:-1]
                        else:
                            if len(player2_name) < 8:  # محدودیت ۸ کاراکتر
                                player2_name += event.unicode

            # پاک کردن صفحه و رسم جعبه‌های ورودی
            self.screen.fill((173, 216, 230))
            self.draw_input_box(player1_name, 500, 250, active1)
            self.draw_input_box(player2_name, 500, 350, active2)

            # نمایش پیام خطا
            if error_message:
                error_surface = self.font.render(error_message, True, (255, 0, 0))  # رنگ قرمز برای خطا
                self.screen.blit(error_surface, (400, 450))  # موقعیت نمایش پیام خطا

            pygame.display.flip()

        self.player1_name = player1_name
        self.player2_name = player2_name

    def display_player_info(self, current_time, player1_bullets, player2_bullets, score1, score2):
        seconds = current_time // 1000
        time1 = 120 - seconds
        time2 = 120 - seconds
        if time1 <= 0:
            time1 = 0
        if time2 <= 0:
            time2 = 0

        player1_info = [
            f"player1 : {self.player1_name}",
            f"time : {time1} seconds ",
            f"bullets : {player1_bullets}",
            f"score : {score1}"
        ]
        for i, line in enumerate(player1_info):
            text = self.font.render(line, True, (1, 87, 155))
            self.screen.blit(text, (20, 20 + i * 30))

        player2_info = [
            f"player2 : {self.player2_name}",
            f"time : {time2} seconds ",
            f"bullets : {player2_bullets}",
            f"score : {score2}"
        ]
        for i, line in enumerate(player2_info):
            text = self.font.render(line, True, (25, 25, 112))
            self.screen.blit(text, (980, 20 + i * 30))

        return time1, time2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 650))
        pygame.display.set_caption("CSshot Game")
        self.running = True
        self.clock = pygame.time.Clock()
        self.player1_bullets = 20
        self.player2_bullets = 20
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 36)
        self.space_pressed = False
        self.enter_pressed = False

    def display_end_screen(self, score1, score2, player1_name, player2_name):
        self.screen.fill((173, 216, 230))

        if score1 > score2:
            result_text = f"{player1_name} wins!"
        elif score2 > score1:
            result_text = f"{player2_name} wins!"
        else:
            result_text = "Player 1 and 2 tied."

        result_surface = self.font.render(result_text, True, (0, 0, 0))
        self.screen.blit(result_surface, (500, 300))

        score_text = f"{player1_name}: {score1}  |  {player2_name}: {score2}"
        score_surface = self.font.render(score_text, True, (0, 0, 0))
        self.screen.blit(score_surface, (450, 350))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run(self):
        get_inputs = Input(self.screen)
        get_inputs.get_player_names()
        self.start_time = pygame.time.get_ticks()

        shoot1 = Shoot(self.screen)
        shoot2 = Shoot(self.screen)

        target1 = Target(random.randint(0, 1165), random.randint(120, 615))
        target2 = Target(random.randint(0, 1165), random.randint(120, 615))
        target3 = Target(random.randint(0, 1165), random.randint(120, 615))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.space_pressed = False
                    elif event.key == pygame.K_RETURN:
                        self.enter_pressed = False

            self.screen.fill((173, 216, 230))

            current_time = pygame.time.get_ticks() - self.start_time
            time1, time2 = get_inputs.display_player_info(current_time, self.player1_bullets, self.player2_bullets, self.score1, self.score2)

            target1.draw(self.screen)
            target2.draw(self.screen)
            target3.draw(self.screen)

            keys = pygame.key.get_pressed()
            shoot1.shooting(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE, time1, self.player1_bullets)
            if keys[pygame.K_SPACE] and not self.space_pressed:
                self.player1_bullets -= 1
                self.space_pressed = True

            shoot2.shooting(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, time2, self.player2_bullets)
            if keys[pygame.K_RETURN] and not self.enter_pressed:
                self.player2_bullets -= 1
                self.enter_pressed = True

            if self.player1_bullets <= 0:
                self.player1_bullets = 0
            if self.player2_bullets <= 0:
                self.player2_bullets = 0

            for shot in shoot1.shotsl:
                if target1.check_collision(shot):
                    self.score1 += target1.hit()
                    target1.respawn()
                if target2.check_collision(shot):
                    self.score1 += target2.hit()
                    target2.respawn()
                if target3.check_collision(shot):
                    self.score1 += target3.hit()
                    target3.respawn()

            for shot in shoot2.shotsl:
                if target1.check_collision(shot):
                    self.score2 += target1.hit()
                    target1.respawn()
                if target2.check_collision(shot):
                    self.score2 += target2.hit()
                    target2.respawn()
                if target3.check_collision(shot):
                    self.score2 += target3.hit()
                    target3.respawn()

            for shot in shoot1.shots:
                pygame.draw.circle(self.screen, (1, 87, 155), shot, 3)
            for shot in shoot2.shots:
                pygame.draw.circle(self.screen, (25, 25, 112), shot, 3)

            if (self.player1_bullets <= 0 and self.player2_bullets <= 0) or (time1 <= 0 and time2 <= 0):
                self.display_end_screen(self.score1, self.score2, get_inputs.player1_name, get_inputs.player2_name)
                self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()     