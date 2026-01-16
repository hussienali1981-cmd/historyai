import React, { useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import CreateJob from "./pages/CreateJob";
import JobStatus from "./pages/JobStatus";

export default function App(){
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [page, setPage] = useState("create");

  if(!token){
    return <div style={{padding:20}}>
      <h2>HistoryAI</h2>
      <Signup onToken={(t)=>{ setToken(t); localStorage.setItem("token", t); }} />
      <hr/>
      <Login onToken={(t)=>{ setToken(t); localStorage.setItem("token", t); }} />
    </div>
  }

  return (
    <div style={{padding:20}}>
      <header>
        <button onClick={()=>{ setPage("create") }}>إنشاء فيديو</button>
        <button onClick={()=>{ setPage("status") }}>حالات الفيديو</button>
        <button onClick={()=>{ localStorage.removeItem("token"); setToken(null); }}>خروج</button>
      </header>
      <main>
        {page==="create" && <CreateJob token={token} />}
        {page==="status" && <JobStatus token={token} />}
      </main>
    </div>
  )
}
