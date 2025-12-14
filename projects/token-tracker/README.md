# Token Tracker

FastAPI backend with LiteLLM telemetry plus a lightweight HTML/CSS/JS chat frontend.

## Backend
1. Install (editable recommended for local dev):
   ```bash
   pip install -e .
   ```
2. Set your environment variables (example for OpenAI):
   ```bash
   export OPENAI_API_KEY=sk-...
   export OPENAI_MODEL=gpt-4o-mini
   ```
3. Run the API (default host `0.0.0.0`, port `8000`):
   ```bash
   token-tracker
   ```
   or
   ```bash
   uvicorn token_tracker.app:app --reload
   ```
4. Test an endpoint:
   ```bash
   curl -X POST http://localhost:8000/my-chat-bot \
     -H "Content-Type: application/json" \
     -d '{"question": "hello"}'
   ```

## Frontend
Static assets live in `frontend/` (`index.html`, `styles.css`, `script.js`). The JS expects the API at `http://localhost:8000` by default.

1. Start a simple web server from the `frontend/` folder (serves on port 8080):
   ```bash
   cd frontend
   python -m http.server 8080
   ```
2. Open the app in a browser:
   ```
   http://localhost:8080
   ```
3. Type a question and submit. Responses and chat history will render in the UI.

If your API runs on a different host/port, set `window.API_BASE` before loading `script.js` in `index.html`:
```html
<script>window.API_BASE = "http://localhost:9000";</script>
<script src="script.js"></script>
```
