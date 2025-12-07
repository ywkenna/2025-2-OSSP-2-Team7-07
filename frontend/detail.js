

console.log("detail.js loaded");

let currentMovie = null;
let isLiked = false;

// ----------------------------
// URL에서 ?id= 값 가져오기
// ----------------------------
function getMovieIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// ----------------------------
// 상세 페이지 렌더링
// ----------------------------
function renderMovieDetail(movie) {
  const posterEl = document.querySelector(".poster-img");
  const titleKoEl = document.querySelector(".box1-name");
  const difficultyEl = document.querySelector(".box1-difficulty");
  const eNameEl = document.querySelector(".box1-e-name");
  const tagBoxEl = document.querySelector(".box1-tag");
  const plotEl = document.querySelector(".box1-plot");

  // 포스터
  if (posterEl) {
    posterEl.src = movie.image;
    posterEl.alt = movie.title_ko;
  }

  // 한글 제목
  if (titleKoEl) {
    titleKoEl.textContent = movie.title_ko;
  }

  // 난이도 (숫자면 그대로, 나중에 CEFR로 바꾸고 싶으면 매핑)
  if (difficultyEl) {
    difficultyEl.textContent = `난이도: ${movie.difficulty}`;
  }

  // 영어 제목 + 연도 + 러닝타임
  if (eNameEl) {
    eNameEl.textContent = `${movie.title_en} · ${movie.year} · ${movie.runtime}m`;
  }

  // 장르 태그
  if (tagBoxEl) {
    const genres = movie.genre.split(",").map((g) => g.trim());
    tagBoxEl.innerHTML = "";
    genres.forEach((g, idx) => {
      const div = document.createElement("div");
      div.className = `tag${idx + 1}`;
      div.textContent = g;
      tagBoxEl.appendChild(div);
    });
  }

  // 줄거리
  if (plotEl) {
    plotEl.textContent = movie.plot;
  }

  // 탭 제목
  document.title = movie.title_ko;

  // 리뷰 목록 렌더링
  renderComments(movie.comments || []);

  // OTT 링크 간단히 표현 (텍스트 버튼 스타일)
  renderOttLinks(movie.ott);
}

// ----------------------------
// OTT 링크 렌더링 (텍스트 버튼형)
// ----------------------------
function renderOttLinks(ott) {
  const box = document.querySelector(".box1-link");
  if (!box || !ott) return;

  box.innerHTML = ""; // 기존 이미지 다 지우고

  const services = [
    { key: "wavve_url",   label: "웨이브" },
    { key: "watcha_url",  label: "왓챠" },
    { key: "netflix_url", label: "넷플릭스" },
    { key: "tiving_url",  label: "티빙" },
    { key: "coupang_url", label: "쿠팡플레이" },
    { key: "disney_url",  label: "디즈니+" },
  ];

  let hasAny = false;

  services.forEach(({ key, label }) => {
    const url = ott[key];
    if (!url) return;

    hasAny = true;
    const a = document.createElement("a");
    a.href = url;
    a.target = "_blank";
    a.className = "ott-pill"; // CSS에서 버튼 모양으로 스타일링하면 예쁨
    a.textContent = label;
    box.appendChild(a);
  });

  if (!hasAny) {
    box.textContent = "시청 가능한 OTT가 없습니다.";
  }
}

// ----------------------------
// 리뷰 목록 렌더링
// ----------------------------
function renderComments(comments) {
  const wrapper = document.querySelector(".detail-review-list-container");
  if (!wrapper) return;

  // 제목(h3)은 유지하고, 카드만 갈아끼우기
  wrapper.innerHTML = `
    <h3 class="section-title">리뷰 목록</h3>
  `;

  if (!comments || comments.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "등록된 리뷰가 없습니다.";
    wrapper.appendChild(empty);
    return;
  }

  comments.forEach((c) => {
    const card = document.createElement("div");
    card.className = "detail-review-card";
    card.innerHTML = `
      <div class="detail-review-user">${c.user}</div>
      <div class="detail-review-right">
        <div class="detail-review-date">${c.created}</div>
        <div class="detail-review-content">
          ${c.content}
        </div>
      </div>
    `;
    wrapper.appendChild(card);
  });
}

// ----------------------------
// 찜 아이콘 UI 업데이트
// ----------------------------
function updateLikeIcon() {
  const btn = document.querySelector(".like-btn");
  if (!btn) return;

  btn.style.cursor = "pointer";
  if (isLiked) {
    btn.style.filter = "";         // 원래 색
    btn.style.opacity = "1";
  } else {
    btn.style.filter = "grayscale(80%)";
    btn.style.opacity = "0.4";
  }
}

// ----------------------------
// like 버튼 클릭 핸들러
// ----------------------------
function setupLikeButton() {
  const btn = document.querySelector(".like-btn");
  if (!btn) return;

  btn.style.cursor = "pointer";

  btn.addEventListener("click", async () => {
    const access = localStorage.getItem("access");
    if (!access) {
      alert("로그인 후 이용 가능합니다.");
      window.location.href = "login.html";
      return;
    }
    if (!currentMovie) return;

    const movieId = currentMovie.id;
    const method = isLiked ? "DELETE" : "POST";

    try {
      const res = await fetch(`${API_BASE}/api/users/like/${movieId}/`, {
        method,
        headers: {
          "Authorization": `Bearer ${access}`,
        },
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        console.error("찜 API 에러:", res.status, err);
        alert("찜 처리 중 오류가 발생했습니다.");
        return;
      }

      isLiked = !isLiked;
      updateLikeIcon();
    } catch (e) {
      console.error(e);
      alert("서버 오류로 찜 처리에 실패했습니다.");
    }
  });
}

// ----------------------------
// 리뷰 등록 버튼 핸들러
// ----------------------------
function setupReviewSubmit() {
  const btn = document.querySelector(".detail-review-submit-btn");
  const textarea = document.querySelector(".detail-review-textarea");
  if (!btn || !textarea) return;

  btn.addEventListener("click", async () => {
    const content = textarea.value.trim();
    if (!content) {
      alert("리뷰 내용을 입력해주세요.");
      return;
    }

    const access = localStorage.getItem("access");
    if (!access) {
      alert("로그인 후 이용 가능합니다.");
      window.location.href = "login.html";
      return;
    }

    const movieId = getMovieIdFromUrl();
    if (!movieId) {
      alert("영화 정보가 없습니다.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/movies/${movieId}/comment/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${access}`,
        },
        body: JSON.stringify({ content }),
      });

      const data = await res.json();

      if (!res.ok) {
        console.error("리뷰 등록 실패:", res.status, data);
        alert("리뷰 등록에 실패했습니다.");
        return;
      }

      alert("리뷰가 등록되었습니다.");
      textarea.value = "";

      // 새 댓글을 목록에 바로 추가
      const comments = currentMovie.comments || [];
      comments.push(data.comment);
      currentMovie.comments = comments;
      renderComments(comments);
    } catch (e) {
      console.error(e);
      alert("서버 오류로 리뷰 등록에 실패했습니다.");
    }
  });
}

// ----------------------------
// 상세 정보 불러오기
// ----------------------------
async function loadMovieDetail() {
  const id = getMovieIdFromUrl();
  if (!id) {
    alert("영화 ID가 없습니다. 홈에서 다시 들어오세요.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/movies/${id}/`);
    if (!res.ok) {
      throw new Error("상세 API 오류: " + res.status);
    }
    const movie = await res.json();
    currentMovie = movie;

    // 로그인 되어 있다면, 유저 정보 불러서 찜 여부 확인
    let likeIds = [];
    if (window.currentUser && Array.isArray(window.currentUser.like_movies)) {
      likeIds = window.currentUser.like_movies;
    }
    isLiked = likeIds.includes(movie.id);

    renderMovieDetail(movie);
    updateLikeIcon();
  } catch (err) {
    console.error("영화 상세 불러오기 실패:", err);
    alert("영화 상세 정보를 불러오는 중 오류가 발생했습니다.");
  }
}

// ----------------------------
// 초기화
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
  // auth.js의 checkAuth가 있다면 먼저 호출해서 window.currentUser 채워줌
  if (typeof checkAuth === "function") {
    checkAuth().then(() => {
      loadMovieDetail();
    });
  } else {
    loadMovieDetail();
  }

  setupLikeButton();
  setupReviewSubmit();
});
