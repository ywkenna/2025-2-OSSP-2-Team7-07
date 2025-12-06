// 로그인 여부 확인: 토큰으로 /api/users/userinfo/ 호출
async function checkAuth() {
  const access = localStorage.getItem("access");
  if (!access) return false;

  try {
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${access}`,
      },
    });

    if (!res.ok) {
      console.warn("userinfo status:", res.status);
      return false;
    }

    const data = await res.json();
    // 전역에 현재 유저 정보 저장 (마이페이지에서 사용)
    window.currentUser = data;
    return true;
  } catch (e) {
    console.error("checkAuth error:", e);
    return false;
  }
}

// 상단 바 버튼 상태 업데이트
function updateNavbar(isAuth) {
  const loginBtn   = document.querySelector(".top-login-btn");
  const signupBtn  = document.querySelector(".top-signup-btn");
  const mypageBtn  = document.querySelector(".top-mypage-btn");
  const logoutBtn  = document.querySelector(".top-logout-btn"); // 있으면 사용

  if (isAuth) {
    if (loginBtn)  loginBtn.style.display  = "none";
    if (signupBtn) signupBtn.style.display = "none";
    if (mypageBtn) mypageBtn.style.display = "inline-block";
    if (logoutBtn) {
      logoutBtn.style.display = "inline-block";
      logoutBtn.onclick = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("username");
        location.href = "login.html";
      };
    }
  } else {
    if (loginBtn)  loginBtn.style.display  = "inline-block";
    if (signupBtn) signupBtn.style.display = "inline-block";
    if (mypageBtn) mypageBtn.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "none";
  }
}
