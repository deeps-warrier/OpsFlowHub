import { Sankey, Tooltip } from "recharts";

export default function RevenueSankey({ data }) {

  const sankeyData = {
    nodes: [
      { name: "Patients" },
      { name: "Consultation" },
      { name: "Lab" },
      { name: "Radiology" },
      { name: "Pharmacy" }
    ],
    links: [
      { source: 0, target: 1, value: data.Consultation || 0 },
      { source: 0, target: 2, value: data.Lab || 0 },
      { source: 0, target: 3, value: data.Radiology || 0 },
      { source: 0, target: 4, value: data.Pharmacy || 0 }
    ]
  };

  return (

    <Sankey
      width={700}
      height={350}
      data={sankeyData}
      nodePadding={40}
      margin={{ top: 20, bottom: 20, left: 20, right: 20 }}
    >
      <Tooltip />
    </Sankey>

  );
}