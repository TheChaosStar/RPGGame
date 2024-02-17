import pygame, json, os, math
from prettytable import PrettyTable

# ------------------------------/ Config /------------------------------
WIDTH, HEIGHT = 1080, 720

# -----------------------------/ Window /-------------------------------
class Window():
    def __init__(self, title:str='', size:tuple=(WIDTH, HEIGHT)):
        pygame.init()
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        self.event = None
        self.time_delta = 0
        self.is_running = True

    def update(self):
        pygame.display.flip()

        self.time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            self.event = event
            if event.type == pygame.QUIT:
                self.is_running = False

    def draw(self, surface:pygame.Surface, pos:tuple=(0, 0)):
        self.surface.blit(surface, pos)

# -----------------------------/ Sprite /-------------------------------
class Sprite():
    def __init__(self):
        self.sprite_folder = './sprites'

    def load(self, path:str) -> pygame.Surface:
        if path[0] == '/': path = self.sprite_folder + path
        elif path[0] != '.': path = self.sprite_folder + '/' + path
        return pygame.image.load(path)
    
# -------------------------------/ Map /--------------------------------
class Map():
    def __init__(self, map_path:str) -> None:
        level = dict(World().Read(map_path))

        self.layers_surface = [Sprite().load(background) for background in level['background']]

        layers_name = list(level['layers'].keys())
        for layer in layers_name:
            sprite_size = (level['layers'][layer]['size']['width'], level['layers'][layer]['size']['height'])
            spritesheet = Sprite().load(level['layers'][layer]['spritesheet_path'])
            img_width, img_height = spritesheet.get_size()
            nb_row, nb_col = (img_width//sprite_size[0], img_height//sprite_size[1])
            data = level['layers'][layer]['data']

            surface = pygame.Surface((len(data[0]) * sprite_size[0], len(data) * sprite_size[1]))
            surface.set_colorkey((0, 0, 0))

            for y, line in enumerate(data):
                for x, index in enumerate(line):
                    if index != -1:
                        sprite_pos = ((index%nb_row) * sprite_size[0], (index//nb_row) * sprite_size[1])
                        surface.blit(spritesheet, (x*sprite_size[0], y*sprite_size[1]), (*sprite_pos, *sprite_size))
            
            self.layers_surface.append(surface)

# ------------------------------/ World /-------------------------------
class World():
    def __init__(self) -> None:
        self.maps_folder = './maps'

    def Read(self, path:str) -> json:
        with open(os.path.join(self.maps_folder, path), 'r') as f:
            return json.loads(f.read())

    def Write(self, path:str, pos:tuple, value:int) -> None:
        current_file_path = self.maps_folder + '/' + path
        data = []

        if not value:
            value = '-1'

        with open(current_file_path, 'r') as map:
            data = map.readlines()

        with open(current_file_path, 'w') as map:
            lenght = len(data[0])
            y = 0
            for index, line in enumerate(data):
                map.seek(y)
                if index == pos[1]:
                    x1 = round((pos[0]-1)/len(line.strip().split()) * len(line))
                    x2 = round(pos[0]/len(line.strip().split()) * len(line))
                    
                    l = line[:x1] + str(value) + line[x2-1:]

                    y += len(l) - lenght


                    map.write(''.join(l))
                else: 
                    map.write(''.join(line))

                y += lenght

    def Create(self, name:str) -> None:
        with open(f'{self.maps_folder}/{name}', 'w') as f:
            f.write('{ "layers": { } }')

# ------------------------------/ Main /--------------------------------
window = Window()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color("#000000"))

map = Map("cave1")

while window.is_running:
    window.update()

    window.draw(background)

    for surface in map.layers_surface:
        window.draw(surface)
