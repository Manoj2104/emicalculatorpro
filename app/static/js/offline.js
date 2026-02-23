/*
==========================================
Offline Support System
==========================================
Features:
- Detect online/offline state
- Save last calculation
- Restore data when offline
- User notification banner
==========================================
*/

const OFFLINE_STORAGE_KEY = "emi_last_calculation";

/* ==============================
   Network Status Detection
============================== */

function updateNetworkStatus() {
    if (!navigator.onLine) {
        showOfflineBanner();
    } else {
        hideOfflineBanner();
    }
}

window.addEventListener("online", updateNetworkStatus);
window.addEventListener("offline", updateNetworkStatus);

function showOfflineBanner() {
    let banner = document.getElementById("offlineBanner");
    if (!banner) {
        banner = document.createElement("div");
        banner.id = "offlineBanner";
        banner.innerText = "You are offline. Showing last saved calculation.";
        banner.style.background = "#F59E0B";
        banner.style.color = "#000";
        banner.style.padding = "10px";
        banner.style.textAlign = "center";
        document.body.prepend(banner);
    }
}

function hideOfflineBanner() {
    const banner = document.getElementById("offlineBanner");
    if (banner) banner.remove();
}

/* ==============================
   Save Last Calculation
============================== */

function saveCalculationOffline(data) {
    localStorage.setItem(OFFLINE_STORAGE_KEY, JSON.stringify(data));
}

/* ==============================
   Restore Last Calculation
============================== */

function restoreCalculationOffline() {
    if (!navigator.onLine) {
        const saved = localStorage.getItem(OFFLINE_STORAGE_KEY);
        if (saved) {
            const data = JSON.parse(saved);

            if (window.updateResults) {
                updateResults(data.calculation);
            }
            if (window.renderChart) {
                renderChart(data.calculation);
            }
        }
    }
}

/* ==============================
   Init
============================== */

document.addEventListener("DOMContentLoaded", () => {
    updateNetworkStatus();
    restoreCalculationOffline();
});