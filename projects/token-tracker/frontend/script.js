const API_BASE = window.API_BASE || "http://localhost:8000";
const apiLabel = document.getElementById("api-base-label");
const chatHistory = document.getElementById("chat-history");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");
const sqlQuery = document.getElementById("sql-query");
const runQueryBtn = document.getElementById("run-query");
const queryResults = document.getElementById("query-results");
const queryStatus = document.getElementById("query-status");

let sessionId = crypto.randomUUID();

function appendMessage(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text || "";
  chatHistory.appendChild(bubble);
  chatHistory.scrollTop = chatHistory.scrollHeight;
  return bubble;
}

async function sendMessage(question) {
  const userBubble = appendMessage("user", question);
  const botBubble = appendMessage("bot", "Thinking...");

  try {
    const resp = await fetch(`${API_BASE}/my-chat-bot`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-user-id": "demo-user",
        "x-org-id": "demo-org",
        "x-session-id": sessionId,
      },
      body: JSON.stringify({ question, session_id: sessionId }),
    });

    if (!resp.ok) {
      throw new Error(`Request failed: ${resp.status}`);
    }

    const data = await resp.json();
    botBubble.textContent = data?.answer || "(no answer)";
    if (data?.picked_agents) {
      const meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent = `Agents: ${data.picked_agents.join(", ")}`;
      botBubble.appendChild(meta);
    }
  } catch (err) {
    botBubble.textContent = `Error: ${err.message}`;
    console.error(err);
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = "";
  sendMessage(question);
});

function setActiveTab(tabName) {
  tabs.forEach((tab) => {
    const active = tab.dataset.tab === tabName;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", active ? "true" : "false");
  });
  panels.forEach((panel) => {
    const active = panel.id === `tab-${tabName}`;
    panel.classList.toggle("active", active);
  });
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => setActiveTab(tab.dataset.tab));
});

function renderTable(columns, rows, truncated) {
  if (!columns.length) {
    return `<div class="muted">No columns returned.</div>`;
  }
  const header = columns.map((c) => `<th>${c}</th>`).join("");
  const body = rows
    .map(
      (row) =>
        `<tr>${row.map((cell) => `<td>${cell === null ? "" : String(cell)}</td>`).join("")}</tr>`
    )
    .join("");
  const note = truncated ? `<div class="muted">Results truncated.</div>` : "";
  return `
    <div class="table-wrap">
      <table>
        <thead><tr>${header}</tr></thead>
        <tbody>${body}</tbody>
      </table>
    </div>
    ${note}
  `;
}

async function runQuery() {
  const sql = sqlQuery.value.trim();
  if (!sql) return;
  queryStatus.textContent = "Running...";
  queryResults.innerHTML = "";
  try {
    const resp = await fetch(`${API_BASE}/telemetry/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sql }),
    });
    const data = await resp.json();
    if (!resp.ok) {
      throw new Error(data?.detail || `Request failed: ${resp.status}`);
    }
    queryResults.innerHTML = renderTable(data.columns, data.rows, data.truncated);
    queryStatus.textContent = `Rows: ${data.rows.length}`;
  } catch (err) {
    queryStatus.textContent = "Error";
    queryResults.innerHTML = `<div class="error">Error: ${err.message}</div>`;
    console.error(err);
  }
}

if (runQueryBtn) {
  runQueryBtn.addEventListener("click", runQuery);
}

if (apiLabel) {
  apiLabel.textContent = API_BASE;
}
