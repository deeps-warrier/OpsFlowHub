import { Routes, Route } from "react-router-dom";
import MainDashboard from "./MainDashboard";
import AdvancedDashboard from "./AdvancedDashboard";

function Footer() {
  return (
    <footer className="app-footer">
      © 2026 · OpsFlowHub v1.0 · Designed and Developed by Deepswarrier
    </footer>
  );
}

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<MainDashboard />} />
        <Route path="/advanced" element={<AdvancedDashboard />} />
      </Routes>

      <Footer />
    </>
  );
}
