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

        /*
         * ==========================================
         * STAGE 1
         * FAST / ESSENTIAL DASHBOARD APIs
         * ==========================================
         */

        const fastRequests = [
            axios.get(`${API}/revenue/kpis`),
            axios.get(`${API}/executive/ip-cards`),
            axios.get(`${API}/revenue/daily`),
            axios.get(`${API}/op/daily`),
            axios.get(`${API}/ip/daily`),
            axios.get(`${API}/revenue/doctor-trends`),
            axios.get(`${API}/op/counts`)
        ];


        const fastResults = await Promise.allSettled(fastRequests);


        fastResults.forEach((result, index) => {

            if (result.status === "rejected") {

                console.error(
                    "FAST API FAILED:",
                    index,
                    result.reason?.config?.url ||
                    result.reason?.message
                );

            }

        });


        const fastData = (index, fallback = null) => {

            if (fastResults[index]?.status === "fulfilled") {
                return fastResults[index].value.data;
            }

            return fallback;

        };


        /*
         * ==========================================
         * SET FAST DATA
         * ==========================================
         */

        setKpis(
            fastData(0)
        );

        setIpCards(
            fastData(1)
        );

        setDailyRevenue(
            fastData(2, []) || []
        );

        setOpDaily(
            fastData(3, []) || []
        );

        setIpDaily(
            fastData(4, []) || []
        );

        setDoctorTrend(
            fastData(5, {}) || {}
        );

        setOpCounts(
            fastData(6)
        );


        /*
         * Dashboard is already usable
         */

        setBackendOk(true);


        console.log(
            "OpsFlowHub: Fast dashboard loaded"
        );


        /*
         * ==========================================
         * STAGE 2
         * EXECUTIVE METRICS
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/executive/metrics`);

            setExec(response.data);

        } catch (error) {

            console.error(
                "Executive metrics failed:",
                error?.config?.url ||
                error?.message
            );

        }


        /*
         * ==========================================
         * STAGE 3
         * DOCTOR / DEPARTMENT
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/revenue/by-doctor`);

            setDoctorRev(
                response.data || {}
            );

        } catch (error) {

            console.error(
                "Doctor revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/top10-departments`);

            setDeptTop(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Department revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        /*
         * ==========================================
         * STAGE 4
         * MONTHLY
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/revenue/monthly-growth`);

            setMonthlyGrowth(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Monthly growth failed:",
                error?.config?.url ||
                error?.message
            );

        }


        /*
         * ==========================================
         * STAGE 5
         * REVENUE BLOCKS
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/revenue/lab`);

            setLabData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Lab revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/radiology`);

            setRadiologyData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Radiology revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/pharmacy`);

            setPharmacyData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Pharmacy revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/physiotherapy`);

            setPhysioData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Physiotherapy revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/homecare`);

            setHomeCareData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Homecare revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        /*
         * ==========================================
         * STAGE 6
         * INSURANCE / OTHER REVENUE
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/revenue/govt-insurance`);

            setGovtData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Government insurance failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/private-insurance`);

            setPrivateData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Private insurance failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/health-package`);

            setHealthData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Health package failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/international`);

            setIntlData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "International revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/fb`);

            setFbData(
                response.data || null
            );

        } catch (error) {

            console.error(
                "F&B revenue failed:",
                error?.config?.url ||
                error?.message
            );

        }


        /*
         * ==========================================
         * STAGE 7
         * ADVANCED ANALYTICS
         * ==========================================
         */

        try {

            const response =
                await axios.get(`${API}/revenue/run-rate`);

            setRunRate(
                response.data || null
            );

        } catch (error) {

            console.error(
                "Run rate failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/revenue/op-mix`);

            setOpMix(
                response.data || null
            );

        } catch (error) {

            console.error(
                "OP mix failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/doctor/productivity`);

            setDoctorProductivity(
                response.data || []
            );

        } catch (error) {

            console.error(
                "Doctor productivity failed:",
                error?.config?.url ||
                error?.message
            );

        }


        try {

            const response =
                await axios.get(`${API}/doctor/conversion`);

            setDoctorConversion(
                response.data || []
            );

        } catch (error) {

            console.error(
                "Doctor conversion failed:",
                error?.config?.url ||
                error?.message
            );

        }


        console.log(
            "OpsFlowHub: Dashboard loading completed"
        );

    }


    loadDashboard();

}, []);

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
