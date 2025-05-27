document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("col1_2Toggle");
  const comparison2 = document.getElementById("Comparison2");

  if (toggleBtn && comparison2) {
    toggleBtn.addEventListener("click", function () {
      const isShown = comparison2.classList.toggle("shown");
      
      toggleBtn.textContent = isShown
        ? "Hide Second Athlete Page"
        : "Show Second Athlete Page";
    });
  }
});


