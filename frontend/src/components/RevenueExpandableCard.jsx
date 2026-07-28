import { useState } from "react";
import "./RevenueExpandableCard.css";

export default function RevenueExpandableCard({ title, total, breakdown }) {
  const [open, setOpen] = useState(false);

  return (
    <div className={`expand-card ${open ? "open" : ""}`}>
      <div className="expand-header" onClick={() => setOpen(!open)}>
        <h4>{title}</h4>
        <div className="right">
          <span className="amount">₹ {total?.toLocaleString()}</span>
          <span className={`arrow ${open ? "rotate" : ""}`}>▼</span>
        </div>
      </div>

      <div className="expand-body">
        {breakdown &&
          Object.entries(breakdown).map(([k, v]) => (
            <div className="row" key={k}>
              <span>{k}</span>
              <span>₹ {v.toLocaleString()}</span>
            </div>
          ))}
      </div>
    </div>
  );
}
