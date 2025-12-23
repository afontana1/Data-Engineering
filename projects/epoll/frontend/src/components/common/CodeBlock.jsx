import React, { useMemo, useState } from "react";
import { loadPyodideInstance } from "../../utils/pyodideLoader";

function indentSnippet(snippet) {
  return snippet
    .split("\n")
    .map((line) => `    ${line}`)
    .join("\n");
}

function CodeBlock({
  title,
  filename,
  code,
  supportingFiles = [],
  runSnippet = null,
}) {
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [isLoadingRuntime, setIsLoadingRuntime] = useState(false);

  const primaryName = useMemo(() => {
    const parts = filename.split("/");
    return parts[parts.length - 1] || "snippet.py";
  }, [filename]);

  const handleRun = async () => {
    setError("");
    setOutput("");
    setIsRunning(true);
    setIsLoadingRuntime(true);

    try {
      const pyodide = await loadPyodideInstance();
      setIsLoadingRuntime(false);

      const sessionDir = `/tmp/run-${
        Date.now().toString(16) + Math.random().toString(16).slice(2, 8)
      }`;
      pyodide.FS.mkdirTree(sessionDir);

      const writeFile = (name, content) => {
        const sanitized = name.split("/").pop();
        pyodide.FS.writeFile(`${sessionDir}/${sanitized}`, content);
        return sanitized;
      };

      const mainFile = writeFile(primaryName, code);
      supportingFiles.forEach((file) => writeFile(file.filename, file.code));

      const resolvedRunner =
        typeof runSnippet === "function"
          ? runSnippet({ sessionDir, mainFile })
          : runSnippet;

      const runner =
        resolvedRunner ||
        `import runpy\nrunpy.run_path("${sessionDir}/${mainFile}", run_name="__main__")`;

      const result = await pyodide.runPythonAsync(
        [
          'import sys, io',
          `sys.path.insert(0, "${sessionDir}")`,
          "_buffer = io.StringIO()",
          "_old_out, _old_err = sys.stdout, sys.stderr",
          "sys.stdout = sys.stderr = _buffer",
          "try:",
          indentSnippet(runner),
          "finally:",
          "    sys.stdout = _old_out",
          "    sys.stderr = _old_err",
          "_buffer.getvalue()",
        ].join("\n")
      );

      setOutput(result.trim() || "(no output)");
    } catch (err) {
      setError(err?.message || String(err));
    } finally {
      setIsRunning(false);
      setIsLoadingRuntime(false);
    }
  };

  return (
    <section className="code-block">
      <div className="code-header">
        <div>
          <span className="code-title">{title}</span>
          <span className="code-filename">{filename}</span>
        </div>
        <button
          className="run-button"
          onClick={handleRun}
          disabled={isRunning}
        >
          {isRunning
            ? isLoadingRuntime
              ? "Loading Python..."
              : "Running..."
            : "Run code"}
        </button>
      </div>

      <pre className="code-pre">
        <code>{code}</code>
      </pre>

      <div className="code-output">
        <div className="code-output__label">Execution output</div>
        {error ? (
          <pre className="code-output__body code-output__body--error">
            {error}
          </pre>
        ) : (
          <pre className="code-output__body">
            {output || "Click Run code to execute the snippet."}
          </pre>
        )}
      </div>
    </section>
  );
}

export default CodeBlock;
