const NEIGHBOR_OFFSETS = [
  [0, 1],
  [0, -1],
  [1, -1],
  [-1, 1],
  [1, 1],
  [-1, -1],
  [1, 0],
  [-1, 0],
];

export const DEFAULT_ROWS = 30;
export const DEFAULT_COLS = 30;

export function createEmptyGrid(rows = DEFAULT_ROWS, cols = DEFAULT_COLS) {
  return Array.from({ length: rows }, () => Array.from({ length: cols }, () => 0));
}

export function createRandomGrid(rows = DEFAULT_ROWS, cols = DEFAULT_COLS) {
  return Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => (Math.random() > 0.7 ? 1 : 0)),
  );
}

export function toggleCell(grid, row, col) {
  return grid.map((r, rIndex) =>
    r.map((cell, cIndex) => {
      if (rIndex === row && cIndex === col) {
        return cell ? 0 : 1;
      }
      return cell;
    }),
  );
}

export function getNextGeneration(grid) {
  const rows = grid.length;
  const cols = rows ? grid[0].length : 0;

  return grid.map((row, rowIndex) =>
    row.map((cell, colIndex) => {
      let neighbors = 0;
      for (const [dx, dy] of NEIGHBOR_OFFSETS) {
        const x = rowIndex + dx;
        const y = colIndex + dy;
        if (x >= 0 && x < rows && y >= 0 && y < cols) {
          neighbors += grid[x][y];
        }
      }

      if (neighbors < 2 || neighbors > 3) return 0;
      if (neighbors === 3) return 1;
      return cell;
    }),
  );
}
