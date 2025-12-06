// score.js

const form = document.getElementById("score-form");
const listBox = document.getElementById("recommend-list");

// 폼이나 박스 못 찾으면 그냥 아무 것도 안 함 (해당 페이지 아님)
if (!form || !listBox) {
  console.warn("score.js: score-form 또는 recommend-list를 찾지 못함");
} else {
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const type = formData.get("type");
    const score = formData.get("score");

    if (!type || !score) {
      alert("시험 종류와 점수를 모두 입력해 주세요!");
      return;
    }

    const numericScore = Number(score);
    if (Number.isNaN(numericScore) || numericScore <= 0) {
      alert("점수는 0보다 큰 숫자로 입력해 주세요.");
      return;
    }

    const url = `${API_BASE}/api/movies/recommend/api/?type=${type}&score=${numericScore}`;
    console.log("추천 API 요청:", url);

    listBox.innerHTML = "<p>추천 영화 불러오는 중...</p>";

    fetch(url)
      .then((res) => {
        if (!res.ok) {
          // 상태코드 로그 남기기
          console.error("추천 API 응답 에러:", res.status);
          throw new Error("추천 API 에러: " + res.status);
        }
        return res.json();
      })
      .then((data) => {
        console.log("추천 API 응답 데이터:", data);

        listBox.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
          listBox.innerHTML = "<p>추천 결과가 없습니다.</p>";
          return;
        }

        data.forEach((movie) => {
          const div = document.createElement("div");
          div.className = "recommend-item";
          div.textContent = `${movie.title_ko} (난이도: ${movie.difficulty})`;
          listBox.appendChild(div);
        });
      })
      .catch((err) => {
        console.error("추천 실패", err);
        listBox.innerHTML = "<p>추천 영화 불러오기 실패 ㅠㅠ</p>";
      });
  });
}
