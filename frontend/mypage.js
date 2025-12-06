

async function loadMyInfo() {
    const access = localStorage.getItem("access");
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
        headers: { "Authorization": `Bearer ${access}` }
    });

    const data = await res.json();

    document.getElementById("user-id").textContent = data.username;
    document.getElementById("user-email").textContent = data.email;
    document.getElementById("user-level").textContent =
        ["A1","A2","B1","B2","C1","C2"][data.english_level];

    loadLikedMovies(data.like_movies);
}

async function loadLikedMovies(likedIds) {
    const container = document.querySelector(".mypage-like-list");
    container.innerHTML = "";

    if (!likedIds || likedIds.length === 0) {
        container.innerHTML = "<p>찜한 영화가 없습니다.</p>";
        return;
    }

    // 영화 상세 정보를 불러오는 API 활용
    for (let id of likedIds) {
        const res = await fetch(`${API_BASE}/api/movies/${id}/`);
        const movie = await res.json();

        const div = document.createElement("div");
        div.className = "mypage-movie-card";

        div.innerHTML = `
            <img src="${movie.image}" class="mypage-movie-img">
            <div class="mypage-movie-name">${movie.title_ko}</div>
            <a href="detail.html?id=${movie.id}" class="mypage-detail-link">자세히 보기</a>
        `;

        container.appendChild(div);
    }
}

loadMyInfo();
