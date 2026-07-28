import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

export default function OPRevenueMixChart({ data }) {

  const chartData = [
    { name: "Consultation", value: data.Consultation || 0 },
    { name: "Pharmacy", value: data.Pharmacy || 0 },
    { name: "Lab", value: data.Lab || 0 },
    { name: "Radiology", value: data.Radiology || 0 }
  ];

  const COLORS = ["#0088FE","#00C49F","#FFBB28","#FF8042"];

  return (

    <PieChart width={400} height={300}>

      <Pie
        data={chartData}
        cx="50%"
        cy="50%"
        outerRadius={100}
        dataKey="value"
        label
      >

        {chartData.map((entry, index) => (
          <Cell key={index} fill={COLORS[index % COLORS.length]} />
        ))}

      </Pie>

      <Tooltip />
      <Legend />

    </PieChart>

  );

}