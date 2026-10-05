// Fast Bingo NextGen Pro - Standard Bingo Engine

let selectedCards = [];
let takenCards = [];

// Professional 100% Standard BINGO Generator (B:1-15, I:16-30, N:31-45, G:46-60, O:61-75)
function generateStandardBingoCard(cardId) {
    function getSeededCol(min, max, count, seedOffset) {
        let nums = [];
        for (let i = min; i <= max; i++) nums.push(i);
        
        let seed = (cardId * 2654435761 + seedOffset * 40503) % 2147483647;
        for (let i = nums.length - 1; i > 0; i--) {
            seed = (seed * 16807) % 2147483647;
            let j = Math.floor((seed / 2147483647) * (i + 1));
            [nums[i], nums[j]] = [nums[j], nums[i]];
        }
        return nums.slice(0, count).sort((a, b) => a - b);
    }

    const b = getSeededCol(1, 15, 5, 101);
    const i = getSeededCol(16, 30, 5, 202);
    const n = getSeededCol(31, 45, 4, 303);
    const g = getSeededCol(46, 60, 5, 404);
    const o = getSeededCol(61, 75, 5, 505);

    let grid = [];
    for (let r = 0; r < 5; r++) {
        let row = [
            b[r],
            i[r],
            r === 2 ? '★' : (r > 2 ? n[r - 1] : n[r]),
            g[r],
            o[r]
        ];
        grid.push(row);
    }
    return grid;
}

// Toggle Cartela Selection (ድጋሜ ሲነካ ቁጥሩን ይለቃል)
function toggleCartelaSelection(cardId) {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.impactOccurred('light');
    }
    
    let index = selectedCards.indexOf(cardId);
    if (index > -1) {
        selectedCards.splice(index, 1);
        showNotification(`ካርቴላ #${cardId} ተለቋል`, false);
    } else {
        if (selectedCards.length >= 6) {
            showNotification("በአንድ ጨዋታ ከ 6 ካርቴላ በላይ መያዝ አይችሉም!", true);
            return;
        }
        selectedCards.push(cardId);
        showNotification(`ካርቴላ #${cardId} ተይዟል`, false);
    }
    updateUI();
}

// Auto Select Card with Vibration and Clean Text
function autoSelectCard() {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.impactOccurred('medium');
    }
    
    let available = [];
    for (let i = 1; i <= 600; i++) {
        if (!takenCards.includes(i) && !selectedCards.includes(i)) {
            available.push(i);
        }
    }
    if (available.length > 0 && selectedCards.length < 6) {
        let randomCard = available[Math.floor(Math.random() * available.length)];
        selectedCards.push(randomCard);
        showNotification(`ሲስተሙ ካርቴላ #${randomCard} መርጦልዎታል!`, false);
        updateUI();
    }
}

// Clean Toast Notification System
function showNotification(msg, isError = false) {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.notificationOccurred(isError ? 'error' : 'success');
    }
    const alertBox = document.getElementById('alert-box');
    if (alertBox) {
        alertBox.innerText = msg;
        alertBox.className = `alert-box show ${isError ? 'error' : 'success'}`;
        setTimeout(() => alertBox.classList.remove('show'), 3000);
    } else {
        alert(msg);
    }
}

function updateUI() {
    const countElem = document.getElementById('selected-count');
    if (countElem) {
        countElem.innerText = selectedCards.length;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
});
