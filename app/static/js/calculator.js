document.addEventListener("DOMContentLoaded", function () {

    let chartInstance;

    const calculateBtn = document.getElementById("calculateBtn");
    const toggleBtn = document.getElementById("toggleScheduleBtn");
    const scheduleSection = document.getElementById("scheduleSection");
    const searchInput = document.getElementById("scheduleSearch");
    const downloadBtn = document.getElementById("downloadExcel");
    const shareBtn = document.getElementById("shareBtn");

    // ========================
    // EMI CALCULATION
    // ========================

    if (calculateBtn) {
        calculateBtn.addEventListener("click", function () {

            const P = parseFloat(document.getElementById("principal")?.value || 0);
            const annualRate = parseFloat(document.getElementById("rate")?.value || 0);
            let tenureValue = parseFloat(document.getElementById("tenure")?.value || 0);
            const tenureType = document.getElementById("tenureType")?.value;
            const startDateInput = document.getElementById("startDate")?.value;

            if (tenureType === "years") tenureValue *= 12;

            const N = tenureValue;
            const R = annualRate / 12 / 100;

            if (N <= 0 || P <= 0 || R <= 0) return;

            const EMI = (P * R * Math.pow(1 + R, N)) / (Math.pow(1 + R, N) - 1);
            const totalPayment = EMI * N;
            const totalInterest = totalPayment - P;

            document.getElementById("emiValue").innerText = formatCurrency(EMI);
            document.getElementById("interestValue").innerText = formatCurrency(totalInterest);
            document.getElementById("totalValue").innerText = formatCurrency(totalPayment);

            if (startDateInput) {
                const startDate = new Date(startDateInput);
                document.getElementById("displayStartDate").innerText =
                    startDate.toLocaleDateString("en-IN");

                calculateEndDate(startDate, N);
            }

            renderChart(P, totalInterest);
            generateSchedule(P, R, EMI, N);
        });
    }

    // ========================
    // TOGGLE
    // ========================

    if (toggleBtn && scheduleSection) {
        toggleBtn.addEventListener("click", function () {
            const isHidden = scheduleSection.style.display === "none" || scheduleSection.style.display === "";
            scheduleSection.style.display = isHidden ? "block" : "none";
            toggleBtn.innerText = isHidden ? "Hide Repayment Schedule" : "View Repayment Schedule";
        });
    }

    // ========================
    // SEARCH
    // ========================

    if (searchInput) {
        searchInput.addEventListener("input", function () {

            const filter = this.value.trim().toLowerCase();
            const rows = document.querySelectorAll("#scheduleTable tbody tr");

            rows.forEach(row => {

                const month = row.cells[0]?.innerText.trim();
                const date = row.cells[1]?.innerText.trim().toLowerCase();
                const cleanText = row.innerText.replace(/₹|,/g, "").toLowerCase();

                let show = false;

                if (/^\d+$/.test(filter)) {
                    show = month === filter;
                } else if (filter.includes("/")) {
                    show = date.includes(filter);
                } else {
                    show = cleanText.includes(filter);
                }

                row.style.display = show ? "" : "none";
            });
        });
    }

    // ========================
    // DOWNLOAD
    // ========================

    if (downloadBtn) {
        downloadBtn.addEventListener("click", function () {

            let csvContent = "\uFEFF";
            const rows = document.querySelectorAll("#scheduleTable tr");

            rows.forEach(row => {
                const cols = row.querySelectorAll("td, th");
                const rowData = Array.from(cols).map(col =>
                    col.innerText.replace(/₹|,/g, "")
                );
                csvContent += rowData.join(",") + "\n";
            });

            const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "emi-repayment-schedule.csv";
            link.click();
        });
    }

    // ========================
    // SHARE
    // ========================

    if (shareBtn) {
        shareBtn.addEventListener("click", function () {

            const emi = document.getElementById("emiValue").innerText;
            const interest = document.getElementById("interestValue").innerText;
            const total = document.getElementById("totalValue").innerText;

            const text = `EMI Summary:
Monthly EMI: ${emi}
Total Interest: ${interest}
Total Payment: ${total}`;

            if (navigator.share) {
                navigator.share({
                    title: "EMI Calculator Result",
                    text: text
                });
            } else {
                navigator.clipboard.writeText(text);
                alert("Copied!");
            }
        });
    }

    // ========================
    // HELPERS
    // ========================

    function calculateEndDate(startDate, months) {
        let endDate = new Date(startDate);
        endDate.setMonth(endDate.getMonth() + months);
        document.getElementById("endDate").innerText =
            endDate.toLocaleDateString("en-IN");
    }

    function generateSchedule(P, R, EMI, N) {

        const tbody = document.querySelector("#scheduleTable tbody");
        if (!tbody) return;

        tbody.innerHTML = "";
        let balance = P;

        const baseDate = document.getElementById("startDate")?.value
            ? new Date(document.getElementById("startDate").value)
            : new Date();

        for (let i = 1; i <= N; i++) {

            const interest = balance * R;
            const principal = EMI - interest;
            balance -= principal;

            const paymentDate = new Date(baseDate);
            paymentDate.setMonth(baseDate.getMonth() + (i - 1));

            const formattedDate =
                paymentDate.getDate().toString().padStart(2, '0') + "/" +
                (paymentDate.getMonth() + 1).toString().padStart(2, '0') + "/" +
                paymentDate.getFullYear();

            const row = document.createElement("tr");

            row.innerHTML = `
                <td data-label="Month">${i}</td>
                <td data-label="Date">${formattedDate}</td>
                <td data-label="EMI">${formatCurrency(EMI)}</td>
                <td data-label="Principal">${formatCurrency(principal)}</td>
                <td data-label="Interest">${formatCurrency(interest)}</td>
                <td data-label="Balance">${formatCurrency(Math.max(balance, 0))}</td>
            `;

            tbody.appendChild(row);
        }
    }

    function formatCurrency(value) {
        return new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR",
            minimumFractionDigits: 2
        }).format(value);
    }

    function renderChart(principal, interest) {
        const ctx = document.getElementById("emiChart");
        if (!ctx) return;

        if (chartInstance) chartInstance.destroy();

        chartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Principal', 'Interest'],
                datasets: [{
                    data: [principal, interest],
                    backgroundColor: ['#10b981', '#3b82f6']
                }]
            },
            options: {
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

});