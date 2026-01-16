import React, { useState } from "react";
import { createJob } from "../api";

export default function CreateJob({ token }){
  const [topic, setTopic] = useState("");
  const [duration, setDuration] = useState(12);
  const [message, setMessage] = useState("");

  async function submit(e){
    e.preventDefault();
    const job = await createJob(token, topic, "ar", duration);
    setMessage(`Job created: ${job.id}`);
  }

  return (
    <form onSubmit={submit}>
      <h3>إنشاء فيديو تاريخي</h3>
      <input placeholder="موضوع (مثال: سقوط الإمبراطورية الرومانية)" value={topic} onChange={e=>setTopic(e.target.value)} />
      <select value={duration} onChange={e=>setDuration(parseInt(e.target.value))}>
        <option value={10}>10 دقيقة</option>
        <option value={12}>12 دقيقة</option>
        <option value={15}>15 دقيقة</option>
      </select>
      <button>ابدأ التوليد</button>
      <div>{message}</div>
    </form>
  )
}
