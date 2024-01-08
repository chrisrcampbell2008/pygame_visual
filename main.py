import pygame as pg
import math
import random
import colorsys


vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1600, 900
CENTER = vec2(WIDTH // 2 , HEIGHT // 2)
PASTEL_COLORS = [
    'gold', 'darkorange', 'tomato', 'mediumseagreen', 'mediumorchid', 'royalblue', 'dodgerblue',
    'deeppink', 'limegreen', 'darkslateblue', 'cyan', 'indianred', 'darkviolet', 'mediumturquoise',
    'salmon', 'darkolivegreen', 'deepskyblue', 'darkcyan', 'darkorchid', 'chartreuse', 'lightcoral',
    'olivedrab', 'skyblue', 'mediumaquamarine'
]
SCIFI_COLORS = [
    '#00FFD2', '#FF61A6', '#5A4FFA', '#FFD900', '#00BFFF', '#FF7E00', '#7FFF00', '#FFD700',
    '#00FA9A', '#C71585', '#483D8B', '#00CED1', '#FF4500', '#32CD32', '#8A2BE2', '#B8860B',
    '#1E90FF', '#6A5ACD', '#FF1493', '#8B4513', '#00FF00', '#20B2AA', '#556B2F'
]
FOREST_COLORS = [
    'darkolivegreen', 'olivedrab', 'forestgreen', 'green', 'darkgreen',
    'saddlebrown', 'sienna', 'peru', 'darkkhaki', 'darkseagreen',
    'mediumseagreen', 'olive', 'seagreen', 'mediumaquamarine', 'darkcyan'
]
FIERY_COLORS = [
    'red', 'orangered', 'darkorange', 'tomato', 'coral', 'darkred',
    'firebrick', 'crimson', 'maroon', 'indianred', 'brown', 'orangered',
    'sienna', 'chocolate'
]
DIVERSE_COLORS = [
    'cornflowerblue', 'darkslategray', 'darkviolet', 'mediumorchid', 'saddlebrown',
    'darkseagreen', 'teal', 'darkcyan', 'indigo', 'darkolivegreen',
    'chocolate', 'darkgoldenrod', 'midnightblue', 'slateblue', 'seagreen'
]
# IMAGE_PATH = "./Zeus_custom/note3.png"
STARS = ["./Zeus_custom/images/star2.png", "./Zeus_custom/images/star3.png", "./Zeus_custom/images/star4.png", "./Zeus_custom/images/star5.png", "./Zeus_custom/images/star6.png"]
MUSIC_NOTES = ["./Zeus_custom/music_notes/note3.png", "./Zeus_custom/music_notes/note4.png", "./Zeus_custom/music_notes/note5.png", "./Zeus_custom/music_notes/note6.png", "./Zeus_custom/music_notes/note7.png", "./Zeus_custom/music_notes/note8.png"]

## TOGGLES ##

NUM_STARS = 1500
# Z_DISTANCE toggle 20-100, default 40
Z_DISTANCE = 40
# 1 -> 200
ALPHA = 2
# -.1 -> .1
ROTATION_SPEED = 0
# (0.02, 0.05)
VELOCITY = (0.02, 0.05)
GLOBAL_STARS = True
PULSE_EFFECT = True
WIGGLING_EFFECT = False
MOUSE_ROTATION = False
SIN_ROTATION = False
SCALE_POS = 20
COLORS = [PASTEL_COLORS, SCIFI_COLORS, FOREST_COLORS, FIERY_COLORS, DIVERSE_COLORS]
OUTER_COLORS = DIVERSE_COLORS
INNER_COLORS = SCIFI_COLORS
# ("Circle", "Rectangle", "Line")
SHAPES = ["Circle", "Rectangle", "Line"]
INNER_SHAPE = "Circle"
OUTER_SHAPE = "Line"
# ("mix", "shape", "image")
OUTER_IMAGES = MUSIC_NOTES
INNER_IMAGES = STARS
OUTER_STARS = "shape"
INNER_STARS = "image"
OPPOSITE_ROTATION = True

class Star:
    def __init__(self, app, star_type, star_pos):
        self.screen = app.screen
        self.pos3d = self.get_pos3d(star_pos)
        self.vel = random.uniform(*VELOCITY)
        # self.vel = (random.uniform(0.05, 0.25)) if star_type == "image" else (random.uniform(0.25, 0.55))
        self.color = random.choice(INNER_COLORS) if star_pos == "inner" else random.choice(OUTER_COLORS)
        self.screen_pos = vec2(0, 0)
        self.size_image = .25
        self.size_shape = .01
        self.image = pg.image.load(random.choice(OUTER_IMAGES)).convert_alpha()
        self.inner_image = pg.image.load(random.choice(INNER_IMAGES)).convert_alpha()
        self.image_rect = self.image.get_rect()
        self.star_type = star_type
        self.star_pos = star_pos
        self.wiggle_offset = random.uniform(0, 2 * math.pi)

    # def get_pos3d(self, star_pos):
    #     angle = random.uniform(0, 2 * math.pi)

    #     if (GLOBAL_STARS):
    #         radius = random.randrange(HEIGHT // SCALE_POS, HEIGHT) * SCALE_POS
    #     elif (star_pos == "outer"):
    #         radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * SCALE_POS
    #     else:
    #         radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * (SCALE_POS // 4)

    #     x = radius * math.sin(angle)
    #     y = radius * math.cos(angle) 
    #     return vec3(x, y, Z_DISTANCE)
        
    def get_pos3d(self, star_pos, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)

        if (GLOBAL_STARS):
            radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        elif (star_pos == "outer"):
            radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        else:
            radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * (scale_pos // 4)

        x = radius * math.sin(angle)
        y = radius * math.cos(angle) 
        return vec3(x, y, Z_DISTANCE)
    
    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d(self.star_pos) if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size_image = Z_DISTANCE / self.pos3d.z * .05
        self.size_shape = (Z_DISTANCE - self.pos3d.z) / (.02 * self.pos3d.z) * .25

        if (PULSE_EFFECT):
            time_elapsed = pg.time.get_ticks() / 1000
            pulsating_frequency = 3.0
            pulsating_amplitude_shape = .5 
            decay_factor = 0.95  # Adjust the decay factor to smooth out the pulsation
            pulsating_factor_shape = 0.5 * math.sin(self.pos3d.z / 20 + pulsating_frequency * time_elapsed) + 1.5
            self.size_shape = (Z_DISTANCE - self.pos3d.z) / (0.02 * self.pos3d.z) * 0.25 * pulsating_factor_shape * pulsating_amplitude_shape
            self.size_shape *= decay_factor        

        if (OPPOSITE_ROTATION):
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_SPEED if self.star_pos != "inner" else -ROTATION_SPEED)
            self.pos3d.xy = self.pos3d.xy.rotate(.05)

            if (MOUSE_ROTATION):
                mouse_pos = CENTER - vec2(pg.mouse.get_pos())
                self.screen_pos += mouse_pos
        
        if SIN_ROTATION:
            time_elapsed = pg.time.get_ticks() / 1000
            oscillation_amplitude = 200
            oscillation_frequency = 0.0001
            rotation_angle = math.sin(time_elapsed * oscillation_frequency) * oscillation_amplitude
            rotated_pos = self.rotate_vector(self.screen_pos, rotation_angle)
            self.screen_pos = rotated_pos

        if (WIGGLING_EFFECT):
            wiggle_amplitude = 30
            wiggle_frequency = 0.01
            self.screen_pos.x += math.sin(self.wiggle_offset) * wiggle_amplitude
            self.screen_pos.y += math.cos(self.wiggle_offset) * wiggle_amplitude
            self.wiggle_offset += wiggle_frequency

    # USED FOR SIN ROTATION
    def rotate_vector(self, vector, angle):
        rotated_x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
        rotated_y = vector.x * math.sin(angle) + vector.y * math.cos(angle)
        return vec2(rotated_x, rotated_y)
    
    def draw(self):
        if (self.star_type == "image"):
            if (self.star_pos == "outer"):
                image = self.image
                scaled_width = int(image.get_width() * self.size_image)
                scaled_height = int(image.get_height() * self.size_image)
                scaled_image = pg.transform.scale(image, (scaled_width, scaled_height))
            else:
                image = self.inner_image
                scaled_width = int(image.get_width() * self.size_image) // 2
                scaled_height = int(image.get_height() * self.size_image) // 2
                scaled_image = pg.transform.scale(image, (scaled_width, scaled_height))
            
            self.image_rect.topleft = self.screen_pos - vec2(image.get_width() // 8, image.get_height() // 8)
            self.screen.blit(scaled_image, self.image_rect)
        else:
            if (self.star_pos == "outer"):
                if (OUTER_SHAPE == "Rectangle"):
                    pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size_shape, self.size_shape))
                elif (OUTER_SHAPE == "Circle"):
                    pg.draw.circle(self.screen, self.color, self.screen_pos, int(self.size_shape // 2), int(self.size_shape // 2))
                else:
                    pg.draw.line(self.screen, self.color, self.screen_pos, self.screen_pos, 1)
            else:
                if (INNER_SHAPE == "Rectangle"):
                    pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size_shape // 2, self.size_shape // 2))
                elif (INNER_SHAPE == "Circle"):
                    pg.draw.circle(self.screen, self.color, self.screen_pos, int(self.size_shape // 4), int(self.size_shape // 4))
                else:
                    pg.draw.line(self.screen, self.color, self.screen_pos, self.screen_pos, 1)

class Starfield:
    def __init__(self, app):
        self.initialize_stars(app)

    def initialize_stars(self, app):
        self.outer_stars = self.create_stars(app, OUTER_STARS, "outer", 1)
        self.inner_stars = self.create_stars(app, INNER_STARS, "inner", 6)

    def refresh_stars(self, app):
        global OUTER_STARS, INNER_STARS
        self.initialize_stars(app)

    def create_stars(self, app, star_type, position, division_factor):
        if star_type == "mix":
            return [Star(app, "image" if i % 2 == 0 else "shape", position) for i in range(NUM_STARS)]
        elif star_type == "image":
            return [Star(app, "image", position) for _ in range(NUM_STARS // division_factor)]
        else:
            return [Star(app, "shape", position) for _ in range(NUM_STARS // division_factor)]

    def run(self, app):
        global WIGGLING_EFFECT, SIN_ROTATION, OUTER_COLORS, INNER_COLORS, SCALE_POS, ROTATION_SPEED, ALPHA, OUTER_SHAPE, INNER_SHAPE, GLOBAL_STARS, COLORS, NUM_STARS, Z_DISTANCE, VELOCITY, PULSE_EFFECT, MOUSE_ROTATION, OUTER_COLORS, OUTER_IMAGES, INNER_COLORS, INNER_IMAGES, INNER_SHAPE, OUTER_STARS, INNER_STARS, SHAPES, OPPOSITE_ROTATION

        keys = pg.key.get_pressed()
        if keys[pg.K_0]:
            WIGGLING_EFFECT = not WIGGLING_EFFECT
            SIN_ROTATION = not SIN_ROTATION
            GLOBAL_STARS = True
            self.refresh_stars(app)
        if keys[pg.K_1]:
            NUM_STARS = 1500
            # Z_DISTANCE toggle 20-100, default 40
            Z_DISTANCE = 40
            # 1 -> 200
            ALPHA = 1
            # -.1 -> .1
            ROTATION_SPEED = 0
            # (0.02, 0.05)
            VELOCITY = (0.02, 0.05)
            GLOBAL_STARS = True
            PULSE_EFFECT = True
            WIGGLING_EFFECT = False
            MOUSE_ROTATION = False
            SIN_ROTATION = False
            SCALE_POS = 20
            COLORS = [PASTEL_COLORS, SCIFI_COLORS, FOREST_COLORS, FIERY_COLORS, DIVERSE_COLORS]
            OUTER_COLORS = DIVERSE_COLORS
            INNER_COLORS = SCIFI_COLORS
            # ("Circle", "Rectangle", "Line")
            SHAPES = ["Circle", "Rectangle", "Line"]
            INNER_SHAPE = "Circle"
            OUTER_SHAPE = "Line"
            # ("mix", "shape", "image")
            OUTER_IMAGES = MUSIC_NOTES
            INNER_IMAGES = STARS
            OUTER_STARS = "shape"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = True
            self.refresh_stars(app)
        if keys[pg.K_2]:
            NUM_STARS = 4000
            Z_DISTANCE = 40
            ALPHA = 1
            ROTATION_SPEED = .2
            VELOCITY = (0.04, 0.07)
            GLOBAL_STARS = True
            PULSE_EFFECT = True
            WIGGLING_EFFECT = True
            MOUSE_ROTATION = False
            SIN_ROTATION = False
            SCALE_POS = 10
            COLORS = [PASTEL_COLORS, SCIFI_COLORS, FOREST_COLORS, FIERY_COLORS, DIVERSE_COLORS]
            OUTER_COLORS = DIVERSE_COLORS
            INNER_COLORS = PASTEL_COLORS
            SHAPES = ["Circle", "Rectangle", "Line"]
            INNER_SHAPE = "Line"
            OUTER_SHAPE = "Line"
            OUTER_IMAGES = MUSIC_NOTES
            INNER_IMAGES = STARS
            OUTER_STARS = "shape"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = True
            self.refresh_stars(app)
            print("After setting to False:", SIN_ROTATION)
        if keys[pg.K_3]:
            NUM_STARS=1500
            Z_DISTANCE=50
            ALPHA=150
            ROTATION_SPEED=3
            VELOCITY=(0.06, 0.1)
            GLOBAL_STARS=False
            PULSE_EFFECT=True
            WIGGLING_EFFECT=False
            MOUSE_ROTATION=False
            SIN_ROTATION=False
            SCALE_POS=20
            OUTER_COLORS = SCIFI_COLORS
            INNER_COLORS = DIVERSE_COLORS
            OUTER_IMAGES=STARS
            INNER_IMAGES=MUSIC_NOTES
            OUTER_STARS="mix"
            INNER_STARS="mix"
            OPPOSITE_ROTATION = False
            self.refresh_stars(app)
        if keys[pg.K_4]:
            NUM_STARS=1500
            Z_DISTANCE=50
            ALPHA=10
            ROTATION_SPEED=.1
            VELOCITY=(0.05, 0.08)
            GLOBAL_STARS=False
            PULSE_EFFECT=True
            WIGGLING_EFFECT=True
            MOUSE_ROTATION=True
            SIN_ROTATION=True
            SCALE_POS=35
            OUTER_IMAGES=STARS
            INNER_IMAGES=MUSIC_NOTES
            OUTER_STARS="image"
            INNER_STARS="image"
            OPPOSITE_ROTATION = False
            self.refresh_stars(app)
        if keys[pg.K_5]:
            NUM_STARS = 1500
            Z_DISTANCE = 40
            ALPHA = 1
            ROTATION_SPEED = .1
            VELOCITY = (0.02, 0.05)
            GLOBAL_STARS = False
            PULSE_EFFECT = True
            WIGGLING_EFFECT = False
            MOUSE_ROTATION = False
            SIN_ROTATION = True
            SCALE_POS = 20
            COLORS = [PASTEL_COLORS, SCIFI_COLORS, FOREST_COLORS, FIERY_COLORS, DIVERSE_COLORS]
            OUTER_COLORS = FIERY_COLORS
            INNER_COLORS = PASTEL_COLORS
            SHAPES = ["Circle", "Rectangle", "Line"]
            INNER_SHAPE = "Circle"
            OUTER_SHAPE = "Line"
            OUTER_IMAGES = MUSIC_NOTES
            INNER_IMAGES = STARS
            OUTER_STARS = "mix"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = True
            self.refresh_stars(app)
        if keys[pg.K_UP]:
            SCALE_POS -= 1
        if keys[pg.K_DOWN]:
            SCALE_POS += 1
        SCALE_POS = max(20, min(40, SCALE_POS))

        if keys[pg.K_LEFT]:
            ROTATION_SPEED -= .01
            # ROTATION_SPEED = max(-0.1, min(0.1, ROTATION_SPEED))
        if keys[pg.K_RIGHT]:
            ROTATION_SPEED += .01
            # ROTATION_SPEED = max(-0.1, min(0.1, ROTATION_SPEED))
        
        # ALPHA = max(1, min(200, ALPHA))
        # ANGLE_MOD = max(1,min(2, ANGLE_MOD))

        all_stars = self.outer_stars + self.inner_stars
        [star.update() for star in all_stars]
        all_stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in all_stars]

# PYTHON SETUP
class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
    
    def update_alpha_surface(self):
        self.starfield.update_alpha(self)

    def run(self, app):
        while True:
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run(app)

            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)

if __name__ == '__main__':
    app = App()
    app.run(app)

