import math
import pygame
import random
import os

class Explosion: 
    # کلاس انفجار   وقتی به تارگت شلیک میشه انفجار رخ میده
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = [SmokeParticle(x, y) for _ in range(15)]  # 15 ذره دود
        self.lifetime = 1.5  # مدت نمایش کل انفجار
        self.current_time = 0
    
    def update(self, dt):
        # اپدیت وضع انفجار در هر فریم
        self.current_time += dt
        for p in self.particles[:]:#اپدیت ذره ها
            if not p.update(dt): #عمر ذره اگه تموم شد
                self.particles.remove(p) #حذف ذره
        return self.current_time < self.lifetime or len(self.particles) > 0 # انفجار فعاله یا نه

    def draw(self, screen): #کشیدن انفجار
        for p in self.particles:
            p.draw(screen)


class MuzzleFlash: #کلاس جرقه دهانه تفنگ - وقتی شلیک می‌کنیم این جرقه میاد
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # اندازه اولیه جرقه
        self.max_radius = 20  # حداکثر اندازه
        self.growth_speed = 2  # سرعت بزرگ شدن
        self.alpha = 200  # شفافیت (۰ تا ۲۵۵)
        self.fade_speed = 8  # سرعت محو شدن
        self.active = True
        self.color = (255, 200, 0)  # رنگ نارنجی-طلایی

    def update(self):
        # بزرگ شدن جرقه
        if self.radius < self.max_radius:
            self.radius += self.growth_speed
        
        # محو شدن تدریجی
        self.alpha = max(0, self.alpha - self.fade_speed)
        if self.alpha <= 0:
            self.active = False

    def draw(self, screen):
        if self.active:
            # ایجاد سطح شفاف برای جرقه
            flash_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            
            # رسم دایره با گرادیان شفافیت (از مرکز به بیرون)
            for r in range(self.radius, 0, -1):
                alpha = int(self.alpha * (r / self.radius))
                color = (*self.color[:3], alpha)
                pygame.draw.circle(flash_surface, color, (self.radius, self.radius), r)
            
            screen.blit(flash_surface, (self.x - self.radius, self.y - self.radius))


class SmokeParticle: #کلاس ذرات دود - برای افکت انفجار استفاده میشه
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 15)
        self.color = (
            random.randint(100, 150),  # خاکستری
            random.randint(100, 150),
            random.randint(100, 150),
            random.randint(200, 255)  # شفافیت اولیه
        )
        self.speed = random.uniform(0.5, 1.5) #سرعت تصادفی
        self.angle = random.uniform(0, math.pi)  # فقط به سمت بالا
        self.lifetime = random.uniform(1.0, 2.0)  # مدت نمایش (ثانیه)
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        # حرکت به سمت بالا با کمی پراکندگی افقی
        self.x += math.cos(self.angle) * 0.5
        self.y -= self.speed  # منفی چون مختصات Y در Pygame به سمت پایین است

        # محو شدن تدریجی
        self.color = (
            self.color[0],
            self.color[1],
            self.color[2],
            int(self.color[3] * (1 - self.current_time/self.lifetime))
        )
        return self.current_time < self.lifetime

    def draw(self, screen):
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.color, (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))


class Target: #کلاس تارگت های معمولی بازی
    def __init__(self):
        self.x = random.randint(40, 1125) 
        self.y = random.randint(120, 575)
        self.points = 0
        self.active = True

    def draw_target(self, screen):
        image_path = os.path.join(os.path.dirname(__file__), "pics", "Target.png")
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (35, 35))
        self.draw(screen, image)

    def draw(self, screen, image):
        if self.active:
            screen.blit(image, (self.x, self.y))

    def hit(self, point, shots, target): #وقتی به هدف شلیک میشه صدا پخش میشه
        self.points = point.point_by_distance(shots, target)
        if self.active:
            self.active = False #هدف غیرفعال میشه
            return self.points #امتیاز رو برمیگردونه
        return 0 # اگه هدف غیرفعال بود امتیازی نمیده
        
    def respawn(self, other_targets): #تولید مجدد هدف
        while True:
            self.x = random.randint(40, 1125)
            self.y = random.randint(120, 575)
            self.active = True

            overlap_found = False
            for target in other_targets:
                # چک کردن تداخل با همه تارگت‌های فعال دیگر
                if target != self and target.active and self.overlap(target.x, target.y):
                    overlap_found = True
                    break
            
            if not overlap_found:
                break
        return self.x, self.y

    def check_collision(self, shot): #چک کردن برخورد تیر با هدف
        return self.x <= shot[0] <= self.x + 35 and self.y <= shot[1] <= self.y + 35

    def overlap(self, other_x, other_y):
        # محاسبه مرکز هر تارگت
        self_center_x = self.x + 17.5
        self_center_y = self.y + 17.5
        other_center_x = other_x + 17.5
        other_center_y = other_y + 17.5
        
        # فاصله بین دو مرکز
        distance = math.sqrt((self_center_x - other_center_x)**2 + (self_center_y - other_center_y)**2)
        
        # اگر فاصله کمتر از قطر تارگت باشد (35 پیکسل) تداخل وجود دارد
        return distance < 35
    

class Items(Target): #کلاس ایتم های ویژه که از کلاس تارگت ارث بری میکند
    def draw_extra_time(self, screen): #زمان اضافه
        image_path = os.path.join(os.path.dirname(__file__), "pics", "Extra_time.png")
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (35, 35))
        self.draw(screen, image)
  
    def draw_extra_bullet(self, screen): #تیر اضافه
        image_path = os.path.join(os.path.dirname(__file__), "pics", "Extra_bullet.png")
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (35, 35))
        self.draw(screen, image)

    def draw_frozen(self, screen): #فریز کردن حریف
        image_path = os.path.join(os.path.dirname(__file__), "pics", "Frozen.png")
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found!")
            exit(1)

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (35, 35))
        self.draw(screen, image)


class Shoot: #مدیریت شلیک ها
    def __init__(self, screen):
        self.screen = screen
        self.shot_x = random.randint(23, 1177)
        self.shot_y = random.randint(103, 627)
        self.shot_speed = 10
        self.shots = []
        self.shotsl = []
        self.shoot_triggered = False
        try: #صدای شلیک
            self.shot_sound = pygame.mixer.Sound(os.path.join("sound effects", "shoot.mp3"))
            self.shot_sound.set_volume(0.1)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load shot sound!")
            self.shot_sound = None
        self.muzzle_flashes = []  # لیست جرقه‌های فعال

    def check_shoot(self, target_x, target_y):
        if target_x <= self.shot_x <= target_x+35 and target_y <= self.shot_y <= target_y+35:
            self.shot_x = random.randint(23, 1177)
            self.shot_y = random.randint(103, 627)
            return self.shot_x, self.shot_y

    def shooting(self, keys, up_key, down_key, left_key, right_key, shoot_key, time, bullets, frozen_until): #مدیریت فرایند شلیک
        if time <= 0 or bullets <= 0: #اگر زمان یا تیر تموم شده
            return
        current_time = pygame.time.get_ticks()
        if current_time < frozen_until: #اگه بازیکن فریز شده
            return
            #حرکت نشانه گیری با کلید ها 
        if keys[up_key]:
            self.shot_y -= self.shot_speed
            if self.shot_y < 103: #محدودیت حرکت به بالا 
                self.shot_y = 103
        if keys[down_key]:
            self.shot_y += self.shot_speed
            if self.shot_y > 627: #محدودیت حرکت به پایین
                self.shot_y = 627
        if keys[left_key]:
            self.shot_x -= self.shot_speed
            if self.shot_x < 23: #محدودیت حرکت به چپ
                self.shot_x = 23
        if keys[right_key]:
            self.shot_x += self.shot_speed
            if self.shot_x > 1177: #محدودیت حرکت به راست
                self.shot_x = 1177

        if keys[shoot_key]:
            if not self.shoot_triggered:
                self.shots.append((self.shot_x, self.shot_y))
                self.shotsl = [(self.shot_x, self.shot_y)] #اخرین شلیک رو ذخیره میکنیم
                self.muzzle_flashes.append(MuzzleFlash(self.shot_x, self.shot_y))
                if self.shot_sound:
                    self.shot_sound.play()
                self.shoot_triggered = True #صدای شلیک
        else:
            self.shoot_triggered = False

    def draw_muzzle_flashes(self, screen):
        for flash in self.muzzle_flashes[:]:
            flash.update()
            flash.draw(screen)
            if not flash.active:
                self.muzzle_flashes.remove(flash)


class Point: #کلاس مدیریت امتیازدهی
    def __init__(self):
        self.d = 0
       
    def point_by_distance(self, shots, target):
        last_shot = shots[-2]
        self.d = (((target.x+17.5) - last_shot[0])**2 + ((target.y+17.5) - last_shot[1])**2) **0.5
    # امتیازدهی بر اساس فاصله
        if 0 <= self.d < 130:
            return 1
        if 130 <= self.d < 260:
            return 2
        if 260 <= self.d < 390:
            return 3
        if 390 <= self.d < 520:
            return 4
        if 520 <= self.d < 650:
            return 5
        if 650 <= self.d < 780:
            return 6
        if 780 <= self.d < 910:
            return 7
        if 910 <= self.d < 1040:
            return 8
        if 1040 <= self.d < 1170:
            return 9
        if 1170 <= self.d <= 1300:
            return 10
        
    def giving_points(self, target, shoot, score, number_of_shots1, shot, targets, point, game):
        self.number_of_shots2_p2 = len(shoot.shots)
        if self.number_of_shots2_p2 - number_of_shots1 == 1:
            score += 5
            game.message_system.add_message("Perfect Shot! +5", (255,111,0))
        
        number_of_shots1 = self.number_of_shots2_p2
        score += target.hit(point, shoot.shots, target)
        target.respawn(targets)
        return score, number_of_shots1


class Input: #کلاس مدیریت ورودی‌های بازی
    def __init__(self, screen):
        self.player1_name = ""
        self.player2_name = ""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.error_message = ""
        try:
            self.background = pygame.image.load(os.path.join("pics", "login_bg.jpg")).convert()
            self.background = pygame.transform.scale(self.background, (1200, 650))
        except:
            print("Warning: Could not load background image!")
            self.background = None
        self.icons = {
            'player': pygame.image.load(os.path.join("pics", "player_icon.png")).convert_alpha(),
            'bullets': pygame.image.load(os.path.join("pics", "bullets_icon.png")).convert_alpha(),
            'score': pygame.image.load(os.path.join("pics", "score_icon.png")).convert_alpha(),
            'time': pygame.image.load(os.path.join("pics", "time_icon.png")).convert_alpha()
        }
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (30, 30))

    def draw_input_box(self, text, x, y, active):
        # ایجاد یک سطح شفاف برای کادر
        s = pygame.Surface((200, 40), pygame.SRCALPHA)
    
        # تعیین رنگ با شفافیت (آلفا=150)
        if active:
            pygame.draw.rect(s, (0, 150, 0, 150), (0, 0, 200, 40), 2)
        else:
            pygame.draw.rect(s, (255, 215, 0, 150), (0, 0, 200, 40), 2)
    
        # نمایش سطح شفاف روی صفحه اصلی
        self.screen.blit(s, (x, y))
    
        # نمایش متن
        text_surface = self.font.render(text, True, (255, 255, 255))  # متن سفید
        self.screen.blit(text_surface, (x + 10, y + 10))
    
        return pygame.Rect(x, y, 200, 40)

    def draw_error_message(self):
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))
            error_width = error_surface.get_width()
            screen_width = self.screen.get_width()
            x_pos = (screen_width - error_width) // 2
            y_pos = 500 + 40 + 20
            self.screen.blit(error_surface,(x_pos, y_pos))  # نمایش پیام خطا زیر جعبه‌های ورودی
    
    def draw_border(self):
        border_color = (0, 0, 0)  # رنگ کادر
        border_width = 3  # ضخامت کادر
        pygame.draw.rect(self.screen, border_color, (7, 7, 1185, 635), border_width)

    def get_player_names(self):
        player1_name = ""
        player2_name = ""
        active1 = True
        active2 = False
        input_box1 = self.draw_input_box(player1_name, 500, 250, active1)
        input_box2 = self.draw_input_box(player2_name, 500, 350, active2)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_RETURN:
                            if len(player1_name) == 0:
                                self.error_message = "Player name cannot be empty!"
                            elif len(player1_name) > 8:
                                self.error_message = "Player name cannot be longer than 8 characters."
                            else:
                                active1 = False
                                active2 = True
                                self.error_message = ""  # پاک کردن پیام خطا
                        elif event.key == pygame.K_BACKSPACE:
                            player1_name = player1_name[:-1]
                            self.error_message = ""  # پاک کردن پیام خطا
                        else:
                            if len(player1_name) < 8:
                                player1_name += event.unicode
                            else:
                                self.error_message = "Player name cannot be longer than 8 characters."
                    elif active2:
                        if event.key == pygame.K_RETURN:
                            if len(player2_name) == 0:
                                self.error_message = "Player name cannot be empty!"
                            elif len(player2_name) > 8:
                                self.error_message = "Player name cannot be longer than 8 characters."
                            else:
                                running = False
                                self.error_message = ""  # پاک کردن پیام خطا
                        elif event.key == pygame.K_BACKSPACE:
                            player2_name = player2_name[:-1]
                            self.error_message = ""  # پاک کردن پیام خطا
                        else:
                            if len(player2_name) < 8:
                                player2_name += event.unicode
                            else:
                                self.error_message = "Player name cannot be longer than 8 characters."

            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((173, 216, 230))
            
            self.draw_input_box(player1_name, 500, 250, active1)
            self.draw_input_box(player2_name, 500, 350, active2)
            self.draw_error_message()  # نمایش پیام خطا
            self.draw_border()  # رسم کادر
            pygame.display.flip()

        self.player1_name = player1_name
        self.player2_name = player2_name

    def display_player_info(self, current_time1, current_time2, player1_bullets, player2_bullets, score1, score2):
        seconds1 = current_time1 // 1000
        seconds2 = current_time2 // 1000
        time1 = 60 - seconds1
        time2 = 60 - seconds2
        if time1 <= 0:
            time1 = 0
        if time2 <= 0:
            time2 = 0

        self.screen.blit(self.icons['bullets'], (15, 50))
        self.screen.blit(self.icons['player'], (15, 20))
        player1_info1 = [
            f"player1 : {self.player1_name}",
            f"bullets : {player1_bullets}"
        ]
        for i, line in enumerate(player1_info1):
            text = self.font.render(line, True, (10, 10, 150))
            self.screen.blit(text, (50, 20 + i * 30))
        self.screen.blit(self.icons['score'], (315, 20))
        self.screen.blit(self.icons['time'], (315, 50))
        player1_info2 = [
            f"score : {score1}",
            f"time : {time1}" 
        ]
        for i, line in enumerate(player1_info2):
            text = self.font.render(line, True, (10,10,150))
            self.screen.blit(text, (350, 20 + i * 30))

        self.screen.blit(self.icons['bullets'], (905, 50))
        self.screen.blit(self.icons['player'], (905, 20))
        player2_info1 = [
            f"player2 : {self.player2_name}",
            f"bullets : {player2_bullets}"
        ]
        for i, line in enumerate(player2_info1):
            text = self.font.render(line, True, (150,10,10))
            self.screen.blit(text, (940, 20 + i * 30))

        self.screen.blit(self.icons['score'], (695, 20)) 
        self.screen.blit(self.icons['time'], (695, 50))
        player2_info2 = [
            f"score : {score2}",
            f"time : {time2}" 
        ]
        for i, line in enumerate(player2_info2):
            text = self.font.render(line, True, (150,10,10))
            self.screen.blit(text, (730, 20 + i * 30))

        return time1, time2


class MessageSystem:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.messages = []  # لیست پیام‌ها به صورت (متن, زمان شروع, رنگ, مدت نمایش)
        self.unique_messages = set()

    def add_message(self, text, color=(255, 255, 255), display_time=2000, is_unique=False):
        if not is_unique or text not in self.unique_messages:
            self.messages.append((text, pygame.time.get_ticks(), color, display_time))
            if is_unique:
                self.unique_messages.add(text)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.messages = [
            (text, time, color, display_time) 
            for (text, time, color, display_time) in self.messages 
            if current_time - time < display_time
        ]
        
        active_messages = {text for (text, _, _, _) in self.messages}
        self.unique_messages = {
            msg for msg in self.unique_messages
            if msg in active_messages
        }

    def draw(self):
        y_offset = 100
        for (text, _, color, _) in self.messages:
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (500, y_offset))
            y_offset += 40


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        try:
            self.countdown_sound = pygame.mixer.Sound(os.path.join("sound effects", "countdown.mp3"))
            self.countdown_sound.set_volume(0.7)  # تنظیم حجم صدا
        except Exception as e:
            print(f"Warning: Could not load countdown sound! Error: {e}")
            self.countdown_sound = None
        try:
            pygame.mixer.music.load(os.path.join("sound effects", "background.mp3"))  
            pygame.mixer.music.set_volume(0.3) 
        except Exception as e:
            print(f"Warning: Could not load background music! Error: {e}")

        self.screen = pygame.display.set_mode((1200, 650))
        pygame.display.set_caption("CSshot Game")
        try:
            self.login_sound = pygame.mixer.Sound(os.path.join("sound effects", "login.mp3"))
            self.login_sound.set_volume(1.0)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load login sound!")
            self.login_sound = None
        self.running = True
        try:
            self.hit_sound = pygame.mixer.Sound(os.path.join("sound effects", "hit.mp3"))
            self.hit_sound.set_volume(0.8)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load hit sound!")
            self.hit_sound = None
        try:
            self.extra_time_sound = pygame.mixer.Sound(os.path.join("sound effects", "extra_time.mp3"))
            self.extra_time_sound.set_volume(0.6)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load extra time sound!")
            self.extra_time_sound = None
        try:
            self.extra_bullet_sound = pygame.mixer.Sound(os.path.join("sound effects", "extra_bullet.mp3"))
            self.extra_bullet_sound.set_volume(0.6)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load extra bullet sound!")
            self.extra_bullet_sound = None
        try:
            self.frozen_sound = pygame.mixer.Sound(os.path.join("sound effects", "frozen.mp3"))
            self.frozen_sound.set_volume(0.6)  # تنظیم حجم صدا
        except:
            print("Warning: Could not load frozen sound!")
            self.frozen_sound = None
        self.clock = pygame.time.Clock()
        self.player1_bullets = 20
        self.player2_bullets = 20
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 36)
        self.font1 = pygame.font.Font(None, 70)
        self.space_pressed = False
        self.enter_pressed = False
        self.number_of_shots1_p1 = 0
        self.number_of_shots1_p2 = 0
        self.player1_frozen_until = 0
        self.player2_frozen_until = 0
        self.message_system = MessageSystem(self.screen)
        self.time_up_shown = {"player1": False, "player2": False}
        self.bullets_out_shown = {"player1": False, "player2": False}
        self.frozen_message_time = 0
        self.last_special_item_time = 0  # زمان آخرین نمایش آیتم ویژه
        self.special_item_interval = 10000  # هر 10 ثانیه (به میلی‌ثانیه)
        self.explosions = []
        self.dt = 0
        try:
            self.win_sound = pygame.mixer.Sound(os.path.join("sound effects", "end.mp3"))
            self.win_sound.set_volume(0.7)
        except:
            print("Warning: Could not load win sound!")
            self.win_sound = None

    def update_explosions(self):
        for explosion in self.explosions[:]:
            if not explosion.update(self.dt):
                self.explosions.remove(explosion)

    def show_countdown(self):
        countdown_font = pygame.font.Font(None, 150)
        if self.countdown_sound:
            self.countdown_sound.play()
        for i in range(3, 0, -1):
            self.screen.fill((173, 216, 230))
            countdown_text = countdown_font.render(str(i), True, (1, 87, 155))
            self.screen.blit(countdown_text, (580, 250))
            pygame.display.flip()
            pygame.time.wait(1000)  # تأخیر 1 ثانیه‌ای
    
        self.screen.fill((173, 216, 230))
        start_text = countdown_font.render("Start!", True, (1, 87, 155))
        self.screen.blit(start_text, (480, 250))
        pygame.display.flip()
        pygame.time.wait(1000)  # تأخیر 1 ثانیه‌ای
        
    def activate_random_special_item(self, targets):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_special_item_time >= self.special_item_interval:
            self.last_special_item_time = current_time
            
            # بررسی آیا آیتم ویژه فعالی وجود دارد یا خیر
            active_special_items = [target for target in targets[3:] if target.active]
            if not active_special_items:  # اگر هیچ آیتم ویژه‌ای فعال نبود
                # انتخاب تصادفی یک آیتم ویژه
                special_item = random.choice(targets[3:])
                special_item.active = True
                special_item.respawn(targets)
                
    def draw_border(self):
        border_color = (0, 0, 0)
        border_width = 3
        pygame.draw.rect(self.screen, border_color, (7, 7, 1185, 635), border_width)

    def display_end_screen(self, score1, score2, player1_name, player2_name):
        self.screen.fill((173, 216, 230))
        pygame.mixer.music.stop()  # توقف موزیک پس‌زمینه
        if self.win_sound:
            self.win_sound.play()
        if score1 > score2:
            result_text = f"{player1_name} wins!"
        elif score2 > score1:
            result_text = f"{player2_name} wins!"
        else:
            result_text = "Player 1 and 2 tied."
        
        center_x = self.screen.get_width() // 2
        result_surface = self.font1.render(result_text, True, (0, 0, 0))
        result_rect = result_surface.get_rect(center=(center_x, 250))
        self.screen.blit(result_surface, result_rect)

        score_text = f"{player1_name}: {score1}  |  {player2_name}: {score2}"
        score_surface = self.font.render(score_text, True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(center_x, 350))
        self.screen.blit(score_surface, score_rect)

        self.draw_border()  # رسم کادر در صفحه پایان بازی
        pygame.display.flip()
        pygame.time.wait(7000)  # 7000 میلی‌ثانیه = 7 ثانیه

    def run(self): #متد اصلی اجرای بازی
        pygame.mixer.init() #راه اندازی سیستم صدا
        if self.login_sound: #پخش صدای ورود به بازی
            self.login_sound.play()
        get_inputs = Input(self.screen) #گرفتن اسم بازیکن ها
        get_inputs.get_player_names()
        if self.login_sound:# قطع صدای ورود
            self.login_sound.stop()  # قطع صدا پس از ورود به 
        self.show_countdown() # نمایش شمارش معکوس
        pygame.mixer.music.play(-1)  # پخش موزیک به صورت لوپ بی‌نهایت
        self.start_time1 = pygame.time.get_ticks()
        self.start_time2 = pygame.time.get_ticks()
        # ایجاد سیستم شلیک برای هر بازیکن
        shoot1 = Shoot(self.screen)
        shoot2 = Shoot(self.screen)
        # ایجاد تارگت های بازی
        target1 = Target()
        target2 = Target()
        target3 = Target()
        target_extra_time = Items()
        target_extra_bullet = Items()
        target_frozen = Items()

        targets = [target1, target2, target3, target_extra_time, target_extra_bullet, target_frozen]
        
        # غیرفعال کردن آیتم‌های ویژه در ابتدا
        for target in targets[3:]:
            target.active = False

        for target in targets:
            shoot1.check_shoot(target.x, target.y)
        for target in targets:
            shoot2.check_shoot(target.x, target.y)

        while self.running:
            self.dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.space_pressed = False
                    elif event.key == pygame.K_RETURN:
                        self.enter_pressed = False

            self.update_explosions()
            self.screen.fill((173, 216, 230))
            shoot1.draw_muzzle_flashes(self.screen)
            shoot2.draw_muzzle_flashes(self.screen)
            
            current_time1 = pygame.time.get_ticks() - self.start_time1
            current_time2 = pygame.time.get_ticks() - self.start_time2
            time1, time2 = get_inputs.display_player_info(current_time1, current_time2, self.player1_bullets, self.player2_bullets, self.score1, self.score2)

            # نمایش پیام تمام شدن زمان (فقط یک بار)
            if time1 <= 0 and not self.time_up_shown["player1"]:
                self.message_system.add_message(f"{get_inputs.player1_name}'s time is up!", 
                                              (245,0,87), is_unique=True)
                self.time_up_shown["player1"] = True
                
            if time2 <= 0 and not self.time_up_shown["player2"]:
                self.message_system.add_message(f"{get_inputs.player2_name}'s time is up!", 
                                              (245,0,87), is_unique=True)
                self.time_up_shown["player2"] = True

            # نمایش پیام تمام شدن تیرها (فقط یک بار)
            if self.player1_bullets <= 0 and not self.bullets_out_shown["player1"]:
                self.message_system.add_message(f"{get_inputs.player1_name} is out of bullets", 
                                              (245,0,87), is_unique=True)
                self.bullets_out_shown["player1"] = True
                
            if self.player2_bullets <= 0 and not self.bullets_out_shown["player2"]:
                self.message_system.add_message(f"{get_inputs.player2_name} is out of bullets", 
                                              (245,0,87), is_unique=True)
                self.bullets_out_shown["player2"] = True

            for explosion in self.explosions:
                explosion.draw(self.screen)
                
            target1.draw_target(self.screen)
            target2.draw_target(self.screen)
            target3.draw_target(self.screen)
            target_extra_time.draw_extra_time(self.screen)
            target_extra_bullet.draw_extra_bullet(self.screen)
            target_frozen.draw_frozen(self.screen)
            
            # فعال کردن تصادفی آیتم ویژه هر 10 ثانیه
            self.activate_random_special_item(targets)

            keys = pygame.key.get_pressed()
            shoot1.shooting(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, 
                          pygame.K_SPACE, time1, self.player1_bullets, self.player1_frozen_until)
            current_time = pygame.time.get_ticks()
            if (keys[pygame.K_SPACE] and not self.space_pressed and self.player1_bullets > 0 and current_time >= self.player1_frozen_until):
                # اگر کلید فاصله فشرده شد و گلوله داشت و فریز نبود
                self.player1_bullets -= 1
                self.space_pressed = True
            # مدیریت شلیک بازیکن دوم (کلیدهای جهت‌دار و اینتر)
            shoot2.shooting(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, 
                          pygame.K_RETURN, time2, self.player2_bullets, self.player2_frozen_until) # اگر کلید اینتر فشرده شد و گلوله داشت و فریز نبود
            if (keys[pygame.K_RETURN] and not self.enter_pressed and self.player2_bullets > 0 and current_time >= self.player2_frozen_until):
                self.player2_bullets -= 1
                self.enter_pressed = True
            # ایجاد سیستم امتیازدهی
            point1 = Point()
            point2 = Point()

            for shot in shoot1.shotsl:
                if target1.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target1, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target1.x + 17.5, target1.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()
                elif target2.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target2, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target2.x + 17.5, target2.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()
                elif target3.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target3, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target3.x + 17.5, target3.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()
                elif target_extra_time.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target_extra_time, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target_extra_time.x + 17.5, target_extra_time.y + 17.5))
                    self.start_time1 += 10000
                    self.message_system.add_message("+10 seconds!", (51,105,30))
                    if self.extra_time_sound:  
                        self.extra_time_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_extra_time.active = False
                elif target_extra_bullet.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target_extra_bullet, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target_extra_bullet.x + 17.5, target_extra_bullet.y + 17.5))
                    self.player1_bullets += 3
                    self.message_system.add_message("+3 bullets!", (103,58,183))
                    if self.extra_bullet_sound: 
                        self.extra_bullet_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_extra_bullet.active = False
                elif target_frozen.check_collision(shot):
                    self.score1, self.number_of_shots1_p1 = point1.giving_points(
                        target_frozen, shoot1, self.score1, self.number_of_shots1_p1, 
                        shot, targets, point1, self)
                    self.explosions.append(Explosion(target_frozen.x + 17.5, target_frozen.y + 17.5))
                    self.player2_frozen_until = pygame.time.get_ticks() + 5000
                    self.message_system.add_message(f"{get_inputs.player2_name} Frozen for 5s!", (0, 0, 255), 5000)
                    if self.frozen_sound:  
                        self.frozen_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_frozen.active = False
            # بررسی برخورد شلیک‌های بازیکن دوم با تارگت ها
            for shot in shoot2.shotsl:
                if target1.check_collision(shot):# برخورد با هدف اول
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target1, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target1.x + 17.5, target1.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()
                elif target2.check_collision(shot):# برخورد با هدف دوم
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target2, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target2.x + 17.5, target2.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()
                elif target3.check_collision(shot):# برخورد با هدف سوم
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target3, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target3.x + 17.5, target3.y + 17.5))
                    if self.hit_sound:  
                        self.hit_sound.play()

                elif target_extra_time.check_collision(shot):# برخورد با آیتم زمان اضافه
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target_extra_time, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target_extra_time.x + 17.5, target_extra_time.y + 17.5))
                    self.start_time2 += 10000
                    self.message_system.add_message("+10 seconds!", (51,105,30))
                    if self.extra_time_sound:  
                        self.extra_time_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_extra_time.active = False

                elif target_extra_bullet.check_collision(shot): # برخورد با آیتم گلوله اضافه
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target_extra_bullet, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target_extra_bullet.x + 17.5, target_extra_bullet.y + 17.5))
                    self.player2_bullets += 3
                    self.message_system.add_message("+3 bullets!", (103,58,183))
                    if self.extra_bullet_sound:  # پخش افکت صوتی جدید
                        self.extra_bullet_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_extra_bullet.active = False

                elif target_frozen.check_collision(shot): # برخورد با آیتم فریز
                    self.score2, self.number_of_shots1_p2 = point2.giving_points(
                        target_frozen, shoot2, self.score2, self.number_of_shots1_p2, 
                        shot, targets, point2, self)
                    self.explosions.append(Explosion(target_frozen.x + 17.5, target_frozen.y + 17.5))
                    self.player1_frozen_until = pygame.time.get_ticks() + 5000
                    self.message_system.add_message(f"{get_inputs.player1_name} Frozen for 5s!", (0, 0, 255), 5000)
                    if self.frozen_sound:  
                        self.frozen_sound.play()
                    if self.hit_sound:  
                        self.hit_sound.play()
                    target_frozen.active = False

            for shot in shoot1.shots:
                pygame.draw.circle(self.screen, (1, 87, 155), shot, 3)
            for shot in shoot2.shots:
                pygame.draw.circle(self.screen, (150, 10, 10), shot, 3)
            # کشیدن حاشیه و خط جداکننده
            self.draw_border()
            pygame.draw.line(self.screen, (0, 0, 0), (7, 85), (1193, 85), 3)
            # شرط پایان بازی - وقتی هر دو بازیکن زمان یا گلوله نداشته باشند
            if (self.player1_bullets <= 0 or time1 <= 0) and (self.player2_bullets <= 0 or time2 <= 0):
                # نمایش پیام "Game is done!" در همان صفحه بازی
                self.screen.fill((173, 216, 230))
                self.draw_border()
                pygame.draw.line(self.screen, (0, 0, 0), (7, 85), (1193, 85), 3)
                start_wait_time = pygame.time.get_ticks()
                waiting = True
                while waiting:
                    if pygame.time.get_ticks() - start_wait_time >= 3000:
                        waiting = False

                    self.screen.fill((173, 216, 230))
                    self.draw_border()
                    pygame.draw.line(self.screen, (0, 0, 0), (7, 85), (1193, 85), 3)
        
                    for shot in shoot1.shots:
                        pygame.draw.circle(self.screen, (1, 87, 155), shot, 3)
                    for shot in shoot2.shots[1:]:
                        pygame.draw.circle(self.screen, (25, 25, 112), shot, 3)
                    # نمایش اطلاعات بازیکن‌ها
                    time1, time2 = get_inputs.display_player_info(current_time1, current_time2, self.player1_bullets, self.player2_bullets, self.score1, self.score2)
                    # کشیدن تارگت ها
                    target1.draw_target(self.screen)
                    target2.draw_target(self.screen)
                    target3.draw_target(self.screen)
                    target_extra_time.draw_extra_time(self.screen)
                    target_extra_bullet.draw_extra_bullet(self.screen)
                    target_frozen.draw_frozen(self.screen)

                     # نمایش پیام پایان بازی
                    done_text = self.font1.render("Game is done!", True, (0, 0, 0))
                    self.screen.blit(done_text, (400, 110))

                    pygame.display.flip()
                    # نمایش صفحه نهایی و امتیازات
                self.display_end_screen(self.score1, self.score2, get_inputs.player1_name, get_inputs.player2_name)
                self.running = False # پایان بازی
            # آپدیت و نمایش پیام‌های سیستم
            self.message_system.update()
            self.message_system.draw()
    
            pygame.display.flip()
            self.clock.tick(60)

        pygame.mixer.music.stop()  # توقف موزیک هنگام خروج
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()