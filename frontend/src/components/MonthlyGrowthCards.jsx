export default function MonthlyGrowthCards({ data }) {
  if (!data) return null;

  const arrow = (value) =>
    value > 0 ? "▲" : value < 0 ? "▼" : "→";

  const arrowClass = (value) =>
    value > 0 ? "up" : value < 0 ? "down" : "flat";

  return (
    <div className="section">
      <h3>Monthly Growth</h3>
      <div className="card-grid">

        <div className="card">
          <h4>MoM Growth</h4>
          <p className={arrowClass(data.mom_growth_percent)}>
            {arrow(data.mom_growth_percent)} {data.mom_growth_percent}%
          </p>
        </div>

        <div className="card">
          <h4>YoY Growth</h4>
          <p className={arrowClass(data.yoy_growth_percent)}>
            {arrow(data.yoy_growth_percent)} {data.yoy_growth_percent}%
          </p>
        </div>

      </div>
    </div>
  );
}
