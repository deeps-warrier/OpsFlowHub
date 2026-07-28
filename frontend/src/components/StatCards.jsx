export default function StatCards({ exec, canteen }) {
  return (
    <div className="cards">
      <div className="card">
        <h4>Total Revenue</h4>
        <p>₹ {(exec.revenue_per_op * exec.op_ip_conversion * 0 + 0) || ""}</p>
      </div>

      <div className="card">
        <h4>Canteen Revenue</h4>
        <p>₹ {canteen.toLocaleString()}</p>
      </div>

      <div className="card">
        <h4>Revenue / OP</h4>
        <p>₹ {exec.revenue_per_op.toLocaleString()}</p>
        <small>Canteen excluded</small>
      </div>

      <div className="card">
        <h4>OP → IP Conversion</h4>
        <p>{exec.op_ip_conversion}%</p>
      </div>

      <div className="card">
        <h4>Bed Load</h4>
        <p>{exec.bed_proxy}%</p>
      </div>
    </div>
  );
}
