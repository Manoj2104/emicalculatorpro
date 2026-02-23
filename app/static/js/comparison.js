/*
==========================================
Loan Comparison Frontend Engine
==========================================
Handles:
- Input collection
- Validation
- API call
- Dynamic result rendering
==========================================
*/

const compareBtn = document.getElementById("compareBtn");
const resultContainer = document.getElementById("comparisonResult");

compareBtn.addEventListener("click", async () => {

    const cards = document.querySelectorAll(".comparison-card");

    let loans = [];

    cards.forEach(card => {
        const principal = parseFloat(card.querySelector(".principal").value);
        const rate = parseFloat(card.querySelector(".rate").value);
        const tenure = parseInt(card.querySelector(".tenure").value);

        if (principal > 0 && rate >= 0 && tenure > 0) {
            loans.push({ principal, rate, tenure });
        }
    });

    if (loans.length < 2) {
        alert("Please enter at least 2 valid loans.");
        return;
    }

    try {
        const response = await fetch("/api/compare-loans", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ loans })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Comparison failed.");
            return;
        }

        renderResults(data.results);

    } catch (error) {
        alert("Network error. Please try again.");
    }
});

/* ==============================
   Render Results
============================== */

function renderResults(results) {

    resultContainer.innerHTML = "";

    results.forEach(loan => {

        const card = document.createElement("div");
        card.classList.add("comparison-result-card");

        if (loan.best_option) {
            card.classList.add("best-loan");
        }

        card.innerHTML = `
            <h4>Loan ${loan.loan_id} ${loan.best_option ? "🏆 Best Option" : ""}</h4>
            <p><strong>EMI:</strong> ${formatCurrency(loan.emi)}</p>
            <p><strong>Total Interest:</strong> ${formatCurrency(loan.total_interest)}</p>
            <p><strong>Total Payment:</strong> ${formatCurrency(loan.total_payment)}</p>
            <p><strong>Efficiency Score:</strong> ${loan.efficiency_score}</p>
        `;

        resultContainer.appendChild(card);
    });
}

/* ==============================
   Currency Format
============================== */

function formatCurrency(amount) {
    return new Intl.NumberFormat(undefined, {
        style: "currency",
        currency: "USD"
    }).format(amount);
}