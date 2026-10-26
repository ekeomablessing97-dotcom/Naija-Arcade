import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaijaArcade - Play, Compete & Win Cash</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass-card { background: rgba(15, 23, 42, 0.90); backdrop-filter: blur(16px); border: 1px solid rgba(212, 175, 55, 0.25); }
        .gold-glow { box-shadow: 0 0 30px rgba(212, 175, 55, 0.2); }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-amber-500 selection:text-slate-950">

    <!-- Navbar -->
    <header class="glass-card border-b border-amber-500/20 sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3 cursor-pointer" onclick="location.reload()">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-amber-400 flex items-center justify-center font-black text-slate-950 text-xl gold-glow">🎮</div>
            <span class="text-2xl font-black tracking-wider bg-gradient-to-r from-amber-400 via-amber-200 to-amber-500 bg-clip-text text-transparent">NaijaArcade</span>
        </div>
        <div class="flex items-center space-x-3">
            <div id="authNavArea">
                <button onclick="openAuthModal()" class="bg-slate-900 border border-amber-500/40 text-amber-400 font-bold px-4 py-2 rounded-xl text-xs hover:bg-amber-500/10 transition">Sign In / Register</button>
            </div>
            <button onclick="openTournamentModal()" class="hidden md:flex bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-4 py-2 rounded-xl text-xs shadow-lg hover:brightness-110 transition items-center space-x-1">
                <span>🏆 ₦500 Tournament</span>
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-4xl mx-auto px-4 py-8 w-full flex-grow space-y-8">
        
        <!-- Hero Banner -->
        <div class="glass-card rounded-3xl p-8 text-center space-y-4 gold-glow relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-48 h-48 bg-amber-500/10 rounded-full blur-2xl pointer-events-none"></div>
            <span id="dailyDateBadge" class="text-xs uppercase tracking-widest text-amber-400 font-extrabold bg-amber-500/10 px-4 py-1.5 rounded-full border border-amber-500/20">Daily Quest & Fresh Rotation Active</span>
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">7 Arcade Games, Board Classics & <span class="text-amber-400">Cash Prizes</span></h1>
            <p class="text-slate-400 text-sm md:text-base max-w-xl mx-auto">Play Snake & Ladder, Stack Blocks, or solve daily trivia challenges!</p>
        </div>

        <!-- Game Selection Grid (7 Games) -->
        <div id="gameHubGrid" class="space-y-4">
            <h2 class="text-xl font-extrabold text-amber-400 flex items-center justify-between">
                <span>🕹️ Choose From 7 Arcade Games</span>
                <span class="text-xs text-slate-400 font-normal">Board games & daily quizzes</span>
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- Game 1: Snake & Ladder -->
                <div onclick="launchGame('snake')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3 border-amber-400/40 bg-amber-500/5">
                    <div class="w-12 h-12 bg-amber-500/20 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">🐍</div>
                    <h3 class="text-lg font-bold text-white">Naija Snake & Ladder</h3>
                    <p class="text-slate-400 text-xs">Roll the dice, climb ladders, and avoid snakes to win!</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Now ➔</span>
                </div>
                <!-- Game 2: Block Stacker -->
                <div onclick="launchGame('blocks')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3 border-amber-400/40 bg-amber-500/5">
                    <div class="w-12 h-12 bg-amber-500/20 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">🏗️</div>
                    <h3 class="text-lg font-bold text-white">Sky-Tower Stacker</h3>
                    <p class="text-slate-400 text-xs">Build the tallest Lagos skyscraper by dropping building blocks.</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Now ➔</span>
                </div>
                <!-- Game 3 -->
                <div onclick="launchGame('trivia')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-amber-500/10 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">🧠</div>
                    <h3 class="text-lg font-bold text-white">Naija Mega Trivia</h3>
                    <p class="text-slate-400 text-xs">Afrobeats, Nollywood & culture. Rotates fresh daily!</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 4 -->
                <div onclick="launchGame('pidgin')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-amber-500/10 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">🗣️</div>
                    <h3 class="text-lg font-bold text-white">Pidgin Word Scramble</h3>
                    <p class="text-slate-400 text-xs">Unscramble rotating Nigerian street slang and expressions.</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 5 -->
                <div onclick="launchGame('reflex')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-amber-500/10 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">🪙</div>
                    <h3 class="text-lg font-bold text-white">Golden Coin Catcher</h3>
                    <p class="text-slate-400 text-xs">Fast-paced 15-second reflex test. Tap coins as fast as you can.</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 6 -->
                <div onclick="launchGame('geography')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-amber-500/10 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">📍</div>
                    <h3 class="text-lg font-bold text-white">States & Capitals Quiz</h3>
                    <p class="text-slate-400 text-xs">Test your knowledge of Nigeria's 36 states and nicknames.</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 7 -->
                <div onclick="launchGame('football')" class="glass-card p-6 rounded-2xl cursor-pointer hover:border-amber-400 transition transform hover:-translate-y-1 space-y-3 md:col-span-3">
                    <div class="w-12 h-12 bg-amber-500/10 text-amber-400 rounded-xl flex items-center justify-center text-2xl border border-amber-500/30">⚽</div>
                    <h3 class="text-lg font-bold text-white">Super Eagles & AFCON Quiz</h3>
                    <p class="text-slate-400 text-xs">Football trivia covering Nigerian legends and tournaments.</p>
                    <span class="inline-block text-xs text-amber-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
            </div>
        </div>

        <!-- Dynamic Active Game Workspace -->
        <div id="gameWorkspace" class="glass-card p-6 md:p-8 rounded-3xl hidden space-y-6"></div>

        <!-- Leaderboard -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="text-lg font-bold text-amber-400 flex items-center justify-between">
                <span>🔥 Weekly Leaderboard Champions</span>
                <span class="text-xs text-slate-400 font-normal">Prize Pool: ₦100,000</span>
            </h3>
            <div class="space-y-2">
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">1. Tunde A. (Lagos)</span>
                    <span class="text-amber-400 font-extrabold">6,850 pts</span>
                </div>
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">2. Chidi K. (Abuja)</span>
                    <span class="text-amber-400 font-extrabold">5,920 pts</span>
                </div>
            </div>
        </div>
    </main>

    <!-- AUTHENTICATION MODAL -->
    <div id="authModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-card max-w-md w-full p-8 rounded-3xl space-y-6 gold-glow relative">
            <button onclick="closeAuthModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            <div class="text-center space-y-2">
                <div class="w-14 h-14 bg-amber-500/10 text-amber-400 rounded-2xl mx-auto flex items-center justify-center text-2xl font-bold border border-amber-500/30">🔐</div>
                <h3 class="text-2xl font-extrabold">Sign In / Register</h3>
                <p class="text-slate-400 text-sm">Save your scores and track your arcade progress.</p>
            </div>
            <form onsubmit="handleAuthSubmit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Username or Alias</label>
                    <input type="text" id="authUsername" required placeholder="e.g. LagosProGamer" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-amber-400 outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Password</label>
                    <input type="password" id="authPassword" required placeholder="••••••••" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-amber-400 outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Save & Access Arcade</button>
            </form>
        </div>
    </div>

    <!-- TOURNAMENT MODAL -->
    <div id="tournamentModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-card max-w-md w-full p-8 rounded-3xl space-y-6 gold-glow relative">
            <button onclick="closeTournamentModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            <div class="text-center space-y-2">
                <div class="w-14 h-14 bg-amber-500/10 text-amber-400 rounded-2xl mx-auto flex items-center justify-center text-2xl font-bold border border-amber-500/30">🏆</div>
                <h3 class="text-2xl font-extrabold">Join Weekly Cash Battle</h3>
                <p class="text-slate-400 text-sm">Entry fee is <strong class="text-amber-400">₦500</strong>. Secure your spot on the live leaderboard!</p>
            </div>
            <form onsubmit="handleTournamentEntry(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">WhatsApp / Phone Number</label>
                    <input type="tel" id="playerPhone" required placeholder="08030000000" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-amber-400 outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Pay ₦500 via Paystack</button>
            </form>
        </div>
    </div>

    <!-- PWA INSTALL APP BANNER -->
    <div id="installBanner" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm glass-card border border-amber-500/40 p-4 rounded-2xl shadow-2xl z-50 hidden flex items-center justify-between space-x-4 gold-glow">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-amber-500 text-slate-950 font-black flex items-center justify-center text-lg">📱</div>
            <div>
                <h4 class="text-xs font-extrabold text-white">Install NaijaArcade</h4>
                <p class="text-[11px] text-slate-400">Add to your home screen for instant gaming!</p>
            </div>
        </div>
        <div class="flex space-x-2">
            <button onclick="installApp()" class="bg-amber-500 text-slate-950 font-extrabold px-3 py-1.5 rounded-xl text-xs">Install</button>
            <button onclick="dismissInstall()" class="text-slate-400 hover:text-white text-xs px-2">✕</button>
        </div>
    </div>

    <!-- Footer -->
    <footer class="glass-card border-t border-amber-500/20 py-6 text-center text-xs text-slate-500">
        &copy; 2026 NaijaArcade. Play smart, win big.
    </footer>

    <!-- Game Scripts -->
    <script>
        const masterTrivia = [
            { q: "Which Nigerian city is known as the Centre of Excellence?", options: ["Abuja", "Lagos", "Port Harcourt", "Kano"], ans: 1 },
            { q: "Who released the global hit album 'Made in Lagos'?", options: ["Burna Boy", "Wizkid", "Davido", "Asake"], ans: 1 },
            { q: "What is the popular street term for serious trouble or drama?", options: ["Gbege", "Kere", "Fela", "Oshe"], ans: 0 },
            { q: "Which Nigerian national team won AFCON in South Africa in 2013?", options: ["Super Falcons", "Super Eagles", "Golden Eaglets", "Flying Eagles"], ans: 1 },
            { q: "In what year did Nigeria gain independence?", options: ["1914", "1960", "1963", "1999"], ans: 1 },
            { q: "Which Nigerian artist is famously known as 'OBO'?", options: ["Wizkid", "Davido", "Rema", "Burna Boy"], ans: 1 },
            { q: "What currency is officially used in Nigeria?", options: ["Cedis", "Dollars", "Naira", "Rand"], ans: 2 },
            { q: "Which state is famously called the 'Gateway State'?", options: ["Ogun", "Oyo", "Ondo", "Ekiti"], ans: 0 },
            { q: "Who directed the blockbuster Nigerian movie 'The Wedding Party'?", options: ["Kemi Adetiba", "Funke Akindele", "Niyi Akinmolayan", "Kunle Afolayan"], ans: 0 },
            { q: "What is the capital of Nigeria?", options: ["Lagos", "Abuja", "Ibadan", "Calabar"], ans: 1 }
        ];

        const masterGeography = [
            { q: "What is the capital of Rivers State?", options: ["Aba", "Port Harcourt", "Uyo", "Yenagoa"], ans: 1 },
            { q: "Which state has the slogan 'Heartbeat of the Nation'?", options: ["Delta", "Edo", "Anambra", "Cross River"], ans: 1 },
            { q: "What is the capital of Kaduna State?", options: ["Zaria", "Kaduna", "Kafanchan", "Kano"], ans: 1 },
            { q: "Which Nigerian state is the largest by land mass?", options: ["Lagos", "Niger", "Borno", "Kano"], ans: 1 },
            { q: "What is the capital of Enugu State?", options: ["Nsukka", "Enugu", "Awka", "Abakaliki"], ans: 1 }
        ];

        const masterFootball = [
            { q: "Who is Nigeria's all-time top goalscorer in international football?", options: ["Jay-Jay Okocha", "Rashidi Yekini", "Kanu Nwankwo", "Victor Osimhen"], ans: 1 },
            { q: "In which year did the Super Eagles win their first Olympic Gold in football?", options: ["1994", "1996", "2000", "2008"], ans: 1 },
            { q: "Which stadium is the home ground of the Super Eagles in Lagos?", options: ["Teslim Balogun Stadium", "Mobolaji Johnson Arena", "National Stadium Surulere", "All of the above"], ans: 3 },
            { q: "Who captained Nigeria to AFCON victory in 2013?", options: ["Vincent Enyeama", "Joseph Yobo", "John Obi Mikel", "Ahmed Musa"], ans: 1 }
        ];

        const pidginWords = [
            { word: "WAHALA", meaning: "trouble" },
            { word: "GBEDU", meaning: "music" },
            { word: "SHABI", meaning: "sure" },
            { word: "AJEBOTTER", meaning: "pampered" },
            { word: "YANGA", meaning: "praise" }
        ];

        function getDailyQuestions(masterArray) {
            const todayCode = new Date().toISOString().slice(0, 10);
            let seed = 0;
            for (let i = 0; i < todayCode.length; i++) seed += todayCode.charCodeAt(i);
            let shuffled = [...masterArray].sort((a, b) => (Math.sin(seed++) + 0.5) - 0.5);
            return shuffled.slice(0, 5);
        }

        let currentActiveQuestions = [];
        let currentQIndex = 0;
        let score = 0;
        let activeGameType = '';

        // Snake & Ladder State
        let snakePos = 1;
        const snakesAndLadders = { 4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 17: 7, 54: 34, 62: 19, 87: 24, 95: 75 };

        // Block Stacker State
        let towerHeight = 0;
        let blockWidth = 100;
        let stackInterval = null;

        window.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('naija_arcade_user');
            if (savedUser) updateNavUser(savedUser);
            
            const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
            document.getElementById('dailyDateBadge').innerText = "Daily Rotation: " + new Date().toLocaleDateString('en-US', options);

            setTimeout(() => {
                if (!localStorage.getItem('pwa_dismissed')) {
                    document.getElementById('installBanner').classList.remove('hidden');
                }
            }, 3000);
        });

        function updateNavUser(username) {
            document.getElementById('authNavArea').innerHTML = `
                <div class="flex items-center space-x-2 bg-slate-900 border border-amber-500/30 px-3 py-1.5 rounded-xl">
                    <span class="text-xs text-amber-400 font-bold">👤 ${username}</span>
                    <button onclick="logoutUser()" class="text-[10px] text-slate-400 hover:text-white underline">Logout</button>
                </div>
            `;
        }

        function logoutUser() {
            localStorage.removeItem('naija_arcade_user');
            location.reload();
        }

        function openAuthModal() { document.getElementById('authModal').classList.remove('hidden'); }
        function closeAuthModal() { document.getElementById('authModal').classList.add('hidden'); }
        function openTournamentModal() { document.getElementById('tournamentModal').classList.remove('hidden'); }
        function closeTournamentModal() { document.getElementById('tournamentModal').classList.add('hidden'); }

        function handleAuthSubmit(e) {
            e.preventDefault();
            const username = document.getElementById('authUsername').value;
            localStorage.setItem('naija_arcade_user', username);
            updateNavUser(username);
            closeAuthModal();
            alert(`Welcome back, ${username}! Your session is saved.`);
        }

        function launchGame(type) {
            activeGameType = type;
            currentQIndex = 0;
            score = 0;
            document.getElementById('gameHubGrid').classList.add('hidden');
            document.getElementById('gameWorkspace').classList.remove('hidden');
            window.scrollTo({ top: 200, behavior: 'smooth' });

            if (type === 'snake') {
                renderSnakeGame();
            } else if (type === 'blocks') {
                renderBlockGame();
            } else if (type === 'trivia') {
                currentActiveQuestions = getDailyQuestions(masterTrivia);
                renderQuizQuestion();
            } else if (type === 'geography') {
                currentActiveQuestions = getDailyQuestions(masterGeography);
                renderQuizQuestion();
            } else if (type === 'football') {
                currentActiveQuestions = getDailyQuestions(masterFootball);
                renderQuizQuestion();
            } else if (type === 'pidgin') {
                currentActiveQuestions = getDailyQuestions(pidginWords);
                renderPidginGame();
            } else if (type === 'reflex') {
                renderReflexGame();
            }
        }

        // --- SNAKE & LADDER LOGIC ---
        function renderSnakeGame() {
            snakePos = 1;
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">Naija Snake & Ladder</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <h3 class="text-2xl font-bold">Current Position: <span id="snakeTile" class="text-amber-400 font-extrabold text-3xl">1</span> / 100</h3>
                    <p class="text-slate-400 text-sm">Roll the die to climb ladders and avoid the snakes!</p>
                    <div id="diceDisplay" class="w-20 h-20 bg-slate-900 border border-amber-500/50 rounded-2xl mx-auto flex items-center justify-center text-4xl font-black text-amber-400 gold-glow">🎲</div>
                    <button onclick="rollDice()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Roll Dice 🎲</button>
                </div>
            `;
        }

        function rollDice() {
            const roll = Math.floor(Math.random() * 6) + 1;
            document.getElementById('diceDisplay').innerText = ['⚀','⚁','⚂','⚃','⚄','⚅'][roll-1];
            snakePos += roll;
            
            let message = `You rolled a ${roll}!`;
            if (snakesAndLadders[snakePos]) {
                const oldPos = snakePos;
                snakePos = snakesAndLadders[snakePos];
                if (snakePos > oldPos) message += ` 🎉 Yay! You climbed a ladder to ${snakePos}!`;
                else message += ` 🐍 Omo! A snake bit you down to ${snakePos}!`;
            }

            if (snakePos >= 100) {
                snakePos = 100;
                score += 500;
                document.getElementById('snakeTile').innerText = snakePos;
                alert('🏆 Congratulations! You won the Snake & Ladder game!');
                endGameScreen();
                return;
            }

            document.getElementById('snakeTile').innerText = snakePos;
            score += roll * 5;
        }

        // --- BLOCK BUILDER / STACKER LOGIC ---
        function renderBlockGame() {
            towerHeight = 0;
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">Sky-Tower Stacker</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <h3 class="text-xl font-bold">Tower Height: <span id="towerScore" class="text-amber-400 text-2xl">0</span> Meters</h3>
                    <div id="stackArea" class="relative h-64 bg-slate-900/80 rounded-2xl border border-slate-800 overflow-hidden flex flex-col-reverse items-center justify-start p-2">
                        <div id="movingBlock" class="w-32 h-8 bg-gradient-to-r from-amber-500 to-amber-300 rounded-lg shadow-lg absolute top-4 transition-all"></div>
                    </div>
                    <button onclick="dropBlock()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Drop Block 🏗️</button>
                </div>
            `;
            startBlockMovement();
        }

        let blockX = 0;
        let blockDir = 1;
        function startBlockMovement() {
            stackInterval = setInterval(() => {
                const block = document.getElementById('movingBlock');
                if (!block) return;
                blockX += blockDir * 4;
                if (blockX > 150 || blockX < -150) blockDir *= -1;
                block.style.transform = `translateX(${blockX}px)`;
            }, 25);
        }

        function dropBlock() {
            clearInterval(stackInterval);
            towerHeight += 1;
            score += 50;
            document.getElementById('towerScore').innerText = towerHeight;

            if (towerHeight >= 10) {
                alert('🏗️ Incredible! You successfully built a 10-story Lagos skyscraper!');
                endGameScreen();
                return;
            }
            startBlockMovement();
        }

        function renderQuizQuestion() {
            if (currentQIndex >= currentActiveQuestions.length) {
                endGameScreen();
                return;
            }
            const q = currentActiveQuestions[currentQIndex];
            let html = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">${activeGameType.toUpperCase()} — Q${currentQIndex + 1}/${currentActiveQuestions.length} (Daily Fresh)</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white">✕ Exit Game</button>
                </div>
                <h3 class="text-xl font-bold text-slate-100">${q.q}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
            `;
            q.options.forEach((opt, idx) => {
                html += `<button onclick="submitQuizAnswer(${idx}, ${q.ans})" class="text-left bg-slate-900 border border-slate-800 hover:border-amber-500/50 p-4 rounded-xl text-sm font-semibold transition active:scale-95">${String.fromCharCode(65 + idx)}. ${opt}</button>`;
            });
            html += `</div>`;
            document.getElementById('gameWorkspace').innerHTML = html;
        }

        function submitQuizAnswer(selected, correct) {
            if (selected === correct) score += 20;
            currentQIndex++;
            renderQuizQuestion();
        }

        function renderPidginGame() {
            if (currentQIndex >= currentActiveQuestions.length) {
                endGameScreen();
                return;
            }
            const item = currentActiveQuestions[currentQIndex];
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">Pidgin Scramble — Word ${currentQIndex + 1}/${currentActiveQuestions.length}</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <h3 class="text-2xl font-bold">Unscramble: <span class="text-amber-400 tracking-widest">${item.word}</span></h3>
                    <p class="text-slate-400 text-sm">Type the English meaning:</p>
                    <input type="text" id="pidginAns" placeholder="e.g. trouble" class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-center text-sm w-full max-w-xs mx-auto outline-none focus:border-amber-400 block">
                    <button onclick="checkPidgin('${item.meaning}')" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3 rounded-xl shadow-lg">Submit Answer</button>
                </div>
            `;
        }

        function checkPidgin(expected) {
            const val = document.getElementById('pidginAns').value.trim().toLowerCase();
            if (val === expected) {
                score += 25;
                alert('Correct! +25 Points');
            } else {
                alert(`Incorrect! It means '${expected}'.`);
            }
            currentQIndex++;
            renderPidginGame();
        }

        function renderReflexGame() {
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">Golden Coin Catcher</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <div id="reflexArea" class="relative h-64 bg-slate-900/60 rounded-2xl border border-slate-800 overflow-hidden flex items-center justify-center cursor-pointer">
                        <button onclick="tapCoin()" id="coinBtn" class="absolute w-14 h-14 bg-amber-400 rounded-full text-slate-950 font-bold text-xl shadow-lg flex items-center justify-center transition active:scale-90">🪙</button>
                    </div>
                    <div class="flex justify-between text-sm font-bold px-4">
                        <div>Score: <span id="refScore" class="text-amber-400">0</span></div>
                        <div>Time: <span id="refTime" class="text-rose-400">15</span>s</div>
                    </div>
                </div>
            `;
            startReflexTimer();
        }

        let refInterval = null;
        function startReflexTimer() {
            let t = 15;
            refInterval = setInterval(() => {
                t--;
                const timeEl = document.getElementById('refTime');
                if (timeEl) timeEl.innerText = t;
                moveCoinRandomly();
                if (t <= 0) {
                    clearInterval(refInterval);
                    endGameScreen();
                }
            }, 1000);
        }

        function moveCoinRandomly() {
            const btn = document.getElementById('coinBtn');
            if (!btn) return;
            const x = Math.floor(Math.random() * 250);
            const y = Math.floor(Math.random() * 150);
            btn.style.transform = `translate(${x - 125}px, ${y - 75}px)`;
        }

        function tapCoin() {
            score += 10;
            const sc = document.getElementById('refScore');
            if (sc) sc.innerText = score;
            moveCoinRandomly();
        }

        function endGameScreen() {
            clearInterval(refInterval);
            clearInterval(stackInterval);
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="text-center space-y-4 py-8">
                    <div class="text-4xl">🏆</div>
                    <h2 class="text-2xl font-extrabold text-amber-400">Game Over!</h2>
                    <p class="text-slate-300">Your Final Score: <strong class="text-white text-xl">${score} Points</strong></p>
                    <div class="flex justify-center gap-4 pt-2">
                        <button onclick="exitGame()" class="bg-slate-900 border border-slate-700 px-6 py-3 rounded-xl font-bold text-sm">Back to Games</button>
                        <button onclick="openTournamentModal()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3 rounded-xl shadow-lg">Enter Cash Tournament</button>
                    </div>
                </div>
            `;
        }

        function exitGame() {
            clearInterval(refInterval);
            clearInterval(stackInterval);
            document.getElementById('gameWorkspace').classList.add('hidden');
            document.getElementById('gameHubGrid').classList.remove('hidden');
        }

        function dismissInstall() {
            document.getElementById('installBanner').classList.add('hidden');
            localStorage.setItem('pwa_dismissed', 'true');
        }

        function installApp() {
            alert('To install NaijaArcade: Tap your browser menu (three dots at top right) and select "Add to Home Screen" or "Install App".');
            dismissInstall();
        }

        function handleTournamentEntry(e) {
            e.preventDefault();
            const phone = document.getElementById('playerPhone').value;
            alert(`Redirecting secure Paystack checkout for ₦500 tournament entry (${phone})...`);
            window.location.href = `https://checkout.paystack.com/?amount=50000`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
