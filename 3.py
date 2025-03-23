import pygame
import random
import os


# کلاس Target
class Target:
    def __init__(self, x, y, points=5, image_path=None):
        self.x = x
        self.y = y
        self.points = points
        self.active = True

        # دریافت مسیر مطلق فایل
        if image_path is None:
            image_path = os.path.join(os.path.dirname(__file__), "pics", "Target.png")

        # بررسی وجود فایل
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        # بارگذاری و تغییر اندازه تصویر هدف
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (35,35))

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def hit(self):
        if self.active:
            self.active = False
            return self.points
        return 0

    def respawn(self):
        # تغییر موقعیت هدف به صورت تصادفی
        self.x = random.randint(0, 1165)
        self.y = random.randint(120, 615)
        self.active = True

    def check(self, list, game, player):
        # بررسی برخورد تیر با هدف
        for shot in list:
            if self.active and self.x <= shot[0] <= self.x + 35 and self.y <= shot[1] <= self.y + 35:
                if player == 1:
                    game.score1 += self.hit()  # افزایش امتیاز بازیکن ۱
                elif player == 2:
                    game.score2 += self.hit()  # افزایش امتیاز بازیکن ۲
                self.respawn()  # ایجاد مجدد هدف



class Shoot:
    
    def __init__(self,screen):
        self.screen = screen
        # موقعیت اولیه تیر
        self.shot_x = random.randint(3, 1194)
        self.shot_y = random.randint(123, 644)
        self.shot_speed = 3
        # لیست موقعیت تیرها
        self.shots = []
        #تیر لحظه ای
        self.shotsl = []

        
    def shooting1(self,time,bullets):
        if time <= 0 :
            return time
        if bullets <= 0 :
            return
        # حرکت موقعیت تیر بعدی با کلیدهای جهت‌دار
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.shot_y -= self.shot_speed
            if self.shot_y<123 :
                self.shot_y=123
        if keys[pygame.K_s]:
            self.shot_y += self.shot_speed
            if self.shot_y>644 :
                self.shot_y=644
        if keys[pygame.K_a]:
            self.shot_x -= self.shot_speed
            if self.shot_x<3 :
                self.shot_x=3
        if keys[pygame.K_d]:
            self.shot_x += self.shot_speed
            if self.shot_x>1194 :
                self.shot_x=1194

        # شلیک تیر با کلید اسپیس
        if keys[pygame.K_SPACE]:
            # اضافه کردن موقعیت تیر به لیست
            self.shots.append((self.shot_x, self.shot_y))
            # اضافه کردن موقعیت تیر به تیر لحظه ای
            self.shotsl = []
            self.shotsl.append((self.shot_x, self.shot_y))


    def shooting2(self,time,bullets):
        if time <= 0 :
            return 
        if bullets <= 0 :
            return
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
        if keys[pygame.K_RETURN]:
            # اضافه کردن موقعیت تیر به لیست
            self.shots.append((self.shot_x, self.shot_y))
            # اضافه کردن موقعیت تیر به تیر لحظه ای
            self.shotsl = []
            self.shotsl.append((self.shot_x, self.shot_y))


    
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
    def display_player_info(self,current_time,player1_bullets,player2_bullets,score1,score2):
        seconds = current_time // 1000  # تبدیل به ثانیه
        time1 = 12 - seconds
        time2 = 120 - seconds
        if time1 <= 0 :
            time1 = 0
        if time2 <= 0 :
            time2 = 0

        # نمایش اطلاعات بازیکن اول (گوشه بالا سمت چپ)
        player1_info = [
            f"player1 : {self.player1_name}",
            f"time : {time1} seconds ",
            f"bullets : {player1_bullets}",
            f"score : {score1}"
        ]
        for i, line in enumerate(player1_info):
            text = self.font.render(line, True, (1,87,155))
            self.screen.blit(text, (20, 20 + i * 30))  # فاصله 30 پیکسل بین خطوط
 
        # نمایش اطلاعات بازیکن دوم (گوشه بالا سمت راست)
        player2_info = [
            f"player2 : {self.player2_name}",
            f"time : {time2} seconds ",
            f"bullets : {player2_bullets}",
            f"score : {score2}"
        ]
        for i, line in enumerate(player2_info):
            text = self.font.render(line, True, (25,25,112))
            self.screen.blit(text, (980, 20 + i * 30))  # تنظیم موقعیت متن برای پنجره بزرگ‌تر

        return time1 , time2




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
        self.screen.fill((173, 216, 230))  # پاک کردن صفحه با رنگ آبی روشن

        # تعیین برنده یا تساوی
        if score1 > score2:
            result_text = f"{player1_name} wins!"
        elif score2 > score1:
            result_text = f"{player2_name} wins!"
        else:
            result_text = "Player 1 and 2 tied."

        # نمایش نتیجه
        result_surface = self.font.render(result_text, True, (0, 0, 0))
        self.screen.blit(result_surface, (500, 300))

        # نمایش امتیازها
        score_text = f"{player1_name}: {score1}  |  {player2_name}: {score2}"
        score_surface = self.font.render(score_text, True, (0, 0, 0))
        self.screen.blit(score_surface, (450, 350))

        pygame.display.flip()  # به‌روزرسانی صفحه

        # منتظر ماندن برای کلیک کاربر
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # اگر کاربر کلیدی فشار داد، بازی بسته شود
                    waiting = False

    def run(self):
        # دریافت نام بازیکنان
        get_inputs = Input(self.screen)
        get_inputs.get_player_names()
        self.start_time = pygame.time.get_ticks()

        #شلیک کردن
        shoot1 = Shoot(self.screen)
        shoot2 = Shoot(self.screen)
  
        # ایجاد سه هدف
        target1 = Target(random.randint(0, 1165), random.randint(120, 615))
        target2 = Target(random.randint(0, 1165), random.randint(120, 615))
        target3 = Target(random.randint(0, 1165), random.randint(120, 615))

        # حلقه اصلی بازی
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:  #  بررسی رها شدن کلید اسپیس یا اینتر
                    if event.key == pygame.K_SPACE:
                        self.space_pressed = False  # کلید اسپیس رها شده است
                    elif event.key == pygame.K_RETURN:
                        self.enter_pressed = False  # کلید اینتر رها شده است


            # پاک کردن صفحه
            self.screen.fill((173, 216, 230))

            
            # نمایش اطلاعات بازیکنان
            current_time = pygame.time.get_ticks() - self.start_time
            time1 , time2 = get_inputs.display_player_info(current_time,self.player1_bullets,self.player2_bullets,self.score1,self.score2)
            
 
            # رسم هدف
            target1.draw(self.screen)
            target2.draw(self.screen)
            target3.draw(self.screen)

            #تیراندازی
            shoot1.shooting1(time1,self.player1_bullets)
            if pygame.key.get_pressed()[pygame.K_SPACE] and not self.space_pressed :
                self.player1_bullets -= 1 
                self.space_pressed = True
                
            shoot2.shooting2(time2,self.player2_bullets)
            if pygame.key.get_pressed()[pygame.K_RETURN] and not self.enter_pressed :
                self.player2_bullets -= 1
                self.enter_pressed = True

            if self.player1_bullets <= 0 :
                self.player1_bullets = 0
                
            if self.player2_bullets <= 0 :
                self.player2_bullets = 0

            
            # بررسی برخورد تیر با هدف
            target1.check(shoot1.shotsl,self,1)
            target1.check(shoot2.shots,self,2)
            target2.check(shoot1.shotsl,self,1)
            target2.check(shoot2.shotsl,self,2)
            target3.check(shoot1.shotsl,self,1)
            target3.check(shoot2.shotsl,self,2)
            

            # نمایش تیرهای هر دو بازیکن
            for shot in shoot1.shots:
                pygame.draw.circle(self.screen, (1,87,155), shot, 3) 
            for shot in shoot2.shots:
                pygame.draw.circle(self.screen, (25,25,112), shot, 3) 

            
        # بررسی پایان بازی
        if (self.player1_bullets <= 0 and self.player2_bullets <= 0) or (time1 <= 0 and time2 <= 0):
            self.display_end_screen(self.score1, self.score2, get_inputs.player1_name, get_inputs.player2_name)
            self.running = False  # پایان بازی


            # به‌روزرسانی صفحه
            pygame.display.flip()
            self.clock.tick(60) # محدود کردن فریم‌ریت به ۶۰ فریم بر ثانیه

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()