import pygame
import random

#class player info bulet time score
class Shoot:
    
    def __init__(self,screen,color):
        self.screen = screen
        self.color = color
        # موقعیت اولیه تیر
        self.shot_x = random.randint(3, 1194)
        self.shot_y = random.randint(123, 644)
        self.shot_speed = 3
        # لیست موقعیت تیرها
        self.shots = []

    def shooting(self):
        # حرکت موقعیت تیر بعدی با کلیدهای جهت‌دار
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.shot_y -= self.shot_speed
            if self.shot_y<123 :
                self.shot_y=123
        if keys[pygame.K_DOWN]:
            self.shot_y += self.shot_speed
            if self.shot_y>644 :
                self.shot_y=644
        if keys[pygame.K_LEFT]:
            self.shot_x -= self.shot_speed
            if self.shot_x<3 :
                self.shot_x=3
        if keys[pygame.K_RIGHT]:
            self.shot_x += self.shot_speed
            if self.shot_x>1194 :
                self.shot_x=1194

        # شلیک تیر با کلید اسپیس
        if keys[pygame.K_SPACE]:
            # اضافه کردن موقعیت تیر به لیست
            self.shots.append((self.shot_x, self.shot_y))

    
class Input:
    def __init__(self,screen):
        self.player1_name = ""
        self.player2_name = ""
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



    #########"""نمایش اطلاعات بازیکنان"""
    def display_player_info(self,current_time,player1_bullets,player2_bullets):
        seconds = current_time // 1000  # تبدیل به ثانیه

        # نمایش اطلاعات بازیکن اول (گوشه بالا سمت چپ)
        player1_info = [
            f"player1 : {self.player1_name}",
            f"time : {seconds} seconds ",
            f"bullets : {player1_bullets}"
        ]
        for i, line in enumerate(player1_info):
            text = self.font.render(line, True, (1,87,155))
            self.screen.blit(text, (20, 20 + i * 30))  # فاصله 30 پیکسل بین خطوط
 
        # نمایش اطلاعات بازیکن دوم (گوشه بالا سمت راست)
        player2_info = [
            f"player2 : {self.player2_name}",
            f"time : {seconds} seconds ",
            f"bullets : {player2_bullets}"
        ]
        for i, line in enumerate(player2_info):
            text = self.font.render(line, True, (25,25,112))
            self.screen.blit(text, (980, 20 + i * 30))  # تنظیم موقعیت متن برای پنجره بزرگ‌تر


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 650)) 
        pygame.display.set_caption("CSshot Game")
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_player = 2
        self.space_pressed = False
        self.player1_bullets = 20
        self.player2_bullets = 21

    def run(self):
        # دریافت نام بازیکنان
        get_inputs = Input(self.screen)
        get_inputs.get_player_names()
        self.start_time = pygame.time.get_ticks()

        #شلیک کردن
        shoot1 = Shoot(self.screen,(250,0,0))
        shoot2 = Shoot(self.screen,(0,0,0))

        # حلقه اصلی بازی
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:  # بررسی رها شدن کلید اسپیس
                    if event.key == pygame.K_SPACE:
                        self.space_pressed = False  # کلید اسپیس رها شده است

            # پاک کردن صفحه
            self.screen.fill((173, 216, 230))

            # نمایش اطلاعات بازیکنان
            current_time = pygame.time.get_ticks() - self.start_time
            get_inputs.display_player_info(current_time,self.player1_bullets,self.player2_bullets)

            #تیراندازی
            if self.current_player==1 :
                shoot1.shooting()
                if pygame.key.get_pressed()[pygame.K_SPACE] and not self.space_pressed:
                    self.current_player = 2  # تعویض نوبت به بازیکن 2
                    self.player1_bullets -= 1
                    self.space_pressed = True
            else :
                shoot2.shooting()
                if pygame.key.get_pressed()[pygame.K_SPACE] and not self.space_pressed:
                    self.current_player = 1  # تعویض نوبت به بازیکن 1
                    self.player2_bullets -= 1
                    self.space_pressed = True

            # نمایش تیرهای هر دو بازیکن
            for shot in shoot1.shots:
                pygame.draw.circle(self.screen, (1,87,155), shot, 3) 
            for shot in shoot2.shots:
                pygame.draw.circle(self.screen, (25,25,112), shot, 3) 


            # به‌روزرسانی صفحه
            pygame.display.flip()
            self.clock.tick(60) # محدود کردن فریم‌ریت به ۶۰ فریم بر ثانیه

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()