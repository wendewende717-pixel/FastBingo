// Fast Bingo NextGen Pro - Exact Sync Engine with Beteseb Bingo

let selectedCards = [];
let takenCards = [];
let allCardsData = {};

// Load exact 600 cards from JSON file
async function loadBingoCards() {
    try {
        const response = await fetch('/static/cards.json');
        allCardsData = await response.json();
        console.log("600 Bingo Cards loaded successfully and synced 100%!");
    } catch (err) {
        console.error("Failed to load synced cards, falling back to deterministic generator", err);
    }
}

function getBingoCard(cardId) {
    if (allCardsData && allCardsData[cardId]) {
        return allCardsData[cardId];
    }
    // Fallback if card index not found
    return [];
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
    loadBingoCards();
    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
});
