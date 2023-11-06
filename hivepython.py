from enum import Enum
import pygame
import math

class Player(Enum):
    WHITE = 0
    BLACK = 1


class Hex:

    def __init__(self, q, r, s, x, y, points):
        self.q = q
        self.r = r
        self.s = s
        self.x = x
        self.y = y
        self.colour = (0,0,0)
        self.points = points
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.points)

class HexGrid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hexagons = {}
        self.hex_size = 20
        self.hex_radius = 20
        self.screen_size = (800, 800)


    def generate_grid(self, N):
        q = -N
        while q <= N:
            r1 = max(-N, -q-N)
            r2 = min(N, -q+N)
            r=r1
            while r<=r2:
                x = self.hex_size * (math.sqrt(3.0)*q + math.sqrt(3.0)/2.0 * r) + self.screen_size[0]/2
                y = self.hex_size * (3.0/2 * r) + self.screen_size[1]/2
                points = self.compute_vertices(x, y, self.hex_radius)
                self.hexagons[(q,r)]=Hex(q,r, -q-r, x, y, points)
                r+=1
            q+=1
    
    def compute_vertices(self, x, y, radius):
        return [tuple((x+radius*math.cos((((i+1)*2*math.pi)/6)+math.pi/2), (y+radius*math.sin((((i+1)*2*math.pi)/6)+math.pi/2))))for i in range(6)]
    
    def get_neighbours(self, hex):
        neighbours = []
        pairs = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        for pair in pairs:
            q, r, s = hex.q + pair[0], hex.r + pair[1], hex.s - pair[0] - pair[1]
            if (q, r) in self.hexagons:
                neighbours.append(self.hexagons[(q, r)])
        return neighbours
    

class Game:
    def __init__(self):
        self.grid = HexGrid(5, 5)
        self.current_player = Player.WHITE
        self.grid.generate_grid(1)
        self.screen = None
        self.clock = None
        self.screen_size = (800, 800)
        self.hex_size = 20
        self.hex_radius = 20

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        

    def gameloop(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        self.handle_input(mx, my)
                
                self.update()
                self.render()
        
    def switch_player(self):
        if self.current_player == Player.WHITE:
            self.current_player == Player.BLACK
        else:
            self.current_player == Player.WHITE

    def handle_input(self, mx, my):
        pos = self.mouse_to_pos(mx, my)
        print(f"Mouse x:{mx}, Mouse y:{my}")
        print(f"Hex: ({pos[0]},{pos[1]},{pos[2]})")

    def mouse_to_pos(self, mouse_x, mouse_y):
        # This needs to be refactored
        x = mouse_x - self.screen_size[0]/2
        y = mouse_y - self.screen_size[1]/2
        fr_q = (math.sqrt(3.0)/3.0 * x - 1.0/3.0 * y)/self.hex_size
        fr_r = (2.0/3.0 * y)/self.hex_size
        fr_s = -fr_q-fr_r
        r_q = round(fr_q)
        r_r = round(fr_r)
        r_s = round(fr_s)
        q_d = abs(r_q - fr_q)
        r_d = abs(r_r - fr_r)
        s_d = abs(r_s - fr_s)
        if q_d > r_d and q_d > s_d:
            r_q = -r_r-r_s
        elif r_d > s_d:
            r_r = -r_q-r_s
        else:
            r_s = -r_q-r_r
        q = r_q
        r = r_r
        s = r_s
        return (q, r, s)


    def update(self):
        pass

    def render(self):
        self.screen.fill((0,255,0))
        for key in self.grid.hexagons.keys():
            self.grid.hexagons[key].draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.setup()
    game.gameloop()
    print("Finished!")
    pygame.quit()
