import {useState} from "react";
import reactLogo from "./assets/react.svg";
import {invoke} from "@tauri-apps/api/core";
import {pyInvoke} from "tauri-plugin-pytauri-api";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    const rsGreeting = await invoke<string>("greet", {name});
    // Learn more about PyTauri commands at https://pytauri.github.io/pytauri/latest/usage/concepts/ipc/
    const pyGreeting = await pyInvoke<string>("greet", {name});
    setGreetMsg(rsGreeting + "\n" + pyGreeting);
  }

  return (
    <main class="container">
      <h1>Welcome to PyTauri</h1>
      <a href="https://github.com/pytauri/pytauri" target="_blank">
        <img src="/pytauri.svg" class="logo pytauri" alt="Pytauri logo"/>
      </a>
      <div class="row">
        <a href="https://vitejs.dev" target="_blank">
          <img src="/vite.svg" class="logo vite" alt="Vite logo"/>
        </a>
        <a href="https://tauri.app" target="_blank">
          <img src="/tauri.svg" class="logo tauri" alt="Tauri logo"/>
        </a>
        <a href="https://react.dev/" target="_blank">
          <img src="./assets/react.svg" class="logo react" alt="React logo"/>
        </a>
        <a href="https://python.org" target="_blank">
          <img src="/python.svg" class="logo python" alt="Python logo"/>
        </a>
      </div>
      <p>Click on any logo to learn more.</p>

      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          greet();
        }}
      >
        <input
          id="greet-input"
          onChange={(e) => setName(e.currentTarget.value)}
          placeholder="Enter a name..."
        />
        <button type="submit">Greet</button>
      </form>
      <p id="greet-msg">{greetMsg}</p>
    </main>
  );
}

export default App;
