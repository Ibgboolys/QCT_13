// QCT Documentation Site - Main JavaScript

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
