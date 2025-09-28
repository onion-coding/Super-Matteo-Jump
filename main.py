import arcade, random

# Constants
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 360
WINDOW_TITLE = "Super Matteo Jump"
TILE_SCALING = 0.1
TILE_SPEED = 6
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.7
PLAYER_JUMP_SPEED = 17

class GameView(arcade.Window):
    """
    Main application class.
    """
    def update(self):
        self.center_x -= TILE_SPEED

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.platform_list = None
        self.obstacle_list = None

    def setup(self):

        self.player_texture = arcade.load_texture(
            "images/character/matteo_idle.png")

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 80
        self.player_sprite.scale = TILE_SCALING

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        self.obstacle_list = arcade.SpriteList()

        for x in range(0, WINDOW_WIDTH+64, 64):
            platform = arcade.Sprite("images/tiles/tile_1.png", scale=TILE_SCALING)
            platform.center_x = x
            platform.center_y = 52
            self.platform_list.append(platform)

        coordinate_list = [[512, 60], [256, 60], [768, 60]]
        for coordinate in coordinate_list:
            lawnmower = arcade.Sprite(
                "images/obstacles/lawn-mower.png", scale=TILE_SCALING*1.25)
            lawnmower.position = coordinate
            self.obstacle_list.append(lawnmower)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, platforms=self.platform_list, gravity_constant=GRAVITY
        )

        self.background_color = arcade.csscolor.LIGHT_SKY_BLUE

    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.platform_list.draw()
        self.obstacle_list.draw()

    def on_update(self, delta_time):

        self.physics_engine.update()

        for platform in self.platform_list:
            platform.center_x -= TILE_SPEED
            if platform.right < 0:
                platform.left = WINDOW_WIDTH

        collided = arcade.check_for_collision_with_list(
            self.player_sprite, self.obstacle_list
        )

        for _ in collided:
            print("hit a lawn mower")

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()