import pygame, os
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

# ------------------------------/ Tile /--------------------------------
class Tile():
    def __init__(self, image, pos):
        self.surface = image
        self.position = pos

# -----------------------------/ Sprite /-------------------------------
class Sprite():
    def __init__(self):
        self.sprite_folder = './sprites'

    def load(self, path:str) -> pygame.Surface:
        if path[0] == '/': path = self.sprite_folder + path
        elif path[0] != '.': path = self.sprite_folder + '/' + path
        return pygame.image.load(path)
    
    def tolist(self, surface:pygame.Surface, size:tuple) -> list[Tile]:
        _list = []
        sprite_width, sprite_height = surface.get_size()
        
        for y in range(0, sprite_height, 16):
            for x in range(0, sprite_width, 16):
                _list.append(Sprite().toTile(surface, size, (x, y), (0, 0)))
                                
        return _list

    def toTile(self, surface:pygame.Surface, size:tuple, pos_image:tuple, pos_screen:tuple) -> Tile:
        image = pygame.Surface(size)
        image.blit(surface, (0, 0), (*pos_image, *size))
        return Tile(image, pos_screen)

# -------------------------------/ Map /--------------------------------
class Map():
    def __init__(self, map_paths:list[str], spritesheet_paths:list[str], sprite_sizes:list[tuple], background_paths:list[str]=None) -> None:
        self.world = World()
        default_sprite_size = sprite_sizes[0]
        default_spritesheet_path = spritesheet_paths[0]

        max_length = max([len(map_paths), len(spritesheet_paths), len(sprite_sizes)])

        if len(spritesheet_paths) == 1:
            spritesheet_paths = [default_spritesheet_path for _ in range(max_length)]
        if len(sprite_sizes) == 1:
            sprite_sizes = [default_sprite_size for _ in range(max_length)]

        self.infos = zip(map_paths, spritesheet_paths, sprite_sizes)

        self.surfaces = [Sprite().load(bg) for bg in background_paths] if background_paths else []

    def load(self):
        sprite = Sprite()

        for info in self.infos:
            tiles = sprite.tolist(sprite.load(info[1]), info[2])
            world = self.world.Read(info[0])
            surface = pygame.Surface((len(world[0]) * info[2][0], len(world) * info[2][1]))
            surface.set_colorkey((0, 0, 0))

            for y, row in enumerate(world):
                for x, index in enumerate(row):
                    if index:
                        surface.blit(tiles[index].surface, (x*info[2][0], y*info[2][1]))

            self.surfaces.append(surface)

# ------------------------------/ World /-------------------------------
class World():
    def __init__(self) -> None:
        self.maps_folder = './maps'

    def Read(self, path:str) -> list:
        current_file_path = self.maps_folder + '/' + path
        
        tab = []

        with open(current_file_path, 'r') as map:
            for line in map.readlines():
                l = []

                for value in line.rstrip().split():
                    if value == '-1': l.append(None)
                    else: l.append(int(value))
                
                tab.append(l)
        
        return tab
    
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

    def Create(self, size:tuple=(WIDTH//16, HEIGHT//16)) -> None:
        index = len(os.listdir(self.maps_folder)) + 1

        f = open(f'./maps/map-{index}', 'a')

        for h in range(size[1]):
            for w in range(size[0]):
                if w == size[0]-1:f.write('-1')
                else: f.write('-1 ')

            if h != size[1]-1: f.write('\n')

        f.close()


# ------------------------------/ Main /--------------------------------
window = Window()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color("#000000"))

# Map
map = Map(
    ['cave1-backward2', 'cave1-backward', 'cave1-platform', 'cave1-forward'], # map files
    ['/mainlev_build.png'], # spritesheet
    [(16, 16)], # sprite size
    ['/background1.png', '/background2.png', '/background3.png', '/background4a.png'] # backrounds
) 
map.load()

print(map.surfaces)

while window.is_running:
    window.update()

    window.draw(background)

    for surface in map.surfaces:
        window.draw(surface)
