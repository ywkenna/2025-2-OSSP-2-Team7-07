const form = document.getElementById("score-form");
const listBox = document.getElementById("recommend-list");

form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const type = formData.get("type");
    const score = formData.get("score");

    fetch(`${API_BASE}/api/movies/recommend/api/?type=${type}&score=${score}`)
        .then(res => res.json())
        .then(data => {
            listBox.innerHTML = "";
            if (!data.length) {
                listBox.innerHTML = "<p>추천 결과가 없습니다.</p>";
                return;
            }

            data.forEach(movie => {
                const div = document.createElement("div");
                div.textContent = `${movie.title_ko} (${movie.difficulty})`;
                listBox.appendChild(div);
            });
        })
        .catch(err => {
            console.error("추천 실패", err);
        });
});
