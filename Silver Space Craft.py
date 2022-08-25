import random
import time
import math
from turtle import speed
import arcade
SCREEN_WIDTH=600
SCREEN_HEIGHT=600
FONT_SIZE=8
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/playerShip2_orange.png')
        self.speed=1
        self.width=48
        self.height=48
        self.angle=180
        self.center_x=random.randint(48,SCREEN_WIDTH-48)
        self.center_y=SCREEN_HEIGHT+12
    def move(self,speed):
        self.speed=speed
        self.center_y-=1*self.speed
class Explosion(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.img='Explosion.png'
        self.width=48
        self.height=48
        self.center_x=x
        self.center_y=y
        self.explosion=arcade.Sprite(self.img,0.01,center_x=self.center_x,center_y=self.center_y)
        self.Sound =(':resources:sounds/explosion2.wav')
    def draw(self):
        self.explosion.draw()
    def sound(self):
        arcade.Sound(self.Sound)
        load=arcade.load_sound(self.Sound)
        arcade.play_sound(load)
class Spacecraft(arcade.Sprite):
    def __init__(self,w,h):
        super().__init__(':resources:images/space_shooter/playerShip1_green.png')
        self.width=48
        self.height=48
        self.center_x=w//2
        self.center_y=48
        self.angle=0
        self.change_angle=0
        self.bullet_list=[]
        self.life=3
        self.score=0
    def rotate(self):
        self.angle+=self.change_angle
    def fire(self):
        self.bullet_list.append(Bullet(self))
        self.bullet_list[0].sound()
class Bullet(arcade.Sprite):
    def __init__(self,host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.center_x=host.center_x
        self.center_y=host.center_y
        self.speed=4
        self.angle=host.angle
        self.Sound =(':resources:sounds/laser2.wav')
    def move(self):
        angel_rad=math.radians(self.angle)
        self.center_x-=self.speed*math.sin(angel_rad)
        self.center_y+=self.speed*math.cos(angel_rad)
    def sound(self):
        arcade.Sound(self.Sound)
        load=arcade.load_sound(self.Sound)
        arcade.play_sound(load)
class Heart(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.img='HEART.png'
        self.heart=arcade.Sprite(self.img,0.03,center_x=x,center_y=y)
    def draw(self):
        self.heart.draw()
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,title="Silver Space Craft",center_window=True)
        self.background_img=arcade.load_texture(':resources:images/backgrounds/stars.png')
        self.spacecraft=Spacecraft(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.enemy_list=[]
        self.enemyspeed=1
        self.start_time=time.time()
        self.speed_increase_time_start=time.time()
        self.explosion=Explosion(-1,-1)
        self.heart=[]
        x=SCREEN_WIDTH-40
        for i in range(int(self.spacecraft.life)):
            self.heart.append(Heart(x,SCREEN_HEIGHT-20))
            x-=20
    def on_draw(self):
        arcade.start_render()
        if self.spacecraft.life<1:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text(text='GAME OVER',start_x=(SCREEN_WIDTH // 2)-66, start_y=(SCREEN_HEIGHT // 2),color=arcade.color.WHITE,font_size=FONT_SIZE*2,align='left',width=SCREEN_WIDTH)
            arcade.exit()
        else:
            for i in range(int(self.spacecraft.life)):
                self.heart[i].draw()
            self.explosion.draw()
            self.spacecraft.draw()
            for i in range(len(self.spacecraft.bullet_list)):
                self.spacecraft.bullet_list[i].draw()
            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()
            arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background_img)
    def on_key_press(self, key, modifers):
        if key==arcade.key.RIGHT:
            self.spacecraft.change_angle=-1
        elif key == arcade.key.LEFT:
            self.spacecraft.change_angle=1
        elif key==arcade.key.SPACE:
            self.spacecraft.fire()
    def on_key_release(self, key, modifiers):
        self.spacecraft.change_angle=0
    def on_update(self,delta_time):
        self.speed_increase_time_end=time.time()
        self.end_time=time.time()
        self.delta=random.randint(3,10)
        self.spacecraft.rotate()
        for i in range(len(self.spacecraft.bullet_list)):
            self.spacecraft.bullet_list[i].move()
        for i in range(len(self.spacecraft.bullet_list)):
            if self.spacecraft.bullet_list[i].center_x>SCREEN_WIDTH or self.spacecraft.bullet_list[i].center_x<0 or self.spacecraft.bullet_list[i].center_y>SCREEN_HEIGHT or self.spacecraft.bullet_list[i].center_y<0:
                del self.spacecraft.bullet_list[i]
                break
        if self.end_time-self.start_time>self.delta:
            self.enemy_list.append(Enemy())
            self.start_time=time.time()
        for i in range(len(self.enemy_list)):
            if self.enemy_list[i].center_y<0:
                self.spacecraft.life-=1
                self.heart.pop()
                del self.enemy_list[i]
                break
        for i in range(len(self.enemy_list)):
            if self.speed_increase_time_end-self.speed_increase_time_start>10:
                self.enemyspeed+=1
                self.speed_increase_time_start=time.time()
            self.enemy_list[i].move(self.enemyspeed)
        for i in range(len(self.spacecraft.bullet_list)):
            for j in range(len(self.enemy_list)):
                if arcade.check_for_collision(self.spacecraft.bullet_list[i],self.enemy_list[j]):
                    self.explosion=Explosion(self.enemy_list[j].center_x,self.enemy_list[j].center_y)
                    self.explosion.sound()
                    del self.enemy_list[j]
                    break
game =Game()
arcade.run()