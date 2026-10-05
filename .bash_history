            cursor: pointer;
        }

        /* Bottom Navigation Bar (Beteseb Style) */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50px;
            background: #111827;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid rgba(255,255,255,0.1);
            z-index: 999;
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #6b7280;
            font-size: 10px;
            font-weight: bold;
            text-decoration: none;
            cursor: pointer;
        }

        .nav-item.active {
            color: var(--accent-blue);
        }

        .nav-icon {
            font-size: 16px;
            margin-bottom: 2px;
        }

        /* Warning Toast */
        .toast-warning {
            position: fixed;
            top: 50px;
            left: 50%;
            transform: translateX(-50%);
            background: #dc2626;
            color: #fff;
            padding: 10px 18px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.5);
            z-index: 1000;
            display: none;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- Red Alert Warning Toast -->
    <div id="toastWarning" class="toast-warning"></div>

    <!-- Top Header Bar -->
    <div class="top-header">
        <button class="nav-top-btn" onclick="goBack()"><span style="font-size:14px;">←</span> Back</button>
        <div class="user-summary">
            <span id="userName" style="font-weight:bold;">Wende</span>
            <span class="wallet-pill"><span id="userBalance">100</span> ETB</span>
        </div>
        <button class="nav-top-btn" onclick="refreshApp()">🔄 Refresh</button>
    </div>

    <!-- Room Selection View -->
    <div id="roomSelectionView">
        <h4 style="text-align:center; color: var(--accent-gold); margin: 10px 0;">🎯 የጨዋታ ክፍል ይምረጡ</h4>
        <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 8px;">
            <div style="background:#151d30; border:1px solid var(--accent-blue); border-radius:10px; padding:12px; text-align:center; cursor:pointer;" onclick="selectRoom(5)">
                <div style="color:var(--accent-gold); font-weight:bold;">ክፍል 5</div>
                <div style="color:#60a5fa; font-weight:bold; font-size:16px;">5 ETB</div>
            </div>
            <div style="background:#151d30; border:1px solid var(--accent-blue); border-radius:10px; padding:12px; text-align:center; cursor:pointer;" onclick="selectRoom(10)">
                <div style="color:var(--accent-gold); font-weight:bold;">ክፍል 10</div>
                <div style="color:#60a5fa; font-weight:bold; font-size:16px;">10 ETB</div>
            </div>
            <div style="background:#151d30; border:1px solid var(--accent-blue); border-radius:10px; padding:12px; text-align:center; cursor:pointer;" onclick="selectRoom(15)">
                <div style="color:var(--accent-gold); font-weight:bold;">ክፍል 15</div>
                <div style="color:#60a5fa; font-weight:bold; font-size:16px;">15 ETB</div>
            </div>
            <div style="background:#151d30; border:1px solid var(--accent-blue); border-radius:10px; padding:12px; text-align:center; cursor:pointer;" onclick="selectRoom(20)">
                <div style="color:var(--accent-gold); font-weight:bold;">ክፍል 20</div>
                <div style="color:#60a5fa; font-weight:bold; font-size:16px;">20 ETB</div>
            </div>
        </div>
    </div>

    <!-- Main Game View -->
    <div id="gameView" class="hidden">
        <div class="game-header">
            <div class="stat-box">GAME ID<br><span class="stat-val">#FB-5-7456</span></div>
            <div class="stat-box">PLAYERS<br><span class="stat-val" id="playerCount">1</span></div>
            <div class="stat-box">BET<br><span class="stat-val" id="betAmount">5 ETB</span></div>
            <div class="stat-box">DERASH<br><span class="stat-val" id="derashAmount">0 ETB</span></div>
            <div class="stat-box">TIMER<br><span class="stat-val" id="timerVal">60s</span></div>
        </div>

        <!-- Smart Controls -->
        <div class="controls-row">
            <input type="number" id="cartelaInput" class="num-input" placeholder="ካርቴላ # (1-600)" onchange="handleManualInput()" min="1" max="600">
            <button class="btn" onclick="handleManualInput()">ያዝ</button>
            <button class="btn btn-gold" onclick="autoPickCartela()">ሲስተሙ ይመረጥልኝ</button>
        </div>

        <!-- Legend -->
        <div style="display:flex; justify-content:space-around; font-size:10px; margin-bottom:5px; color:#94a3b8;">
            <span><span style="color:#1e293b;">■</span> ክፍት</span>
            <span><span style="color:var(--accent-red);">■</span> የተያዘ (ሌሎች)</span>
            <span><span style="color:var(--accent-green);">■</span> የኔ ካርቴላ</span>
        </div>

        <!-- 600 Cartelas Grid -->
        <div class="cartela-picker-grid" id="cartelaGrid"></div>

        <!-- Selected Cartelas Side-by-Side Display -->
        <div style="font-weight:bold; font-size:11px; margin: 6px 0; color:var(--accent-gold);">
            ✨ የተያዙ ካርቴላዎች (<span id="selectedCount">0</span>/6)፦
        </div>
        <div class="active-cards-container" id="activeCardsContainer">
            <div style="color:#64748b; font-size:11px; text-align:center; width:100%; padding:10px;">
                ምንም ካርቴላ አልያዙም። ከላይ ቁጥር መርጠው ይያዙ!
            </div>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchTab('game', this)">
            <div class="nav-icon">🎮</div>
            <span>Game</span>
        </div>
        <div class="nav-item" onclick="switchTab('history', this)">
            <div class="nav-icon">📜</div>
            <span>History</span>
        </div>
        <div class="nav-item" onclick="switchTab('wallet', this)">
            <div class="nav-icon">👛</div>
            <span>Wallet</span>
        </div>
        <div class="nav-item" onclick="switchTab('profile', this)">
            <div class="nav-icon">👤</div>
            <span>Profile</span>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        let currentBalance = 100;
        let currentBet = 5;
        let mySelectedCartelas = [];
        let takenByOthers = [5, 12, 45, 88, 120];
        let timerRunning = false;
        let timerSeconds = 60;
        let timerInterval = null;

        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('userName').innerText = tg.initDataUnsafe.user.first_name;
        }

        function triggerVibration(pattern = [200, 100, 200]) {
            if (navigator.vibrate) {
                navigator.vibrate(pattern);
            }
        }

        function showWarning(msg) {
            triggerVibration([300, 100, 300, 100, 300]); // Strong vibration
            const toast = document.getElementById('toastWarning');
            toast.innerText = msg;
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 3000);
        }

        function updateBalanceDisplay() {
            document.getElementById('userBalance').innerText = currentBalance;
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
            } else {
                tg.close();
            }
        }

        function refreshApp() {
            location.reload();
        }

        function startTimer() {
            if (!timerRunning) {
                timerRunning = true;
                document.getElementById('playerCount').innerText = "2";
                document.getElementById('derashAmount').innerText = (currentBet * 2) + " ETB";
                
                timerInterval = setInterval(() => {
                    timerSeconds--;
                    document.getElementById('timerVal').innerText = timerSeconds + "s";
                    if (timerSeconds <= 0) {
                        clearInterval(timerInterval);
                        showWarning("⏰ ጨዋታው ተጀምሯል!");
                    }
                }, 1000);
            }
        }

        function renderGrid() {
            const grid = document.getElementById('cartelaGrid');
            grid.innerHTML = '';
            for (let i = 1; i <= 600; i++) {
                const btn = document.createElement('div');
                btn.className = 'cartela-btn';
                btn.innerText = i;
                
                if (mySelectedCartelas.includes(i)) {
                    btn.classList.add('selected');
                } else if (takenByOthers.includes(i)) {
                    btn.classList.add('taken');
                } else {
                    btn.onclick = () => toggleSelectCartela(i);
                }
                grid.appendChild(btn);
            }
        }

        function toggleSelectCartela(num) {
            if (takenByOthers.includes(num)) {
                showWarning('ይህ ካርቴላ በሌላ ተጫዋች ተይዟል!');
                return;
            }

            const index = mySelectedCartelas.indexOf(num);
            if (index > -1) {
                mySelectedCartelas.splice(index, 1);
                currentBalance += currentBet;
            } else {
                // Rule: Max 6 Cartelas Limit
                if (mySelectedCartelas.length >= 6) {
                    showWarning('⚠️ ከአንድ ተጫዋች በላይ እስከ 6 ካርቴላ ብቻ መያዝ ይቻላል!');
                    return;
                }

                // Rule: Check Balance
                if (currentBalance < currentBet) {
                    showWarning('❌ በቂ ቀሪ ሂሳብ የለዎትም! እባክዎን ብር ይሙሉወ።');
                    return;
                }

                mySelectedCartelas.push(num);
                currentBalance -= currentBet;

                // Rule: Start 60s timer when 2nd condition/player selects
                if (mySelectedCartelas.length >= 1) {
                    startTimer();
                }
            }

            updateBalanceDisplay();
            renderGrid();
            renderActiveCards();
        }

        function handleManualInput() {
            const input = document.getElementById('cartelaInput');
            const val = parseInt(input.value);
            if (val >= 1 && val <= 600) {
                toggleSelectCartela(val);
                input.value = '';
            }
        }

        function autoPickCartela() {
            if (mySelectedCartelas.length >= 6) {
                showWarning('⚠️️ ከአንድ ተጫዋች በላይ እስከ 6 ካርቴላ ብቻ መያዝ ይቻላል!');
                return;
            }
            let rand;
            do {
                rand = Math.floor(Math.random() * 600) + 1;
            } while (mySelectedCartelas.includes(rand) || takenByOthers.includes(rand));
            
            triggerVibration([100, 50, 100]); // Soft pleasant vibration
            toggleSelectCartela(rand);
        }

        function generateBingoNumbers(cartelaId) {
            let card = [];
            let cols = [[1,15], [16,30], [31,45], [46,60], [61,75]];
            for (let c = 0; c < 5; c++) {
                let colNums = [];
                let min = cols[c][0], max = cols[c][1];
                for (let r = 0; r < 5; r++) {
                    let num = min + ((cartelaId * (r + 1) * (c + 3)) % (max - min + 1));
                    colNums.push(num);
                }
                card.push(colNums);
            }
            return card;
        }

        function renderActiveCards() {
            const container = document.getElementById('activeCardsContainer');
            document.getElementById('selectedCount').innerText = mySelectedCartelas.length;

            if (mySelectedCartelas.length === 0) {
                container.innerHTML = `<div style="color:#64748b; font-size:11px; text-align:center; width:100%; padding:10px;">ምንም ካርቴላ አልያዙም። ከላይ ቁጥር መርጠው ይያዙ!</div>`;
                return;
            }

            container.innerHTML = '';
            mySelectedCartelas.forEach(cId => {
                const cardData = generateBingoNumbers(cId);
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
                            gridHTML += `<div class="bingo-cell" onclick="this.classList.toggle('marked')">${num}</div>`;
                        }
                    }
                }

                cardDiv.innerHTML = `
                    <div class="bingo-card-title">Cartela No : ${cId}</div>
                    <div class="bingo-grid">${gridHTML}</div>
                    <button class="bingo-claim-btn" onclick="claimBingo(${cId})">🔥 BINGO</button>
                `;

                container.appendChild(cardDiv);
            });
        }

        function claimBingo(cartelaId) {
            triggerVibration([100, 100, 100, 100, 300]);
            alert(`🎉 እንኳን ደስ አለዎት! በካርቴላ #${cartelaId} BINGO ብለዋል!`);
        }

        function switchTab(tabName, el) {
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            el.classList.add('active');

            if (tabName !== 'game') {
                showWarning(`ℹ️ የ ${tabName.toUpperCase()} ገፅ በቅርቡ ክፍት ይሆናል!`);
            }
        }

        updateBalanceDisplay();
    </script>
</body>
</html>
EOF

git add static/index.html
git commit -m "Update layout with top/bottom bars, max 6 cartelas limit, and vibration alerts"
git push origin main
cd FastBingo
cat << 'EOF' > static/script.js
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
EOF

git add .
git commit -m "Update bingo engine and fix room logic"
git push origin main
