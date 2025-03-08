import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import About from "./components/About";

function App() {
  return (
    <Router>
      <nav style={{ padding: "10px", background: "#282c34", color: "white" }}>
        <Link to="/" style={{ margin: "10px", color: "white", textDecoration: "none" }}>Dashboard</Link>
        <Link to="/about" style={{ margin: "10px", color: "white", textDecoration: "none" }}>About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;