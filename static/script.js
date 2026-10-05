// Fast Bingo NextGen Pro - JavaScript Engine

let selectedCards = [];
let takenCards = [];

// 1. Standard BINGO Card Generator (600 Unique Non-repeating Cards)
function generateStandardBingoCard(cardId) {
    function getUniqueRandoms(min, max, count) {
        let nums = [];
        for (let i = min; i <= max; i++) nums.push(i);
        let seed = cardId * 997; 
        for (let i = nums.length - 1; i > 0; i--) {
            let j = Math.floor(((seed = (seed * 9301 + 49297) % 233280) / 233280) * (i + 1));
            [nums[i], nums[j]] = [nums[j], nums[i]];
        }
        return nums.slice(0, count).sort((a, b) => a - b);
    }

    const b = getUniqueRandoms(1, 15, 5);
    const i = getUniqueRandoms(16, 30, 5);
    const n = getUniqueRandoms(31, 45, 4);
    const g = getUniqueRandoms(46, 60, 5);
    const o = getUniqueRandoms(61, 75, 5);

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

// 2. Toggle Selection Logic (ድጋሜ ሲነካ ቁጥሩን እንዲለቅ)
function toggleCartelaSelection(cardId) {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.impactOccurred('light');
    }
    
    let index = selectedCards.indexOf(cardId);
    if (index > -1) {
        selectedCards.splice(index, 1);
    } else {
        if (selectedCards.length >= 6) {
            showNotification("በአንድ ጨዋታ ከ 6 ካርቴላ በላይ መያዝ አይችሉም!", true);
            return;
        }
        selectedCards.push(cardId);
    }
    updateUI();
}

// 3. Auto Select with Vibration Feedback (ሲስተሙ ሲመርጥ)
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
        updateUI();
    }
}

// 4. Clean Warning Notification (ባላንስ እና ገደብ ማሳወቂያ)
function showNotification(msg, isError = false) {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.notificationOccurred(isError ? 'error' : 'warning');
    }
    const alertBox = document.getElementById('alert-box');
    if (alertBox) {
        alertBox.innerText = msg;
        alertBox.classList.add('show');
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
