# PythonScripts

## Game of life

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Game_of_life_loaf.svg/98px-Game_of_life_loaf.svg.png" width="100">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Game_of_life_block_with_border.svg/66px-Game_of_life_block_with_border.svg.png" width="100">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/07/Game_of_life_pulsar.gif" width="100">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/4f/Animated_Hwss.gif" width="100">
</p>

Source: [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)


This is a pyhon scirpt that simulates the game of life. It uses the [TKinter](https://docs.python.org/3/library/tkinter.html) library to simulate the game.

### A small background on the game of life

The Game of Life is a cellular automaton created by mathematician John Conway. The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. The game is played on a two-dimensional grid of square cells, each of which can be either alive or dead. Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

These rules, which are similar to those used in Conway's Game of Life, result in complex patterns emerging from simple starting conditions.

The game can be played on any size grid, but is usually played on a square grid. The game is played by first creating a grid of cells, with each cell being either alive or dead. The game is then played by letting the cells interact with each other according to the rules above. The game ends when there are no more cells that can interact with each other.

This kind of simulation gives us insight into how complex systems can emerge from simple rules. 

Check the Wikipedia page for more information: [Game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)



    
