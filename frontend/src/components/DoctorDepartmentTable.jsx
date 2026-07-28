import { useState } from "react"
import "./dashboard-table.css"

export default function DoctorDepartmentTable({ data }) {

  const [search,setSearch] = useState("")

  const filtered = (data || []).filter(d =>
    (d.doctor || "").toLowerCase().includes(search.toLowerCase()) ||
    (d.department || "").toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="dashboard-card">

      <div className="dashboard-title">
        Doctor Performance Matrix
      </div>

      <input
        placeholder="Search doctor or department..."
        value={search}
        onChange={e=>setSearch(e.target.value)}
        style={{
          marginBottom:"10px",
          padding:"8px",
          width:"300px"
        }}
      />

      <table className="dashboard-table">

        <thead>
          <tr>
            <th>Department</th>
            <th>Doctor</th>
            <th>OP</th>
            <th>IP</th>
            <th>Total Revenue</th>
            <th>Pharmacy</th>
            <th>Lab</th>
            <th>Radiology</th>
          </tr>
        </thead>

        <tbody>

          {filtered.map((r,i)=>(
            <tr key={i}>

              <td>{r.department}</td>
              <td>{r.doctor}</td>

              <td className="op">{r.op || 0}</td>
              <td className="ip">{r.ip || 0}</td>

              <td className="revenue">
                ₹ {(r.revenue || 0).toLocaleString()}
              </td>

              <td className="pharmacy">
                ₹ {(r.pharmacy || 0).toLocaleString()}
              </td>

              <td className="lab">
                ₹ {(r.lab || 0).toLocaleString()}
              </td>

              <td className="radiology">
                ₹ {(r.radiology || 0).toLocaleString()}
              </td>

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  )
}