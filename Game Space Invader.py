# Space Invaders
# Sound (For Windows only)
# Python 3.6 on Windows

import turtle
import random
import pygame
import sys

# Set up Sound
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
bgm = pygame.mixer.Sound("bgm.wav")
fire_sound = pygame.mixer.Sound("laser.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")
bgm.play(loops=-1)

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")

# Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")
turtle.register_shape("apple.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(4)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 272)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player_speed = 20

# Choose a number of enemies
number_of_enemies = 5

# Create an empty list of enemies
enemies = []

# Add enemies
for temp in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)
enemy_speed = 6


# Create the player's bullet
class BulletClass:
    bullet_speed = 15

    def __init__(self):
        self.bullet = turtle.Turtle()
        self.bullet.shape("apple.gif")
        self.bullet.penup()
        self.bullet.speed(0)
        self.bullet.shapesize(0.5, 0.5)
        self.bullet.hideturtle()
        self.bullet.setposition(0, -300)
        self.status = "ready"

    def fire_bullet(self, position):
        if self.status == "ready":
            fire_sound.play(loops=0)
            self.status = "fire"
            # Move the bullet to the just above the player
            self.bullet.setposition(position.xcor(), position.ycor()+10)
            self.bullet.showturtle()

    def reset_bullet(self):
        self.bullet.hideturtle()
        self.status = "ready"
        self.bullet.setposition(0, -300)

    def move_bullet(self):
        if self.bullet.ycor() > 275:
            self.reset_bullet()
            self.status = "ready"

        if self.status == "fire":
            y = self.bullet.ycor()
            y += self.bullet_speed
            self.bullet.sety(y)


number_of_bullet = 5

bullet_array = {}
for j in range(number_of_bullet):
    bullet_array[j] = BulletClass()


def fire():
    for j in range(5):
        if bullet_array[j].status == "ready":
            bullet_array[j].fire_bullet(player)
            break


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def is_collision(t1, t2):
    if abs(t1.ycor() - t2.ycor()) < 30:
        if abs(t1.xcor() - t2.xcor()) < 30:
            return True
    return False


def quit_game():
    global game_status
    game_status = "End"


# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire, "space")
turtle.onkey(quit_game, "q")

game_status = "Playing"
enemy_status = "alive"
praise_word = ["Nice!!", "Good!!",  "Prefect!!",
               "Amazing!!", "Fantastic!!", "Great!!"]
i = 0
# Main game loop
while True:

    for enemy in enemies:
        # Move the enemy
        if enemy_status == "alive":
            x = enemy.xcor()
            x += enemy_speed
            enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            enemy_status = "down"

        if enemy_status == "down":
            y = enemy.ycor()
            y -= 6
            i += 1
            enemy.sety(y)

        if i == 30:
            i = 0
            enemy_speed *= -1
            enemy_status = "alive"

        # Move bullet
        for j in range(number_of_bullet):
            bullet_array[j].move_bullet()

        # Check for a collision between the bullet and the enemy
        for j in range(number_of_bullet):
            if is_collision(bullet_array[j].bullet, enemy):
                explosion_sound.play(loops=0)

                # Reset the enemy
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)

                # Reset bullet
                bullet_array[j].reset_bullet()

                # Update the score
                i = random.randint(0, 5)
                print(praise_word[i])
                score += 10
                score_pen.clear()
                score_string = "Score: %s" % score
                score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        if is_collision(player, enemy):
            explosion_sound.play(loops=0)
            player.hideturtle()
            enemy.hideturtle()
            print("You Dead")
            quit_game()

        if game_status == "End":
            print("Your Score was:", score)
            sys.exit("Thanks for play!!")



