document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("data-body");
    const emptyMessage = document.getElementById("empty-message");

    async function loadData() {
        const response = await fetch("/api/data");
        const data = await response.json();

        tableBody.innerHTML = "";

        if (data.length === 0) {
            emptyMessage.classList.remove("d-none");
            return;
        }

        emptyMessage.classList.add("d-none");

        data.forEach(item => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.feature1}</td>
                <td>${item.feature2}</td>
                <td>${item.category}</td>
                <td>
                    <form action="/delete/${item.id}" method="POST">
                        <button class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            `;

            tableBody.appendChild(row);
        });
    }

    loadData();
});
