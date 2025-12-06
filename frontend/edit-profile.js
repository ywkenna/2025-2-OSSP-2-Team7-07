

async function loadUserInfo() {
    const access = localStorage.getItem("access");

    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
        headers: { "Authorization": `Bearer ${access}` }
    });

    const data = await res.json();

    document.getElementById("edit-name").value = data.first_name;
    document.getElementById("edit-email").value = data.email;
    document.getElementById("edit-level").value = data.english_level;
}

document.getElementById("edit-save").addEventListener("click", async () => {
    const access = localStorage.getItem("access");

    const payload = {
        first_name: document.getElementById("edit-name").value,
        email: document.getElementById("edit-email").value,
        english_level: Number(document.getElementById("edit-level").value)
    };

    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access}`
        },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("수정 완료되었습니다.");
        window.location.href = "mypage.html";
    } else {
        alert("수정 실패");
    }
});

loadUserInfo();
