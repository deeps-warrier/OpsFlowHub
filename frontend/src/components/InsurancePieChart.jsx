import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { useEffect, useState } from "react";

export default function InsurancePieChart({ govtTotal, privateTotal }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setTimeout(() => setShow(true), 200);
  }, []);

  const data = [
    { name: "Govt Insurance", value: govtTotal || 0 },
    { name: "Private Insurance", value: privateTotal || 0 }
  ];

  const total = (govtTotal || 0) + (privateTotal || 0);

  const COLORS = ["#3b82f6", "#22c55e"];

  if (total === 0) return null;

  return (
    <div className={`insurance-chart ${show ? "show" : ""}`}>
      <h4 style={{ marginBottom: 15 }}>Insurance Share</h4>

      <div className="donut-wrapper" style={{ height: 250 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              innerRadius={70}
              outerRadius={100}
              paddingAngle={4}
              dataKey="value"
              className="donut-segment"
            >
              {data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `₹ ${value.toLocaleString()}`} />
          </PieChart>
        </ResponsiveContainer>
        
        <div className="donut-center">
          ₹ {total.toLocaleString()}
        </div>
      </div>
    </div>
    
  );
}
