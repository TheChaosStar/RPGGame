import pygame, os
from prettytable import PrettyTable

# ------------------------------/ Config /------------------------------
WIDTH, HEIGHT = 800, 600

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
                    else: l.append(value)
                
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
        self.time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            self.event = event
            if event.type == pygame.QUIT:
                self.is_running = False

        pygame.display.update()

    def draw(self, surface:pygame.Surface, pos:tuple=(0, 0)):
        self.surface(surface, pos)


# ------------------------------/ Main /--------------------------------
window = Window()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color("#000000"))

# World
world = World()
# world.Create((10, 10))
world.Write('map-1', (5, 1), None)

while window.is_running:
    window.update()
    window.draw(background)