// Filters catalog tables across all domain sections. Hides a domain section
// entirely when none of its rows match, and shows a "no results" message when
// nothing matches anywhere.
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  if (!input) return;

  const sections = Array.from(document.querySelectorAll(".domain"));
  const empty = document.getElementById("noResults");

  function apply() {
    const q = input.value.trim().toLowerCase();
    let anyVisible = false;

    sections.forEach((section) => {
      const rows = Array.from(section.querySelectorAll("tbody tr"));
      let visibleInSection = 0;

      rows.forEach((row) => {
        const match = row.textContent.toLowerCase().includes(q);
        row.style.display = match ? "" : "none";
        if (match) visibleInSection++;
      });

      section.style.display = visibleInSection ? "" : "none";
      if (visibleInSection) anyVisible = true;
    });

    if (empty) empty.style.display = anyVisible ? "none" : "";
  }

  input.addEventListener("input", apply);
});
