console.log("home.js loaded!");

const API_BASE = "http://127.0.0.1:8000";

const cardContainer = document.querySelector(".card-container");
const searchInput = document.getElementById("search-query");
const genreSelect = document.getElementById("genre-select");
const difficultySelect = document.getElementById("difficulty-select");
const filterBtn = document.querySelector(".filter-btn");


// ---------------------------
// 3) 영화 카드 렌더링
// ---------------------------
function renderMovies(movies) {
  cardContainer.innerHTML = "";

  if (!movies || movies.length === 0) {
    cardContainer.innerHTML = "<p>검색 결과가 없습니다.</p>";
    return;
  }

  movies.forEach(movie => {
    console.log("IMAGE RAW:", movie.image);

    const a = document.createElement("a");
    a.className = "card";
    a.href = `detail.html?id=${movie.id}`;

    const posterUrl = movie.image;   // ← 프론트는 그냥 이거면 끝

    a.innerHTML = `
      <img src="${posterUrl}" alt="${movie.title_ko}" class="card-img">
      <div class="card-level-text">난이도: ${movie.difficulty ?? "-"} </div>
      <div class="card-name">${movie.title_ko}</div>
      <div class="card-ename">
        ${movie.title_en} · ${movie.year} · ${movie.runtime}m
      </div>
      <div class="card-tag">${movie.genre}</div>
    `;

    cardContainer.appendChild(a);
  });

}


// ---------------------------
// 4) API 요청
// ---------------------------
function fetchMovies(params = {}) {
  let url;

  // 검색 조건이 하나라도 있으면 search API
  if (params.query || params.genre || params.difficulty) {
    url = new URL(`${API_BASE}/api/movies/search/`);
  } else {
    url = new URL(`${API_BASE}/api/movies/list/`);
  }

  // 검색어
  if (params.query) url.searchParams.set("query", params.query);

  // 장르 (전체는 제외)
  if (params.genre && params.genre !== "전체") {
    url.searchParams.set("genre", params.genre);
  }

  // 난이도 (전체는 제외)
  if (params.difficulty && params.difficulty !== "전체") {
    url.searchParams.set("difficulty", params.difficulty);
  }

  fetch(url.toString())
    .then(res => res.json())
    .then(data => renderMovies(data))
    .catch(err => {
      console.error("영화 목록 불러오기 실패:", err);
      cardContainer.innerHTML = "<p>영화 불러오기 실패</p>";
    });
}


// ---------------------------
// 5) 처음 로딩 시 전체 영화 불러오기
// ---------------------------
fetchMovies();


// ---------------------------
// 6) 검색 버튼 클릭
// ---------------------------
if (filterBtn) {
  filterBtn.addEventListener("click", () => {
    const query = searchInput?.value.trim();
    const genre = genreSelect?.value;
    const difficulty = difficultySelect?.value;

    fetchMovies({ query, genre, difficulty });
  });
}


// ---------------------------
// 7) 엔터키 검색
// ---------------------------
if (searchInput) {
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      filterBtn.click();
    }
  });
}
