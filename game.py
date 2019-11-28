from tkinter import*
import random
import numpy as np
width = 900
height = 300
pad_w = 10
pad_h = 100
ball_r = 30
root = Tk()
m1=3
m0=1
root.geometry('900x300')
c = Canvas(root, width=width, height=height, background="#003300")
c.pack()
# нарисуем разметку
c.create_line(pad_w, 0, pad_w, height, fill='white')
c.create_line(width-pad_w, 0, width-pad_w, height, fill='white')
c.create_line(width/2, 0, width/2, height, fill='white')
# мяч
ball = c.create_oval(width/2-ball_r/2,
                     height/2-ball_r/2,
                     width/2+ball_r/2,
                     height/2+ball_r/2, fill='white')
# ракетки
pad_right = c.create_oval(width-10, height/2-30, width-70, height/2 + 30, fill='yellow')
pad_left = c.create_oval(10, height/2-30, 70, height/2 + 30, fill='yellow')
dx = random.randint(-2, -2)
dy = random.randint(-1, 1)

score_1 = 0
score_2 = 0
p1_text = c.create_text(width-width/6, 25, text=score_1, font='Arial 20', fill ='white')
p2_text = c.create_text(width/6, 25, text=score_2, font='Arial 20', fill ='white')

def update_score(player):
    global score_1, score_2
    if player == 'right':
        score_1+=1
        c.itemconfig(p1_text, text=score_1)
    else:
        score_2+=1
        c.itemconfig(p2_text, text=score_2)

def respawn():
    global dx, dy
    c.coords(ball, width/2-ball_r/2,
                     height/2-ball_r/2,
                     width/2+ball_r/2,
                     height/2+ball_r/2,)
    dx = dx/dx*3
    dy = random.randint(-3, 3)
    if dy == 0:
        dy+=1

def move_ball():
    # далеко от стенок
    if (c.coords(ball)[2] < width-pad_w) and (c.coords(ball)[0] > pad_w):
        c.move(ball, dx, dy)
    # удар с ракеткой
    if c.coords(ball)[2] >= width - pad_w:
        if c.coords(pad_right)[1] <= (c.coords(ball)[1]+c.coords(ball)[3])/2 <= c.coords(pad_right)[3]:
            bounce('strike')
        else:
            update_score('left')
            respawn()
    if c.coords(ball)[0] <= pad_w:
        if c.coords(pad_left)[1] <= (c.coords(ball)[1]+c.coords(ball)[3])/2 <= c.coords(pad_left)[3]:
            bounce('strike')
        else:
            update_score('right')
            respawn()
    if c.coords(ball)[1] + dy < 0 or c.coords(ball)[3] + dy > height:
        bounce('wall')
    # удар с шариком
    if (((c.coords(ball)[0]+c.coords(ball)[2])/2 - (c.coords(pad_left)[0]+c.coords(pad_left)[2])/2 )**2 + \
            ((c.coords(ball)[1] + c.coords(ball)[3]) / 2 - (c.coords(pad_left)[1] + c.coords(pad_left)[3]) / 2)**2) < 2025:
        bounce('contactl')
    if (((c.coords(ball)[0]+c.coords(ball)[2])/2 - (c.coords(pad_right)[0]+c.coords(pad_right)[2])/2 )**2 + \
            ((c.coords(ball)[1] + c.coords(ball)[3]) / 2 - (c.coords(pad_right)[1] + c.coords(pad_right)[3]) / 2)**2) < 2025:
        bounce('contactr')
    root.after(11, move_ball)


vlpad_y = 0
vlpad_x = 0
vrpad_x = 0
vrpad_y = 0
speedl = 4
speedr = 4


def move_pad_left():

    c.move(pad_left, vlpad_x, vlpad_y)
    root.after(10, move_pad_left)


def move_pad_right():

    c.move(pad_right, vrpad_x, vrpad_y)
    root.after(10, move_pad_right)


c.focus_set()


def movement_handler(event):
    # управление движением с клавиатуры

    global vlpad_x, vlpad_y, vrpad_x, vrpad_y, speedr, speedl
    if event.keysym == 'w':
        vlpad_y = -speedl
    elif event.keysym == 's':
        vlpad_y = speedl
    elif event.keysym == 'a':
        vlpad_x = -speedl
    elif event.keysym == 'd':
        vlpad_x = speedl
    elif event.keysym == 'Up':
        vrpad_y = -speedr
    elif event.keysym == 'Down':
        vrpad_y = speedr
    elif event.keysym == 'Right':
        vrpad_x = speedr
    elif event.keysym == 'Left':
        vrpad_x = -speedr


def stop_pad(event):
    global vrpad_x, vrpad_y, vlpad_x, vlpad_y
    if event.keysym in ('w', 's', 'a', 'd'):
        vlpad_x = 0
        vlpad_y = 0
    if event.keysym in ('Up', 'Down', 'Left', 'Right'):
        vrpad_y = 0
        vrpad_x = 0


c.bind('<KeyRelease>', stop_pad)
c.bind('<KeyPress>', movement_handler)



def collision(v1x, v1y, c1x, c1y, c2x, c2y):
    # упругий отскок от неподвижной ракетки, с ускорением
    v1 = np.array([v1x, v1y])
    c1 = np.array([c1x, c1y])
    c2 = np.array([c2x, c2y])
    n = c1 - c2
    a =(n[0]**2+n[1]**2)**0.5
    n = n/a
    print(n)
    a1 = np.dot(v1, n)
    v1_new =v1-2*n*a1
    return v1_new*1.05


def bounce(action):
    # отскок мяча
    global dx, dy
    # отскок от стены
    if action == 'wall':
        dy = -dy
        c.move(ball, dx, dy)
    # отскок от ракетки
    if action == 'contactl':
        dx = collision(dx, dy, (c.coords(ball)[0] + c.coords(ball)[2]) / 2, (c.coords(ball)[1]+c.coords(ball)[3])/2,\
                                        (c.coords(pad_left)[1]+c.coords(pad_left)[3])/2, (c.coords(pad_left)[1]+c.coords(pad_left)[3])/2)[0]
        dy = collision(dx, dy, (c.coords(ball)[0] + c.coords(ball)[2]) / 2, (c.coords(ball)[1]+c.coords(ball)[3])/2,\
                                        (c.coords(pad_left)[1]+c.coords(pad_left)[3])/2, (c.coords(pad_left)[1]+c.coords(pad_left)[3])/2)[1]
        c.move(ball, 2*dx, 2*dy)
    if action == 'contactr':
        dx = collision(dx, dy, (c.coords(ball)[0] + c.coords(ball)[2]) / 2, (c.coords(ball)[1]+c.coords(ball)[3])/2,\
                                        (c.coords(pad_right)[1]+c.coords(pad_right)[3])/2, (c.coords(pad_right)[1]+c.coords(pad_right)[3])/2)[0]
        dy = collision(dx, dy, (c.coords(ball)[0] + c.coords(ball)[2]) / 2, (c.coords(ball)[1]+c.coords(ball)[3])/2,\
                                        (c.coords(pad_right)[1]+c.coords(pad_right)[3])/2, (c.coords(pad_right)[1]+c.coords(pad_right)[3])/2)[1]
        c.move(ball, 2*dx, 2*dy)







move_ball()
move_pad_right()
move_pad_left()


root.mainloop()
