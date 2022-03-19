import pygame, sys

level_map = [
'XXXXXXXXXXXXXXXXXXXXXXX',
'X                     X',
'X  P                  X',
'XXXXXX     XX         X',
'X               XXXXXXX',
'X      X              X',
'XXXXXXX               X',
'X                 XXXXX',
'X               XX    X',
'X                     X',
'XXXXXXXXXXXXXXXXXXXXXXX']

tile_size = 64

pygame.init()
screen_width, screen_height = 1200, len(level_map) * tile_size
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('ORANGE')
        self.rect = self.image.get_rect(topleft=pos)
    def update(self, x_shift):
        self.rect.x += x_shift
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)

level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run()
    pygame.display.update()
    clock.tick(FPS)
