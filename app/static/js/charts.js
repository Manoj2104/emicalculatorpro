/*
==========================================
Advanced Chart Engine
==========================================
Handles:
- Pie Chart (Principal vs Interest)
- Line Chart (Balance over time)
- Clean destroy before re-render
==========================================
*/

let globalChart = null;

/* ==============================
   Destroy Existing Chart
============================== */

function destroyChart() {
    if (globalChart) {
        globalChart.destroy();
        globalChart = null;
    }
}

/* ==============================
   Render Pie Chart
============================== */

function renderPieChart(canvasId, principal, interest) {

    destroyChart();

    const ctx = document.getElementById(canvasId).getContext("2d");

    globalChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Principal", "Interest"],
            datasets: [{
                data: [principal, interest]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });
}

/* ==============================
   Render Line Chart
============================== */

function renderBalanceChart(canvasId, labels, balanceData) {

    destroyChart();

    const ctx = document.getElementById(canvasId).getContext("2d");

    globalChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Remaining Balance",
                data: balanceData,
                fill: false,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}