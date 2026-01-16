import React, { useState } from "react";
import { signup } from "../api";

export default function Signup({ onToken }){
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");

  async function submit(e){
    e.preventDefault();
    const res = await signup(email,password);
    onToken(res.access_token);
  }

  return (
    <form onSubmit={submit}>
      <h3>تسجيل حساب جديد</h3>
      <input placeholder="البريد" value={email} onChange={e=>setEmail(e.target.value)} />
      <input placeholder="كلمة المرور" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button>تسجيل</button>
    </form>
  )
}
