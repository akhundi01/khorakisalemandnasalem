import pygame # اضافه کردن کتابخونه پایگیم
import random
import time
import sqlite3 # اضافه کردن اس کیو لایت سه که برای ساهت دیتا بیس است


pygame.init() # همه قابلیت های پایگیم را اضافه می کند تا از آن استفاده کنیم


f = open('file.txt', 'r')
x = f.read()  # خواندن اطلاعات از این فایل

pygame.display.set_icon(pygame.image.load("Icon.ico"))

# متغیر ها 
display_width = 1000
display_height = 690
floor_x = 0
gravity = 0.6
bird_movement = 0
pipe_list = []
game_status = True
bird_list_index = 0
game_font = pygame.font.Font('img/font/Flappy.TTF', 40) # فونت نرم افزار
game_font2 = pygame.font.Font('img/font/tahomabd.ttf', 21)
run  = True
score = 0 # متغیری که امتیاز در آن قرار می گیرد
high_score = 0
active_score = True


def bg_random(x):
    global display_width
    global display_height, main_screen

    r_choice = random.choice([1, 2])
    b = f"img/img/{r_choice}.jpg"
    if x == "bg":
        if  r_choice == 2:
            display_width = 1000
            display_height = 560
            main_screen = pygame.display.set_mode([display_width, display_height])
            return b
        else:
            return b        
    elif x == "size":
        if r_choice == 2:
            display_width = 1000
            display_height = 560
            return [display_width, display_height]
        else:
            display_width = 1000
            display_height = 560
            return [display_width, display_height]


pygame.display.set_caption('بازی') # تایتل یا عنوان نرم افزار

create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 100)
pygame.time.set_timer(create_pipe, 3000) # هر چند لحظه یک بار به صورت خودکار اجرا می شود

win_sound = pygame.mixer.Sound('img/sound/smb_stomp.wav') # متغیری که فایل صوتی در آن قرار دارد
game_over_sound = pygame.mixer.Sound('img/sound/smb_mariodie.wav')


background_image = pygame.image.load(bg_random("bg"))# متغیری که بک گراند صفحه در آن قرار دارد

bird_image_down = pygame.transform.scale2x(
    pygame.image.load('img/img/red_bird_down_flap.png')) 

bird_image_mid = pygame.transform.scale2x(
    pygame.image.load('img/img/red_bird_mid_flap.png'))

bird_image_up = pygame.transform.scale2x(
    pygame.image.load('img/img/red_bird_up_flap.png'))

bird_list = [bird_image_down, bird_image_mid, bird_image_up]

bird_image = bird_list[bird_list_index]

image = pygame.image.load('img/img/{}.png'.format(random.choice(['nasalem1', 'nasalem2', "nasalem3", "nasalem4",]))) # متغیری که به صورت اتفاقی عکسی را انتخاب می کند


def generate_pipe_rect():# تابعی که مکان قرار گیری غذا های ناسالم را به صورت اتفاقی انتخاب می کند
    random_pipe = random.randrange(300, 600) # عدد را بین رنج داده شد به صورت اتفاقی انتخاب می کند
    pipe_rect_top = image.get_rect(midbottom=(2111-300, random_pipe-260))
    pipe_rect_bottom = pygame.image.load('img/img/{}.png'.format(random.choice(
        ['nasalem1', 'nasalem2', "nasalem3", "nasalem4",]))).get_rect(midtop=(2111, random_pipe))
    return pipe_rect_top, pipe_rect_bottom


def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            main_screen.blit(image, pipe) # قرار گیری غذا های ناسالم در پنجره
            main_screen.blit(image, pipe)

        else:
            main_screen.blit(image, pipe)
            main_screen.blit(image, pipe)


def check_collision(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe): # چک می کنه که آیا برخوردی بوده یا نه
            game_over_sound.play()
            time.sleep(3)

            if score >= 60:
                # امتیاز را در دیتا بیس ثبت می کند
                conn = sqlite3.connect("db.db") 
                cur = conn.cursor()
                cur.execute(f"INSERT INTO {x} VALUES(11,{score})")
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect("db.db") 
                cur = conn.cursor()
                cur.execute(f"INSERT INTO {x} VALUES(1,{score})")
                conn.commit()
                conn.close()

            active_score = True
            return False
        if bird_image_rect.top <= -220 or bird_image_rect.bottom >= 900:# و اگه پرنده از محدوده های داده شده خارج شود
            # آهنگی را پخش می کند و امتیازات صفر می شود
            game_over_sound.play()
            time.sleep(3)

            if score >= 60:
                # امتیازات در دیتا بیس ثبت می شوند
                conn = sqlite3.connect("db.db")
                cur = conn.cursor()
                cur.execute(
                    f"INSERT INTO {x} VALUES(1,{score})")
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect("db.db") 
                cur = conn.cursor()
                cur.execute(f"INSERT INTO {x} VALUES(1,{score})")
                conn.commit()
                conn.close()
            active_score = True
            return False
    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(90, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    # تابعی که امتیازات و مرحله بازی را نشان می دهد
    if status == 'active':
        text1 = game_font.render(str(score), False, 'white')
        text1_rect = text1.get_rect(center=(940, 30))
        main_screen.blit(text1, text1_rect)

        text1 = game_font2.render("Level 3", False, 'pink')
        text1_rect = text1.get_rect(center=(60, 30))
        main_screen.blit(text1, text1_rect) # در صفحه قرار می دهد


def update_score():
    # امتیازات را اگر برخورد نکرده باشد یا از صفحه خارج نشده باشد بروزسانی می کند
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1 # به امتیازات یکی اضافه می کند
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        if score > 50: pass
        high_score = score

    return high_score


bird_image_rect = bird_image.get_rect(center=(100, 480))


main_screen = pygame.display.set_mode(bg_random("size"))

clock = pygame.time.Clock()


while run == True: # بی نهایت تا وقتی شرط مورد نظر فالس برنگرداند اجرا می شود
    for event in pygame.event.get(): # رویداد های را می گیرد مثلا اگه ماوس حرکت کنه متوجه می شود
        if event.type == pygame.QUIT:# چک می کنه اگه روی دکمه کلوز کلید شد دستورات داخلش اجرا شود

            run = False  # این متغیر را فالس می کند و شرط دیگه درست برنمی گرداند و برنامه بسته می شود
            pygame.quit()
            import Software as s
            s.G1()  # این کلاس اجرا می کند

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:# چک می کنه که اگر کاربر روی کلید اسپیس رو فشار داد
                bird_movement = 0 
                bird_movement -= 15 # مختصات صفحه پانزده تا به سمت بالا حرکت کنه
            if event.key == pygame.K_r and game_status == False: # این شرط ها ترو برگردونن
                # همه متغیر ها به داده هایی که در ابتدا داشتن بر می گردن
                image = pygame.image.load(
                    'img/img/{}.png'.format(random.choice(['nasalem1', 'nasalem2', "nasalem3", "nasalem4"])))  # انتخاب تصویر
                background_image = pygame.image.load(bg_random("bg"))

                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (100, 100)
                bird_movement = 0
                score = 0

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0

            bird_image, bird_image_rect = bird_animation()

    main_screen.blit(background_image, (0, 0))

    if game_status:
        main_screen.blit(bird_image, bird_image_rect) # مختصات قرار گیری پرنده

        game_status = check_collision(pipe_list)

        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)

        bird_movement += gravity
        bird_image_rect.centery += bird_movement

        update_score() # افزایش امتیاز

        display_score('active')

    pygame.display.update()

    clock.tick(100) # سرعت بازی 