document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("col1_2Toggle");
  const comparison2 = document.getElementById("Comparison2");

  if (toggleBtn && comparison2) {
    toggleBtn.addEventListener("click", function () {
      comparison2.classList.toggle("d-none");
      toggleBtn.textContent = comparison2.classList.contains("d-none")
        ? "Show Second Athlete Page"
        : "Hide Second Athlete Page";
    });
  }
});


