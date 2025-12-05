// Equations page JavaScript

function renderEquations() {
    const container = document.getElementById('equations-container');
    const searchInput = document.getElementById('eq-search');
    const labeledOnly = document.getElementById('labeled-only');
    const numberedOnly = document.getElementById('numbered-only');

    if (!equationsData.equations) {
        container.innerHTML = '<p>No equation data available.</p>';
        return;
    }

    function display() {
        const searchTerm = searchInput.value.toLowerCase();
        const onlyLabeled = labeledOnly && labeledOnly.checked;
        const onlyNumbered = numberedOnly && numberedOnly.checked;

        const filtered = equationsData.equations.filter(eq => {
            const matchesSearch = !searchTerm ||
                (eq.label && eq.label.toLowerCase().includes(searchTerm)) ||
                eq.location.toLowerCase().includes(searchTerm) ||
                eq.content.toLowerCase().includes(searchTerm);

            const matchesLabeled = !onlyLabeled || eq.label;
            const matchesNumbered = !onlyNumbered || eq.is_numbered;

            return matchesSearch && matchesLabeled && matchesNumbered;
        });

        let html = '';

        if (filtered.length === 0) {
            html = '<p>No equations found matching your criteria.</p>';
        } else {
            filtered.forEach(eq => {
                html += `<div class="equation-card">`;

                if (eq.label) {
                    html += `<h4><code>${eq.label}</code></h4>`;
                } else {
                    html += `<h4>Unlabeled</h4>`;
                }

                html += `<p><strong>Location:</strong> <code>${eq.location}</code></p>`;

                if (eq.section) {
                    html += `<p><strong>Section:</strong> ${eq.section}</p>`;
                }

                const preview = eq.content.substring(0, 200);
                html += `<pre class="equation-preview">\\[${preview}${eq.content.length > 200 ? '...' : ''}\\]</pre>`;

                if (eq.references && eq.references.length > 0) {
                    html += `<p><strong>References:</strong> ${eq.references.join(', ')}</p>`;
                }

                html += `</div>`;
            });
        }

        container.innerHTML = html;

        // Trigger MathJax rendering
        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    }

    searchInput.addEventListener('input', display);
    if (labeledOnly) labeledOnly.addEventListener('change', display);
    if (numberedOnly) numberedOnly.addEventListener('change', display);

    display();
}

window.addEventListener('DOMContentLoaded', renderEquations);
