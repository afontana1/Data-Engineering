import { useEffect, useMemo, useState } from 'react';
import {
  DEFAULT_COLS,
  DEFAULT_ROWS,
  createEmptyGrid,
  createRandomGrid,
  getNextGeneration,
  toggleCell,
} from './helpers/gameOfLife.js';
import './App.css';

const SPEED_MIN = 50;
const SPEED_MAX = 600;

function App() {
  const [grid, setGrid] = useState(() => createRandomGrid());
  const [isRunning, setIsRunning] = useState(false);
  const [speed, setSpeed] = useState(160);
  const [generation, setGeneration] = useState(0);

  useEffect(() => {
    if (!isRunning) return undefined;

    const tick = () => {
      setGrid((current) => getNextGeneration(current));
      setGeneration((current) => current + 1);
    };

    const interval = setInterval(tick, speed);
    return () => clearInterval(interval);
  }, [isRunning, speed]);

  const aliveCount = useMemo(
    () => grid.reduce((sum, row) => sum + row.reduce((rowSum, cell) => rowSum + cell, 0), 0),
    [grid],
  );

  function handleStartStop() {
    setIsRunning((running) => !running);
  }

  function handleReset() {
    setGrid(createRandomGrid());
    setGeneration(0);
  }

  function handleClear() {
    setGrid(createEmptyGrid());
    setGeneration(0);
    setIsRunning(false);
  }

  function handleCellClick(row, col) {
    setGrid((current) => toggleCell(current, row, col));
  }

  return (
    <main className="page">
      <div className="headline">
        <div>
          <h1>Conway&apos;s Game of Life</h1>
          <p className="subtext">Vite + React rewrite with modular helpers</p>
        </div>
      </div>

      <section className="toolbar">
        <div className="controls">
          <button className="btn-primary" onClick={handleStartStop}>
            {isRunning ? 'Pause simulation' : 'Start simulation'}
          </button>
          <button className="btn-secondary" onClick={handleReset}>
            Randomize grid
          </button>
          <button className="btn-ghost" onClick={handleClear}>
            Clear
          </button>
        </div>

        <div className="speed">
          <label htmlFor="speed">Speed</label>
          <input
            id="speed"
            type="range"
            min={SPEED_MIN}
            max={SPEED_MAX}
            step={10}
            value={speed}
            onChange={(event) => setSpeed(Number(event.target.value))}
          />
          <span>{speed} ms</span>
        </div>
      </section>

      <div className="grid-shell">
        <div
          className="grid"
          style={{
            gridTemplateColumns: `repeat(${DEFAULT_COLS}, 20px)`,
          }}
        >
          {grid.map((row, rowIndex) =>
            row.map((cell, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`cell ${cell ? 'alive' : ''}`}
                onClick={() => handleCellClick(rowIndex, colIndex)}
              />
            )),
          )}
        </div>
        <div className="meta">
          <span>Generation: {generation}</span>
          <span>Alive cells: {aliveCount}</span>
          <span>
            Grid: {DEFAULT_ROWS} × {DEFAULT_COLS}
          </span>
        </div>
      </div>
    </main>
  );
}

export default App;
