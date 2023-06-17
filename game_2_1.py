from tkinter.messagebox import *
import pygame
import math
import sqlite3
import random


user1_f = open("file1.txt", 'r')
user1 = user1_f.read()
user1_f.close()

user2_f = open("file2.txt", 'r')
user2 = user2_f.read()
user2_f.close()


pygame.init()
pygame.display.set_icon(pygame.image.load("Icon.ico"))


WIDTH = 480
HEIGHT= 480
ROWS = 3
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("دوز 1")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SALEM_IMAGE = pygame.transform.scale(pygame.image.load("img/img/salem{}.png".format(random.randrange(1, 9))), (150, 150))
NASALEM_IMAGE = pygame.transform.scale(pygame.image.load("img/img/nasalem{}.png".format(random.randrange(1, 5))), (150, 150))


END_FONT = pygame.font.SysFont('arial', 40)

def app():
    def insert_into_db(user):
        if user == "user 1":
            conn = sqlite3.connect("db.db")
            cur = conn.cursor()
            cur.execute(f"INSERT INTO {user1} VALUES(:level,:score)",{'level':"doz 1",'score': f'{user1}'})
            conn.commit()
            conn.close()
        elif user == "user 2":
            conn = sqlite3.connect("db.db")
            cur = conn.cursor()
            cur.execute(f"INSERT INTO {user2} VALUES(:level,:score)",{'level':"doz 1",'score': f'{user2}'})
            conn.commit()
            conn.close()

    def draw_grid():
        gap = WIDTH // ROWS

        x = 0
        y = 0

        for i in range(ROWS):
            x = i * gap
            pygame.draw.line(SCREEN, GRAY, (x, 0), (x, WIDTH), 3)
            pygame.draw.line(SCREEN, GRAY, (0, x), (WIDTH, x), 3)


    def initialize_grid():
        dis_to_center = WIDTH // ROWS // 2

        game_array = [[None, None, None], [None, None, None], [None, None, None]]

        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x = dis_to_center * (2 * j + 1)
                y = dis_to_center * (2 * i + 1)

                game_array[i][j] = (x, y,"", True)

        return game_array


    def click(game_array):
        global user1_trun, user2_trun, images

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x, y, char, user1_play = game_array[i][j]

                dis = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)

                if dis < WIDTH // ROWS // 2 and user1_play:
                    if user1_trun:  
                        images.append((x, y, SALEM_IMAGE))
                        user1_trun = False
                        user2_trun = True
                        game_array[i][j] = (x, y, f'{user1}', False)

                        insert_into_db('user1')

                    elif user2_trun:  
                        images.append((x, y, NASALEM_IMAGE))
                        user1_trun = True
                        user2_trun = False
                        game_array[i][j] = (x, y, f"{user2}", False)
                        insert_into_db('user2')
                    
    def has_won(game_array):
        for row in range(len(game_array)):
            if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
                if game_array[row][0][2] == user1:
                    insert_into_db("user 1")
                else:
                    insert_into_db("user 2")

                display_message(game_array[row][0][2].upper())
                insert_into_db("user 2")
                return True

        for col in range(len(game_array)):
            if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
                if game_array[0][col][2] == user1:
                    insert_into_db("user 1")
                else:
                    insert_into_db("user 2")

                display_message(game_array[0][col][2].upper())
                insert_into_db("user 1")
                return True

        if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
            if game_array[0][0][2] == user1:
                insert_into_db("user 1")
            else:
                insert_into_db("user 2")

            display_message(game_array[0][0][2].upper())
            insert_into_db("user 2")
            return True

        if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
            if game_array[0][2][2] == user1:
                insert_into_db("user 1")
            else:
                insert_into_db("user 2")

            display_message(game_array[0][2][2].upper())
            return True
        
        return False


    def has_drawn(game_array):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                if game_array[i][j][2] == "":
                    return False

        display_message(f"{user1} = {user2}")
        return True


    def display_message(content):
        pygame.time.delay(500)
        SCREEN.fill(WHITE)
        end_text = END_FONT.render(content, 1, BLACK)
        SCREEN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
        # pygame.display.update()
        pygame.display.flip()

        pygame.time.delay(3000)


    def render():
        try:
            SCREEN.fill(WHITE)
            draw_grid()

            for image in images:
                x, y, IMAGE = image
                SCREEN.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

            pygame.display.update()
        except:
            pass
    
    def main():
        global user1_trun, user2_trun, images, draw

        images = []
        draw = False

        run = True

        user1_trun = True
        user2_trun = False

        game_array = initialize_grid()

        while run == True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        import Software as s
                        s.G2()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click(game_array)
            except:
                pass

            render()

            if has_won(game_array) or has_drawn(game_array):
                run = False


    while 1:
        main()
