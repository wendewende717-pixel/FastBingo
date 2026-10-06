let selectedCards = [];
let takenCards = [];
let currentRoom = 5;

// Standard BINGO Card Generator (600 Valid Cards)
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

// Toggle Cartela Selection
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
    renderGrid();
    renderSelectedCards();
}

// Auto Select Card
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
        renderGrid();
        renderSelectedCards();
    }
}

// Clean Toast Notification
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

// Render 1-80 Grid
function renderGrid() {
    const gridContainer = document.getElementById('cartela-grid');
    if (!gridContainer) return;
    
    let html = '';
    for (let i = 1; i <= 80; i++) {
        let isSelected = selectedCards.includes(i);
        let isTaken = takenCards.includes(i);
        let btnClass = 'grid-btn';
        if (isSelected) btnClass += ' selected';
        if (isTaken) btnClass += ' taken';
        
        html += `<button class="${btnClass}" onclick="toggleCartelaSelection(${i})">${i}</button>`;
    }
    gridContainer.innerHTML = html;
}

// Render Selected Cartelas with Bingo Standard Numbers
function renderSelectedCards() {
    const container = document.getElementById('selected-cartelas-container');
    const countElem = document.getElementById('selected-count');
    if (countElem) countElem.innerText = selectedCards.length;
    if (!container) return;

    let html = '';
    selectedCards.forEach(cardId => {
        let matrix = generateStandardBingoCard(cardId);
        html += `<div class="cartela-card">
            <div class="cartela-header">Cartela No : ${cardId}</div>
            <div class="bingo-header-row">
                <span>B</span><span>I</span><span>N</span><span>G</span><span>O</span>
            </div>
            <div class="bingo-grid-matrix">`;
        
        matrix.forEach(row => {
            row.forEach(val => {
                let cellClass = val === '★' ? 'cell free' : 'cell';
                html += `<div class="${cellClass}">${val}</div>`;
            });
        });
        
        html += `</div>
            <button class="bingo-btn">🔥 BINGO</button>
        </div>`;
    });
    container.innerHTML = html;
}

function selectRoom(roomAmount) {
    currentRoom = roomAmount;
    document.getElementById('room-selection-screen').style.display = 'none';
    document.getElementById('game-screen').style.display = 'block';
    renderGrid();
}

function backToRooms() {
    document.getElementById('room-selection-screen').style.display = 'block';
    document.getElementById('game-screen').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
    renderGrid();
});
