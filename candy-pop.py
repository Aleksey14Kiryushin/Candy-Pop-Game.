from pygame import *
from time import time as now_time
from random import *
import os
# Создать цикл по строкам, и проверять есть ли схожие картинки

clock = time.Clock()

# Расположение
x = 400
y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

class Picture(sprite.Sprite):
    def __init__(self, width, height, x, y, picture, x_num, y_num):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x
        self.y = y 
        # Классификация по столбам и строчкам
        self.x_num = x_num 
        self.y_num = y_num
        
        self.picture_VISIABLE = picture
        self.width = width
        self.height = height

        self.chosen = False
        self.name = picture

        self.rectangle_draging = False

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def delete(self):
        new_name = choice(pictures_list) 
        while new_name == self.name:
            new_name = choice(pictures_list)
            print("name is", new_name)
        new_name = "background.jpg" 
        self.image = transform.scale(image.load(new_name), (self.width, self.height))
        self.name = new_name

# Window
global_height = 800
global_width = 800
window = display.set_mode((global_width,global_height))

# Create Pictures
pictures_list = ["brilliant_1st.png", "brilliant_2nd.png", "brilliant_3rd.jpeg", "brilliant_4th.jpg", "brilliant_5th.jpg"]
for i in range(5):
    shuffle(pictures_list)
    pictures_list += pictures_list

group_pictures = sprite.Group() # all pictures
picture_list = list()

x = 65
y = 125
x_num = 1
y_num = 1
for line in range(4):
    row_list = list()

    for picture in range(5):
        new_picture = Picture(100, 100, x, y, pictures_list[picture+(5*line)], x_num, y_num)
        x += 150 
        x_num += 1
        group_pictures.add(new_picture)

        row_list.append(new_picture)

    picture_list.append(row_list)

    x = 65
    y += 150
    x_num = 1
    y_num += 1

display.set_caption("Candy-Pop")
display.set_icon(image.load("background.jpg")) 
background = transform.scale(image.load("background.jpg"), (global_height, global_width))

game_Play = True 
dragging = False
delete_list = list()
while game_Play:
    window.blit(background, (0,0))

    # Events
    for event_get in event.get():
        # Quit the app
        if event_get.type == QUIT:
            game_Play = False

        elif event_get.type == MOUSEBUTTONDOWN:
            if event_get.button == 1:   
                for picture in group_pictures:         
                    if picture.rect.collidepoint(event_get.pos):
                        picture.rectangle_draging = True
                        dragging = True
                        picture_chsn = picture 
                        mouse_x, mouse_y = event_get.pos
                        offset_x = picture.rect.x - mouse_x
                        offset_y = picture.rect.y - mouse_y

        elif event_get.type == MOUSEBUTTONUP:
            if event_get.button == 1: 
                # Если место занято, то картинки меняются местами
                for picture in group_pictures:
                    # if picture.rect.x >= picture.x - 150 and picture.rect.x <= picture.x:
                    #     if picture.rect.y >= picture.y - 50 and picture.rect.y <= picture.y + 50:
                    # print("LEFT")  
                    if picture.rectangle_draging:                                     
                        for picture_left in group_pictures:
                            if picture != picture_left: 
                                if sprite.collide_rect(picture_left, picture):
                                    
                                    print("Pict X", picture.x)
                                    print("Pict Left", picture_left.x)
                                    # Для картинки слева
                                    picture_left.rect.x = picture.x
                                    picture_left.rect.y = picture.y

                                    # Для премещенной картинки
                                    before_x = picture.rect.x
                                    before_y = picture.rect.y
                                
                                    picture.rect.x = picture_left.x
                                    picture.rect.y = picture_left.y

                                    picture.x = before_x
                                    picture_left.x = picture_left.rect.x

                                    picture.y = picture.rect.y
                                    picture_left.y = picture_left.rect.y

                                    before_x = picture.x_num
                                    picture.x_num = picture_left.x_num
                                    picture_left.x_num = before_x

                                    before_y = picture.y_num
                                    picture.y_num = picture_left.y_num
                                    picture_left.y_num = before_y

                                    print("Pict X", picture.x)
                                    print("Pict Left", picture_left.x)

                #  Удалять схожие по X  
                                    # delete_list = list()
                                    # counter = 1
                                    # for picture_del in group_pictures:
                                    #     # Left
                                    #     while picture_del.name == picture.name:
                                    #         if picture_del != picture:
                                            
                                    #             if picture_del.x_num == picture.x_num - counter:
                                    #                 counter += 1
                                    #                 delete_list.append(picture_del)
                                    #     counter = 1
                                    #     # Right
                                    #     while picture_del.name == picture.name:
                                    #         if picture_del != picture:
                                    #             if picture_del.x_num == picture.x_num + counter:
                                    #                 counter += 1   
                                    #                 delete_list.append(picture_del)


                                            # if picture_del.y_num == picture.y_num:

                                            # По Y
                                            # if picture_del.y_num == picture.y_num - 1 or picture_del.y_num == picture.y_num + 1:
                                            #     # X = X
                                            #     if picture_del.x_num == picture.x_num:  
                                            #         if picture_del.name == picture.name:  
                                            #             delete_list.append(picture_del)
                                    # right
                                    
                                    for row in picture_list: 
                                        for j in range(len(row)): 
                                            counter = 1
                                            if j != len(row) - 1:
                                                while row[j].name == row[j+counter].name:      
                                                    delete_list.append(row[j+counter])
                                                    counter += 1  
                                                    print("COUNTER", counter)
                                                    print("row", len(row))
                                                    print("j", j)
                                                    if (counter + j >= len(row) - 2):
                                                        break

                                        delete_list.append(picture) 
                                        print("LEN", len(delete_list))
                                        if len(delete_list) >= 3:
                                            for picture_del in delete_list:
                                                print("Delete",picture_del.name) 
                                                # Удаление
                                                picture_del.delete()
                                        delete_list = list()

                    picture.rectangle_draging = False
                    dragging = False

        elif event_get.type == MOUSEMOTION:
            for picture in group_pictures:
                if picture.rectangle_draging:
                    mouse_x, mouse_y = event_get.pos
                    picture.rect.x = mouse_x + offset_x
                    picture.rect.y = mouse_y + offset_y
                    

    # showing pictures
    for picture in group_pictures:
        picture.reset()

    display.update()

    clock.tick(60)