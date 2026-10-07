let selectedCards = [];
let takenCards = [];
let currentBet = 5;
let currentBalance = 100;

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

function showToast(msg) {
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.notificationOccurred('warning');
    }
    const toast = document.getElementById('toastWarning');
    if (toast) {
        toast.innerText = msg;
        toast.style.display = 'block';
        setTimeout(() => toast.style.display = 'none', 3000);
    }
}

function selectRoom(bet) {
    currentBet = bet;
    document.getElementById('betAmount').innerText = bet + " ETB";
    document.getElementById('roomSelectionView').classList.add('hidden');
    document.getElementById('gameView').classList.remove('hidden');
    renderGrid();
}

function goBack() {
    if (!document.getElementById('gameView').classList.contains('hidden')) {
        document.getElementById('gameView').classList.add('hidden');
        document.getElementById('roomSelectionView').classList.remove('hidden');
    }
}

function toggleCartelaSelection(cardId) {
    let index = selectedCards.indexOf(cardId);
    if (index > -1) {
        selectedCards.splice(index, 1);
        currentBalance += currentBet;
    } else {
        if (selectedCards.length >= 6) {
            showToast("በአንድ ጨዋታ ከ 6 ካርቴላ በላይ መያዝ አይችሉም!");
            return;
        }
        if (currentBalance < currentBet) {
            showToast("በቂ ቀሪ ሂሳብ የለዎትም! እባክዎን ብር ይሙሉ");
            return;
        }
        selectedCards.push(cardId);
        currentBalance -= currentBet;
    }
    document.getElementById('userBalance').innerText = currentBalance;
    renderGrid();
    renderActiveCards();
}

function handleManualInput() {
    const input = document.getElementById('cartelaInput');
    const val = parseInt(input.value);
    if (val >= 1 && val <= 600) {
        toggleCartelaSelection(val);
        input.value = '';
    }
}

function autoPickCartela() {
    if (selectedCards.length >= 6) {
        showToast("በአንድ ጨዋታ ከ 6 ካርቴላ በላይ መያዝ አይችሉም!");
        return;
    }
    let rand;
    do {
        rand = Math.floor(Math.random() * 600) + 1;
    } while (selectedCards.includes(rand) || takenCards.includes(rand));
    
    if (window.Telegram && Telegram.WebApp && Telegram.WebApp.HapticFeedback) {
        Telegram.WebApp.HapticFeedback.impactOccurred('medium');
    }
    showToast(`ሲስተሙ ካርቴላ #${rand} መርጦልዎታል!`);
    toggleCartelaSelection(rand);
}

function renderGrid() {
    const grid = document.getElementById('cartelaGrid');
    grid.innerHTML = '';
    for (let i = 1; i <= 80; i++) {
        const btn = document.createElement('div');
        btn.className = 'cartela-btn';
        btn.innerText = i;
        if (selectedCards.includes(i)) btn.classList.add('selected');
        btn.onclick = () => toggleCartelaSelection(i);
        grid.appendChild(btn);
    }
}

function renderActiveCards() {
    const container = document.getElementById('activeCardsContainer');
    document.getElementById('selectedCount').innerText = selectedCards.length;

    if (selectedCards.length === 0) {
        container.innerHTML = `<div style="color:#64748b; font-size:11px; text-align:center; width:100%; padding:10px;">ምንም ካርቴላ አልያዙም። ከላይ ቁጥር መርጠው ይያዙ!</div>`;
        return;
    }

    container.innerHTML = '';
    selectedCards.forEach(cId => {
        const cardData = generateStandardBingoCard(cId);
        const cardDiv = document.createElement('div');
        cardDiv.className = 'bingo-card';

        let gridHTML = `
            <div class="b-head">B</div>
            <div class="i-head">I</div>
            <div class="n-head">N</div>
            <div class="g-head">G</div>
            <div class="o-head">O</div>
        `;

        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 5; c++) {
                if (r === 2 && c === 2) {
                    gridHTML += `<div class="bingo-cell marked">★</div>`;
                } else {
                    let num = cardData[c][r];
                    gridHTML += `<div class="bingo-cell">${num}</div>`;
                }
            }
        }

        cardDiv.innerHTML = `
            <div class="bingo-card-title">Cartela No : ${cId}</div>
            <div class="bingo-grid">${gridHTML}</div>
            <button class="bingo-claim-btn" onclick="alert('🔥 BINGO!')">🔥 BINGO</button>
        `;

        container.appendChild(cardDiv);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
    }
});
