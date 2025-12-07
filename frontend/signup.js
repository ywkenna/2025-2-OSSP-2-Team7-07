const API_BASE = "http://127.0.0.1:8000";

document.querySelector(".signup-btn").addEventListener("click", () => {
    const username = document.getElementById("signup-id").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const pw = document.getElementById("signup-pw").value.trim();
    const pw2 = document.getElementById("signup-pw-confirm").value.trim();

    if (!username || !email || !pw || !pw2) {
        alert("모든 정보를 입력해주세요");
        return;
    }
    if (pw !== pw2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    // 영어 레벨 완전 삭제 버전 → 백엔드에서도 optional 처리했으므로 안 보내도 됨.
    fetch(`${API_BASE}/api/users/register/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username,
            password: pw,
            email,
            first_name: username
        }),
    })
    .then((res) => {
        if (res.ok) {
            alert("회원가입 성공! 로그인하세요.");
            window.location.href = "login.html";
        } else {
            res.json().then(err => {
                console.log("서버 에러:", err);
                alert("회원가입 실패: " + JSON.stringify(err));
            });
        }
    })
    .catch(() => alert("서버 오류가 발생했습니다."));
});
