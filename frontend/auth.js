const API_BASE = "http://127.0.0.1:8000";

// --------------------------
// 1) Access Token이 유효한지 검사
// --------------------------
async function checkAuth() {
    const access = localStorage.getItem("access");
    if (!access) return false;

    // 만료 여부 확인 불가능 → 즉시 API 호출로 검사
    try {
        const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
            headers: { "Authorization": `Bearer ${access}` }
        });

        if (res.ok) {
            return true;
        } else {

        }
    } catch {
        return false;
    }
}

// --------------------------
// 3) 로그아웃
// --------------------------
function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("username");
    window.location.href = "login.html";
}

// --------------------------
// 4) 로그인 UI 업데이트
// --------------------------
// --------------------------
// 4) 로그인 UI 업데이트 (이름 + 레벨 표시)
// --------------------------
async function updateNavbar() {
    const loginBtn = document.querySelector(".top-login-btn");
    const signupBtn = document.querySelector(".top-signup-btn");

    const access = localStorage.getItem("access");
    if (!access) return;

    try {
        const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
            headers: { "Authorization": `Bearer ${access}` }
        });
        const data = await res.json();

        if (data.username) {
            const username = data.username;
            const level = data.english_level;  // 0~5

            // CEFR 문자열 매핑
            const levelMap = ["A1", "A2", "B1", "B2", "C1", "C2"];
            const levelStr = level !== null ? levelMap[level] : "-";

            // UI 변경
            if (loginBtn) loginBtn.style.display = "none";

            if (signupBtn) {
                signupBtn.textContent = `${username} (${levelStr}) / 로그아웃`;
                signupBtn.addEventListener("click", logout);
            }
        }
    } catch (e) {
        console.log("Navbar update failed:", e);
    }
}

