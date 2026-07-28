export default function DoctorConversionTable({ data = [] }) {

return (

<table className="dashboard-table">

<thead>
<tr>
<th>Doctor</th>
<th>OP</th>
<th>Lab %</th>
<th>Radiology %</th>
<th>Pharmacy %</th>
<th>Revenue / Patient</th>
</tr>
</thead>

<tbody>

{data.map((d,i)=>{

const revenue = d.revenue_per_patient || 0

return (

<tr key={i}>
<td>{d.doctor}</td>
<td>{d.op || 0}</td>
<td>{d.lab_percent || 0}%</td>
<td>{d.radiology_percent || 0}%</td>
<td>{d.pharmacy_percent || 0}%</td>
<td>₹ {revenue.toLocaleString()}</td>
</tr>

)

})}

</tbody>

</table>

)

}