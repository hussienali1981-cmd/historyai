import React, { useState } from "react";
import { login } from "../api";

export default function Login({ onToken }){
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");

  async function submit(e){
    e.preventDefault();
    const res = await login(email,password);
    onToken(res.access_token);
  }

  return (
    <form onSubmit={submit}>
      <h3>تسجيل دخول</h3>
      <input placeholder="البريد" value={email} onChange={e=>setEmail(e.target.value)} />
      <input placeholder="كلمة المرور" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button>دخول</button>
    </form>
  )
}
