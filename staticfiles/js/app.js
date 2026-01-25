// Character counter for textareas with data-maxlength
function initCharCounters() {
  const textareas = document.querySelectorAll("textarea[data-maxlength]");
  textareas.forEach((textarea) => {
    const max = parseInt(textarea.dataset.maxlength, 10);
    const counter = textarea
      .closest("form")
      ?.querySelector("[data-char-count]");

    if (!counter) return;

    const update = () => {
      const remaining = max - textarea.value.length;
      counter.textContent = remaining;
      counter.style.color = remaining < 0 ? "#fca5a5" : "#9ca3af";
    };

    textarea.addEventListener("input", update);
    update();
  });
}

// Like button toggle
function initLikeButtons() {
  document.querySelectorAll("[data-like-button]").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("liked");
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initCharCounters();
  initLikeButtons();
});
