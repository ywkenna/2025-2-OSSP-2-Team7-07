// ----------------------------
// 1) API 주소
// ----------------------------
const API_BASE = "http://127.0.0.1:8000";


// ----------------------------
// 2) URL에서 ?id= 값 가져오기
// ----------------------------
function getMovieIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}


// ----------------------------
// 3) 상세 페이지 화면에 렌더링
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
    const posterUrl = `${API_BASE}/${movie.image}`;
    posterEl.src = posterUrl;
    posterEl.alt = movie.title_ko;
  }

  // 한글 제목
  if (titleKoEl) {
    titleKoEl.textContent = movie.title_ko;
  }

  // 난이도
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
}


// ----------------------------
// 4) API에서 영화 상세 정보 불러오기
// ----------------------------
function loadMovieDetail() {
  const id = getMovieIdFromUrl();
  if (!id) {
    alert("영화 ID가 없습니다. 홈에서 다시 들어오세요.");
    return;
  }

  fetch(`${API_BASE}/api/movies/${id}/`)
    .then((res) => {
      if (!res.ok) {
        throw new Error("상세 API 오류: " + res.status);
      }
      return res.json();
    })
    .then((movie) => {
      renderMovieDetail(movie);
    })
    .catch((err) => {
      console.error("영화 상세 불러오기 실패:", err);
      alert("영화 상세 정보를 불러오는 중 오류가 발생했습니다.");
    });
}


// ----------------------------
// 5) 페이지 로드되면 실행
// ----------------------------
loadMovieDetail();
