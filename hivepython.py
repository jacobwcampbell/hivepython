from enum import Enum
import pygame

class Player(Enum):
    WHITE = 0
    BLACK = 1


class Hex:

    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

class HexGrid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hexagons = {}

    def generate_grid(self):
        for q in range(-self.width, self.width+1):
            for r in range(max(-self.height, -q-self.width), min(self.height, -q+self.width)+1):
                s = -q-r
                self.hexagons[(q, r)]= Hex(q, r, s)
    
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
        self.grid.generate_grid()
        self.screen = None
        self.clock = None

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
                
                self.update()
                self.render()
        
    def switch_player(self):
        if self.current_player == Player.WHITE:
            self.current_player == Player.BLACK
        else:
            self.current_player == Player.WHITE

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.fill((0,255,0))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.setup()
    game.gameloop()
    pygame.quit()
