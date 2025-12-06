
// ----------------------------
// URL에서 영화 id 추출
// ----------------------------
function getMovieIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// ----------------------------
// 상세 렌더링
// ----------------------------
function renderMovieDetail(movie) {
  document.querySelector(".poster-img").src = movie.image;

  document.querySelector(".box1-name").textContent = movie.title_ko;
  document.querySelector(".box1-difficulty").textContent = `난이도: ${movie.difficulty}`;
  document.querySelector(".box1-e-name").textContent = `${movie.title_en} · ${movie.year} · ${movie.runtime}m`;
  document.querySelector(".box1-plot").textContent = movie.plot;

  // 장르 태그
  const tagBox = document.querySelector(".box1-tag");
  tagBox.innerHTML = "";
  movie.genre.split(",").forEach((g, i) => {
    const div = document.createElement("div");
    div.className = `tag${i+1}`;
    div.textContent = g.trim();
    tagBox.appendChild(div);
  });
  
  if (movie.status) {
    renderStatusBars(movie.status);
  }

  renderComments(movie.comments || []);
  updateLikeButton(movie.id);
}

// ----------------------------
// 난이도 상세 막대(status)
// ----------------------------
function renderStatusBars(status) {
  if (!status) return;

  setBar(0, status.word_avg_level / 5);          // 평균 난이도 (0~5)
  setBar(1, status.phrase_ratio);                // 숙어 비율 (0~1)
  setBar(2, status.clause_ratio);                // 절 비율 (0~1)
  setBar(3, status.avg_speed / 5);               // 문장 빠르기 (0~5로 가정)
  setBar(4, status.pron_acc);                    // 발음 정확도 (0~1)
  setBar(5, status.overlap_ratio);               // 중첩 발화 비율 (0~1)
}

function setBar(index, normalized) {
  const bars = document.querySelectorAll(".bar-fill");
  if (!bars[index]) return;

  const percent = Math.min(100, Math.max(0, normalized * 100));
  bars[index].style.width = `${percent}%`;
}


// ----------------------------
// 상세 정보 API 호출
// ----------------------------
function loadMovieDetail() {
  const id = getMovieIdFromUrl();
  if (!id) {
    alert("잘못된 접근입니다.");
    return;
  }

  fetch(`${API_BASE}/api/movies/${id}/`)
    .then(res => res.json())
    .then(movie => renderMovieDetail(movie))
    .catch(err => {
      console.error(err);
      alert("상세 정보를 불러오는 중 오류 발생");
    });
}

// ----------------------------
// 좋아요 버튼
// ----------------------------
function updateLikeButton(movieId) {
  const btn = document.querySelector(".like-btn");
  const access = localStorage.getItem("access");

  if (!access) {
    btn.textContent = "♡ 로그인 필요";
    return;
  }

  btn.textContent = "♡ 찜하기";
  btn.onclick = () => toggleLike(movieId, false);
}

function toggleLike(movieId, isLiked) {
  const access = localStorage.getItem("access");
  if (!access) {
    alert("로그인이 필요합니다.");
    return;
  }

  fetch(`${API_BASE}/api/users/like/${movieId}/`, {
    method: isLiked ? "DELETE" : "POST",
    headers: { "Authorization": `Bearer ${access}` }
  })
    .then(res => {
      if (res.ok) {
        alert(isLiked ? "찜 취소됨" : "찜 완료!");
        updateLikeButton(movieId);
      } else {
        alert("처리 중 오류 발생");
      }
    });
}

// ----------------------------
// 댓글 렌더링
// ----------------------------
function renderComments(comments) {
  const list = document.querySelector(".comment-list");
  list.innerHTML = "";

  if (comments.length === 0) {
    list.innerHTML = "<p>댓글이 없습니다.</p>";
    return;
  }

  comments.forEach(c => {
    const div = document.createElement("div");
    div.className = "comment-item";
    div.innerHTML = `
      <strong>${c.user}</strong>
      <p>${c.content}</p>
      <span>${c.created}</span>
    `;
    list.appendChild(div);
  });
}

// ----------------------------
// 댓글 작성
// ----------------------------
function registerComment() {
  const id = getMovieIdFromUrl();
  const access = localStorage.getItem("access");
  const text = document.querySelector(".comment-input").value.trim();

  if (!access) {
    alert("로그인이 필요합니다.");
    return;
  }
  if (!text) {
    alert("댓글을 입력하세요.");
    return;
  }

  const formData = new FormData();
  formData.append("content", text);

  fetch(`${API_BASE}/api/movies/${id}/comments/`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${access}` },
    body: formData,
  })
    .then(async (res) => {
      let data = null;
      try {
        data = await res.json();
      } catch (e) {
        // HTML 응답 등일 때 JSON 파싱 실패 → 무시
      }

      if (!res.ok) {
        alert(data?.error || `리뷰 등록 실패 (status: ${res.status})`);
        console.error("리뷰 등록 실패:", res.status, data);
        return;
      }

      alert("리뷰 등록 완료");
      location.reload();
    })
    .catch((err) => {
      console.error("리뷰 등록 fetch 에러:", err);
      alert("리뷰 등록 중 네트워크 오류가 발생했습니다.");
    });
}


// ----------------------------
// 페이지 로드
// ----------------------------
loadMovieDetail();
document.querySelector(".comment-btn")?.addEventListener("click", registerComment);

