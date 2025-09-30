import arcade, random

# Constants
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 360
WINDOW_TITLE = "Super Matteo Jump"
TILE_SCALING = 0.1
TILE_SPEED = 8
GRAVITY = 0.7
PLAYER_JUMP_SPEED = 17

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self._spawn_timer = 0

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.platform_list = None
        self.obstacle_list = None
        self.obstacle = None
        self.difficulty = 1
        self.score = 1

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
        self.obstacle_list = arcade.SpriteList(use_spatial_hash=True)

        for x in range(0, WINDOW_WIDTH+64, 64):
            platform = arcade.Sprite("images/tiles/tile_1.png", scale=TILE_SCALING)
            platform.center_x = x
            platform.center_y = 52
            self.platform_list.append(platform)

        self.obstacle_list = arcade.SpriteList()
        self.obstacles_data = [
            ("lawn-mower.png", TILE_SCALING * 1.7, 74),
            ("water.png", TILE_SCALING, 52),
            ("doggy.png", TILE_SCALING, 70),
            ("bird.png", TILE_SCALING, 170)
        ]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, platforms=self.platform_list, gravity_constant=GRAVITY
        )

        self.background_color = arcade.csscolor.LIGHT_SKY_BLUE

    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.platform_list.draw()
        self.obstacle_list.draw()

        arcade.draw_text(
            f"{int(self.score):05}",
            WINDOW_WIDTH * 0.98,
            WINDOW_HEIGHT * 0.95,
            arcade.color.BLACK,
            18,
            anchor_x="right",
            anchor_y="top"
        )

    def on_update(self, delta_time):

        self.score += delta_time * self.difficulty * 15

        if self.difficulty < 3.5:
            self.difficulty += 0.03 * delta_time

        self._spawn_timer += delta_time
        if self._spawn_timer > 1:
            print(self._spawn_timer)
            self._spawn_timer = 0
            filename, scale, y = random.choice(self.obstacles_data)
            obs = arcade.Sprite("images/obstacles/" + filename, scale=scale)
            obs.center_x = WINDOW_WIDTH + 50
            obs.center_y = y
            self.obstacle_list.append(obs)

        for platform in self.platform_list:
            platform.center_x -= TILE_SPEED * self.difficulty
            if platform.right < 0:
                platform.left = WINDOW_WIDTH

        for lawnmower in self.obstacle_list:
            lawnmower.center_x -= TILE_SPEED * self.difficulty
            if lawnmower.right <0:
                pass

        collided = arcade.check_for_collision_with_list(
            self.player_sprite, self.obstacle_list
        )

        self.physics_engine.update()

        for _ in collided:
            print("hit a lawn mower")

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        pass

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()