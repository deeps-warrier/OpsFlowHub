import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function CombinedDailyChart({ revenue, op, ip }) {
  if (!revenue || !op || !ip) return null;

  /**
   * Normalize all three datasets by date
   * revenue: [{ date, total }]
   * op      : [{ date, count }]
   * ip      : [{ date, count }]
   */

  const map = {};

  revenue.forEach(r => {
    map[r.date] = {
      date: r.date,
      revenue: r.total || 0,
      op: 0,
      ip: 0
    };
  });

  op.forEach(o => {
    if (!map[o.date]) {
      map[o.date] = { date: o.date, revenue: 0, op: 0, ip: 0 };
    }
    map[o.date].op = o.count || 0;
  });

  ip.forEach(i => {
    if (!map[i.date]) {
      map[i.date] = { date: i.date, revenue: 0, op: 0, ip: 0 };
    }
    map[i.date].ip = i.count || 0;
  });

  const data = Object.values(map).sort((a, b) =>
    a.date.localeCompare(b.date)
  );

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />

        <Line
          type="monotone"
          dataKey="revenue"
          stroke="#4f46e5"
          strokeWidth={2}
          name="Revenue"
        />

        <Line
          type="monotone"
          dataKey="op"
          stroke="#16a34a"
          strokeWidth={2}
          name="OP Count"
        />

        <Line
          type="monotone"
          dataKey="ip"
          stroke="#dc2626"
          strokeWidth={2}
          name="IP Count"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
