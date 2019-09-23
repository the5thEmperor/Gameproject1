import arcade
import pathlib
from enum import auto, Enum


class MoveEnum(Enum):
        NONE = auto()
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()

class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed:int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window
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

class Shot (arcade.Sprite):
    def __init__(self, shot_path:str,game_window):
        super().__init__(shot_path)
        self.speed = 25
        self.game = game_window
        self.shot_x = None
        self.shot_y = None
        self.is_fired = False

    def fire (self):
        self.center_x += self.speed
        




class MinimalArcade(arcade.Window):
    def __init__(self, image_name:str, shot_name:str, sound_name:str, background_name:str, screen_w:int = 1024, screen_h:int = 800):
        super().__init__(screen_w, screen_h)
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.shot_path = pathlib.Path.cwd() / 'Assets' / shot_name
        self.sound_path = pathlib.Path.cwd() / 'Assets' / sound_name
        self.background_path = pathlib.Path.cwd() / 'Assets' / background_name
        self.shot_sound = arcade.sound.load_sound(self.sound_path)
        self.background = arcade.Sprite(self.background_path)
        self.background2 = arcade.Sprite(self.background_path)
        self.background_speed = 5
        self.background.center_x = screen_w // 2
        self.background.center_y = screen_h // 2
        self.background.change_x = -self.background_speed
        self.background2.center_x = screen_w * 3 // 2
        self.background2.center_y = screen_h // 2
        self.background2.change_x = -self.background_speed
        self.backgroundlist = arcade.SpriteList()
        self.backgroundlist.append(self.background)
        self.backgroundlist.append(self.background2)
        self.pict = None
        self.shot = None
        self.direction = MoveEnum.NONE
        self.pictlist = None
        self.shotlist = arcade.SpriteList()
        self.shot_fired = False


    def setup(self):
        self.pict = MinimalSprite(str(self.image_path), speed=3, game_window=self)
        self.pict.center_x = 200
        self.pict.center_y = 500
        self.pictlist = arcade.SpriteList()
        self.pictlist.append(self.pict)

    def on_update(self, delta_time: float):
        self.pict.move(self.direction)
        if self.background.left == -1080:
            self.background.center_x = 1080 + 1080 // 2
        if self.background2.left == -1080:
            self.background2.center_x = 1080 + 1080 // 2
        self.backgroundlist.update()
        self.shotlist.update()

    def on_draw(self):
        arcade.start_render()  # Code to draw screen goes here
        self.backgroundlist.draw()
        self.pictlist.draw()
        self.shotlist.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key ==arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.SPACE:
            self.shot = Shot(str(self.shot_path), game_window=self)
            self.shot.center_x = self.pict.center_x
            self.shot.center_y = self.pict.center_y
            self.shot_fired = True
            self.shot.change_x = 25
            self.shotlist.append(self.shot)
            arcade.play_sound(self.shot_sound)


    def on_key_release(self, key: int, modifiers: int):
        if (key == arcade.key.UP or key == arcade.key.W) and self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and self.direction == MoveEnum.DOWN: self.direction = MoveEnum.NONE

def main():
    window = MinimalArcade("Bernesestandstill1.png", "rsz_tennisball.png", "dogruff.wav", "grassbackground.jpg", screen_w=1080)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()