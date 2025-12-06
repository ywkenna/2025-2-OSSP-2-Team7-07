const idInput = document.getElementById("signup-id");
const emailInput = document.getElementById("signup-email");
const pwInput = document.getElementById("signup-pw");
const pwCheckInput = document.getElementById("signup-pw-confirm");

const signupBtn = document.querySelector(".signup-btn");

signupBtn.addEventListener("click", () => {
    const username = idInput.value.trim();
    const email = emailInput.value.trim();
    const password = pwInput.value.trim();
    const password2 = pwCheckInput.value.trim();

    if (!username || !email || !password || !password2) {
        alert("모든 정보를 입력하세요.");
        return;
    }

    if (password !== password2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    fetch(`${API_BASE}/api/users/register/`, {   // ★ 수정됨
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error || data.detail) {
                alert(JSON.stringify(data));
                return;
            }

            alert("회원가입 성공!");
            window.location.href = "login.html";
        })
        .catch(err => {
            console.error(err);
            alert("회원가입 중 오류 발생");
        });
});
