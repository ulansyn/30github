import pygame
import sys
import heapq

# ================================
# Настройки игры и карты
# ================================

TILE_SIZE = 40
COLOR_FLOOR    = (230, 230, 230)
COLOR_OBSTACLE = (50, 50, 50)
COLOR_GARBAGE  = (255, 215, 0)
COLOR_VACUUM   = (50, 150, 255)
COLOR_GRID     = (200, 200, 200)

# Карта задаётся как список строк.
# Символы:
#   '#' - препятствие (объект, стена, мебель)
#   'G' - мусор
#   'V' - стартовая позиция пылесоса
#   '.' или пробел - свободная клетка
MAP_DATA = [
    "#############################",
    "#V.....#.......#GGG.......##",
    "#......#.......#..G...##...#",
    "#......#####...#..G.........#",
    "#............####...........#",
    "#...G.......................#",
    "#.............###...........#",
    "###............#........#...#",
    "#.......G......#........#...#",
    "#GG............#...........G#",
    "#############################"
]

MAP_HEIGHT = len(MAP_DATA)
MAP_WIDTH = max(len(row) for row in MAP_DATA)

# ================================
# Функции для поиска пути (A*)
# ================================

def heuristic(a, b):
    """Манхэттенское расстояние между точками a и b"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, obstacles):
    (x, y) = pos
    neighbors = []
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= MAP_WIDTH or ny >= MAP_HEIGHT:
            continue
        if (nx, ny) in obstacles:
            continue
        neighbors.append((nx, ny))
    return neighbors

def astar(start, goal, obstacles):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in get_neighbors(current, obstacles):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# ================================
# Основной класс игры
# ================================

class VacuumSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
        pygame.display.set_caption("Симулятор робота-пылесоса")
        self.clock = pygame.time.Clock()
        self.running = True

        self.obstacles = set()
        self.garbages = set()
        self.vacuum_pos = None

        self.parse_map()

        self.current_path = []

        self.move_delay = 300  # мс
        self.last_move_time = pygame.time.get_ticks()

    def parse_map(self):
        for y, row in enumerate(MAP_DATA):
            for x, char in enumerate(row):
                if char == '#':
                    self.obstacles.add((x, y))
                elif char.upper() == 'G':
                    self.garbages.add((x, y))
                elif char.upper() == 'V':
                    if self.vacuum_pos is None:
                        self.vacuum_pos = (x, y)
                    else:
                        print("Обнаружено несколько позиций для пылесоса, используется первая!")
        if self.vacuum_pos is None:
            self.vacuum_pos = (MAP_WIDTH // 2, MAP_HEIGHT // 2)

    def choose_next_target(self):
        if not self.garbages:
            return None, None

        sorted_garbage = sorted(self.garbages, key=lambda pos: heuristic(self.vacuum_pos, pos))
        for target in sorted_garbage:
            path = astar(self.vacuum_pos, target, self.obstacles)
            if path is not None:
                return target, path
        return None, None

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return
        self.last_move_time = current_time

        if not self.current_path or len(self.current_path) <= 1:
            target, path = self.choose_next_target()
            if path is None:
                return
            self.current_path = path

        next_cell = self.current_path[1]
        self.vacuum_pos = next_cell
        self.current_path.pop(0)

        if self.vacuum_pos in self.garbages:
            self.garbages.remove(self.vacuum_pos)
            print(f"Убран мусор в клетке {self.vacuum_pos}")
            self.current_path = []

    def draw_grid(self):
        for x in range(0, MAP_WIDTH * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, MAP_HEIGHT * TILE_SIZE))
        for y in range(0, MAP_HEIGHT * TILE_SIZE, TILE_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (MAP_WIDTH * TILE_SIZE, y))

    def draw(self):
        self.screen.fill(COLOR_FLOOR)

        for (x, y) in self.obstacles:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)

        for (x, y) in self.garbages:
            rect = pygame.Rect(x * TILE_SIZE + TILE_SIZE//4, y * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
            pygame.draw.rect(self.screen, COLOR_GARBAGE, rect)

        if self.vacuum_pos:
            x, y = self.vacuum_pos
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.ellipse(self.screen, COLOR_VACUUM, rect)

        if self.current_path and len(self.current_path) >= 2:
            points = [ (cell[0]*TILE_SIZE+TILE_SIZE//2, cell[1]*TILE_SIZE+TILE_SIZE//2) for cell in self.current_path ]
            pygame.draw.lines(self.screen, (0, 255, 0), False, points, 3)

        self.draw_grid()

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()

            if not self.garbages:
                print("Весь мусор убран!")
                pygame.time.wait(1000)
                self.running = False

            self.clock.tick(60)
        pygame.quit()
        sys.exit()

# ================================
# Запуск игры
# ================================

if __name__ == '__main__':
    game = VacuumSimulator()
    game.run()
