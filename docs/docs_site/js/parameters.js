// Parameters page JavaScript

function renderParameters() {
    const container = document.getElementById('parameters-container');
    const searchInput = document.getElementById('param-search');
    const categoryFilter = document.getElementById('category-filter');

    if (!parametersData.parameters) {
        container.innerHTML = '<p>No parameter data available.</p>';
        return;
    }

    function display() {
        const searchTerm = searchInput.value.toLowerCase();
        const category = categoryFilter.value;

        let html = '';
        let count = 0;

        for (const [name, instances] of Object.entries(parametersData.parameters)) {
            const filtered = instances.filter(inst => {
                const matchesSearch = !searchTerm ||
                    name.toLowerCase().includes(searchTerm) ||
                    (inst.value && inst.value.toLowerCase().includes(searchTerm)) ||
                    inst.location.toLowerCase().includes(searchTerm);

                const matchesCategory = category === 'all' || inst.category === category;

                return matchesSearch && matchesCategory;
            });

            if (filtered.length > 0) {
                count++;
                html += `<div class="param-group">
                    <h3>${name}</h3>`;

                filtered.forEach(inst => {
                    html += `<div class="param-instance">
                        <p><strong>Location:</strong> <code>${inst.location}</code></p>`;

                    if (inst.value) {
                        html += `<p><strong>Value:</strong> ${inst.value}`;
                        if (inst.unit) html += ` ${inst.unit}`;
                        if (inst.uncertainty) html += ` ± ${inst.uncertainty}`;
                        html += `</p>`;
                    }

                    html += `<p><strong>Symbol:</strong> <code>${inst.symbol}</code></p>
                        <p><strong>Category:</strong> <span class="badge badge-${inst.category}">${inst.category}</span></p>
                    </div>`;
                });

                html += `</div>`;
            }
        }

        if (count === 0) {
            html = '<p>No parameters found matching your criteria.</p>';
        }

        container.innerHTML = html;
    }

    searchInput.addEventListener('input', display);
    categoryFilter.addEventListener('change', display);

    display();
}

window.addEventListener('DOMContentLoaded', renderParameters);
