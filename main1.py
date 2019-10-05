import sys, logging, os, random, math, open_color, arcade, time

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Battle"

NUM_ENEMIES = 10
NUM_ROCKS = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 100
ENEMY_HP = 500
HIT_SCORE = 50
KILL_SCORE = 150


class Laser(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the laser
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("PNG/Lasers/laserGreen10.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the laser
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("PNG/playership2_green.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an enemy cargo ship
        Parameter: position: (x,y) tuple
        '''
        super().__init__("PNG/Enemies/enemyRed4.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Meteor(arcade.Sprite):
    def __init__(self,position):
        '''initializes danger'''
        super().__init__("PNG/Meteors/meteorGrey_big1.png",0.75)
        (self.center_x,self.center_y)= position

class EnemyDeath(arcade.Sprite):
    def __init__(self,position):
        '''if enemy dies'''
        super().__init__("Explosion/explosion08.png",0.15)
        (self.center_x,self.center_y)=position

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.rock_list=arcade.SpriteList()
        self.death_list=arcade.SpriteList()
    def setup(self):
        '''
        Set up enemies
        '''
        for r in range(NUM_ROCKS):
            x=120*(r+1)+40
            y=300
            rock=Meteor((x,y))
            self.rock_list.append(rock)

        for i in range(NUM_ENEMIES):
            x = 60 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)  
          

    def update(self, delta_time):
        self.laser_list.update()
        for e in self.enemy_list:
                if arcade.check_for_collision_with_list(e,self.laser_list):
                    e.hp =e.hp - BULLET_DAMAGE
                    self.score=self.score+HIT_SCORE
                    for a in self.laser_list:
                        a.kill()
                if e.hp==0:
                    self.score=self.score+KILL_SCORE
                    x=e.center_x
                    y=e.center_y
                    Death=EnemyDeath((x,y))
                    self.death_list.append(Death)
                    e.kill()
                if self.score == 4000:
                    time.sleep(1)
                    self.close()
        for m in self.rock_list:
            if arcade.check_for_collision_with_list(m,self.laser_list):
                for a in self.laser_list:
                    a.kill()
        if arcade.check_for_collision_with_list(self.player,self.rock_list):
            time.sleep(1)
            self.close()
        if arcade.check_for_collision_with_list(self.player,self.enemy_list):
            time.sleep(1)
            self.close()
        
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.laser_list.draw()
        self.rock_list.draw()
        self.enemy_list.draw()
        self.death_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x
        self.player.center_y=y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            laser = Laser((x,y),(0,10),BULLET_DAMAGE)
            self.laser_list.append(laser)
            

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()