import pygame as pg
import math
import random
import colorsys

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1600, 900
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
SCIFI_SPACE_COLORS = [
    '#00FFD2', '#FF61A6', '#5A4FFA', '#FFD900', '#00BFFF', '#FF7E00', '#7FFF00', '#FFD700',
    '#00FA9A', '#C71585', '#483D8B', '#00CED1', '#FF4500', '#32CD32', '#8A2BE2', '#B8860B',
    '#1E90FF', '#6A5ACD', '#FF1493', '#8B4513', '#00FF00', '#20B2AA', '#556B2F'
]
Z_DISTANCE = 40
IMAGES = ["./DanD/images/blb.png", "./DanD/images/star2.png", "./DanD/images/star3.png",
          "./DanD/images/star4.png", "./DanD/images/star5.png", "./DanD/images/star6.png"]
MUSIC_NOTES = ["./DanD/music_notes/note3.png", "./DanD/music_notes/note4.png", "./DanD/music_notes/note5.png",
               "./DanD/music_notes/note6.png", "./DanD/music_notes/note7.png", "./DanD/music_notes/note8.png"]
ALPHA = 10

class Star:
    def __init__(self, app, star_type):
        self.screen = app.screen
        self.pos3d = self.get_pos3d(star_type)
        self.vel = random.uniform(0.01, 0.05)
        self.color = random.choice(SCIFI_SPACE_COLORS)
        self.screen_pos = vec2(0, 0)
        self.size_image = 0.25
        self.size_shape = 0.01
        self.image = pg.image.load(random.choice(MUSIC_NOTES)).convert_alpha()
        self.center_image = pg.image.load(random.choice(IMAGES)).convert_alpha()
        self.image_rect = self.image.get_rect()
        self.star_type = star_type
        self.wiggle_offset = random.uniform(0, 2 * math.pi)

    def get_pos3d(self, star_type, scale_pos=20):
        angle = random.uniform(0, 2 * math.pi)
        if star_type == "rectangle" or star_type == "image":
            radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        else:
            radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * (scale_pos // 4)
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d(self.star_type) if self.pos3d.z < 1 else self.pos3d
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size_image = Z_DISTANCE / self.pos3d.z * 0.05
        self.size_shape = (Z_DISTANCE - self.pos3d.z) / (0.02 * self.pos3d.z) * 0.25

        # Add wiggling effect
        wiggle_amplitude = 3
        wiggle_frequency = 0.05
        self.screen_pos.x += math.sin(self.wiggle_offset) * wiggle_amplitude
        self.screen_pos.y += math.cos(self.wiggle_offset) * wiggle_amplitude
        self.wiggle_offset += wiggle_frequency

    def draw(self):
        if self.star_type == "image" or self.star_type == "center":
            image = self.image if self.star_type == "image" else self.center_image
            scaled_width = int(image.get_width() * self.size_image)
            scaled_height = int(image.get_height() * self.size_image)
            scaled_image = pg.transform.scale(image, (scaled_width, scaled_height))
            self.image_rect.topleft = self.screen_pos - vec2(image.get_width() // 8, image.get_height() // 8)
            self.screen.blit(scaled_image, self.image_rect)
        else:
            pg.draw.circle(self.screen, self.color, self.screen_pos, int(self.size_shape // 2), int(self.size_shape // 2))

class Starfield:
    def __init__(self, app):
        self.stars = [Star(app, "image" if i % 2 == 0 else "rectangle") for i in range(NUM_STARS)]
        self.center_stars = [Star(app, "center") for i in range(NUM_STARS // 5)]

    def run(self):
        all_stars = self.stars + self.center_stars
        [star.update() for star in all_stars]
        all_stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in all_stars]

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)

    def run(self):
        while True:
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()
            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)

if __name__ == '__main__':
    app = App()
    app.run()
