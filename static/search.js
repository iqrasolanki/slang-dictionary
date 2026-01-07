const input = document.querySelector('input[name="word"]');
const box = document.createElement("div");
box.className = "live-suggestions";
input.parentNode.appendChild(box);

input.addEventListener("input", async () => {
  const q = input.value.trim();
  if (q.length < 2) {
    box.innerHTML = "";
    return;
  }

  const res = await fetch(`/suggestions?q=${q}`);
  const data = await res.json();

  box.innerHTML = "";
  data.results.forEach(word => {
    const div = document.createElement("div");
    div.textContent = word;
    div.onclick = () => {
      input.value = word;
      input.form.submit();
    };
    box.appendChild(div);
  });
});
