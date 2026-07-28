import "./DoctorLeaderboard.css";

export default function DoctorLeaderboard({ data, trends = {} }) {
  if (!data) return null;

  const rows = Object.entries(data)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const max = rows[0][1];

  const medalClass = (i) =>
    i === 0 ? "gold" : i === 1 ? "silver" : i === 2 ? "bronze" : "";

  const medalIcon = (i) =>
    i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i + 1;

  return (
    <div className="doctor-leaderboard">
      <h3>Top Doctors by Revenue</h3>

      {rows.map(([rawName, value], i) => {
        const [name, dept = "--"] = rawName.split("|").map(s => s.trim());
        const trend = trends[name]?.trend || "flat";

        return (
          <div className={`doc-row ${medalClass(i)}`} key={rawName}>
            <div className="rank">{medalIcon(i)}</div>

            <div className="doc-info">
              <div className="doc-name">{name}</div>
              <div className="doc-dept">{dept}</div>
            </div>

            <div className="bar">
              <div
                className="fill"
                style={{ width: `${(value / max) * 100}%` }}
              />
            </div>

            <div className="amount">
              ₹ {value.toLocaleString()}
              <span className={`trend ${trend}`}>
                {trend === "up" && " ↑"}
                {trend === "down" && " ↓"}
                {trend === "flat" && " →"}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
