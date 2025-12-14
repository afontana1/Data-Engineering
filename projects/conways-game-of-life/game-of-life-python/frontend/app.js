const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");
const statusEl = document.getElementById("status");
const genEl = document.getElementById("generation");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

let socket = null;
let currentDims = { width: 0, height: 0 };

function readConfig() {
  const gensVal = document.getElementById("generations").value;
  return {
    url: document.getElementById("wsUrl").value.trim(),
    payload: {
      width: Number(document.getElementById("width").value),
      height: Number(document.getElementById("height").value),
      generations: gensVal ? Number(gensVal) : null,
      delay_ms: Number(document.getElementById("delay").value),
      pattern: document.getElementById("pattern").value,
      random_fill: Number(document.getElementById("randomFill").value),
      wrap: document.getElementById("wrap").checked,
    },
  };
}

function setStatus(text, color = "#cbd5e1") {
  statusEl.textContent = text;
  statusEl.style.color = color;
}

function setButtons(running) {
  startBtn.disabled = running;
  stopBtn.disabled = !running;
}

function draw(state) {
  const { width, height, alive } = state;
  if (width !== currentDims.width || height !== currentDims.height) {
    currentDims = { width, height };
  }
  const cellSize = Math.max(
    1,
    Math.min(canvas.width / width, canvas.height / height)
  );
  ctx.fillStyle = "#0b1222";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#22d3ee";
  alive.forEach(([y, x]) => {
    ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
  });
}

function disconnect() {
  if (socket) {
    socket.close(1000, "Client stop");
    socket = null;
  }
  setStatus("Disconnected");
  setButtons(false);
}

function start() {
  if (socket) {
    disconnect();
  }
  const { url, payload } = readConfig();
  socket = new WebSocket(url);
  setStatus("Connecting...");
  setButtons(true);

  socket.addEventListener("open", () => {
    setStatus("Connected", "#4ade80");
    socket.send(JSON.stringify(payload));
  });

  socket.addEventListener("message", (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.error) {
        setStatus(`Error: ${data.error}`, "#f87171");
        disconnect();
        return;
      }
      if (typeof data.generation === "number") {
        genEl.textContent = `Generation: ${data.generation}`;
        draw(data);
      }
    } catch (err) {
      console.error("Bad message", err);
    }
  });

  socket.addEventListener("close", () => {
    if (socket) {
      setStatus("Closed");
    }
    setButtons(false);
  });

  socket.addEventListener("error", () => {
    setStatus("WebSocket error", "#f87171");
    disconnect();
  });
}

startBtn.addEventListener("click", start);
stopBtn.addEventListener("click", disconnect);

// Initial canvas clear
ctx.fillStyle = "#0b1222";
ctx.fillRect(0, 0, canvas.width, canvas.height);
