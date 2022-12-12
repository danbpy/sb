import arcade
import time
import random as ran

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Plants VS Zombies"

def lawn_x(x):
    if 253<x<325:
        clmn = 1
        center_x = 289

    elif 325<x<397:
        clmn = 2
        center_x = 360

    elif 397<x<478:
        clmn = 3
        center_x = 440

    elif 551>x>478:
        clmn = 4
        center_x = 520

    elif 636>x>551:
        clmn = 5
        center_x = 595   

    elif 715>x>636:
        clmn = 6
        center_x = 676

    elif 784>x>715:
        clmn = 7
        center_x = 750

    elif 867>x>784:
        clmn = 8
        center_x = 825

    elif 938>x>867:
        clmn = 9
        center_x = 905    
        
    return center_x,clmn

    

def lawn_y(y):
    if 44<y<138:
        line = 1
        center_y = 91

    elif 138<y<228:
        line = 2
        center_y = 193

    elif 228<y<325:
        line = 3
        center_y = 276

    elif 325<y<413:
        line = 4
        center_y = 369

    elif 413<y<515:
        line = 5
        center_y = 464
        
    return center_y,line

class Plant(arcade.AnimatedTimeSprite):
    def __init__(self,hp,cost):
        super(). __init__(0.12)
        self.hp = hp
        self.cost = cost
        self.line = 0
        self.clmn = 0
        
    def update(self):
        if self.hp<=0:
            self.kill()

    def plentig(self,x,y,line,clmn):
        self.center_x = x
        self.center_y = y
        self.line = line
        self.clmn = clmn

class SunFlower(Plant):
    def __init__(self):
        super().__init__(hp = 80,cost = 50)
        self.texture = arcade.load_texture("sun1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("sun1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("sun2.png"))
        self.sun_spawn = time.time()

    def update(self):
        super().update()
        if time.time()-self.sun_spawn>=15:
            sun = Sun(self.center_x+20,self.center_y+20)
            arcade.play_sound(window.sunspawn)
            window.spawn.append(sun)
            self.sun_spawn = time.time()
            
class Sun(arcade.Sprite):
    def __init__(self,position_x,position_y):
        super().__init__("sun.png",0.12)
        self.center_x = position_x
        self.center_y = position_y
    
    def update(self):
        self.angle+=1

class PeaShooter(Plant):
    def __init__(self):
        super().__init__(hp = 80,cost = 100)
        self.texture = arcade.load_texture("pea1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("pea1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("pea2.png"))
        for i in range(3):    
            self.textures.append(arcade.load_texture("pea1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("pea3.png"))
        self.pea_spawn = time.time()

    def update(self):
        super().update()
        z = False
        for zombi in window.zombis:
            if zombi.line == self.line:
                z = True
        if time.time()-self.pea_spawn>=2 and z == True:
            shoot = Shoot(self.center_x+10,self.center_y+10)
            arcade.play_sound(window.peaspawn)
            window.shots.append(shoot)
            self.pea_spawn = time.time()

class Shoot(arcade.Sprite):
    def __init__(self,position_x,position_y):
        super().__init__("bul.png",0.12)
        self.center_x = position_x
        self.center_y = position_y
        self.change_x = 5
        self.dmg = 5

    def update(self):
        self.center_x += self.change_x
        if self.center_x>SCREEN_WIDTH:
            self.kill()
        hits = arcade.check_for_collision_with_list(self,window.zombis)
        if len(hits)>0:
            arcade.play_sound(window.hit)
            for zombi in hits:
                zombi.hp-=self.dmg
                self.kill()

class WallNut(Plant):
    def __init__(self):
        super().__init__(hp = 200,cost = 50)
        self.texture = arcade.load_texture("nut1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("nut1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("nut2.png"))
        for i in range(3):    
            self.textures.append(arcade.load_texture("nut3.png"))

class Torchwood(Plant):
    def __init__(self):
        super().__init__(hp = 80,cost = 175)
        self.texture = arcade.load_texture("tree1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("tree1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("tree2.png"))
        for i in range(3):    
            self.textures.append(arcade.load_texture("tree3.png"))

    def update(self):
        super().update()
        fire_pea = arcade.check_for_collision_with_list(self,window.shots)
        for pea in fire_pea:
            pea.dmg = 10
            pea.texture = arcade.load_texture("firebul.png")

class Zombie(arcade.AnimatedTimeSprite):
    def __init__(self,hp,line):
        super().__init__(0.08)
        self.hp = hp
        self.line = line
        self.center_x = SCREEN_WIDTH
        self.change_x = 0.2

    def update(self):
        self.center_x-=self.change_x
        if self.hp <= 0:
            self.kill()
            window.killed_z+=1
        eating = False   
        if self.center_x<200:
            window.game = False
        food = arcade.check_for_collision_with_list(self,window.plants)
        for plant in food:
            if self.line == plant.line:
                plant.hp -= 0.5
                eating = True
        if eating:
            self.change_x = 0
        else:
            self.change_x = 0.2

class Zom(Zombie):
    def __init__(self,line):
        super().__init__(hp = 30,line = line)
        self.texture = arcade.load_texture("zom1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("zom1.png"))
        for k in range(3):
            self.textures.append(arcade.load_texture("zom2.png"))

class Buck(Zombie):
    def __init__(self,line):
        super().__init__(hp = 60,line = line)
        self.texture = arcade.load_texture("buck1.png")
        for i in range(5):
            self.textures.append(arcade.load_texture("buck1.png"))
        for k in range(1):
            self.textures.append(arcade.load_texture("buck2.png"))

class Cone(Zombie):
    def __init__(self,line):
        super().__init__(hp = 50,line = line)
        self.texture = arcade.load_texture("cone1.png")
        for i in range(5):
            self.textures.append(arcade.load_texture("cone1.png"))
        for k in range(1):
            self.textures.append(arcade.load_texture("cone2.png"))            
        
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game = False
        self.status = True
        self.back = arcade.load_texture("background.jpg")
        self.menu = arcade.load_texture("menu_vertical.png")
        self.spawn = arcade.SpriteList()
        self.plants = arcade.SpriteList()
        self.seed = None
        self.lawns=[]
        self.sun = 200
        self.killed_z = 0
        self.zombi_time = time.time()
        self.label_time = time.time()
        self.zombis = arcade.SpriteList()
        self.shots = arcade.SpriteList()
        self.end = arcade.load_texture("end.png")
        
    # начальные значения
    def setup(self):
        self.grasswalk = arcade.load_sound("grasswalk.mp3")
        arcade.play_sound(self.grasswalk)

        self.hit = arcade.load_sound("hit.mp3")

        self.peaspawn = arcade.load_sound("peaspawn.mp3")

        self.sunspawn = arcade.load_sound("sunspawn.mp3")

        self.seed_sound = arcade.load_sound("seed.mp3")

    # отрисовка
    def on_draw(self):
        arcade.start_render()
        if self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.back)
            arcade.draw_texture_rectangle(60, 300, 130, 600, self.menu)
            self.plants.draw()
            arcade.draw_text(f"{self.sun}",39,495,arcade.color.BLACK,20)
            if 20>time.time()-self.label_time>17:
                arcade.draw_text("ZOMBIE COMING",200,270,arcade.color.RED,80)
            self.spawn.draw()
            self.shots.draw()
            self.zombis.draw()
            if self.seed!=None:
                self.seed.draw()
        if self.game == False:
            arcade.set_background_color(arcade.color.BLACK)
            if self.status:
                self.end = arcade.load_texture("logo.png")
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH-400, SCREEN_HEIGHT-300, self.end)
            else:
                self.end = arcade.load_texture("logo.png")
                arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH-400, SCREEN_HEIGHT-300, self.end)
        
    # игровая логика
    def update(self, delta_time):
        self.plants.update_animation()
        self.plants.update()
        self.spawn.update()
        self.shots.update()
        self.zombis.update_animation()
        self.zombis.update()
        if time.time()-self.zombi_time>20 and self.killed_z<20:
            rand = ran.randint(44,515)
            center_y,line = lawn_y(rand)
            typ = ran.randint(1,3)
            if typ == 1:
                zombi = Zom(line)
            elif typ == 2:
                zombi = Buck(line)
            else:
                zombi = Cone(line)
            zombi.center_y = center_y
            self.zombis.append(zombi)
            self.zombi_time = time.time()
        if self.killed_z>=15 and len(self.zombis) == 0:
            self.end = arcade.load_texture("logo.png")
            self.game = False
        if self.game == False:
            for plant in self.plants:
                plant.stop()
                plant.kill()

            for zombi in self.zombis:
                zombi.stop()
                zombi.kill()
    
    # нажатить кнопку мыши
    def on_mouse_press(self, x, y, button, modifiers):
       print(x,y)
       if x>10  and x<105 and y>375 and y<480:
           print("SunFlower")
           self.seed = SunFlower()
           if self.seed!=None:
               self.seed.center_x = x
               self.seed.center_y = y
       if 104>x>12 and 367>y>261:
           print("PeaShooter")
           self.seed = PeaShooter()

       if 105>x>15 and 250>y>147:
           print("WallNut")
           self.seed = WallNut()

       if 105>x>13 and 133>y>32:
           print("Torchwood")
           self.seed = Torchwood()

       for sun in self.spawn:
           if sun.left<x<sun.right and sun.bottom<y<sun.top:
               self.sun+=25
               sun.kill()
           
    # движение мыши
    def on_mouse_motion(self, x, y, dx, dy):
       if self.seed!=None:
               self.seed.center_x = x
               self.seed.center_y = y
               self.seed.alpha = 150

    # отпустить кнопку мыши
    def on_mouse_release(self, x, y, button, modifiers):
        if self.game:
            if 235<x<937 and 505>y>34 and self.seed is not None:
                center_x,clmn  = lawn_x(x)
                center_y,line = lawn_y(y)
                cost = self.seed.cost
                if (clmn,line) not in self.lawns and self.sun>=cost:
                    self.sun-=cost
                    self.lawns.append((clmn,line))
                    self.seed.plentig(center_x,center_y,line,clmn)
                    arcade.play_sound(self.seed_sound)
                    self.seed.alpha = 255
                    self.plants.append(self.seed)
                    self.seed = None
            elif 120>x>0 and self.seed is not None:
                self.seed = None
        if self.status:
            self.status = False
            self.game = True

window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
