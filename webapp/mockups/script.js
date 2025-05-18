document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("col1_2Toggle");
  const comparison2 = document.getElementById("Comparison2");

  if (toggleBtn && comparison2) {
    toggleBtn.addEventListener("click", function () {
      const isHidden = comparison2.classList.toggle("hidden");
      toggleBtn.textContent = isHidden
        ? "Show Second Athlete Page"
        : "Hide Second Athlete Page";
    });
  }
});