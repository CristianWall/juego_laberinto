import time
import pygame
import heapq

class Node:
    def __init__(self, state, parent, action, g_cost, h_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_cost = g_cost  # Costo real desde el inicio
        self.h_cost = h_cost  # Costo estimado hacia la meta

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

class AStarFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        heapq.heappush(self.frontier, node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier vacía")
        else:
            return heapq.heappop(self.frontier)

class MazeAStarFrontier:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Laberinto debe tener exactamente un punto de inicio (A) y un punto de llegada (B).")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if contents[i][j] == "A":
                    self.start = (i, j)
                    row.append(False)
                elif contents[i][j] == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif contents[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def heuristic(self, state):
        """Heurística h(n) para estimar el costo desde el estado actual hasta la meta."""
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self, pantalla, ANCHO_CELDA, ALTO_CELDA, draw_cell):
        """Resolver el laberinto utilizando el algoritmo A*."""
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None, g_cost=0, h_cost=self.heuristic(self.start))
        frontier = AStarFrontier()
        frontier.add(start)
        self.explored = set()

        start_time = time.time()  # Empezar el cronómetro

        while True:
            if frontier.empty():
                raise Exception("No hay solución")

            node = frontier.remove()
            self.num_explored += 1

            # Dibujar el camino explorado en amarillo
            draw_cell(node.state[1], node.state[0], (255, 255, 0))  # Amarillo
            pygame.display.update()
            time.sleep(0.1)

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)

                # Dibujar el camino final en celeste
                for cell in cells:
                    draw_cell(cell[1], cell[0], (0, 255, 255))  # Celeste
                    pygame.display.update()
                    time.sleep(0.1)

                end_time = time.time()  # Terminar el cronómetro
                elapsed_time = end_time - start_time
                return elapsed_time, self.num_explored  # Devuelve el tiempo y los pasos

                # Mostrar el tiempo en la consola
                print(f"Tiempo total de exploración y solución: {elapsed_time:.2f} segundos")
                print(f"Estados explorados: {self.num_explored}")

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                g_cost = node.g_cost + 1  # Cada paso tiene un costo de 1
                h_cost = self.heuristic(state)
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, g_cost=g_cost, h_cost=h_cost)
                    frontier.add(child)
