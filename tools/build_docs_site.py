#!/usr/bin/env python3
"""
QCT Documentation Site Builder

Generates a static HTML documentation site with:
- Searchable parameter database
- Equation index
- Analysis document catalog
- Simulation results gallery

Author: AI Assistant
Date: 2025-11-16
"""

import json
from pathlib import Path
from typing import List, Dict
import shutil


class QCTDocsBuilder:
    """Build static documentation site for QCT"""

    def __init__(self, root_dir: Path, output_dir: Path):
        self.root_dir = Path(root_dir)
        self.output_dir = Path(output_dir)
        self.data_dir = self.root_dir / 'data'

    def build(self):
        """Build complete documentation site"""
        print("Building QCT documentation site...")

        # Create output structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'css').mkdir(exist_ok=True)
        (self.output_dir / 'js').mkdir(exist_ok=True)
        (self.output_dir / 'data').mkdir(exist_ok=True)

        # Generate pages
        self.build_index()
        self.build_parameters_page()
        self.build_equations_page()
        self.build_analyses_page()
        self.build_simulations_page()

        # Copy static files
        self.build_css()
        self.build_js()

        # Copy data files
        self.copy_data_files()

        print(f"✓ Documentation site built at: {self.output_dir}")

    def build_index(self):
        """Build main index page"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCT Research Documentation</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <h1>Quantum Compression Theory</h1>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="parameters.html">Parameters</a></li>
            <li><a href="equations.html">Equations</a></li>
            <li><a href="analyses.html">Analyses</a></li>
            <li><a href="simulations.html">Simulations</a></li>
        </ul>
    </nav>

    <main class="container">
        <section class="hero">
            <h2>Quantum Compression Theory Research</h2>
            <p class="subtitle">Microscopic quantum condensate framework for fundamental physics</p>
        </section>

        <section class="overview">
            <h3>Project Overview</h3>
            <p>
                <strong>Quantum Compression Theory (QCT)</strong> is a theoretical physics framework
                proposing a microscopic quantum condensate to explain fundamental physics phenomena
                from neutrino condensate dynamics.
            </p>

            <div class="stats-grid">
                <div class="stat-card">
                    <h4>Parameters</h4>
                    <p class="stat-number" id="param-count">Loading...</p>
                    <p>Physical parameters tracked</p>
                </div>
                <div class="stat-card">
                    <h4>Equations</h4>
                    <p class="stat-number" id="eq-count">Loading...</p>
                    <p>Mathematical equations indexed</p>
                </div>
                <div class="stat-card">
                    <h4>Analyses</h4>
                    <p class="stat-number" id="analysis-count">Loading...</p>
                    <p>Research analyses documented</p>
                </div>
                <div class="stat-card">
                    <h4>Simulations</h4>
                    <p class="stat-number" id="sim-count">Loading...</p>
                    <p>Numerical simulations</p>
                </div>
            </div>
        </section>

        <section class="quick-links">
            <h3>Quick Navigation</h3>
            <div class="links-grid">
                <a href="parameters.html" class="link-card">
                    <h4>📊 Parameter Database</h4>
                    <p>Browse all QCT physical parameters with values, locations, and consistency checks</p>
                </a>
                <a href="equations.html" class="link-card">
                    <h4>🔢 Equation Index</h4>
                    <p>Searchable index of all equations with cross-reference validation</p>
                </a>
                <a href="analyses.html" class="link-card">
                    <h4>📝 Research Analyses</h4>
                    <p>Comprehensive collection of theoretical analyses and reviews</p>
                </a>
                <a href="simulations.html" class="link-card">
                    <h4>🖥️ Simulations</h4>
                    <p>Numerical simulations and computational results</p>
                </a>
            </div>
        </section>

        <section class="status">
            <h3>Current Status</h3>
            <div class="status-box warning">
                <h4>⚠️ Pre-submission Phase (Revision 5.6)</h4>
                <p>Major revisions required before submission. See <a href="analyses.html#critical">Critical Issues</a>.</p>
            </div>
        </section>
    </main>

    <footer>
        <p>Quantum Compression Theory © 2025 Boleslav Plhák | Generated: 2025-11-16</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""

        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_parameters_page(self):
        """Build interactive parameters page"""
        # Load parameter data
        params_file = self.data_dir / 'parameters.json'
        params_data = {}

        if params_file.exists():
            with open(params_file, 'r', encoding='utf-8') as f:
                params_data = json.load(f)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCT Parameters | QCT Documentation</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <h1>Quantum Compression Theory</h1>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="parameters.html" class="active">Parameters</a></li>
            <li><a href="equations.html">Equations</a></li>
            <li><a href="analyses.html">Analyses</a></li>
            <li><a href="simulations.html">Simulations</a></li>
        </ul>
    </nav>

    <main class="container">
        <h2>QCT Parameter Database</h2>

        <div class="search-box">
            <input type="text" id="param-search" placeholder="Search parameters by name, value, or location...">
        </div>

        <div class="filter-controls">
            <label>Filter by category:</label>
            <select id="category-filter">
                <option value="all">All</option>
                <option value="fundamental">Fundamental</option>
                <option value="fitted">Fitted</option>
                <option value="calibrated">Calibrated</option>
                <option value="derived">Derived</option>
                <option value="measured">Measured</option>
                <option value="predicted">Predicted</option>
            </select>
        </div>

        <div id="parameters-container">
            <p>Loading parameters...</p>
        </div>
    </main>

    <footer>
        <p>Quantum Compression Theory © 2025 Boleslav Plhák</p>
    </footer>

    <script>
        const parametersData = {json.dumps(params_data, ensure_ascii=False)};
    </script>
    <script src="js/parameters.js"></script>
</body>
</html>
"""

        with open(self.output_dir / 'parameters.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_equations_page(self):
        """Build equations index page"""
        eqs_file = self.data_dir / 'equations.json'
        eqs_data = {}

        if eqs_file.exists():
            with open(eqs_file, 'r', encoding='utf-8') as f:
                eqs_data = json.load(f)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCT Equations | QCT Documentation</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <nav class="navbar">
        <h1>Quantum Compression Theory</h1>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="parameters.html">Parameters</a></li>
            <li><a href="equations.html" class="active">Equations</a></li>
            <li><a href="analyses.html">Analyses</a></li>
            <li><a href="simulations.html">Simulations</a></li>
        </ul>
    </nav>

    <main class="container">
        <h2>QCT Equation Index</h2>

        <div class="search-box">
            <input type="text" id="eq-search" placeholder="Search equations by label, content, or location...">
        </div>

        <div class="filter-controls">
            <label><input type="checkbox" id="labeled-only"> Labeled equations only</label>
            <label><input type="checkbox" id="numbered-only"> Numbered equations only</label>
        </div>

        <div id="equations-container">
            <p>Loading equations...</p>
        </div>
    </main>

    <footer>
        <p>Quantum Compression Theory © 2025 Boleslav Plhák</p>
    </footer>

    <script>
        const equationsData = {json.dumps(eqs_data, ensure_ascii=False)};
    </script>
    <script src="js/equations.js"></script>
</body>
</html>
"""

        with open(self.output_dir / 'equations.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_analyses_page(self):
        """Build analyses catalog page"""
        # Find all markdown analysis files
        analyses = []
        for md_file in self.root_dir.glob('*.md'):
            if md_file.name not in ['README.md', 'CLAUDE.md', 'TREE.md']:
                analyses.append({
                    'name': md_file.name,
                    'path': str(md_file.relative_to(self.root_dir)),
                    'size': md_file.stat().st_size
                })

        analyses.sort(key=lambda x: x['name'])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCT Analyses | QCT Documentation</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <h1>Quantum Compression Theory</h1>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="parameters.html">Parameters</a></li>
            <li><a href="equations.html">Equations</a></li>
            <li><a href="analyses.html" class="active">Analyses</a></li>
            <li><a href="simulations.html">Simulations</a></li>
        </ul>
    </nav>

    <main class="container">
        <h2>Research Analyses</h2>

        <div class="search-box">
            <input type="text" id="analysis-search" placeholder="Search analyses...">
        </div>

        <section id="critical" class="critical-section">
            <h3>⚠️ Critical Issues</h3>
            <ul>
                <li><a href="https://github.com/Ibgboolys/QCT_9/blob/main/PEER_REVIEW_CRITICAL_ANALYSIS.md">Peer Review Critical Analysis</a> - Comprehensive review of major issues</li>
            </ul>
        </section>

        <section>
            <h3>All Analyses ({len(analyses)} documents)</h3>
            <div class="analyses-grid">
"""

        for analysis in analyses:
            html += f"""                <div class="analysis-card">
                    <h4>{analysis['name'].replace('_', ' ').replace('.md', '')}</h4>
                    <p class="file-info">{analysis['size'] // 1024} KB</p>
                    <a href="https://github.com/Ibgboolys/QCT_9/blob/main/{analysis['path']}" class="btn">View Analysis</a>
                </div>
"""

        html += """            </div>
        </section>
    </main>

    <footer>
        <p>Quantum Compression Theory © 2025 Boleslav Plhák</p>
    </footer>

    <script src="js/analyses.js"></script>
</body>
</html>
"""

        with open(self.output_dir / 'analyses.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_simulations_page(self):
        """Build simulations gallery page"""
        sim_dir = self.root_dir / 'QCT_7-QCT' / 'simulations'
        simulations = []

        if sim_dir.exists():
            for py_file in sim_dir.glob('*.py'):
                simulations.append({
                    'name': py_file.name,
                    'path': str(py_file.relative_to(self.root_dir))
                })

        simulations.sort(key=lambda x: x['name'])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QCT Simulations | QCT Documentation</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <h1>Quantum Compression Theory</h1>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="parameters.html">Parameters</a></li>
            <li><a href="equations.html">Equations</a></li>
            <li><a href="analyses.html">Analyses</a></li>
            <li><a href="simulations.html" class="active">Simulations</a></li>
        </ul>
    </nav>

    <main class="container">
        <h2>Numerical Simulations</h2>

        <div class="search-box">
            <input type="text" id="sim-search" placeholder="Search simulations...">
        </div>

        <section>
            <h3>All Simulations ({len(simulations)} scripts)</h3>
            <div class="simulations-grid">
"""

        for sim in simulations:
            html += f"""                <div class="sim-card">
                    <h4>{sim['name'].replace('_', ' ').replace('.py', '')}</h4>
                    <a href="https://github.com/Ibgboolys/QCT_9/blob/main/{sim['path']}" class="btn">View Code</a>
                </div>
"""

        html += """            </div>
        </section>
    </main>

    <footer>
        <p>Quantum Compression Theory © 2025 Boleslav Plhák</p>
    </footer>

    <script src="js/simulations.js"></script>
</body>
</html>
"""

        with open(self.output_dir / 'simulations.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_css(self):
        """Generate CSS styles"""
        css = """/* QCT Documentation Site Styles */

:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;
    --success-color: #27ae60;
    --warning-color: #f39c12;
    --bg-color: #ecf0f1;
    --card-bg: #ffffff;
    --text-color: #2c3e50;
    --border-radius: 8px;
    --shadow: 0 2px 8px rgba(0,0,0,0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background: var(--bg-color);
}

.navbar {
    background: var(--primary-color);
    color: white;
    padding: 1rem 2rem;
    box-shadow: var(--shadow);
}

.navbar h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.navbar ul {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.navbar a {
    color: white;
    text-decoration: none;
    transition: opacity 0.3s;
}

.navbar a:hover, .navbar a.active {
    opacity: 0.8;
    text-decoration: underline;
}

.container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
}

.hero {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
    color: white;
    border-radius: var(--border-radius);
    margin-bottom: 2rem;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.stat-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    text-align: center;
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: var(--secondary-color);
    margin: 0.5rem 0;
}

.links-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.link-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    text-decoration: none;
    color: var(--text-color);
    transition: transform 0.3s, box-shadow 0.3s;
}

.link-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.link-card h4 {
    margin-bottom: 0.5rem;
    color: var(--secondary-color);
}

.search-box {
    margin: 2rem 0;
}

.search-box input {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border: 2px solid #ddd;
    border-radius: var(--border-radius);
    transition: border-color 0.3s;
}

.search-box input:focus {
    outline: none;
    border-color: var(--secondary-color);
}

.filter-controls {
    margin: 1rem 0;
    padding: 1rem;
    background: var(--card-bg);
    border-radius: var(--border-radius);
}

.status-box {
    padding: 1.5rem;
    border-radius: var(--border-radius);
    margin: 1rem 0;
}

.status-box.warning {
    background: #fff3cd;
    border-left: 4px solid var(--warning-color);
}

.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: var(--secondary-color);
    color: white;
    text-decoration: none;
    border-radius: var(--border-radius);
    transition: background 0.3s;
}

.btn:hover {
    background: var(--primary-color);
}

footer {
    text-align: center;
    padding: 2rem;
    background: var(--primary-color);
    color: white;
    margin-top: 4rem;
}

@media (max-width: 768px) {
    .navbar ul {
        flex-direction: column;
        gap: 0.5rem;
    }

    .hero h2 {
        font-size: 1.8rem;
    }
}
"""

        with open(self.output_dir / 'css' / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css)

    def build_js(self):
        """Generate JavaScript files"""
        # Main JS
        main_js = """// QCT Documentation Site - Main JavaScript

// Load statistics
fetch('data/parameters.json')
    .then(res => res.json())
    .then(data => {
        const count = document.getElementById('param-count');
        if (count) count.textContent = data.metadata.total_parameters || 0;
    })
    .catch(err => console.error('Error loading parameters:', err));

fetch('data/equations.json')
    .then(res => res.json())
    .then(data => {
        const count = document.getElementById('eq-count');
        if (count) count.textContent = data.metadata.total_equations || 0;
    })
    .catch(err => console.error('Error loading equations:', err));

// Count analyses and simulations from DOM
window.addEventListener('DOMContentLoaded', () => {
    const analysisCards = document.querySelectorAll('.analysis-card');
    const analysisCount = document.getElementById('analysis-count');
    if (analysisCount) analysisCount.textContent = analysisCards.length;

    const simCards = document.querySelectorAll('.sim-card');
    const simCount = document.getElementById('sim-count');
    if (simCount) simCount.textContent = simCards.length;
});
"""

        with open(self.output_dir / 'js' / 'main.js', 'w', encoding='utf-8') as f:
            f.write(main_js)

        # Parameters JS
        params_js = """// Parameters page JavaScript

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
"""

        with open(self.output_dir / 'js' / 'parameters.js', 'w', encoding='utf-8') as f:
            f.write(params_js)

        # Equations JS
        eqs_js = """// Equations page JavaScript

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
                html += `<pre class="equation-preview">\\\\[${preview}${eq.content.length > 200 ? '...' : ''}\\\\]</pre>`;

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
"""

        with open(self.output_dir / 'js' / 'equations.js', 'w', encoding='utf-8') as f:
            f.write(eqs_js)

        # Analyses JS
        analyses_js = """// Analyses page JavaScript
const searchInput = document.getElementById('analysis-search');

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.analysis-card');

        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(term) ? 'block' : 'none';
        });
    });
}
"""

        with open(self.output_dir / 'js' / 'analyses.js', 'w', encoding='utf-8') as f:
            f.write(analyses_js)

        # Simulations JS
        sims_js = """// Simulations page JavaScript
const searchInput = document.getElementById('sim-search');

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.sim-card');

        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(term) ? 'block' : 'none';
        });
    });
}
"""

        with open(self.output_dir / 'js' / 'simulations.js', 'w', encoding='utf-8') as f:
            f.write(sims_js)

    def copy_data_files(self):
        """Copy JSON data files to site"""
        data_files = ['parameters.json', 'equations.json']

        for filename in data_files:
            src = self.data_dir / filename
            dst = self.output_dir / 'data' / filename

            if src.exists():
                shutil.copy(src, dst)
                print(f"✓ Copied {filename}")


def main():
    root_dir = Path(__file__).parent.parent
    output_dir = root_dir / 'docs_site'

    builder = QCTDocsBuilder(root_dir, output_dir)
    builder.build()

    print("\n✓ Documentation site ready!")
    print(f"  Open: {output_dir / 'index.html'}")


if __name__ == '__main__':
    main()
