import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // This lets Vite treat .py files as importable assets (for ?raw)
  assetsInclude: ["**/*.py"],
  server: {
    port: 5173, // change if you like
  },
});
