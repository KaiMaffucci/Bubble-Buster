#Bubble Buster

#imports
from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

#builds GUI
HEIGHT = 600
WIDTH = 800
window = Tk()
window.title("Bubble Buster")
c = Canvas(window, width = WIDTH, height = HEIGHT, bg = "darkblue")
c.pack()

#builds submarine
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill = "red")
ship_id2 = c.create_oval(0, 0, 30, 30, outline = "red")
ship_r = 15
mid_x = WIDTH / 2
mid_y = HEIGHT / 2
c.move(ship_id, mid_x, mid_y)
c.move(ship_id2, mid_x, mid_y)

#controls the submarine
ship_spd = 15
def move_ship(event):
    if event.keysym == "Up":
        c.move(ship_id, 0, -ship_spd)
        c.move(ship_id2, 0, -ship_spd)
    elif event.keysym == "Down":
        c.move(ship_id, 0, ship_spd)
        c.move(ship_id2, 0, ship_spd)
    elif event.keysym == "Left":
        c.move(ship_id, -ship_spd, 0)
        c.move(ship_id2, -ship_spd, 0)
    elif event.keysym == "Right":
        c.move(ship_id, ship_spd, 0)
        c.move(ship_id2, ship_spd, 0)
    elif event.keysym == "BackSpace" or event.keysym == "Escape":
        window.destroy()
c.bind_all("<Key>", move_ship) #tells the program to run this whenever a key is pressed

#bubbles
bub_id = list()
bub_r = list()
bub_speed = list()
min_bub_r = 10
max_bub_r = 30
max_bub_spd = 10
gap = 100
def create_bubble():
    x = WIDTH + gap
    y = randint(0, HEIGHT)
    r = randint(min_bub_r, max_bub_r)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline = "white")
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, max_bub_spd))

#function to make bubbles move
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

#function that gets coords of bubble based off of id
def get_coords(id_num):
    pos = c.coords(id_num)
    #works out coords of middle bubble
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y

#function to make bubbles pop
def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]

#function to clean up bubbles that go off screen
def clean_up_bubs():
    for i in range(len(bub_id) - 1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -gap:
            del_bubble(i)

#function for figuring out the distance between two points
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

#function for detecting submarine + bubble collision
def collision():
    points = 0
    for bub in range(len(bub_id) - 1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (ship_r + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub)
    return points

#creates scoreboard and functions to manage it
c.create_text(50, 30, text = "TIME", fill = "white")
c.create_text(150, 30, text = "SCORE", fill = "white")
time_text = c.create_text(50, 50, fill = "white")
score_text = c.create_text(150, 50, fill = "white")
def show_score(score):
    c.itemconfig(score_text, text = str(score))
def show_time(time_left):
    c.itemconfig(time_text, text = str(time_left))

bub_chance = 5
time_limit = 30
score = 0
level_score = 0
level = 1
end = time() + time_limit + 4
playing = True
#level one message
level_text = c.create_text(mid_x, mid_y, text = "LEVEL 1", fill = "white", font = ("helvetica", 30))
window.update()
sleep(3)
c.delete(level_text)
window.update()
#main game loop
while playing == True:
    #generates bubble at random
    if randint(1, bub_chance) == 1:
        create_bubble()
    move_bubbles() #moves bubs
    clean_up_bubs() #cleans up off screen bubs
    #score
    points_from_collision = collision()
    score += points_from_collision
    level_score += points_from_collision
    #if they get to next level do stuff
    if level_score > 1000:
        for i in range(len(bub_id) - 1, -1, -1):
            del_bubble(i)
        level_score = 0
        level += 1
        end = time() + time_limit + 4
        bub_chance += 1
        #next level message
        level_text = c.create_text(mid_x, mid_y, text = "LEVEL " + str(level), fill = "white", font = ("helvetica", 30))
        show_score(score)
        window.update()
        sleep(3)
        c.delete(level_text)
        window.update()
    #display score and time
    show_score(score)
    show_time(int(end - time()))
    window.update() #show everything thats added to canvas
    sleep(0.01) #delay so you have time
    #if they lose, game over screen
    if time() > end:
        c.create_text(mid_x, mid_y, text = "GAME OVER", fill = "white", font = ("helvetica", 30))
        c.create_text(mid_x, mid_y + 30, text = "Score: " + str(score), fill = "white")
        window.update()
        sleep(3)
        playing = False
