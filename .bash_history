    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
});
EOF

cat << 'EOF' > rooms_config.py
ROOMS = [
    {"id": 5, "name": "ክፍል 5", "stake": 5, "type": "STANDARD"},
    {"id": 10, "name": "ክፍል 10", "stake": 10, "type": "STANDARD"},
    {"id": 15, "name": "ክፍል 15", "stake": 15, "type": "STANDARD"},
    {"id": 20, "name": "ክፍል 20", "stake": 20, "type": "STANDARD"},
    {"id": 25, "name": "ክፍል 25", "stake": 25, "type": "STANDARD"},
    {"id": 50, "name": "ክፍል 50", "stake": 50, "type": "STANDARD"},
    {"id": 100, "name": "ክፍል 100", "stake": 100, "type": "STANDARD"},
    {"id": 200, "name": "ክፍል 200", "stake": 200, "type": "STANDARD"},
    {"id": 500, "name": "👑 VIP ክፍል 500", "stake": 500, "type": "VIP"}
]
EOF

git add .
git commit -m "Update rooms up to VIP 500 ETB, fix cartela generator and grid size"
git push origin main
cd FastBingo
cat << 'EOF' > static/script.js
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
EOF

git add .
git commit -m "Update rooms up to VIP 500 ETB, fix cartela generator and grid size"
git push origin main
cd FastBingo
cat << 'EOF' > static/script.js
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
EOF

cat << 'EOF' > rooms_config.py
ROOMS = [
    {"id": 5, "name": "ክፍል 5", "stake": 5, "type": "STANDARD"},
    {"id": 10, "name": "ክፍል 10", "stake": 10, "type": "STANDARD"},
    {"id": 15, "name": "ክፍል 15", "stake": 15, "type": "STANDARD"},
    {"id": 20, "name": "ክፍል 20", "stake": 20, "type": "STANDARD"},
    {"id": 25, "name": "ክፍል 25", "stake": 25, "type": "STANDARD"},
    {"id": 50, "name": "ክፍል 50", "stake": 50, "type": "STANDARD"},
    {"id": 100, "name": "ክፍል 100", "stake": 100, "type": "STANDARD"},
    {"id": 200, "name": "ክፍል 200", "stake": 200, "type": "STANDARD"},
    {"id": 500, "name": "👑 VIP ክፍል 500", "stake": 500, "type": "VIP"}
]
EOF

git add .
git commit -m "Fix rooms up to VIP 500 ETB, clean up cartela generator and layout up to grid 80"
git push origin main
cd FastBingo
# 1. Update static/script.js
cat << 'EOF' > static/script.js
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
EOF

# 2. Update Rooms in static/index.html
cat << 'EOF' > static/index.html
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Fast Bingo Bot</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div id="alert-box" class="alert-box"></div>

    <!-- Header Bar -->
    <div class="header">
        <button class="nav-btn" onclick="backToRooms()">← Back</button>
        <div class="user-info">
            <span id="user-name">Wende</span>
            <span class="balance-badge" id="user-balance">100 ETB</span>
        </div>
        <button class="nav-btn" onclick="location.reload()">🔄 Refresh</button>
    </div>

    <!-- ROOM SELECTION SCREEN -->
    <div id="room-selection-screen" class="screen">
        <h2 class="title">🎯 የጨዋታ ክፍል ይምረጡ</h2>
        <div class="rooms-grid">
            <button class="room-card" onclick="selectRoom(5)"><h3>ክፍል 5</h3><p>5 ETB</p></button>
            <button class="room-card" onclick="selectRoom(10)"><h3>ክፍል 10</h3><p>10 ETB</p></button>
            <button class="room-card" onclick="selectRoom(15)"><h3>ክፍል 15</h3><p>15 ETB</p></button>
            <button class="room-card" onclick="selectRoom(20)"><h3>ክፍል 20</h3><p>20 ETB</p></button>
            <button class="room-card" onclick="selectRoom(25)"><h3>ክፍል 25</h3><p>25 ETB</p></button>
            <button class="room-card" onclick="selectRoom(50)"><h3>ክፍል 50</h3><p>50 ETB</p></button>
            <button class="room-card" onclick="selectRoom(100)"><h3>ክፍል 100</h3><p>100 ETB</p></button>
            <button class="room-card" onclick="selectRoom(200)"><h3>ክፍል 200</h3><p>200 ETB</p></button>
            <button class="room-card vip-room" onclick="selectRoom(500)"><h3>👑 VIP ክፍል</h3><p>500 ETB</p></button>
        </div>
    </div>

    <!-- GAME PLAY SCREEN -->
    <div id="game-screen" class="screen" style="display:none;">
        <div class="game-meta">
            <div>GAME ID<br><b>#FB-5-7456</b></div>
            <div>PLAYERS<br><b>2</b></div>
            <div>BET<br><b id="current-bet">20 ETB</b></div>
            <div>DERASH<br><b>40 ETB</b></div>
            <div>TIMER<br><b id="timer-display">30s</b></div>
        </div>

        <div class="controls-bar">
            <input type="text" placeholder="ካርቴላ # (1-600)" id="manual-input">
            <button class="btn-primary" onclick="autoSelectCard()">ያዝ</button>
            <button class="btn-warning" onclick="autoSelectCard()">ሲስተሙ ይምረጡልዎት</button>
        </div>

        <!-- Grid 1-80 -->
        <div id="cartela-grid" class="cartela-grid-80"></div>

        <div class="selected-header">
            ✨ የተያዙ ካርቴላዎች (<span id="selected-count">0</span>/6):-
        </div>

        <div id="selected-cartelas-container" class="cartelas-list"></div>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>
EOF

# 3. Git Commit and Push to Render
git add .
git commit -m "Complete WebApp fix: Add rooms up to VIP 500 ETB, grid 80, valid BINGO matrix, toggle selection"
git push origin main
