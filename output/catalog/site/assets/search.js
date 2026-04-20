document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("searchInput");
    const table = document.getElementById("catalogTable");

    if (!input || !table) {
        console.warn("Search disabled: searchInput or catalogTable not found");
        return;
    }

    const rows = table.getElementsByTagName("tr");

    input.addEventListener("keyup", function () {
        const filter = input.value.toLowerCase();

        // Skip header row
        for (let i = 1; i < rows.length; i++) {
            const rowText = rows[i].textContent.toLowerCase();
            rows[i].style.display = rowText.includes(filter) ? "" : "none";
        }
    });
});
``