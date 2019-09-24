#To move up and down use either up/down or w/s. To fire the shot use spacebar

#import files
import arcade
import pathlib
from enum import auto, Enum

#create class of enum for recording movement keystrokes
class MoveEnum(Enum):
        NONE = auto()
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()

#create class for the player sprite
class Sprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed:int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window
    #function for movement check what direction was pushed and move accordingly
    #only allows up and down movement currently
    def move (self, direction:MoveEnum):
        if direction == MoveEnum.UP:
            if self.top < 800:
                self.center_y += self.speed
        elif direction == MoveEnum.DOWN:
            if self.bottom > 0:
                self.center_y -= self.speed
        elif direction == MoveEnum.LEFT:
            self.center_x += self.speed
        elif direction == MoveEnum.RIGHT:
            self.center_x -= self.speed
        else:  #should be MoveEnum.NONE
            pass

#create class for the shot sprite
class Shot (arcade.Sprite):
    def __init__(self, shot_path:str,game_window):
        super().__init__(shot_path)
        self.speed = 25
        self.game = game_window
        self.shot_x = None
        self.shot_y = None
        self.is_fired = False
#function to move the shot after it was fired
    def fire (self):
        self.center_x += self.speed

#create class to set up game
class Game(arcade.Window):
    def __init__(self, image_name:str, shot_name:str, sound_name:str, background_name:str, screen_w:int = 1024, screen_h:int = 800):
        super().__init__(screen_w, screen_h)
        #establish the path for all the used assets
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.shot_path = pathlib.Path.cwd() / 'Assets' / shot_name
        self.sound_path = pathlib.Path.cwd() / 'Assets' / sound_name
        self.background_path = pathlib.Path.cwd() / 'Assets' / background_name
        #load the sound to be played on keystroke
        self.shot_sound = arcade.sound.load_sound(self.sound_path)
        #create the object variables for the background sprites
        self.background = arcade.Sprite(self.background_path)
        self.background2 = arcade.Sprite(self.background_path)
        #set the attributes of the background sprites
        self.background_speed = 5
        self.background.center_x = screen_w // 2
        self.background.center_y = screen_h // 2
        self.background.change_x = -self.background_speed
        self.background2.center_x = screen_w * 3 // 2
        self.background2.center_y = screen_h // 2
        self.background2.change_x = -self.background_speed
        #create the spritelist for the background and append the two background
        self.backgroundlist = arcade.SpriteList()
        self.backgroundlist.append(self.background)
        self.backgroundlist.append(self.background2)
        #create the variables for the player sprite and and shot sprite and set them none
        self.pict = None
        self.shot = None
        #set the direction to start as NONE
        self.direction = MoveEnum.NONE
        #create the spritelist and shotlist variables
        self.pictlist = None
        self.shotlist = arcade.SpriteList()
        self.shot_fired = False


    def setup(self):
        self.pict = Sprite(str(self.image_path), speed=3, game_window=self)
        self.pict.center_x = 200
        self.pict.center_y = 500
        self.pictlist = arcade.SpriteList()
        self.pictlist.append(self.pict)

    def on_update(self, delta_time: float):
        self.pict.move(self.direction)
        #determine if the scrolling background has moved offscreen and reset them
        if self.background.left == -1080:
            self.background.center_x = 1080 + 1080 // 2
        if self.background2.left == -1080:
            self.background2.center_x = 1080 + 1080 // 2
        #update the background and shot list to move the screen and shots
        self.backgroundlist.update()
        self.shotlist.update()

    def on_draw(self):
        arcade.start_render()  # Code to draw screen goes here
        #draw the sprites from all lists
        self.backgroundlist.draw()
        self.pictlist.draw()
        self.shotlist.draw()


    def on_key_press(self, key, modifiers):
        #determine the key press and do the approiate action
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key ==arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        #if the player shoots create the shot sprite and append it to the list
        elif key == arcade.key.SPACE:
            self.shot = Shot(str(self.shot_path), game_window=self)
            self.shot.center_x = self.pict.center_x
            self.shot.center_y = self.pict.center_y
            self.shot_fired = True
            self.shot.change_x = 25
            self.shotlist.append(self.shot)
            arcade.play_sound(self.shot_sound)


    def on_key_release(self, key: int, modifiers: int):
        #make it so when the player releases the key the sprite stops
        if (key == arcade.key.UP or key == arcade.key.W) and self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and self.direction == MoveEnum.DOWN: self.direction = MoveEnum.NONE

def main():
    #call the window with the appropriate assets and run the game
    window = Game("Bernesestandstill1.png", "rsz_tennisball.png", "dogruff.wav", "grassbackground.jpg", screen_w=1080)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()