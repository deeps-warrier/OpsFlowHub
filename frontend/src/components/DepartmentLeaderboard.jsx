export default function DepartmentLeaderboard({ data }) {
  if (!data) return null;

  const total = Object.values(data).reduce((a, b) => a + b, 0);

  const rows = Object.entries(data)
    .sort((a, b) => b[1] - a[1]);

  return (
    <div className="leaderboard-card">
      <h3>Top 10 Departments</h3>

      {rows.map(([dept, value], i) => {
        const percent = ((value / total) * 100);
        const width = (value / rows[0][1]) * 100;

        return (
          <div key={dept} className="leader-row">
            <div className="rank">{i + 1}</div>
            <div className="doc-name">{dept}</div>

            <div className="bar">
              <div
                className="fill"
                style={{ width: `${width}%` }}
              />
            </div>

            <div className="amt">
              ₹ {value.toLocaleString()}
              <div style={{ fontSize: 11, color: "#94a3b8" }}>
                {percent.toFixed(1)}%
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
