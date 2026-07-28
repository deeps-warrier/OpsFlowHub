import "./AdvancedDashboard.css";
import { useEffect, useState } from "react";
import axios from "axios";
import DoctorDepartmentTable from "./components/DoctorDepartmentTable";
import DepartmentTotalsTable from "./components/DepartmentTotalsTable";

export default function AdvancedDashboard() {

  const [matrix,setMatrix] = useState([])
  const [deptTotals,setDeptTotals] = useState([])

  const [departments,setDepartments] = useState([])
  const [doctors,setDoctors] = useState([])

  const [start,setStart] = useState("")
  const [end,setEnd] = useState("")
  const [department,setDepartment] = useState("")
  const [doctor,setDoctor] = useState("")


  async function loadFilters(){

    try{

      const res = await axios.get(
        "http://127.0.0.1:8000/analytics/filter-options"
      )

      setDepartments(res.data.departments || [])
      setDoctors(res.data.doctors || [])

    }catch(e){
      console.error("Filter load error",e)
    }

  }


  async function loadData(){

    try{

      const matrixRes = await axios.get(
        "http://127.0.0.1:8000/analytics/doctor-department-matrix",
        {
          params:{ start,end,department,doctor }
        }
      )

      const deptRes = await axios.get(
        "http://127.0.0.1:8000/analytics/department-totals",
        {
          params:{ start,end,department,doctor }
        }
      )

      setMatrix(matrixRes.data || [])
      setDeptTotals(deptRes.data || [])

    }catch(e){
      console.error("Advanced dashboard error",e)
    }

  }


  useEffect(()=>{
    loadData()
    loadFilters()
  },[])



  return (

    <div className="advanced-container">

      <h2 className="advanced-title">
        CFO & Operations Dashboard
      </h2>


      {/* FILTER BAR */}

      <div className="filter-card">

        <input
          type="date"
          value={start}
          onChange={e=>setStart(e.target.value)}
        />

        <input
          type="date"
          value={end}
          onChange={e=>setEnd(e.target.value)}
        />

        <select
          value={department}
          onChange={e=>setDepartment(e.target.value)}
        >
          <option value="">All Departments</option>

          {departments.map((d)=>(
            <option key={d} value={d}>{d}</option>
          ))}
        </select>

        <select
          value={doctor}
          onChange={e=>setDoctor(e.target.value)}
        >
          <option value="">All Doctors</option>

          {doctors.map((d)=>(
            <option key={d} value={d}>{d}</option>
          ))}
        </select>

        <button onClick={loadData}>
          Apply
        </button>

      </div>


      {/* DOCTOR MATRIX */}

      <div className="section">
        <DoctorDepartmentTable data={matrix}/>
      </div>


      {/* DEPARTMENT TOTALS */}

      <div className="section">
        <DepartmentTotalsTable data={deptTotals}/>
      </div>


    </div>
  )
}