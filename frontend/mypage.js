// mypage.js
console.log("mypage.js loaded");

// 이 파일에서는 API_BASE 선언하지 않는다!!
// mypage.html 안에서 아래처럼 이미 선언되어 있다고 가정:
// <script> const API_BASE = "http://127.0.0.1:8000"; </script>

const CEFR_LABELS = ["A1", "A2", "B1", "B2", "C1", "C2"];

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initMyPage();
});

// ------------------------------
//  탭 전환
// ------------------------------
function initTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  const contentBoxes = document.querySelectorAll(".content-box");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const targetId = btn.dataset.target;
      contentBoxes.forEach((box) => {
        if (box.id === targetId) {
          box.classList.add("show");
        } else {
          box.classList.remove("show");
        }
      });
    });
  });
}

// ------------------------------
//  영어 점수 → CEFR 레벨 index(0~5)
// ------------------------------
function convertToCefr(type, score) {
  score = Number(score);

  if (type === "toeic") {
    if (score >= 945) return 5;
    if (score >= 785) return 4;
    if (score >= 550) return 3;
    if (score >= 225) return 2;
    return 1;
  }

  if (type === "toefl") {
    if (score >= 95) return 5;
    if (score >= 72) return 4;
    if (score >= 42) return 3;
    return 2;
  }

  if (type === "ielts") {
    if (score > 8.0) return 5;
    if (score >= 7.0) return 4;
    if (score >= 5.5) return 3;
    if (score >= 4.0) return 2;
    if (score >= 2.5) return 1;
    return 0;
  }

  return 0;
}

// ------------------------------
//  마이페이지 초기화
// ------------------------------
async function initMyPage() {
  const access = localStorage.getItem("access");

  const inputSection = document.getElementById("score-input-section");
  const resultSection = document.getElementById("score-result-section");
  const saveBtn = document.getElementById("save-score-btn");
  const editBtn = document.getElementById("edit-score-btn");

  // 버튼 이벤트 먼저 연결
  if (saveBtn) {
    saveBtn.addEventListener("click", saveScoreToServer);
  }
  if (editBtn) {
    editBtn.addEventListener("click", () => {
      if (inputSection && resultSection) {
        inputSection.style.display = "block";
        resultSection.style.display = "none";
      }
    });
  }

  // 로그인 안 한 경우: 영어 성적 입력폼만 보이고, 나머지는 비워둠
  if (!access) {
    if (inputSection && resultSection) {
      inputSection.style.display = "block";
      resultSection.style.display = "none";
    }
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${access}`,
      },
    });

    if (!res.ok) {
      console.warn("userinfo 불러오기 실패:", res.status);
      if (inputSection && resultSection) {
        inputSection.style.display = "block";
        resultSection.style.display = "none";
      }
      return;
    }

    const user = await res.json();
    console.log("userinfo:", user);

    // 상단 프로필
    updateProfileHeader(user);

    // 네비게이션(로그인/로그아웃 버튼)도 갱신
    if (typeof updateNavbar === "function") {
      updateNavbar();
    }

    // 영어 레벨 UI 적용
    updateEnglishScoreUI(user);

    // 찜한 영화
    await renderWishlist(user);

    // 내 리뷰
    await renderMyReviews(user);

  } catch (e) {
    console.error("마이페이지 초기화 중 오류:", e);
    if (inputSection && resultSection) {
      inputSection.style.display = "block";
      resultSection.style.display = "none";
    }
  }
}

// ------------------------------
//  영어 성적 저장 (PATCH /api/users/userinfo/)
// ------------------------------
async function saveScoreToServer() {
  const type = document.getElementById("test-type")?.value;
  const score = document.getElementById("test-score")?.value.trim();
  const access = localStorage.getItem("access");

  if (!access) {
    alert("로그인이 필요합니다.");
    return;
  }
  if (!type || !score) {
    alert("시험 종류와 점수를 모두 입력해 주세요.");
    return;
  }

  const level = convertToCefr(type, score);
  console.log("계산된 CEFR 레벨:", level);

  try {
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${access}`,
      },
      body: JSON.stringify({
        english_level: level,
        // 백엔드에서 허용한다면 시험 종류/점수도 같이 보내고,
        // 아니라면 english_level만 보내도 됩니다.
        // test_type: type,
        // test_score: score,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      console.error("성적 저장 실패:", res.status, err);
      alert("성적 저장 실패: 다시 시도해 주세요.");
      return;
    }

    const data = await res.json();
    console.log("성적 저장 후 응답:", data);

    // UI 업데이트
    const inputSection = document.getElementById("score-input-section");
    const resultSection = document.getElementById("score-result-section");

    document.getElementById("saved-test").textContent = type.toUpperCase();
    document.getElementById("saved-score").textContent = score;
    const savedLevel = Number(data.english_level);
    document.getElementById("saved-level").textContent =
      CEFR_LABELS[savedLevel] ?? "";

    if (inputSection && resultSection) {
      inputSection.style.display = "none";
      resultSection.style.display = "block";
    }

    alert("성적이 저장되었습니다.");
  } catch (e) {
    console.error("성적 저장 중 오류:", e);
    alert("서버 오류가 발생했습니다.");
  }
}

// ------------------------------
//  영어 레벨 불러왔을 때 UI 반영
// ------------------------------
function updateEnglishScoreUI(user) {
  const inputSection = document.getElementById("score-input-section");
  const resultSection = document.getElementById("score-result-section");

  const level = user.english_level;

  if (level === null || level === undefined) {
    // 아직 영어 레벨 없으면 입력폼만
    if (inputSection && resultSection) {
      inputSection.style.display = "block";
      resultSection.style.display = "none";
    }
    return;
  }

  const idx = Number(level);

  const savedLevelEl = document.getElementById("saved-level");
  const savedTestEl = document.getElementById("saved-test");
  const savedScoreEl = document.getElementById("saved-score");

  if (savedLevelEl) savedLevelEl.textContent = CEFR_LABELS[idx] ?? "";
  // test_type / test_score를 백엔드에 안 저장한다면 일단 빈 값으로 둠
  if (savedTestEl) savedTestEl.textContent = "";
  if (savedScoreEl) savedScoreEl.textContent = "";

  if (inputSection && resultSection) {
    inputSection.style.display = "none";
    resultSection.style.display = "block";
  }
}

// ------------------------------
//  프로필 영역 업데이트
// ------------------------------
function updateProfileHeader(user) {
  const userIdEl = document.querySelector(".userid");
  if (userIdEl) {
    userIdEl.textContent = `${user.username} 님`;
  }

  const profileBox = document.querySelector(".profile-info");
  if (profileBox) {
    const emailP = profileBox.querySelector("p:nth-of-type(1)");
    if (emailP) {
      emailP.textContent = `Email: ${user.email || "-"}`;
    }
  }

  const profileImg = document.getElementById("profile-img");
  if (profileImg) {
    if (user.profile_image) {
      profileImg.src = user.profile_image;
    }
    // 없으면 기본 icon.png 그대로 사용
  }
}

// ------------------------------
//  찜한 영화 렌더링 (user.like_movies 사용)
// ------------------------------
async function renderWishlist(user) {
  const container = document.querySelector(".wishlist-container");
  if (!container) return;

  const likedIds = user.like_movies || [];
  console.log("like_movies:", likedIds);

  if (likedIds.length === 0) {
    container.innerHTML = "<p>찜한 영화가 없습니다.</p>";
    return;
  }

  const res = await fetch(`${API_BASE}/api/movies/list/`);
  if (!res.ok) {
    container.innerHTML = "<p>영화를 불러오는 데 실패했습니다.</p>";
    return;
  }
  const movies = await res.json();

  const likedMovies = movies.filter((m) => likedIds.includes(m.id));

  if (likedMovies.length === 0) {
    container.innerHTML = "<p>찜한 영화가 없습니다.</p>";
    return;
  }

  container.innerHTML = "";
  likedMovies.forEach((movie) => {
    const a = document.createElement("a");
    a.href = `detail.html?id=${movie.id}`;
    a.className = "wishlist-card-link";

    const card = document.createElement("div");
    card.className = "wishlist-card";

    card.innerHTML = `
      <img src="${movie.image}" alt="${movie.title_ko}" class="card-img">
      <div class="card-name">${movie.title_ko}</div>
      <div class="card-ename">
        ${movie.title_en} · ${movie.year} · ${movie.runtime}m
      </div>
      <div class="card-tag">${movie.genre}</div>
    `;

    a.appendChild(card);
    container.appendChild(a);
  });
}

// ------------------------------
//  내 리뷰 렌더링
// ------------------------------
async function renderMyReviews(user) {
  const container = document.querySelector(".review-container");
  if (!container) return;

  container.innerHTML = "<p>내 리뷰를 불러오는 중...</p>";

  const res = await fetch(`${API_BASE}/api/movies/list/`);
  if (!res.ok) {
    container.innerHTML = "<p>영화를 불러오는 데 실패했습니다.</p>";
    return;
  }
  const movies = await res.json();

  const detailPromises = movies.map((m) =>
    fetch(`${API_BASE}/api/movies/${m.id}/`).then((r) => r.json())
  );

  const details = await Promise.all(detailPromises);

  const myReviews = [];
  details.forEach((movieDetail) => {
    (movieDetail.comments || []).forEach((c) => {
      if (c.user === user.username) {
        myReviews.push({
          movie: movieDetail,
          comment: c,
        });
      }
    });
  });

  if (myReviews.length === 0) {
    container.innerHTML = "<p>작성한 리뷰가 없습니다.</p>";
    return;
  }

  container.innerHTML = "";
  myReviews.forEach(({ movie, comment }) => {
    const a = document.createElement("a");
    a.href = `detail.html?id=${movie.id}`;
    a.className = "review-card-link";

    const card = document.createElement("div");
    card.className = "review-card";

    card.innerHTML = `
      <img src="${movie.image}" alt="${movie.title_ko}" class="review-poster">
      <div class="review-content">
        <div class="review-header">
          <span class="review-title">${movie.title_ko}</span>
        </div>
        <span class="review-date">${comment.created}</span>
        <p class="review-text">
          ${comment.content}
        </p>
      </div>
    `;

    a.appendChild(card);
    container.appendChild(a);
  });
}
