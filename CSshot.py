import pygame

class Input:
    def __init__(self,screen):
        self.player1_name = ""
        self.player2_name = ""
        self.player1_bullets = 10
        self.player2_bullets = 10
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        
    #تابع برای رسم جعبه ورودی متن
    def draw_input_box(self, text, x, y, active):
        input_box = pygame.Rect(x, y, 200, 40)
        color = (1, 87, 155) if active else (66, 165, 245)
        pygame.draw.rect(self.screen, color, input_box, 2)
        text_surface = self.font.render(text, True, (26, 35, 126))
        self.screen.blit(text_surface, (x + 5, y + 5))
        return input_box

    #دریافت نام بازیکنان به‌صورت گرافیکی
    def get_player_names(self):
        player1_name = ""
        player2_name = ""
        active1 = True
        active2 = False
        input_box1 = self.draw_input_box(player1_name, 500, 250, active1)  # تنظیم موقعیت جعبه‌ها
        input_box2 = self.draw_input_box(player2_name, 500, 350, active2)  # تنظیم موقعیت جعبه‌ها

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_RETURN:
                            active1 = False
                            active2 = True
                        elif event.key == pygame.K_BACKSPACE:
                            player1_name = player1_name[:-1]
                        else:
                            player1_name += event.unicode
                    elif active2:
                        if event.key == pygame.K_RETURN:
                            running = False
                        elif event.key == pygame.K_BACKSPACE:
                            player2_name = player2_name[:-1]
                        else:
                            player2_name += event.unicode

            self.screen.fill((173, 216, 230))
            self.draw_input_box(player1_name, 500, 250, active1)
            self.draw_input_box(player2_name, 500, 350, active2)
            pygame.display.flip()

        self.player1_name = player1_name
        self.player2_name = player2_name



    ####################"""نمایش اطلاعات بازیکنان"""
    def display_player_info(self,current_time):
        seconds = current_time // 1000  # تبدیل به ثانیه

        # نمایش اطلاعات بازیکن اول (گوشه بالا سمت چپ)
        player1_info = [
            f"player1 : {self.player1_name}",
            f"time : {seconds} seconds ",
            f"bullets : {self.player1_bullets}"
        ]
        for i, line in enumerate(player1_info):
            text = self.font.render(line, True, (1, 87, 155))
            self.screen.blit(text, (50, 50 + i * 30))  # فاصله 30 پیکسل بین خطوط

        # نمایش اطلاعات بازیکن دوم (گوشه بالا سمت راست)
        player2_info = [
            f"player2 : {self.player2_name}",
            f"time : {seconds} seconds ",
            f"bullets : {self.player2_bullets}"
        ]
        for i, line in enumerate(player2_info):
            text = self.font.render(line, True, (25,25,112))
            self.screen.blit(text, (900, 50 + i * 30))  # تنظیم موقعیت متن برای پنجره بزرگ‌تر



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700)) 
        pygame.display.set_caption("CSshot Game")
        self.running = True

    def run(self):
        # دریافت نام بازیکنان
        get_inputs = Input(self.screen)
        get_inputs.get_player_names()
        self.start_time = pygame.time.get_ticks()

        # حلقه اصلی بازی
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # پاک کردن صفحه
            self.screen.fill((173, 216, 230))

            # نمایش اطلاعات بازیکنان
            current_time = pygame.time.get_ticks() - self.start_time
            get_inputs.display_player_info(current_time)

            # به‌روزرسانی صفحه
            pygame.display.flip()

        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()