console.log("home.js loaded!");

const cardContainer    = document.querySelector(".card-container");
const searchInput      = document.getElementById("search-query");
const genreSelect      = document.getElementById("genre-select");
const difficultySelect = document.getElementById("difficulty-select");
const yearSelect       = document.getElementById("year-select");   // ★ 추가
const sortSelect       = document.getElementById("sort-select");   // ★ 추가
const filterBtn        = document.querySelector(".filter-btn");

// ---------------------------------------------------------------------
// 1) 찜한 영화 불러오기
// ---------------------------------------------------------------------
async function getLikedMovieIds() {
  const access = localStorage.getItem("access");
  if (!access) return [];  // 로그인 안 되어 있으면 그냥 빈 배열

  try {
    const res = await fetch(`${API_BASE}/api/users/userinfo/`, {
      headers: { "Authorization": `Bearer ${access}` }
    });

    if (res.status === 401) return [];  // 권한없음 → 찜 목록 없음 처리
    if (!res.ok) return [];

    const data = await res.json();
    return data.like_movies || [];

  } catch (e) {
    console.error("getLikedMovieIds error", e);
    return [];
  }
}


// ---------------------------------------------------------------------
// 2) 영화 카드 렌더링
// ---------------------------------------------------------------------
async function renderMovies(movies) {
  cardContainer.innerHTML = "";

  // 찜한 영화 리스트 가져옴
  const likedIds = await getLikedMovieIds();

  movies.forEach(movie => {
    const filename = movie.image.split("/").pop();
    const imgUrl   = `${API_BASE}/static/movies/images/${filename}`;

    const a = document.createElement("a");
    a.className = "card";
    a.href = `detail.html?id=${movie.id}`;

    a.innerHTML = `
      <img src="${imgUrl}" alt="${movie.title_ko}" class="card-img">
      <div class="card-like">${"♡"}</div>
      <div class="card-level-text">난이도: ${movie.difficulty ?? "-"}</div>
      <div class="card-name">${movie.title_ko}</div>
      <div class="card-ename">${movie.title_en} · ${movie.year} · ${movie.runtime}m</div>
      <div class="card-tag">${movie.genre}</div>
    `;

    cardContainer.appendChild(a);
  });
}

// ---------------------------------------------------------------------
// 3) 영화 API 요청
// ---------------------------------------------------------------------
function fetchMovies(params = {}) {
  let url;

  // 하나라도 필터가 걸려 있으면 /search/ 사용
  if (params.query || params.genre || params.difficulty || params.year || params.sort) {
    url = new URL(`${API_BASE}/api/movies/search/`);
  } else {
    url = new URL(`${API_BASE}/api/movies/list/`);
  }

  if (params.query) url.searchParams.set("query", params.query);
  if (params.genre && params.genre !== "전체") url.searchParams.set("genre", params.genre);

  // 난이도 (0~5, ""는 전체)
  if (params.difficulty && params.difficulty !== "전체") {
    url.searchParams.set("difficulty", params.difficulty);
  }

  // 개봉 연도 범위 (백엔드에서 year_range 처리하는 부분이 이미 있음)
  if (params.year && params.year !== "전체") {
    url.searchParams.set("year", params.year);
  }

  // 정렬 옵션
  if (params.sort) {
    url.searchParams.set("sort", params.sort);
  }

  console.log("fetchMovies URL:", url.toString());

  fetch(url.toString())
    .then(res => res.json())
    .then(data => renderMovies(data))
    .catch(err => {
      console.error("영화 불러오기 실패:", err);
      cardContainer.innerHTML = "<p>영화 불러오기 실패</p>";
    });
}

// ---------------------------------------------------------------------
// 4) 기본 영화 리스트 로딩
// ---------------------------------------------------------------------
fetchMovies();

// ---------------------------------------------------------------------
// 5) 검색 버튼 클릭
// ---------------------------------------------------------------------
if (filterBtn) {
  filterBtn.addEventListener("click", () => {
    const query      = searchInput?.value.trim();
    const genre      = genreSelect?.value;
    const difficulty = difficultySelect?.value;
    const year       = yearSelect?.value;
    const sortValue  = sortSelect?.value;

    // 프론트 select 값 → 백엔드 sort 파라미터로 매핑
    let sortParam = "";
    if (sortValue === "desc")      sortParam = "difficulty_desc"; // 어려운순
    else if (sortValue === "asc")  sortParam = "difficulty_asc";  // 쉬운순
    else if (sortValue === "new")  sortParam = "year_desc";       // 최신순
    else if (sortValue === "old")  sortParam = "year_asc";        // 오래된순

    fetchMovies({ query, genre, difficulty, year, sort: sortParam });
  });
}

// ---------------------------------------------------------------------
// 6) Enter 키로 검색
// ---------------------------------------------------------------------
if (searchInput) {
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      filterBtn.click();
    }
  });
}
