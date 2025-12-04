const API_BASE = "http://127.0.0.1:8000";

document.querySelector(".signup-btn").addEventListener("click", () => {
    const username = document.getElementById("signup-id").value.trim();
    const pw = document.getElementById("signup-pw").value.trim();
    const pw2 = document.getElementById("signup-pw-confirm").value.trim();
    const englishLevelStr = document.getElementById("english-level").value;

    if (!username || !pw || !pw2) {
        alert("모든 정보를 입력해주세요");
        return;
    }
    if (pw !== pw2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    // CEFR 문자열 → 숫자 매핑
    const levelMap = {
        "A1": 0,
        "A2": 1,
        "B1": 2,
        "B2": 3,
        "C1": 4,
        "C2": 5
    };
    const englishLevel = levelMap[englishLevelStr];

    fetch(`${API_BASE}/api/users/register/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username,
            password: pw,
            first_name: username,
            english_level: englishLevel
        }),
    })
    .then((res) => {
        if (res.ok) {
            alert("회원가입 성공! 로그인하세요.");
            window.location.href = "login.html";
        } else {
            res.json().then(err => console.log("서버 에러:", err));
            alert("회원가입 실패: 입력값을 확인해주세요.");
        }
    })
    .catch(() => alert("서버 오류가 발생했습니다."));
});
