import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import DailyRevenueChart from "./components/DailyRevenueChart";
import OPDailyChart from "./components/OPDailyChart";
import IPDailyChart from "./components/IPDailyChart";
import CombinedDailyChart from "./components/CombinedDailyChart";
import DoctorLeaderboard from "./components/DoctorLeaderboard";
import OPCard from "./components/OPCard";
import DepartmentLeaderboard from "./components/DepartmentLeaderboard";
import MonthlyGrowthCards from "./components/MonthlyGrowthCards";
import RevenueExpandableCard from "./components/RevenueExpandableCard";
import InsurancePieChart from "./components/InsurancePieChart";
import OPRevenueMixChart from "./components/OPRevenueMixChart";
import DoctorConversionTable from "./components/DoctorConversionTable";

const API = "https://opsflowhub-backend.onrender.com";

export default function MainDashboard() {

const navigate = useNavigate();

const [backendOk,setBackendOk] = useState(false);

const [kpis,setKpis] = useState(null);
const [exec,setExec] = useState(null);
const [ipCards,setIpCards] = useState(null);

const [dailyRevenue,setDailyRevenue] = useState([]);
const [opDaily,setOpDaily] = useState([]);
const [ipDaily,setIpDaily] = useState([]);

const [doctorRev,setDoctorRev] = useState({});
const [doctorTrend,setDoctorTrend] = useState({});
const [opCounts,setOpCounts] = useState(null);

const [deptTop,setDeptTop] = useState(null);
const [monthlyGrowth,setMonthlyGrowth] = useState(null);

const [labData,setLabData] = useState(null);
const [radiologyData,setRadiologyData] = useState(null);
const [govtData,setGovtData] = useState(null);
const [privateData,setPrivateData] = useState(null);
const [healthData,setHealthData] = useState(null);
const [intlData,setIntlData] = useState(null);
const [fbData,setFbData] = useState(null);

const [pharmacyData,setPharmacyData] = useState(null);
const [physioData,setPhysioData] = useState(null);
const [homeCareData,setHomeCareData] = useState(null);

const [runRate,setRunRate] = useState(null);

const [opMix,setOpMix] = useState(null);
const [doctorProductivity,setDoctorProductivity] = useState([]);
const [doctorConversion,setDoctorConversion] = useState([]);


useEffect(() => {

    async function loadDashboard() {

        const requests = [

            axios.get(`${API}/revenue/kpis`),

            axios.get(`${API}/executive/metrics`),

            axios.get(`${API}/executive/ip-cards`),

            axios.get(`${API}/revenue/daily`),

            axios.get(`${API}/op/daily`),

            axios.get(`${API}/ip/daily`),

            axios.get(`${API}/revenue/by-doctor`),

            axios.get(`${API}/revenue/doctor-trends`),

            axios.get(`${API}/op/counts`),

            axios.get(`${API}/revenue/top10-departments`),

            axios.get(`${API}/revenue/monthly-growth`),

            axios.get(`${API}/revenue/lab`),

            axios.get(`${API}/revenue/radiology`),

            axios.get(`${API}/revenue/govt-insurance`),

            axios.get(`${API}/revenue/health-package`),

            axios.get(`${API}/revenue/private-insurance`),

            axios.get(`${API}/revenue/international`),

            axios.get(`${API}/revenue/fb`),

            axios.get(`${API}/revenue/pharmacy`),

            axios.get(`${API}/revenue/physiotherapy`),

            axios.get(`${API}/revenue/homecare`),

            axios.get(`${API}/revenue/run-rate`),

            axios.get(`${API}/revenue/op-mix`),

            axios.get(`${API}/doctor/productivity`),

            axios.get(`${API}/doctor/conversion`)

        ];


        const results = await Promise.allSettled(requests);


        results.forEach((result,index) => {

            if (result.status === "rejected") {

                console.error(
                    "FAILED API:",
                    index,
                    result.reason?.config?.url ||
                    result.reason?.message ||
                    result.reason
                );

            }

        });


        const data = (index,fallback=null) => {

            if (results[index]?.status === "fulfilled") {

                return results[index].value.data;

            }

            return fallback;

        };


        setKpis(data(0));

        setExec(data(1));

        setIpCards(data(2));


        setDailyRevenue(data(3,[]));

        setOpDaily(data(4,[]));

        setIpDaily(data(5,[]));


        setDoctorRev(data(6,{}) || {});

        setDoctorTrend(data(7,{}) || {});


        setOpCounts(data(8));

        setDeptTop(data(9));

        setMonthlyGrowth(data(10));


        setLabData(data(11));

        setRadiologyData(data(12));


        setGovtData(data(13));

        setHealthData(data(14));

        setPrivateData(data(15));

        setIntlData(data(16));

        setFbData(data(17));


        setPharmacyData(data(18));

        setPhysioData(data(19));

        setHomeCareData(data(20));


        setRunRate(data(21));

        setOpMix(data(22));


        setDoctorProductivity(data(23,[]) || []);

        setDoctorConversion(data(24,[]) || []);


        const successfulRequests = results.filter(
            result => result.status === "fulfilled"
        ).length;


        setBackendOk(successfulRequests > 0);


        console.log(
            `OpsFlowHub: ${successfulRequests}/${results.length} API calls successful`
        );

    }


    loadDashboard();

}, []);

setKpis(kpisRes.data)
setExec(execRes.data)
setIpCards(ipCardsRes.data)

setDailyRevenue(dailyRevRes.data || [])
setOpDaily(opRes.data || [])
setIpDaily(ipRes.data || [])

setDoctorRev(doctorRes.data || {})
setDoctorTrend(trendRes.data || {})
setOpCounts(opCountsRes.data || null)

setDeptTop(deptRes.data || null)
setMonthlyGrowth(growthRes.data || null)

setLabData(labRes.data || null)
setRadiologyData(radioRes.data || null)

setGovtData(govtRes.data || null)
setPrivateData(privateRes.data || null)

setHealthData(healthRes.data)
setIntlData(intlRes.data)
setFbData(fbRes.data)

setPharmacyData(pharmacyRes.data)
setPhysioData(physioRes.data)
setHomeCareData(homeCareRes.data)

setRunRate(runRateRes.data)
setOpMix(opMixRes.data)

setDoctorProductivity(productivityRes.data || [])
setDoctorConversion(conversionRes.data || [])

setBackendOk(true)

}catch(err){

console.error("Dashboard load failed",err)
setBackendOk(false)

}

}

loadDashboard()

},[])

return (

<div className="container">

{/* Header */}

<div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>

<div>
<h1>OpsFlowHub</h1>
<h2>Hospital Operations Dashboard</h2>
</div>

<button
className="advanced-btn"
onClick={() => navigate("/advanced")}
>
Advanced View
</button>

</div>

{backendOk && (
<div className="status">
Backend connected ✅
</div>
)}

{/* Revenue KPIs */}

{(kpis || opCounts) && (

<div className="section">

<h3>Revenue & OP KPIs</h3>

<div className="card-grid">

{kpis && (
<>
<div className="card">
<h4>Revenue MTD</h4>
<p>₹ {kpis.mtd?.toFixed(0)}</p>
</div>

<div className="card">
<h4>Revenue CYTD</h4>
<p>₹ {kpis.cytd?.toFixed(0)}</p>
</div>

<div className="card">
<h4>Revenue FYTD</h4>
<p>₹ {kpis.fytd?.toFixed(0)}</p>
</div>
</>
)}

{opCounts && <OPCard data={opCounts} />}

{runRate && (
<div className="card">
<h4>Month End Forecast</h4>
<p>₹ {runRate.month_end_forecast?.toLocaleString()}</p>
</div>
)}

</div>

</div>
)}

{/* Executive Metrics */}

{exec && (

<div className="section">

<h3>Executive Metrics</h3>

<div className="card-grid">

<div className="card">
<h4>Avg Revenue / OP</h4>
<p>₹ {exec.revenue_per_op?.toLocaleString()}</p>
</div>

<div className="card">
<h4>Avg Revenue / IP</h4>
<p>₹ {exec.revenue_per_ip?.toLocaleString()}</p>
</div>

<div className="card">
<h4>Revenue / Bed Day</h4>
<p>₹ {exec.revenue_per_bed_day?.toLocaleString()}</p>
</div>

<div className="card">
<h4>OP → IP Conversion</h4>
<p>{exec.op_ip_conversion}%</p>
</div>

<div className="card">
<h4>Bed Load %</h4>
<p>{exec.bed_proxy}%</p>
</div>

</div>

</div>

)}

{/* OP Mix */}

{opMix && (

<div className="section">

<h3>OP Revenue Mix</h3>

<div className="card">
<OPRevenueMixChart data={opMix}/>
</div>

</div>

)}

{/* Doctor Productivity */}

{doctorProductivity && doctorProductivity.length > 0 && (

<div className="section">

<h3>Doctor Productivity</h3>

<div className="card">

<table className="dashboard-table">

<thead>
<tr>
<th>Doctor</th>
<th>OP Visits</th>
<th>Revenue / OP</th>
</tr>
</thead>

<tbody>

{doctorProductivity.map((d,i)=>(

<tr key={i}>
<td>{d.doctor}</td>
<td>{d.op_count}</td>
<td>₹ {(d.revenue_per_op || 0).toLocaleString()}</td>
</tr>

))}

</tbody>

</table>

</div>

</div>

)}

{/* Doctor Conversion */}

{doctorConversion && doctorConversion.length > 0 && (

<div className="section">

<h3>Doctor Diagnostic Conversion</h3>

<div className="card">

<DoctorConversionTable data={doctorConversion}/>

</div>

</div>

)}

{monthlyGrowth && (
<MonthlyGrowthCards data={monthlyGrowth}/>
)}

{/* Revenue Blocks */}

<div className="section">

<h3>Revenue Blocks</h3>

<div className="card-grid">

{pharmacyData && (
<RevenueExpandableCard
title="Pharmacy Revenue"
total={pharmacyData.total}
breakdown={pharmacyData.breakdown}
/>
)}

{labData && (
<RevenueExpandableCard
title="Lab Revenue"
total={labData.total}
breakdown={labData.breakdown}
/>
)}

{radiologyData && (
<RevenueExpandableCard
title="Radiology Revenue"
total={radiologyData.total}
breakdown={radiologyData.breakdown}
/>
)}

{physioData && (
<RevenueExpandableCard
title="Physiotherapy"
total={physioData.total}
breakdown={physioData.breakdown}
/>
)}

{homeCareData && (
<div className="card">
<h4>Home Care</h4>
<p>₹ {homeCareData.total?.toLocaleString()}</p>
</div>
)}

{healthData && (
<div className="card">
<h4>Health Package</h4>
<p>₹ {healthData.total?.toLocaleString()}</p>
</div>
)}

{intlData && (
<div className="card">
<h4>International Patients</h4>
<p>₹ {intlData.total?.toLocaleString()}</p>
</div>
)}

{fbData && (
<div className="card">
<h4>F & B Revenue</h4>
<p>₹ {fbData.total?.toLocaleString()}</p>
</div>
)}

</div>

</div>

{/* Insurance */}

{(govtData || privateData) && (

<div className="section">

<h3>Insurance</h3>

<div className="card-grid">

{govtData && (
<RevenueExpandableCard
title="Govt Insurance"
total={govtData.total}
breakdown={govtData.breakdown}
/>
)}

{privateData && (
<RevenueExpandableCard
title="Private Insurance"
total={privateData.total}
breakdown={privateData.breakdown}
/>
)}

{govtData?.total > 0 && privateData?.total > 0 && (
<InsurancePieChart
govtTotal={govtData.total}
privateTotal={privateData.total}
/>
)}

</div>

</div>

)}

{/* Charts */}

{dailyRevenue.length > 0 && (
<div className="section">
<h3>Daily Revenue Trend</h3>
<div className="card">
<DailyRevenueChart data={dailyRevenue}/>
</div>
</div>
)}

{opDaily.length > 0 && (
<div className="section">
<h3>Daily OP Trend</h3>
<div className="card">
<OPDailyChart data={opDaily}/>
</div>
</div>
)}

{ipDaily.length > 0 && (
<div className="section">
<h3>Daily IP Trend</h3>
<div className="card">
<IPDailyChart data={ipDaily}/>
</div>
</div>
)}

{dailyRevenue.length>0 && opDaily.length>0 && ipDaily.length>0 && (
<div className="section">
<h3>OP vs IP vs Revenue</h3>
<div className="card">
<CombinedDailyChart
revenue={dailyRevenue}
op={opDaily}
ip={ipDaily}
/>
</div>
</div>
)}

{/* Doctor Leaderboard */}

{doctorRev && Object.keys(doctorRev).length > 0 && (
<div className="section">
<DoctorLeaderboard data={doctorRev} trends={doctorTrend}/>
</div>
)}

{/* Department Leaderboard */}

{deptTop && (
<div className="section">
<DepartmentLeaderboard data={deptTop}/>
</div>
)}

</div>

)

}
