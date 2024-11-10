import React from "react";
// import ReactDOM from "react-dom";
import App from "./components/App";
import { createRoot } from 'react-dom/client';
import "./styles.css";

// ReactDOM.render(<App />, document.getElementById("root"));

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
