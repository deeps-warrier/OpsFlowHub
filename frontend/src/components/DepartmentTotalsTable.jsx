import "./dashboard-table.css"

export default function DepartmentTotalsTable({ data }) {

  return (
    <div className="dashboard-card">

      <div className="dashboard-title">
        Department Performance
      </div>

      <table className="dashboard-table">

        <thead>
          <tr>
            <th>Department</th>
            <th>OP</th>
            <th>IP</th>
            <th>Total Revenue</th>
            <th>Pharmacy</th>
            <th>Lab</th>
            <th>Radiology</th>
          </tr>
        </thead>

        <tbody>
          {data.map((r,i)=>(
            <tr key={i}>
              <td>{r.department}</td>
              <td className="op">{r.op}</td>
              <td className="ip">{r.ip}</td>
              <td className="revenue">₹ {r.revenue.toLocaleString()}</td>
              <td className="pharmacy">₹ {r.pharmacy.toLocaleString()}</td>
              <td className="lab">₹ {r.lab.toLocaleString()}</td>
              <td className="radiology">₹ {r.radiology.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>

      </table>

    </div>
  )
}


