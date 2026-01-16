import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function signup(email, password){
  const res = await axios.post(`${API_BASE}/signup`, { email, password });
  return res.data;
}

export async function login(email, password){
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  const res = await axios.post(`${API_BASE}/token`, params);
  return res.data;
}

export function authHeader(token){
  return { headers: { Authorization: `Bearer ${token}` } };
}

export async function createJob(token, topic, language="ar", duration=12){
  const res = await axios.post(`${API_BASE}/api/jobs`, { topic, language, duration_minutes: duration }, authHeader(token));
  return res.data;
}

export async function getJob(token, id){
  const res = await axios.get(`${API_BASE}/api/jobs/${id}`, authHeader(token));
  return res.data;
}
