const API_BASE = window.API_BASE || "http://localhost:8000";
const apiLabel = document.getElementById("api-base-label");
const chatHistory = document.getElementById("chat-history");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");

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

if (apiLabel) {
  apiLabel.textContent = API_BASE;
}
