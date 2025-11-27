import turtle
import random
import threading
import pygame

#  CONFIG

NAME = "Shreya"
WIDTH, HEIGHT = 1100, 550
BG_COLOR = "black"

GOLD = "#d4af37"
BRIGHT_GOLD = "#ffd700"
SOFT_GLOW = "#806000"
LEAF_GREEN = "#0b8f2f"
ROSE_RED = "#ff3b47"

AUDIO_FILE = r"C:\Users\ajayp\Downloads\happy-birthday.mp3"

#  AUDIO SETUP (pygame)

pygame.mixer.init()

def play_music():
    try:
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print("Music error:", e)

#  WINDOW SETUP

win = turtle.Screen()
win.setup(WIDTH, HEIGHT)
win.title(f"Happy Birthday - {NAME}")
win.bgcolor(BG_COLOR)
win.tracer(False)

def in_box(x, y, box):
    return box["left"] < x < box["right"] and box["bottom"] < y < box["top"]


#  BORDER

def draw_border():
    border = turtle.Turtle(visible=False)
    border.speed(0)
    border.penup()
    margin = 20
    left = -WIDTH // 2 + margin
    right = WIDTH // 2 - margin
    top = HEIGHT // 2 - margin
    bottom = -HEIGHT // 2 + margin

    border.color(GOLD)
    border.width(3)
    border.setpos(left, bottom)
    border.pendown()
    border.setpos(left, top)
    border.setpos(right, top)
    border.setpos(right, bottom)
    border.setpos(left, bottom)


#  TITLE + NAME

TITLE_Y = 180
TITLE_BOX = {"left": -480, "right": 480, "top": 270, "bottom": 80}

def draw_title_and_name():
    title_pen = turtle.Turtle(visible=False)
    title_pen.penup()
    title_pen.color("white")
    title_pen.setpos(0, TITLE_Y)
    title_pen.write("🎉 HAPPY BIRTHDAY 🎉",
                    align="center",
                    font=("Georgia", 40, "bold"))

    name_y = TITLE_Y - 60

    outline_pen = turtle.Turtle(visible=False)
    outline_pen.penup()
    outline_pen.color(GOLD)

    offsets = [(-2,0),(2,0),(0,-2),(0,2)]
    for dx,dy in offsets:
        outline_pen.setpos(dx, name_y + dy)
        outline_pen.write(NAME, align="center", font=("Georgia", 30, "italic"))

    name_pen = turtle.Turtle(visible=False)
    name_pen.penup()
    name_pen.color("white")
    name_pen.setpos(0, name_y)
    name_pen.write(NAME, align="center", font=("Georgia", 30, "italic"))


#  ROSE
ROSE_X, ROSE_Y = 0, -20
ROSE_BOX = {"left": -220, "right": 220, "top": 110, "bottom": -220}

def draw_rose():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    outline = "#8b0000"  
    fill = "#d40000"          
    center = "#700000"        

    # ========== Draw Petals ==========
    t.width(3)
    t.color(outline, fill)

    for i in range(6):  
        t.penup()
        t.goto(ROSE_X, ROSE_Y)
        t.setheading(60 * i)
        t.forward(15)
        t.pendown()

        t.begin_fill()
        t.circle(60, 60)
        t.left(110)
        t.circle(60, 60)
        t.end_fill()

    # ========== Draw Center ==========
    t.penup()
    t.goto(ROSE_X, ROSE_Y - -10)
    t.color(outline, center)
    t.pendown()
    t.begin_fill()
    t.circle(15)
    t.end_fill()


#  EMOJIS + SPARKLES

EMOJIS = ["🎂", "✨", "🍷", "🥂"]
NUM_EMOJIS = 24
MIN_DIST = 60

BOTTOM_BOX = {"left": -480, "right": 480, "top": -HEIGHT//2 + 80, "bottom": -HEIGHT//2 + 20}

emoji_data = []

def place_emojis():
    placed = []

    def too_close(x, y):
        return any(((px-x)**2 + (py-y)**2)**0.5 < MIN_DIST for px,py in placed)

    for _ in range(NUM_EMOJIS):
        while True:
            x = random.randint(-WIDTH//2+40, WIDTH//2-40)
            y = random.randint(-HEIGHT//2+40, HEIGHT//2-40)

            if in_box(x,y,TITLE_BOX) or in_box(x,y,ROSE_BOX) or in_box(x,y,BOTTOM_BOX) or too_close(x,y):
                continue

            placed.append((x,y))

            size = random.randint(18,26)

            glow = turtle.Turtle(visible=False)
            glow.penup()
            glow.color(SOFT_GLOW)
            glow.setpos(x,y)
            glow.write(random.choice(EMOJIS), align="center", font=("Arial", size+6))

            sparkle = turtle.Turtle(visible=False)
            sparkle.penup()
            sparkle.color(BRIGHT_GOLD)

            emoji_data.append({"x":x,"y":y,"sparkle":sparkle,"on":False})
            break

def animate_sparkles():
    for e in emoji_data:
        s = e["sparkle"]
        if random.random() < 0.3:
            if e["on"]:
                s.clear()
                e["on"] = False
            else:
                s.clear()
                s.setpos(e["x"] + random.randint(-15,15), e["y"] + random.randint(-15,15))
                s.write("✨", align="center", font=("Arial", 14))
                e["on"] = True

    win.update()
    win.ontimer(animate_sparkles, 200)


#  MESSAGE

def draw_bottom_message():
    m = turtle.Turtle(visible=False)
    m.penup()
    m.color(GOLD)
    m.setpos(0, -HEIGHT//2 + 40)
    m.write("May God bless you with Happiness",
            align="center", font=("Georgia", 16, "italic"))

def stop_and_close():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    win.bye()


#  MAIN RUN

draw_border()
draw_title_and_name()
draw_rose()
draw_bottom_message()
place_emojis()
win._root.protocol("WM_DELETE_WINDOW", stop_and_close)

win.update()

animate_sparkles()
threading.Thread(target=play_music, daemon=True).start()

win.mainloop()
