// config.js
const API_BASE = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("access");
}

function authHeaders(isJson = true) {
  const headers = {};

  if (isJson) headers["Content-Type"] = "application/json";

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  return headers;
}
