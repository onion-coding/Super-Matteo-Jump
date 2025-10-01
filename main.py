import arcade, random

# Constants
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 360
WINDOW_TITLE = "Super Matteo Jump"
TILE_SCALING = 0.1
TILE_SPEED = 8
GRAVITY = 0.7
PLAYER_JUMP_SPEED = 17

class Player():
    def __init__(self):
        pass

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None
        self.platform_list = None
        self.obstacle_list = None
        self.obstacle = None
        self.obstacles_data = None
        self.physics_engine = None
        self.game_over = False

    def setup(self):

        self.player_texture = arcade.load_texture(
            "images/character/matteo_idle.png")

        self._last_filename = None
        self._repeat_count = 0

        self._next_spawn_time = 0
        self._spawn_timer = 0
        self.difficulty = 1
        self.score = 1

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

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                             arcade.color.RED, 50, anchor_x="center", anchor_y="center")

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

        if not self.game_over:
            self.physics_engine.update()

            self.score += delta_time * self.difficulty * 15

            if self.difficulty < 3.5:
                self.difficulty += 0.03 * delta_time

            self._spawn_timer += delta_time
            if self._spawn_timer > self._next_spawn_time:
                self._spawn_timer = 0
                self._next_spawn_time = random.uniform(0.8, 2)

                filename, scale, y = random.choice(self.obstacles_data)

                if filename == self._last_filename:
                    self._repeat_count += 1
                    if self._repeat_count >= 3:
                        while filename == self._last_filename:
                            filename, scale, y = random.choice(self.obstacles_data)
                        self._repeat_count = 0
                else:
                    self._repeat_count = 0
                self._last_filename = filename

                if filename == "bird.png":
                    y = random.choice([80, 170, 230])
                obs = arcade.Sprite("images/obstacles/" + filename, scale=scale)
                obs.center_x = WINDOW_WIDTH + 50
                obs.center_y = y
                self.obstacle_list.append(obs)

                if filename == "water.png":
                    if self.difficulty < 2:
                        block_count = random.randint(1, 3)
                    elif self.difficulty < 3:
                        block_count = random.randint(2, 4)
                    elif self.difficulty < 3.49:
                        block_count = random.randint(3, 5)
                    else:
                        block_count = random.randint(4, 6)

                    print("blocks:", block_count)

                    for i in range(block_count):
                        obs = arcade.Sprite("images/obstacles/water.png", scale=scale)
                        obs.center_x = WINDOW_WIDTH + 50 + (obs.width * i)
                        obs.center_y = y
                        self.obstacle_list.append(obs)

                else:
                    obs = arcade.Sprite("images/obstacles/" + filename, scale=scale)
                    obs.center_x = WINDOW_WIDTH + 50
                    obs.center_y = y
                    self.obstacle_list.append(obs)

            for obs in self.obstacle_list:
                obs.center_x -= TILE_SPEED * self.difficulty

            for platform in self.platform_list:
                platform.center_x -= TILE_SPEED * self.difficulty

            # check leftmost platform
            rightmost = max(p.right for p in self.platform_list)
            for platform in self.platform_list:
                if platform.right < 0:
                    platform.left = rightmost
                    rightmost = platform.right

            collided = arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list)
            if collided:
                self.game_over = True

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_JUMP_SPEED // 2

        if self.game_over:
            self.setup()
            self.game_over = False

    def on_key_release(self, key, modifiers):
        pass

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()