import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function DailyRevenueChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div style={{ height: 320 }}>
      <h3 style={{ marginBottom: 10 }}>Daily Revenue Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={(v) => `₹ ${v.toLocaleString()}`} />
          <Line
            type="monotone"
            dataKey="total"
            stroke="#4f46e5"
            strokeWidth={3}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
