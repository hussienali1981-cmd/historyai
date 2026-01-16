import React, { useState } from "react";
import { getJob } from "../api";

export default function JobStatus({ token }){
  const [jobId, setJobId] = useState("");
  const [job, setJob] = useState(null);

  async function check(e){
    e.preventDefault();
    const res = await getJob(token, jobId);
    setJob(res);
  }

  return (
    <div>
      <h3>حالة الفيديو</h3>
      <form onSubmit={check}>
        <input placeholder="Job ID" value={jobId} onChange={e=>setJobId(e.target.value)} />
        <button>تحقق</button>
      </form>
      {job && <div>
        <p>الحالة: {job.status}</p>
        {job.status==="done" && <a href={job.result_path} target="_blank">تحميل الفيديو</a>}
        {job.error && <pre>{job.error}</pre>}
      </div>}
    </div>
  )
}
