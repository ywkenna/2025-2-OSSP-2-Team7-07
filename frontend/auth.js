// auth.js

const API_BASE = "http://127.0.0.1:8000";

// 토큰 가져오기
function getToken() {
  return localStorage.getItem("access");
}

// 공통 헤더
function authHeaders(isJson = true) {
  const headers = {};
  if (isJson) headers["Content-Type"] = "application/json";

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  return headers;
}

// ✅ 로그인 여부 + 유저 정보
async function checkAuth() {
  const access = getToken();
  if (!access) {
    window.currentUser = null;
    return false;
  }

  try {
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${access}`,
      },
    });

    if (!res.ok) {
      console.warn("userinfo status:", res.status);
      window.currentUser = null;
      if (res.status === 401 || res.status === 403) {
        localStorage.removeItem("access");
      }
      return false;
    }

    const data = await res.json();
    window.currentUser = data;
    return true;
  } catch (e) {
    console.error("checkAuth error:", e);
    window.currentUser = null;
    return false;
  }
}

// ✅ 상단 네비게이션 버튼 바꾸기
function updateNavbar() {
  const loginBtn = document.querySelector(".top-login-btn");
  const signupBtn = document.querySelector(".top-signup-btn");

  if (!loginBtn || !signupBtn) return;

  if (window.currentUser) {
    // 로그인 상태
    loginBtn.textContent = "마이페이지";
    loginBtn.href = "mypage.html";

    signupBtn.textContent = "로그아웃";
    signupBtn.href = "#";
    signupBtn.onclick = (e) => {
      e.preventDefault();
      localStorage.removeItem("access");
      window.currentUser = null;
      alert("로그아웃되었습니다.");
      window.location.href = "home.html";
    };
  } else {
    // 비로그인 상태
    loginBtn.textContent = "로그인";
    loginBtn.href = "login.html";
    loginBtn.onclick = null;

    signupBtn.textContent = "회원가입";
    signupBtn.href = "signup.html";
    signupBtn.onclick = null;
  }
}
