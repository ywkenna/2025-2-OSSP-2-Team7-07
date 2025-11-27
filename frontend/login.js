const API_BASE = "http://127.0.0.1:8000";

document.querySelector(".login-btn").addEventListener("click", () => {
    const username = document.getElementById("userid").value.trim();
    const password = document.getElementById("userpw").value.trim();

    if (!username || !password) {
        alert("아이디와 비밀번호를 입력하세요!");
        return;
    }

    fetch(`${API_BASE}/api/users/login/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password }),
    })
    .then((res) => res.json())
    .then((data) => {
        if (data.access) {
            // 토큰 저장
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            localStorage.setItem("username", data.user.username);

            alert("로그인 성공!");
            window.location.href = "home.html";
        } else {
            alert("로그인 실패: 아이디 또는 비밀번호 오류");
        }
    })
    .catch(() => alert("서버 오류가 발생했습니다."));
});
