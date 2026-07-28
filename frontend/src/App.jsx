import { Routes, Route } from "react-router-dom";
import MainDashboard from "./MainDashboard";
import AdvancedDashboard from "./AdvancedDashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainDashboard />} />
      <Route path="/advanced" element={<AdvancedDashboard />} />
    </Routes>
  );
}
