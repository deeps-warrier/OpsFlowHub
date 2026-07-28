import { useState } from "react";

export default function OPCard({ data }) {
  const [open, setOpen] = useState(false);

  if (!data) return null;

  return (
    <div className="card" onClick={() => setOpen(!open)} style={{ cursor: "pointer" }}>
      <h4>Total OP</h4>
      <p style={{ fontSize: "22px", fontWeight: "600" }}>
        {data.TOTAL || 0}
      </p>

      {open && (
        <div style={{ marginTop: "10px", fontSize: "14px" }}>
          <div>New: {data.New || 0}</div>
          <div>Follow-up: {data.Followup || 0}</div>
          <div>Revisit: {data.Renewal || 0}</div>
        </div>
      )}
    </div>
  );
}
