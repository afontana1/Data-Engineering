let pyodidePromise = null;

function injectPyodideScript() {
  return new Promise((resolve, reject) => {
    if (typeof window === "undefined") {
      reject(new Error("Pyodide can only load in the browser"));
      return;
    }

    if (window.loadPyodide) {
      resolve();
      return;
    }

    const existing = document.querySelector('script[data-pyodide-loader="1"]');
    if (existing) {
      existing.addEventListener("load", () => resolve());
      existing.addEventListener("error", () =>
        reject(new Error("Failed to load Pyodide script"))
      );
      return;
    }

    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js";
    script.async = true;
    script.dataset.pyodideLoader = "1";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Pyodide script"));
    document.head.appendChild(script);
  });
}

export async function loadPyodideInstance() {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      await injectPyodideScript();
      return window.loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/",
      });
    })();
  }
  return pyodidePromise;
}
