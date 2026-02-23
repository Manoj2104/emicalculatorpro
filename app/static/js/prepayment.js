/*
==========================================
Prepayment Simulation Frontend Engine
==========================================
Handles:
- Input validation
- API call
- Result rendering
- Error handling
==========================================
*/

const simulateBtn = document.getElementById("simulateBtn");

const principalInput = document.getElementById("pp_principal");
const rateInput = document.getElementById("pp_rate");
const tenureInput = document.getElementById("pp_tenure");

const lumpSumInput = document.getElementById("pp_lump_sum");
const afterMonthInput = document.getElementById("pp_after_month");
const extraMonthlyInput = document.getElementById("pp_extra_monthly");

const newTenureEl = document.getElementById("pp_new_tenure");
const tenureReducedEl = document.getElementById("pp_tenure_reduced");
const interestSavedEl = document.getElementById("pp_interest_saved");

simulateBtn.addEventListener("click", async () => {

    const principal = parseFloat(principalInput.value);
    const rate = parseFloat(rateInput.value);
    const tenure = parseInt(tenureInput.value);

    const lump_sum = parseFloat(lumpSumInput.value) || 0;
    const after_month = parseInt(afterMonthInput.value) || 0;
    const extra_monthly = parseFloat(extraMonthlyInput.value) || 0;

    if (!principal || principal <= 0 ||
        !rate || rate < 0 ||
        !tenure || tenure <= 0) {
        alert("Please enter valid loan details.");
        return;
    }

    if ((lump_sum > 0 && after_month > 0 && extra_monthly > 0)) {
        alert("Choose either Lump Sum OR Monthly Extra EMI, not both.");
        return;
    }

    if (!( (lump_sum > 0 && after_month > 0) || extra_monthly > 0 )) {
        alert("Please provide prepayment details.");
        return;
    }

    try {

        const response = await fetch("/api/prepayment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                principal,
                rate,
                tenure,
                lump_sum,
                after_month,
                extra_monthly
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Simulation failed.");
            return;
        }

        renderResult(data.prepayment_result);

    } catch (error) {
        alert("Network error. Please try again.");
    }

});

/* ==============================
   Render Result
============================== */

function renderResult(result) {

    newTenureEl.textContent = result.new_tenure_months + " Months";
    tenureReducedEl.textContent = result.tenure_reduced + " Months";
    interestSavedEl.textContent = formatCurrency(result.interest_saved);

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