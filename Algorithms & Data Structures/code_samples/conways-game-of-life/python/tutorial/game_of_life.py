import tkinter as tk
import random


class GameOfLife:
    def __init__(self, rows, cols, cell_size=10, speed=1):
        """
        This function initializes the GameOfLife object.

        Parameters
        ----------
        rows : int
            The number of rows in the grid.
        cols : int
            The number of columns in the grid.
        cell_size : int, optional
            The size of each cell in the grid. The default is 10.
        speed : int, optional
            The speed of the game. The default is 1.

        Returns
        -------
        None.
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.speed = speed
        self.grid = self.create_grid()
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white",
        )
        self.canvas.pack()
        self.window.resizable(False, False)
        self.window.title("Game of Life")

        self.draw_grid()
        self.create_buttons()
        self.create_label()
        self.window.mainloop()

    def create_buttons(self):
        """
        Create the start, stop, reset and speed buttons.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        # Create a start button
        self.start_button = tk.Button(self.window, text="Start", command=self.run)
        # Create a stop button
        self.stop_button = tk.Button(
            self.window, text="Stop", command=self.window.destroy
        )
        # Create a reset button
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset)
        # Create a speed slider
        self.speed_slider = tk.Scale(
            self.window,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            label="Speed",
            command=self.change_speed,
        )
        self.speed_slider.set(self.speed)

        self.start_button.pack()
        self.stop_button.pack()
        self.reset_button.pack()
        self.speed_slider.pack()

    def create_label(self):
        """
        Add label to show the generation.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        self.generation = 0
        self.label = tk.Label(self.window, text=f"Generation: {self.generation}")
        self.label.pack()

    def update_generation(self):
        """
        Update the generation label.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        self.label.config(text=f"Generation: {self.generation}")

    def create_grid(self):
        """
        Create the grid.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        grid : list
            The grid.
        """
        grid = []
        for row in range(self.rows):  # Loop through the rows
            grid.append([])
            for col in range(self.cols):  # Loop through the columns
                # Append a random number to the grid
                grid[row].append(random.randint(0, 1))
        return grid

    def draw_grid(self):
        """
        Draw the grid.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        for row in range(self.rows):  # Loop through the rows
            for col in range(self.cols):  # Loop through the columns
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # If the cell is alive
                if self.grid[row][col] == 1:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="orange", outline="black"
                    )
                # If the cell is dead
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="white", outline="black"
                    )

    def update(self):
        """
        Update the grid.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        new_grid = []
        for row in range(self.rows):
            new_grid.append([])
            for col in range(self.cols):
                # Append the new cell state to the grid
                new_grid[row].append(self.get_new_cell_state(row, col))
        # Update the grid
        self.grid = new_grid
        # Delete all the items on the canvas
        self.canvas.delete("all")
        # Draw the new grid
        self.draw_grid()
        self.window.after(500 // self.speed, self.update)
        # Update the generation
        self.generation += 1
        self.update_generation()

    def get_new_cell_state(self, row, col):
        """
        Get the new cell state.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.
        row : int
            The row of the cell.
        col : int
            The column of the cell.

        Returns
        -------
        new_state : int
            The new state of the cell.
        """
        # Get the number of neighbours
        num_neighbours = self.get_num_neighbours(row, col)
        # If the cell is alive
        if self.grid[row][col] == 1:
            # If the cell has less than 2 neighbours
            if num_neighbours < 2:
                # The cell dies
                return 0
            # If the cell has 2 or 3 neighbours
            elif num_neighbours == 2 or num_neighbours == 3:
                # The cell stayes alive
                return 1
            elif num_neighbours > 3:
                # The cell dies
                return 0
        # If the cell is dead
        else:
            # If the cell has 3 neighbours
            if num_neighbours == 3:
                # The cell becomes alive
                return 1
            # If the cell has less than 3 neighbours
            else:
                # The cell stays dead
                return 0

    def get_num_neighbours(self, row, col):
        """
        Get the number of neighbours.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.
        row : int
            The row of the cell.
        col : int
            The column of the cell.

        Returns
        -------
        num_neighbours : int
            The number of neighbours.
        """
        num_neighbours = 0
        for i in range(-1, 2):  # Loop through the rows
            for j in range(-1, 2):  # Loop through the columns
                # If the cell is itself
                if i == 0 and j == 0:
                    # Skip the cell
                    continue
                # Calculate the neighbour row
                neighbour_row = row + i
                # Calculate the neighbour column
                neighbour_col = col + j
                # If the neighbour is out of bounds
                if (
                    neighbour_row < 0
                    or neighbour_row >= self.rows
                    or neighbour_col < 0
                    or neighbour_col >= self.cols
                ):
                    # Skip the cell
                    continue
                # Add the neighbour to the number of neighbours
                num_neighbours += self.grid[neighbour_row][neighbour_col]
        return num_neighbours

    def run(self):
        """
        Run the game.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        self.update()

    def reset(self):
        """
        Reset the game.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.

        Returns
        -------
        None.
        """
        self.grid = self.create_grid()
        self.canvas.delete("all")
        self.draw_grid()
        # Reset the generation
        self.generation = 0
        self.update_generation()

    def change_speed(self, speed):
        """
        Change the speed of the game.

        Parameters
        ----------
        self : GameOfLife
            The GameOfLife object.
        speed : int
            The speed of the game.

        Returns
        -------
        None.
        """
        self.speed = int(speed)


if __name__ == "__main__":
    game = GameOfLife(25, 25, 10, 100)
