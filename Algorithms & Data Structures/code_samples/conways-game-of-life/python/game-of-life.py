import os
from itertools import product
from random import randint
from time import sleep

# Very clean implementation
# https://gist.github.com/Per48edjes/096d9fd67994986b3b92082cdf708734

# Another clean implementation
# https://gist.github.com/ramalho/da5590bc38c973408839


class Cell:
    def __init__(self, state):
        self._state = state
        self._future_state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def switch_state(self):
        self._state = not self._state

    def update_future_state(self, new_state):
        self._future_state = new_state

    def next_gen(self):
        self._state = self._future_state

    def __str__(self):
        if self._state:
            return "*"
        else:
            return " "


class Board:
    def __init__(self, height, width):
        self._matrix = [
            [Cell(state=False) for _ in range(width)] for _ in range(height)
        ]

    def __str__(self):
        row_repr = ""
        for row in self._matrix:
            row_repr += "".join([str(cell) for cell in row] + ["\n"])
        return row_repr

    def get_cell(self, y, x):
        return self._matrix[y][x]

    def get_cell_state(self, y, x):
        return self._matrix[y][x].state

    def set_cell_state(self, y, x, new_state):
        self._matrix[y][x].state = new_state


class Game:
    def __init__(self, height, width, pct_alive=0.33):
        self._height = height
        self._width = width
        self._board = Board(height, width)
        self._generate_board_initial_state(pct_alive)

    def play(self, n=100):
        """
        Main method called on Game object to play game for n generations
        """
        for _ in range(n):
            os.system("clear")
            self._display_board()
            sleep(0.5)
            self._update_future_states()
            self._update_next_generation()

    def _display_board(self):
        print(self._board)

    def _generate_board_initial_state(self, pct_alive):
        """
        Instantiate 0th generation of game with live cells based on pct_alive
        """
        num_initial_live_cells = round(self._height * self._width * pct_alive)
        while num_initial_live_cells > 0:
            x = randint(0, self._width - 1)
            y = randint(0, self._height - 1)
            if not self._board.get_cell(y, x).state:
                self._board.get_cell(y, x).switch_state()
                num_initial_live_cells += -1

    def _get_neighbors_indices(self, y, x):
        """
        Return indices of neighbors of element located at y, x
        """
        left, center, right, top, middle, bottom = x - 1, x, x + 1, y + 1, y, y - 1
        horizontal_idx = [
            loc for loc in (left, center, right) if ((loc >= 0) and (loc < self._width))
        ]
        vertical_idx = [
            loc
            for loc in (top, middle, bottom)
            if ((loc >= 0) and (loc < self._height))
        ]
        neighbor_indices = set(product(vertical_idx, horizontal_idx)) - {(y, x)}
        return neighbor_indices

    def _get_alive_cells_indices(self):
        """
        Return indices of alive cells in current generation
        """
        live_cells_indices = []
        for y in range(self._height):
            for x in range(self._width):
                if self._board.get_cell_state(y, x):
                    live_cells_indices.append((y, x))
        return live_cells_indices

    def _get_alive_count(self, loc_indices):
        """
        Return count of alive cells in set of loc_indices
        """
        alive_counter = 0
        for y, x in loc_indices:
            if self._board.get_cell_state(y, x):
                alive_counter += 1
        return alive_counter

    def _get_cell_next_state(self, y, x):
        """
        Returns the next state of a cell at y, x given state of neighboring
        cells in the current generation
        """
        neighbor_indices = self._get_neighbors_indices(y, x)
        alive_neighbor_count = self._get_alive_count(neighbor_indices)
        if (self._board.get_cell_state(y, x) and (alive_neighbor_count in (2, 3))) or (
            not self._board.get_cell_state(y, x) and (alive_neighbor_count != 3)
        ):
            return self._board.get_cell_state(y, x)
        else:
            return not self._board.get_cell_state(y, x)

    def _update_future_states(self):
        for y in range(self._height):
            for x in range(self._width):
                new_state = self._get_cell_next_state(y, x)
                self._board.get_cell(y, x).update_future_state(new_state)

    def _update_next_generation(self):
        """
        Update cells accordingly to replace board with new_board
        """
        for y in range(self._height):
            for x in range(self._width):
                self._board.get_cell(y, x).next_gen()


if __name__ == "__main__":
    game = Game(80, 80)
    game.play()
