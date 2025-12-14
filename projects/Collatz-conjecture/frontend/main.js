const seqStartEl = document.getElementById("seqStart");
const seqMaxEl = document.getElementById("seqMax");
const seqResultEl = document.getElementById("seqResult");
const scanStartEl = document.getElementById("scanStart");
const scanCountEl = document.getElementById("scanCount");
const scanMaxEl = document.getElementById("scanMax");
const scanResultEl = document.getElementById("scanResult");
const apiBaseEl = document.getElementById("apiBase");

const runSequenceBtn = document.getElementById("runSequence");
const runScanBtn = document.getElementById("runScan");

function getBaseUrl() {
  return apiBaseEl.value.replace(/\/+$/, "");
}

async function runSequence() {
  const start = Number(seqStartEl.value);
  const maxSteps = seqMaxEl.value ? Number(seqMaxEl.value) : undefined;

  seqResultEl.textContent = "Loading...";
  try {
    const response = await fetch(`${getBaseUrl()}/collatz/sequence`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, max_steps: maxSteps }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    seqResultEl.textContent = JSON.stringify(data, null, 2);
    renderSequenceChart(data);
  } catch (err) {
    seqResultEl.textContent = `Error: ${err.message}`;
    renderSequenceChart(null);
  }
}

async function runScan() {
  const start = Number(scanStartEl.value);
  const count = Number(scanCountEl.value);
  const maxSteps = scanMaxEl.value ? Number(scanMaxEl.value) : undefined;

  scanResultEl.textContent = "Loading...";
  try {
    const response = await fetch(`${getBaseUrl()}/collatz/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, count, max_steps: maxSteps }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    scanResultEl.textContent = JSON.stringify(data, null, 2);
    renderScanChart(data);
  } catch (err) {
    scanResultEl.textContent = `Error: ${err.message}`;
    renderScanChart(null);
  }
}

runSequenceBtn.addEventListener("click", runSequence);
runScanBtn.addEventListener("click", runScan);

function renderSequenceChart(data) {
  const container = document.getElementById("seqChart");
  if (!container) return;
  if (!data || !Array.isArray(data.sequence)) {
    container.innerHTML = "";
    return;
  }
  const points = data.sequence.map((value, idx) => [idx, value]);
  Highcharts.chart("seqChart", {
    chart: { type: "line" },
    title: { text: `Sequence for start ${data.start}` },
    xAxis: { title: { text: "Iteration" } },
    yAxis: { title: { text: "Value" } },
    series: [
      {
        name: "Value",
        data: points,
      },
    ],
    legend: { enabled: false },
    credits: { enabled: false },
  });
}

function renderScanChart(data) {
  const container = document.getElementById("scanChart");
  if (!container) return;
  if (!data || !Array.isArray(data.data)) {
    container.innerHTML = "";
    return;
  }
  const categories = data.data.map((item) => item.start);
  const iterations = data.data.map((item) => item.iterations);
  Highcharts.chart("scanChart", {
    chart: { type: "column" },
    title: { text: "Iterations per start" },
    xAxis: { categories, title: { text: "Start" } },
    yAxis: { min: 0, title: { text: "Iterations" } },
    series: [{ name: "Iterations", data: iterations }],
    credits: { enabled: false },
  });
}
