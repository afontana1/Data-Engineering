# Conway's Game of Life (Vite + React)

A small Conway's Game of Life implementation rebuilt on Vite with modular helper functions and a refreshed UI.

## Quick start

```bash
npm install
npm run dev
```

Then open the URL Vite prints (default `http://localhost:5173`).

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — production build
- `npm run preview` — preview the production build locally
- `npm run lint` — run eslint on the `src` directory

## How it works

- Grid logic lives in `src/helpers/gameOfLife.js` (grid creation, neighbor counting, next generation, toggling).
- UI and controls live in `src/App.jsx`; the root render is in `src/main.jsx`.
- Styles are in `src/App.css` and `src/index.css`.
- Static assets can go in `public/` and are served by Vite.

## Gameplay controls

- **Start/Pause**: toggles the simulation loop.
- **Randomize grid**: seeds a new random starting state.
- **Clear**: wipes the board.
- **Speed slider**: adjusts the interval between generations.
- Click any cell to toggle it alive/dead while paused or running.

## Notes

- This project now targets Vite, React 18, and ES modules. The previous Create React App tooling and tests were removed.
- Default grid size is 30x30; tweak `DEFAULT_ROWS` and `DEFAULT_COLS` in `src/helpers/gameOfLife.js` if you want a different dimension.
