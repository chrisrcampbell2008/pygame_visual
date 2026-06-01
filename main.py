import pygame as pg
import math
import random
import glob
import os


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
SPACE_COLORS = [
    # mostly white — weighted toward neutral
    (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
    # blue-white (O/B type)
    (200, 220, 255), (210, 228, 255), (185, 210, 255),
    # warm white / yellow-white (A/F type)
    (255, 252, 230), (255, 248, 210), (255, 245, 200),
    # pale orange (K type)
    (255, 228, 185), (255, 218, 170),
]
STARS = ["./images/star2.png", "./images/star3.png", "./images/star4.png", "./images/star5.png", "./images/star6.png"]
MUSIC_NOTES = ["./music_notes/note3.png", "./music_notes/note4.png", "./music_notes/note5.png", "./music_notes/note6.png", "./music_notes/note7.png", "./music_notes/note8.png"]
SPACE_IMAGE_FILES = sorted(glob.glob("./space_images/processed/*.png"))

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
MAX_SHAPE_SIZE = 9999
SPEED_MULTIPLIER = 1.0
MOUSE_VANISHING_POINT = False
NUM_NEBULAE = 0
FLARE_STARS = False
FLIGHT_ANGLE = vec2(0, 0)
ROTATION_FLIGHT = False

# Images loaded once from disk; scaled surfaces cached by (surface id, w, h)
_IMAGE_CACHE = {}
_SCALE_CACHE = {}

def get_image(path):
    if path not in _IMAGE_CACHE:
        _IMAGE_CACHE[path] = pg.image.load(path).convert_alpha()
    return _IMAGE_CACHE[path]

def get_scaled(surface, w, h):
    key = (id(surface), w, h)
    if key not in _SCALE_CACHE:
        _SCALE_CACHE[key] = pg.transform.scale(surface, (w, h))
    return _SCALE_CACHE[key]


class Star:
    def __init__(self, app, star_type, star_pos):
        self.screen = app.screen
        self.pos3d = self.get_pos3d(star_pos)
        self.vel = random.uniform(*VELOCITY)
        self.color = random.choice(INNER_COLORS) if star_pos == "inner" else random.choice(OUTER_COLORS)
        self.screen_pos = vec2(0, 0)
        self.size_image = .25
        self.size_shape = .01
        image_list = OUTER_IMAGES if star_pos == "outer" else INNER_IMAGES
        self.image = get_image(random.choice(image_list))
        self.image_rect = self.image.get_rect()
        self.star_type = star_type
        self.star_pos = star_pos
        self.wiggle_offset = random.uniform(0, 2 * math.pi)
        self.is_flare = FLARE_STARS and random.random() < 0.10

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

    def update(self, time_elapsed):
        if ROTATION_FLIGHT:
            yaw   = FLIGHT_ANGLE.x * math.pi / 2
            pitch = FLIGHT_ANGLE.y * math.pi / 2
            cy, sy = math.cos(yaw), math.sin(yaw)
            cp, sp = math.cos(pitch), math.sin(pitch)
            v = self.vel * SPEED_MULTIPLIER
            self.pos3d.x -= sy * cp * v
            self.pos3d.y += sp * v
            self.pos3d.z -= cy * cp * v
            depth = sy * cp * self.pos3d.x - sp * self.pos3d.y + cy * cp * self.pos3d.z
            if depth < 1 or self.pos3d.z < 0.5:
                self.pos3d = self.get_pos3d(self.star_pos)
        else:
            self.pos3d.z -= self.vel * SPEED_MULTIPLIER
            self.pos3d = self.get_pos3d(self.star_pos) if self.pos3d.z < 1 else self.pos3d

        vp = CENTER + vec2(FLIGHT_ANGLE.x * 280, FLIGHT_ANGLE.y * 180) if (MOUSE_VANISHING_POINT and not ROTATION_FLIGHT) else CENTER
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / max(self.pos3d.z, 0.5) + vp

        self.size_image = Z_DISTANCE / self.pos3d.z * .05
        self.size_shape = (Z_DISTANCE - self.pos3d.z) / (.02 * self.pos3d.z) * .25

        if (PULSE_EFFECT):
            pulsating_factor_shape = 0.5 * math.sin(self.pos3d.z / 20 + 3.0 * time_elapsed) + 1.5
            self.size_shape = (Z_DISTANCE - self.pos3d.z) / (0.02 * self.pos3d.z) * 0.25 * pulsating_factor_shape * 0.5
            self.size_shape *= 0.95

        self.size_shape = min(self.size_shape, MAX_SHAPE_SIZE)

        if (OPPOSITE_ROTATION):
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_SPEED if self.star_pos != "inner" else -ROTATION_SPEED)
            self.pos3d.xy = self.pos3d.xy.rotate(.05)

            if (MOUSE_ROTATION):
                mouse_pos = CENTER - vec2(pg.mouse.get_pos())
                self.screen_pos += mouse_pos

        if SIN_ROTATION:
            rotation_angle = math.sin(time_elapsed * 0.0001) * 50
            rotated_pos = self.rotate_vector(self.screen_pos, rotation_angle)
            self.screen_pos = rotated_pos

        if (WIGGLING_EFFECT):
            wiggle_amplitude = 30
            self.screen_pos.x += math.sin(self.wiggle_offset) * wiggle_amplitude
            self.screen_pos.y += math.cos(self.wiggle_offset) * wiggle_amplitude
            self.wiggle_offset += 0.01

    def rotate_vector(self, vector, angle):
        rotated_x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
        rotated_y = vector.x * math.sin(angle) + vector.y * math.cos(angle)
        return vec2(rotated_x, rotated_y)

    def draw(self):
        if self.is_flare:
            cx, cy = int(self.screen_pos.x), int(self.screen_pos.y)
            arm = max(1, int(self.size_shape))
            diag = max(1, arm // 2)
            pg.draw.line(self.screen, 'white', (cx - arm, cy), (cx + arm, cy), 1)
            pg.draw.line(self.screen, 'white', (cx, cy - arm), (cx, cy + arm), 1)
            pg.draw.line(self.screen, 'white', (cx - diag, cy - diag), (cx + diag, cy + diag), 1)
            pg.draw.line(self.screen, 'white', (cx - diag, cy + diag), (cx + diag, cy - diag), 1)
            return
        if (self.star_type == "image"):
            if (self.star_pos == "outer"):
                w = max(1, int(self.image.get_width() * self.size_image))
                h = max(1, int(self.image.get_height() * self.size_image))
            else:
                w = max(1, int(self.image.get_width() * self.size_image) // 2)
                h = max(1, int(self.image.get_height() * self.size_image) // 2)
            scaled_image = get_scaled(self.image, w, h)
            self.image_rect.topleft = self.screen_pos - vec2(self.image.get_width() // 8, self.image.get_height() // 8)
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

class Nebula:
    def __init__(self, app, z_override=None, angle_sector=None):
        self.screen = app.screen
        self.vel = random.uniform(0.03, 0.07)
        self.image = get_image(random.choice(SPACE_IMAGE_FILES))
        self.screen_pos = vec2(0, 0)
        self.size = 0.1
        self.angle_sector = angle_sector  # (base_angle, width) or None
        self.pos3d = self._spawn(z_override)

    def _spawn(self, z=None):
        if self.angle_sector:
            base, width = self.angle_sector
            angle = base + random.uniform(0, width)
        else:
            angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 20, HEIGHT) * 20
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, z if z is not None else random.uniform(Z_DISTANCE * 0.7, Z_DISTANCE))

    def update(self, _time_elapsed):
        if ROTATION_FLIGHT:
            yaw   = FLIGHT_ANGLE.x * math.pi / 2
            pitch = FLIGHT_ANGLE.y * math.pi / 2
            cy, sy = math.cos(yaw), math.sin(yaw)
            cp, sp = math.cos(pitch), math.sin(pitch)
            v = self.vel * SPEED_MULTIPLIER
            self.pos3d.x -= sy * cp * v
            self.pos3d.y += sp * v
            self.pos3d.z -= cy * cp * v
            depth = sy * cp * self.pos3d.x - sp * self.pos3d.y + cy * cp * self.pos3d.z
            if depth < 1 or self.pos3d.z < 0.5:
                self.pos3d = self._spawn(z=random.uniform(Z_DISTANCE * 0.7, Z_DISTANCE))
                self.image = get_image(random.choice(SPACE_IMAGE_FILES))
        else:
            self.pos3d.z -= self.vel * SPEED_MULTIPLIER
            if self.pos3d.z < 1:
                self.pos3d = self._spawn(z=random.uniform(Z_DISTANCE * 0.7, Z_DISTANCE))
                self.image = get_image(random.choice(SPACE_IMAGE_FILES))

        vp = CENTER + vec2(FLIGHT_ANGLE.x * 280, FLIGHT_ANGLE.y * 180) if (MOUSE_VANISHING_POINT and not ROTATION_FLIGHT) else CENTER
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / max(self.pos3d.z, 0.5) + vp
        self.size = Z_DISTANCE / self.pos3d.z * 0.22

    def draw(self):
        w = max(1, int(self.image.get_width() * self.size))
        h = max(1, int(self.image.get_height() * self.size))
        scaled = get_scaled(self.image, w, h)
        rect = scaled.get_rect(center=(int(self.screen_pos.x), int(self.screen_pos.y)))
        self.screen.blit(scaled, rect)


class Starfield:
    def __init__(self, app):
        self.initialize_stars(app)

    def initialize_stars(self, app):
        self.outer_stars = self.create_stars(app, OUTER_STARS, "outer", 1)
        self.inner_stars = self.create_stars(app, INNER_STARS, "inner", 6)
        # Stagger nebulae evenly across z so they don't all arrive at once
        if NUM_NEBULAE > 0:
            z_step = Z_DISTANCE / NUM_NEBULAE
            a_step = 2 * math.pi / NUM_NEBULAE
            self.nebulae = [
                Nebula(app,
                       z_override=z_step * i + random.uniform(0, z_step),
                       angle_sector=(a_step * i, a_step))
                for i in range(NUM_NEBULAE)
            ]
        else:
            self.nebulae = []

    def refresh_stars(self, app):
        self.initialize_stars(app)

    def create_stars(self, app, star_type, position, division_factor):
        if star_type == "mix":
            return [Star(app, "image" if i % 2 == 0 else "shape", position) for i in range(NUM_STARS)]
        elif star_type == "image":
            return [Star(app, "image", position) for _ in range(NUM_STARS // division_factor)]
        else:
            return [Star(app, "shape", position) for _ in range(NUM_STARS // division_factor)]

    def run(self, app):
        global WIGGLING_EFFECT, SIN_ROTATION, OUTER_COLORS, INNER_COLORS, SCALE_POS, ROTATION_SPEED, ALPHA, OUTER_SHAPE, INNER_SHAPE, GLOBAL_STARS, COLORS, NUM_STARS, Z_DISTANCE, VELOCITY, PULSE_EFFECT, MOUSE_ROTATION, OUTER_COLORS, OUTER_IMAGES, INNER_COLORS, INNER_IMAGES, INNER_SHAPE, OUTER_STARS, INNER_STARS, SHAPES, OPPOSITE_ROTATION, SPACE_COLORS, MAX_SHAPE_SIZE, SPEED_MULTIPLIER, MOUSE_VANISHING_POINT, NUM_NEBULAE, FLARE_STARS, ROTATION_FLIGHT

        keys = pg.key.get_pressed()
        if keys[pg.K_0]:
            WIGGLING_EFFECT = not WIGGLING_EFFECT
            SIN_ROTATION = not SIN_ROTATION
            GLOBAL_STARS = True
            self.refresh_stars(app)
        if keys[pg.K_1]:
            ROTATION_FLIGHT = False
            NUM_STARS = 2000
            Z_DISTANCE = 40
            ALPHA = 4
            ROTATION_SPEED = 0
            VELOCITY = (0.06, 0.18)
            GLOBAL_STARS = True
            PULSE_EFFECT = False
            WIGGLING_EFFECT = False
            MOUSE_ROTATION = False
            SIN_ROTATION = False
            SCALE_POS = 20
            OUTER_COLORS = SPACE_COLORS
            INNER_COLORS = SPACE_COLORS
            INNER_SHAPE = "Circle"
            OUTER_SHAPE = "Circle"
            OUTER_STARS = "shape"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = False
            MAX_SHAPE_SIZE = 2
            SPEED_MULTIPLIER = 0.3
            MOUSE_VANISHING_POINT = True
            NUM_NEBULAE = 12
            FLARE_STARS = True
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
            self.refresh_stars(app)
        if keys[pg.K_2]:
            MAX_SHAPE_SIZE = 9999
            SPEED_MULTIPLIER = 1.0
            MOUSE_VANISHING_POINT = False
            NUM_NEBULAE = 0
            FLARE_STARS = False
            ROTATION_FLIGHT = False
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
            NUM_STARS = 8000
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
        if keys[pg.K_3]:
            MAX_SHAPE_SIZE = 9999
            SPEED_MULTIPLIER = 1.0
            MOUSE_VANISHING_POINT = False
            NUM_NEBULAE = 0
            FLARE_STARS = False
            ROTATION_FLIGHT = False
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
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
            MAX_SHAPE_SIZE = 9999
            SPEED_MULTIPLIER = 1.0
            MOUSE_VANISHING_POINT = False
            NUM_NEBULAE = 0
            FLARE_STARS = False
            ROTATION_FLIGHT = False
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
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
            MAX_SHAPE_SIZE = 9999
            SPEED_MULTIPLIER = 1.0
            MOUSE_VANISHING_POINT = False
            NUM_NEBULAE = 0
            FLARE_STARS = False
            ROTATION_FLIGHT = False
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
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
        if MOUSE_VANISHING_POINT:
            mouse_pos = vec2(pg.mouse.get_pos())
            FLIGHT_ANGLE.x = (mouse_pos.x - CENTER.x) / CENTER.x
            FLIGHT_ANGLE.y = (mouse_pos.y - CENTER.y) / CENTER.y
            if keys[pg.K_COMMA]:
                SPEED_MULTIPLIER = max(0.1, SPEED_MULTIPLIER - 0.05)
            if keys[pg.K_PERIOD]:
                SPEED_MULTIPLIER = min(10.0, SPEED_MULTIPLIER + 0.05)
        else:
            if keys[pg.K_UP]:
                SCALE_POS -= 1
            if keys[pg.K_DOWN]:
                SCALE_POS += 1
            SCALE_POS = max(1, min(100, SCALE_POS))
            if keys[pg.K_LEFT]:
                ROTATION_SPEED -= .01
            if keys[pg.K_RIGHT]:
                ROTATION_SPEED += .01
        if keys[pg.K_6]:
            ROTATION_FLIGHT = False
            MAX_SHAPE_SIZE = 9999
            SPEED_MULTIPLIER = 1.0
            MOUSE_VANISHING_POINT = False
            NUM_NEBULAE = 0
            FLARE_STARS = False
            ROTATION_FLIGHT = False
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
            NUM_STARS = 1500
            Z_DISTANCE = 40
            ALPHA = 1
            ROTATION_SPEED = 0
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
            SHAPES = ["Circle", "Rectangle", "Line"]
            INNER_SHAPE = "Circle"
            OUTER_SHAPE = "Line"
            OUTER_IMAGES = MUSIC_NOTES
            INNER_IMAGES = STARS
            OUTER_STARS = "shape"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = True
            self.refresh_stars(app)

        if keys[pg.K_7]:
            NUM_STARS = 2000
            Z_DISTANCE = 40
            ALPHA = 4
            ROTATION_SPEED = 0
            VELOCITY = (0.06, 0.18)
            GLOBAL_STARS = True
            PULSE_EFFECT = False
            WIGGLING_EFFECT = False
            MOUSE_ROTATION = False
            SIN_ROTATION = False
            SCALE_POS = 20
            OUTER_COLORS = SPACE_COLORS
            INNER_COLORS = SPACE_COLORS
            INNER_SHAPE = "Circle"
            OUTER_SHAPE = "Circle"
            OUTER_STARS = "shape"
            INNER_STARS = "shape"
            OPPOSITE_ROTATION = False
            MAX_SHAPE_SIZE = 2
            SPEED_MULTIPLIER = 0.3
            MOUSE_VANISHING_POINT = True
            NUM_NEBULAE = 12
            FLARE_STARS = True
            ROTATION_FLIGHT = True
            FLIGHT_ANGLE.x = 0
            FLIGHT_ANGLE.y = 0
            self.refresh_stars(app)

        time_elapsed = pg.time.get_ticks() / 1000
        all_stars = self.outer_stars + self.inner_stars
        for star in all_stars:
            star.update(time_elapsed)
        for nebula in self.nebulae:
            nebula.update(time_elapsed)
        all_objects = all_stars + self.nebulae
        all_objects.sort(key=lambda o: o.pos3d.z, reverse=True)
        for obj in all_objects:
            obj.draw()

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)
        self.alpha_surface = pg.Surface(RES)
        self.background = None
        bg_path = "./space_images/background/milkyway_large.jpg"
        if os.path.exists(bg_path):
            raw = pg.image.load(bg_path).convert()
            iw, ih = raw.get_size()
            # Fit-height: scale so full panoramic band is visible
            bh = int(HEIGHT * 1.08)
            bw = max(int(iw * bh / ih), int(WIDTH * 1.08))
            bg = pg.transform.smoothscale(raw, (bw, bh))
            # Pre-darken to ~5%
            dark = pg.Surface((bw, bh))
            dark.fill((13, 12, 16))
            bg.blit(dark, (0, 0), special_flags=pg.BLEND_MULT)
            self.background = bg
            self.bg_ox = -((bw - WIDTH) // 2)
            self.bg_oy = -((bh - HEIGHT) // 2)

    def run(self):
        while True:
            pg.mouse.set_visible(not MOUSE_VANISHING_POINT)
            effective_alpha = max(2, min(50, int(20 / SPEED_MULTIPLIER))) if MOUSE_VANISHING_POINT else ALPHA
            self.alpha_surface.set_alpha(effective_alpha)
            self.screen.blit(self.alpha_surface, (0, 0))
            if MOUSE_VANISHING_POINT and self.background:
                bg_alpha = int(50 + min(max(SPEED_MULTIPLIER - 0.1, 0), 9.9) / 9.9 * 30)
                self.background.set_alpha(bg_alpha)
                bg_shift = 150 if ROTATION_FLIGHT else 70
                bx = self.bg_ox - int(FLIGHT_ANGLE.x * bg_shift)
                by = self.bg_oy - int(FLIGHT_ANGLE.y * int(bg_shift * 0.35))
                self.screen.blit(self.background, (bx, by), special_flags=pg.BLEND_ADD)
            self.starfield.run(self)

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
            self.clock.tick(60)

def apply_preset_1():
    global NUM_STARS, Z_DISTANCE, ALPHA, ROTATION_SPEED, VELOCITY, GLOBAL_STARS, PULSE_EFFECT
    global WIGGLING_EFFECT, MOUSE_ROTATION, SIN_ROTATION, SCALE_POS, OUTER_COLORS, INNER_COLORS
    global INNER_SHAPE, OUTER_SHAPE, OUTER_STARS, INNER_STARS, OPPOSITE_ROTATION
    global MAX_SHAPE_SIZE, SPEED_MULTIPLIER, MOUSE_VANISHING_POINT, NUM_NEBULAE, FLARE_STARS
    NUM_STARS = 2000; Z_DISTANCE = 40; ALPHA = 4; ROTATION_SPEED = 0
    VELOCITY = (0.06, 0.18); GLOBAL_STARS = True; PULSE_EFFECT = False
    WIGGLING_EFFECT = False; MOUSE_ROTATION = False; SIN_ROTATION = False; SCALE_POS = 20
    OUTER_COLORS = SPACE_COLORS; INNER_COLORS = SPACE_COLORS
    INNER_SHAPE = "Circle"; OUTER_SHAPE = "Circle"
    OUTER_STARS = "shape"; INNER_STARS = "shape"; OPPOSITE_ROTATION = False
    MAX_SHAPE_SIZE = 2; SPEED_MULTIPLIER = 0.3
    MOUSE_VANISHING_POINT = True; NUM_NEBULAE = 12; FLARE_STARS = True
    ROTATION_FLIGHT = False
    FLIGHT_ANGLE.x = 0; FLIGHT_ANGLE.y = 0

if __name__ == '__main__':
    pg.init()
    apply_preset_1()
    app = App()
    app.run()
