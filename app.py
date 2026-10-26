import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaijaArcade v2.5 - Live Cash Tournament Hub</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #030712; color: #f8fafc; }
        .glass-panel { background: rgba(15, 23, 42, 0.98); backdrop-filter: blur(24px); border: 1px solid rgba(234, 179, 8, 0.4); box-shadow: 0 0 30px rgba(234, 179, 8, 0.15); }
        .retro-arcade-cabinet { background: #020617; border: 4px solid #eab308; box-shadow: inset 0 0 35px rgba(234, 179, 8, 0.25), 0 0 25px rgba(234, 179, 8, 0.3); }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-yellow-500 selection:text-slate-950">

    <!-- Navbar -->
    <header class="glass-panel border-b border-yellow-500/30 sticky top-0 z-50 px-4 md:px-6 py-3.5 flex justify-between items-center">
        <div class="flex items-center space-x-2.5 cursor-pointer" onclick="location.reload()">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-yellow-600 to-yellow-400 flex items-center justify-center font-black text-slate-950 text-xl shadow-lg">🕹️</div>
            <span class="text-xl md:text-2xl font-black tracking-wider bg-gradient-to-r from-yellow-400 via-amber-200 to-yellow-500 bg-clip-text text-transparent">NaijaArcade</span>
        </div>
        <div class="flex items-center space-x-2">
            <button onclick="openTournamentModal()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-3.5 py-2 rounded-xl text-xs shadow-lg hover:brightness-110 transition flex items-center space-x-1">
                <span>🏆 ₦500 Tournament</span>
            </button>
            <div id="authNavArea">
                <button onclick="openAuthModal()" class="bg-slate-900 border border-yellow-500/50 text-yellow-400 font-bold px-3.5 py-2 rounded-xl text-xs hover:bg-yellow-500/10 transition">Sign In</button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-4xl mx-auto px-4 py-8 w-full flex-grow space-y-8">
        
        <!-- Hero Banner -->
        <div class="glass-panel rounded-3xl p-8 text-center space-y-4 relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-48 h-48 bg-yellow-500/10 rounded-full blur-2xl pointer-events-none"></div>
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">Nigeria's #1 <span class="text-yellow-400">Cash Tournament</span> Arcade</h1>
            <p class="text-slate-400 text-sm md:text-base max-w-xl mx-auto">Play authentic board games, block puzzles, and cultural trivia head-to-head for real cash prizes.</p>
        </div>

        <!-- Game Selection Grid with Category Menu -->
        <div id="gameHubGrid" class="space-y-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <h2 class="text-xl font-extrabold text-yellow-400">🎮 Select Arcade Game</h2>
                
                <!-- Category Filter Menu -->
                <div class="flex flex-wrap gap-2 text-xs font-bold">
                    <button onclick="filterCategory('all', this)" class="cat-btn bg-yellow-500 text-slate-950 px-3 py-1.5 rounded-xl transition">All Games</button>
                    <button onclick="filterCategory('board', this)" class="cat-btn bg-slate-900 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-xl hover:border-yellow-500 transition">Board Classics</button>
                    <button onclick="filterCategory('action', this)" class="cat-btn bg-slate-900 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-xl hover:border-yellow-500 transition">Action & Puzzles</button>
                    <button onclick="filterCategory('trivia', this)" class="cat-btn bg-slate-900 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-xl hover:border-yellow-500 transition">Trivia & Culture</button>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="gamesContainer">
                <!-- Game 1: Board -->
                <div data-category="board" onclick="launchGame('snake')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3 border-yellow-400/50 bg-yellow-500/5">
                    <div class="w-12 h-12 bg-yellow-500/20 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🐍</div>
                    <h3 class="text-lg font-bold text-white">Naija Snake & Ladder</h3>
                    <p class="text-slate-400 text-xs">Authentic 10x10 arcade board box with live token hopping.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Now ➔</span>
                </div>
                <!-- Game 2: Action / Puzzle -->
                <div data-category="action" onclick="launchGame('blocks')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3 border-yellow-400/50 bg-yellow-500/5">
                    <div class="w-12 h-12 bg-yellow-500/20 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🧩</div>
                    <h3 class="text-lg font-bold text-white">Block-Fit Puzzle</h3>
                    <p class="text-slate-400 text-xs">Tetris-style grid box where square & L-blocks fit & clear rows!</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Now ➔</span>
                </div>
                <!-- Game 3: Trivia -->
                <div data-category="trivia" onclick="launchGame('trivia')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🧠</div>
                    <h3 class="text-lg font-bold text-white">Naija Mega Trivia</h3>
                    <p class="text-slate-400 text-xs">15 Expanded questions on Afrobeats & culture.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 4: Trivia -->
                <div data-category="trivia" onclick="launchGame('pidgin')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🗣️</div>
                    <h3 class="text-lg font-bold text-white">Pidgin Word Scramble</h3>
                    <p class="text-slate-400 text-xs">Decode street slang under time pressure.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 5: Action -->
                <div data-category="action" onclick="launchGame('reflex')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🪙</div>
                    <h3 class="text-lg font-bold text-white">Golden Coin Catcher</h3>
                    <p class="text-slate-400 text-xs">Fast 15-second reflex test against the clock.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 6: Trivia -->
                <div data-category="trivia" onclick="launchGame('geography')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">📍</div>
                    <h3 class="text-lg font-bold text-white">States & Capitals Quiz</h3>
                    <p class="text-slate-400 text-xs">15 Expanded state & capital questions.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 7: Trivia -->
                <div data-category="trivia" onclick="launchGame('football')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3 md:col-span-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">⚽</div>
                    <h3 class="text-lg font-bold text-white">Super Eagles & AFCON Quiz</h3>
                    <p class="text-slate-400 text-xs">15 Expanded football trivia challenges.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
            </div>
        </div>

        <!-- Dynamic Active Game Workspace -->
        <div id="gameWorkspace" class="glass-panel p-6 md:p-8 rounded-3xl hidden space-y-6"></div>

        <!-- Leaderboard -->
        <div class="glass-panel p-6 rounded-2xl space-y-4">
            <h3 class="text-lg font-bold text-yellow-400 flex items-center justify-between">
                <span>🔥 Weekly Leaderboard Champions</span>
                <span class="text-xs text-slate-400 font-normal">Prize Pool: ₦100,000</span>
            </h3>
            <div class="space-y-2">
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">1. Tunde A. (Lagos)</span>
                    <span class="text-yellow-400 font-extrabold">8,450 pts</span>
                </div>
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">2. Chidi K. (Abuja)</span>
                    <span class="text-yellow-400 font-extrabold">7,920 pts</span>
                </div>
            </div>
        </div>
    </main>

    <!-- AUTHENTICATION MODAL -->
    <div id="authModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-panel max-w-md w-full p-8 rounded-3xl space-y-6 relative">
            <button onclick="closeAuthModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            <div class="text-center space-y-2">
                <div class="w-14 h-14 bg-yellow-500/10 text-yellow-400 rounded-2xl mx-auto flex items-center justify-center text-2xl font-bold border border-yellow-500/30">🔐</div>
                <h3 class="text-2xl font-extrabold">Sign In / Register</h3>
                <p class="text-slate-400 text-sm">Save your scores and track your head-to-head matches.</p>
            </div>
            <form onsubmit="handleAuthSubmit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Username or Alias</label>
                    <input type="text" id="authUsername" required placeholder="e.g. LagosProGamer" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-yellow-400 outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Password</label>
                    <input type="password" id="authPassword" required placeholder="••••••••" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-yellow-400 outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Save & Access Arcade</button>
            </form>
        </div>
    </div>

    <!-- TOURNAMENT MATCHMAKING MODAL -->
    <div id="tournamentModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-panel max-w-md w-full p-8 rounded-3xl space-y-6 relative text-center">
            <button onclick="closeTournamentModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            <div id="matchmakingState" class="space-y-4">
                <div class="w-16 h-16 bg-yellow-500/10 text-yellow-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-yellow-500/30 animate-pulse">⚔️</div>
                <h3 class="text-2xl font-extrabold">Weekly Cash Tournament</h3>
                <p class="text-slate-400 text-sm">Entry fee: <strong class="text-yellow-400">₦500</strong>. Tap below to find your live opponent!</p>
                <button onclick="startMatchmaking()" class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Find Opponent & Pay ₦500</button>
            </div>
        </div>
    </div>

    <!-- PWA INSTALL APP BANNER -->
    <div id="installBanner" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm glass-panel border border-yellow-500/40 p-4 rounded-2xl shadow-2xl z-50 hidden flex items-center justify-between space-x-4">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-yellow-500 text-slate-950 font-black flex items-center justify-center text-lg">📱</div>
            <div>
                <h4 class="text-xs font-extrabold text-white">Install NaijaArcade</h4>
                <p class="text-[11px] text-slate-400">Add to home screen for instant gaming!</p>
            </div>
        </div>
        <div class="flex space-x-2">
            <button onclick="installApp()" class="bg-yellow-500 text-slate-950 font-extrabold px-3 py-1.5 rounded-xl text-xs">Install</button>
            <button onclick="dismissInstall()" class="text-slate-400 hover:text-white text-xs px-2">✕</button>
        </div>
    </div>

    <!-- Footer -->
    <footer class="glass-panel border-t border-yellow-500/20 py-6 text-center text-xs text-slate-500">
        &copy; 2026 NaijaArcade v2.5. Play smart, win big.
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
            { q: "What is the capital of Nigeria?", options: ["Lagos", "Abuja", "Ibadan", "Calabar"], ans: 1 },
            { q: "Which Nigerian singer popularized the term 'Buga'?", options: ["Kizz Daniel", "Tekno", "Fireboy", "Olamide"], ans: 0 },
            { q: "What is the longest river in Nigeria?", options: ["River Niger", "River Benue", "River Osun", "River Kaduna"], ans: 0 },
            { q: "Which ethnic group is mostly associated with the 'Atilogwu' dance?", options: ["Yoruba", "Igbo", "Hausa", "Ijaw"], ans: 1 },
            { q: "What does 'Wahala' mean in Nigerian Pidgin?", options: ["Joy", "Trouble", "Money", "Food"], ans: 1 },
            { q: "Which Nigerian stadium is the largest?", options: ["Teslim Balogun", "Moshood Abiola", "Godswill Akpabio", "National Stadium Surulere"], ans: 1 }
        ];

        const masterGeography = [
            { q: "What is the capital of Rivers State?", options: ["Aba", "Port Harcourt", "Uyo", "Yenagoa"], ans: 1 },
            { q: "Which state has the slogan 'Heartbeat of the Nation'?", options: ["Delta", "Edo", "Anambra", "Cross River"], ans: 1 },
            { q: "What is the capital of Kaduna State?", options: ["Zaria", "Kaduna", "Kafanchan", "Kano"], ans: 1 },
            { q: "Which Nigerian state is the largest by land mass?", options: ["Lagos", "Niger", "Borno", "Kano"], ans: 1 },
            { q: "What is the capital of Enugu State?", options: ["Nsukka", "Enugu", "Awka", "Abakaliki"], ans: 1 },
            { q: "Which state is known as the 'Coal City State'?", options: ["Enugu", "Ebonyi", "Imo", "Abia"], ans: 0 },
            { q: "What is the capital of Delta State?", options: ["Warri", "Asaba", "Sapele", "Ughelli"], ans: 1 },
            { q: "Which state is called the 'Land of Promise'?", options: ["Akwa Ibom", "Cross River", "Rivers", "Bayelsa"], ans: 0 },
            { q: "What is the capital of Ondo State?", options: ["Owo", "Akure", "Ondo City", "Ikare"], ans: 1 },
            { q: "Which state has the nickname 'Pace Setter State'?", options: ["Oyo", "Ogun", "Osun", "Ekiti"], ans: 0 },
            { q: "What is the capital of Plateau State?", options: ["Jos", "Langtang", "Pankshin", "Bukuru"], ans: 0 },
            { q: "Which state is known as the 'Sunshine State'?", options: ["Ondo", "Ekiti", "Kwara", "Kogi"], ans: 0 },
            { q: "What is the capital of Sokoto State?", options: ["Wurno", "Sokoto", "Tambuwal", "Gwadabawa"], ans: 1 },
            { q: "Which state is the 'Home of Peace'?", options: ["Plateau", "Benue", "Nasarawa", "Taraba"], ans: 0 },
            { q: "What is the capital of Borno State?", options: ["Biu", "Maiduguri", "Gwoza", "Dikwa"], ans: 1 }
        ];

        const masterFootball = [
            { q: "Who is Nigeria's all-time top goalscorer in international football?", options: ["Jay-Jay Okocha", "Rashidi Yekini", "Kanu Nwankwo", "Victor Osimhen"], ans: 1 },
            { q: "In which year did the Super Eagles win their first Olympic Gold in football?", options: ["1994", "1996", "2000", "2008"], ans: 1 },
            { q: "Which stadium is the home ground of the Super Eagles in Lagos?", options: ["Teslim Balogun Stadium", "Mobolaji Johnson Arena", "National Stadium Surulere", "All of the above"], ans: 3 },
            { q: "Who captained Nigeria to AFCON victory in 2013?", options: ["Vincent Enyeama", "Joseph Yobo", "John Obi Mikel", "Ahmed Musa"], ans: 1 },
            { q: "Which Nigerian club won the CAF Champions League in 2003 and 2004?", options: ["Enyimba FC", "Shooting Stars", "Rangers International", "Kano Pillars"], ans: 0 },
            { q: "Who won the African Footballer of the Year in 1999?", options: ["Kanu Nwankwo", "Sunday Oliseh", "Victor Ikpeba", "Austin Okocha"], ans: 0 },
            { q: "Which Nigerian female footballer has won African Women Footballer of the Year a record number of times?", options: ["Asisat Oshoala", "Perpetua Nkwocha", "Cynthia Uwak", "Desire Oparanozie"], ans: 0 },
            { q: "In which World Cup did Nigeria reach the Round of 16 for the first time?", options: ["1990", "1994", "1998", "2014"], ans: 1 },
            { q: "Who scored Nigeria's first-ever World Cup goal in 1994?", options: ["Rashidi Yekini", "Daniel Amokachi", "Emmanuel Amuneke", "Finidi George"], ans: 0 },
            { q: "Which coach led Nigeria to the 1994 AFCON and World Cup?", options: ["Clemens Westerhof", "Boniface Chukwu", "Shaibu Amodu", "Stephen Keshi"], ans: 0 },
            { q: "What is the nickname of the Nigerian National Women's Football Team?", options: ["Super Falcons", "Super Tigress", "Golden Queens", "Falconets"], ans: 0 },
            { q: "Which Nigerian player won the Premier League with Chelsea?", options: ["John Obi Mikel", "Victor Moses", "Both of the above", "None"], ans: 2 },
            { q: "In what year did Nigeria win the FIFA U-17 World Cup for the first time?", options: ["1985", "1993", "2007", "2013"], ans: 0 },
            { q: "Who scored the winning goal in the 2013 AFCON final for Nigeria?", options: ["Sunday Mba", "Emmanuel Emenike", "Victor Moses", "Ahmed Musa"], ans: 0 },
            { q: "Which Nigerian goalkeeper famously saved penalties at the 2013 AFCON?", options: ["Vincent Enyeama", "Ike Shorunmu", "Peter Rufai", "Daniel Akpeyi"], ans: 0 }
        ];

        const pidginWords = [
            { word: "WAHALA", meaning: "trouble" },
            { word: "GBEDU", meaning: "music" },
            { word: "SHABI", meaning: "sure" },
            { word: "AJEBOTTER", meaning: "pampered" },
            { word: "YANGA", meaning: "praise" },
            { word: "OGENDE", meaning: "money" },
            { word: "JAPA", meaning: "run" }
        ];

        function filterCategory(cat, btn) {
            document.querySelectorAll('.cat-btn').forEach(b => {
                b.className = "cat-btn bg-slate-900 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-xl hover:border-yellow-500 transition";
            });
            btn.className = "cat-btn bg-yellow-500 text-slate-950 px-3 py-1.5 rounded-xl transition font-bold";

            document.querySelectorAll('.game-card').forEach(card => {
                if (cat === 'all' || card.getAttribute('data-category') === cat) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function getDailyQuestions(masterArray) {
            const todayCode = new Date().toISOString().slice(0, 10);
            let seed = 0;
            for (let i = 0; i < todayCode.length; i++) seed += todayCode.charCodeAt(i);
            let shuffled = [...masterArray].sort((a, b) => (Math.sin(seed++) + 0.5) - 0.5);
            return shuffled.slice(0, 10);
        }

        let currentActiveQuestions = [];
        let currentQIndex = 0;
        let score = 0;
        let activeGameType = '';
        let quizTimerInterval = null;
        let timeLeft = 20;

        let snakePos = 1;
        const snakesAndLadders = { 4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 17: 7, 54: 34, 62: 19, 87: 24, 95: 75 };

        let tetrisGrid = Array(12).fill().map(() => Array(8).fill(0));
        let tetrisScore = 0;
        const tetrisShapes = [
            { name: "Square Block ◼️", color: "bg-yellow-400", shape: [[1,1],[1,1]] },
            { name: "L-Block 📐", color: "bg-amber-600", shape: [[1,0],[1,0],[1,1]] },
            { name: "T-Block ➕", color: "bg-purple-500", shape: [[0,1,0],[1,1,1]] }
        ];
        let currentShapeIdx = 0;

        window.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('naija_arcade_user');
            if (savedUser) updateNavUser(savedUser);

            setTimeout(() => {
                if (!localStorage.getItem('pwa_dismissed')) {
                    document.getElementById('installBanner').classList.remove('hidden');
                }
            }, 3000);
        });

        function updateNavUser(username) {
            document.getElementById('authNavArea').innerHTML = `
                <div class="flex items-center space-x-1.5 bg-slate-900 border border-yellow-500/30 px-3 py-2 rounded-xl">
                    <span class="text-xs text-yellow-400 font-bold">👤 ${username}</span>
                    <button onclick="logoutUser()" class="text-[10px] text-slate-400 hover:text-white underline ml-1">Out</button>
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
            alert(`Welcome back, ${username}! Session saved.`);
        }

        function startMatchmaking() {
            const stateBox = document.getElementById('matchmakingState');
            stateBox.innerHTML = `
                <div class="w-16 h-16 bg-yellow-500/10 text-yellow-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-yellow-500/30 animate-spin">🔍</div>
                <h3 class="text-2xl font-extrabold">Searching for Opponent...</h3>
                <p class="text-slate-400 text-sm">Matching you with another player in Nigeria...</p>
            `;

            setTimeout(() => {
                const opponents = ["Chidi_Pro (Abuja)", "LagosChamp99", "IbadanBoy_01", "KanoGamer22", "PortHarcourtKing"];
                const matchedOpp = opponents[Math.floor(Math.random() * opponents.length)];
                stateBox.innerHTML = `
                    <div class="w-16 h-16 bg-emerald-500/10 text-emerald-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-emerald-500/30">⚔️</div>
                    <h3 class="text-2xl font-extrabold text-emerald-400">Opponent Found!</h3>
                    <p class="text-slate-300 text-sm">Matched against <strong class="text-white">${matchedOpp}</strong>!</p>
                    <button onclick="confirmTournamentPayment('${matchedOpp}')" class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition mt-2">Proceed to Paystack ₦500</button>
                `;
            }, 2500);
        }

        function confirmTournamentPayment(opponent) {
            alert(`Redirecting to Paystack payment page for tournament match against ${opponent}...`);
            window.location.href = "https://paystack.com";
        }

        function launchGame(type) {
            activeGameType = type;
            currentQIndex = 0;
            score = 0;
            document.getElementById('gameHubGrid').classList.add('hidden');
            document.getElementById('gameWorkspace').classList.remove('hidden');
            window.scrollTo({ top: 200, behavior: 'smooth' });

            if (type === 'snake') {
                renderSnakeBoard();
            } else if (type === 'blocks') {
                renderTetrisPuzzle();
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

        function renderSnakeBoard() {
            snakePos = 1;
            drawSnakeGrid();
        }

        function drawSnakeGrid() {
            let boardHTML = `
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest flex items-center gap-1.5">🐍 Naija Snake & Ladder Cabinet</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <!-- RETRO ARCADE CABINET CONTAINER -->
                <div class="retro-arcade-cabinet p-4 rounded-3xl max-w-md mx-auto space-y-4">
                    <div class="flex justify-between text-[11px] font-bold text-yellow-400 px-1 border-b border-yellow-500/20 pb-2">
                        <span>🪜 LADDERS: 4➔14, 9➔31, 28➔84</span>
                        <span>🐍 SNAKES: 95➔75, 62➔19</span>
                    </div>
                    <div class="grid grid-cols-10 gap-1.5 bg-black p-3 rounded-2xl border-2 border-yellow-500/45 aspect-square">
            `;
            for (let r = 10; r >= 1; r--) {
                let rowTiles = [];
                for (let c = 1; c <= 10; c++) {
                    let tileNum = (r % 2 === 0) ? ((r - 1) * 10 + c) : (r * 10 - (c - 1));
                    rowTiles.push(tileNum);
                }
                if (r % 2 !== 0) rowTiles.reverse();
                rowTiles.forEach(t => {
                    let isPlayerHere = (t === snakePos);
                    let badge = isPlayerHere ? '<div class="w-6 h-6 bg-yellow-400 text-slate-950 rounded-full font-black text-[10px] flex items-center justify-center shadow-lg animate-bounce">🟢</div>' : `<span class="text-[10px] text-yellow-500/70 font-bold">${t}</span>`;
                    let hasLadder = snakesAndLadders[t] && snakesAndLadders[t] > t;
                    let hasSnake = snakesAndLadders[t] && snakesAndLadders[t] < t;
                    let extraClass = hasLadder ? 'border-emerald-500 bg-emerald-950/80 shadow-md' : (hasSnake ? 'border-rose-500 bg-rose-950/80 shadow-md' : 'border-slate-800 bg-slate-900/90');
                    boardHTML += `<div class="rounded-md flex items-center justify-center border ${extraClass} relative h-7 md:h-10">${badge}</div>`;
                });
            }
            boardHTML += `</div>
                </div>
                <div class="text-center space-y-3 pt-2">
                    <div id="diceResult" class="text-lg font-bold text-yellow-400">Current Tile: ${snakePos} / 100</div>
                    <button id="rollBtn" onclick="rollStepDice()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Roll Dice 🎲</button>
                </div>
            `;
            document.getElementById('gameWorkspace').innerHTML = boardHTML;
        }

        function rollStepDice() {
            const roll = Math.floor(Math.random() * 6) + 1;
            document.getElementById('rollBtn').disabled = true;
            let targetPos = snakePos + roll;
            if (targetPos > 100) targetPos = 100;

            let currentStep = snakePos;
            let hopInterval = setInterval(() => {
                if (currentStep < targetPos) {
                    currentStep++;
                    snakePos = currentStep;
                    drawSnakeGrid();
                } else {
                    clearInterval(hopInterval);
                    if (snakesAndLadders[snakePos]) {
                        let old = snakePos;
                        snakePos = snakesAndLadders[snakePos];
                        setTimeout(() => {
                            drawSnakeGrid();
                            alert(snakePos > old ? "🪜 You climbed a ladder!" : "🐍 Omo! A snake bit you!");
                            if (snakePos >= 100) {
                                alert("🏆 You won the match!");
                                endGameScreen();
                            }
                        }, 300);
                    } else if (snakePos >= 100) {
                        alert("🏆 You reached Tile 100 and won!");
                        endGameScreen();
                    } else {
                        const rb = document.getElementById('rollBtn');
                        if(rb) rb.disabled = false;
                    }
                }
            }, 250);
        }

        function renderTetrisPuzzle() {
            tetrisGrid = Array(12).fill().map(() => Array(8).fill(0));
            tetrisScore = 0;
            currentShapeIdx = Math.floor(Math.random() * tetrisShapes.length);
            drawTetrisBoard();
        }

        function drawTetrisBoard() {
            let shapeObj = tetrisShapes[currentShapeIdx];
            let html = `
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest flex items-center gap-1.5">🧩 Block-Fit Arcade Cabinet</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <div class="text-center space-y-4">
                    <div class="text-sm font-bold">Puzzle Score: <span id="tetrisScoreVal" class="text-yellow-400 text-xl">${tetrisScore}</span> pts</div>
                    
                    <!-- RETRO ARCADE CABINET CONTAINER -->
                    <div class="retro-arcade-cabinet p-4 rounded-3xl max-w-xs mx-auto space-y-3">
                        <div class="text-xs text-slate-300 font-semibold">Incoming Shape: <strong class="text-yellow-400">${shapeObj.name}</strong></div>
                        <div class="flex justify-center items-center gap-2 h-14 bg-black rounded-2xl border-2 border-yellow-500/40">
            `;
            
            shapeObj.shape.forEach(row => {
                row.forEach(cell => {
                    let activeCol = cell === 1 ? shapeObj.color + ' shadow-md scale-95 rounded' : 'opacity-0';
                    html += `<div class="w-4 h-4 ${activeCol}"></div>`;
                });
            });

            html += `       </div>

                        <!-- Visual 12x8 Grid Box -->
                        <div class="grid grid-cols-8 gap-1 bg-black p-3 rounded-2xl border-2 border-yellow-500/40">
            `;

            for (let r = 0; r < 12; r++) {
                for (let c = 0; c < 8; c++) {
                    let isFilled = tetrisGrid[r][c] === 1;
                    let tileColor = isFilled ? 'bg-yellow-400 border-yellow-300 shadow-md scale-95' : 'bg-slate-900/90 border-slate-800';
                    html += `<div class="w-7 h-7 rounded border ${tileColor} transition-all"></div>`;
                }
            }

            html += `</div>
                    </div>
                    <button onclick="dropTetrisShape()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Drop & Fit Piece 🔽</button>
                </div>
            `;
            document.getElementById('gameWorkspace').innerHTML = html;
        }

        function dropTetrisShape() {
            let placed = false;
            for (let r = 11; r >= 0; r--) {
                let slotsAvailable = 0;
                for (let c = 0; c < 8; c++) {
                    if (tetrisGrid[r][c] === 0) slotsAvailable++;
                }
                if (slotsAvailable >= 2) {
                    tetrisGrid[r][2] = 1;
                    tetrisGrid[r][3] = 1;
                    placed = true;
                    break;
                }
            }

            tetrisScore += 180;
            currentShapeIdx = (currentShapeIdx + 1) % tetrisShapes.length;
            drawTetrisBoard();

            if (tetrisScore >= 900) {
                alert("🏆 Magnificent! Rows cleared perfectly! You defeated your opponent!");
                endGameScreen();
            }
        }

        function renderQuizQuestion() {
            if (currentQIndex >= currentActiveQuestions.length) {
                endGameScreen();
                return;
            }
            timeLeft = 20;
            clearInterval(quizTimerInterval);
            
            const q = currentActiveQuestions[currentQIndex];
            let html = `
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest">${activeGameType.toUpperCase()} — Q${currentQIndex + 1}/${currentActiveQuestions.length}</span>
                    <span class="text-xs text-rose-400 font-bold">⏱️ <span id="quizTimer">20</span>s</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <h3 class="text-xl font-bold text-slate-100">${q.q}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
            `;
            q.options.forEach((opt, idx) => {
                html += `<button onclick="submitQuizAnswer(${idx}, ${q.ans})" class="text-left bg-slate-900 border border-slate-800 hover:border-yellow-500/50 p-4 rounded-xl text-sm font-semibold transition active:scale-95">${String.fromCharCode(65 + idx)}. ${opt}</button>`;
            });
            html += `</div>`;
            document.getElementById('gameWorkspace').innerHTML = html;

            quizTimerInterval = setInterval(() => {
                timeLeft--;
                const tEl = document.getElementById('quizTimer');
                if (tEl) tEl.innerText = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(quizTimerInterval);
                    alert("⏰ Time's up!");
                    currentQIndex++;
                    renderQuizQuestion();
                }
            }, 1000);
        }

        function submitQuizAnswer(selected, correct) {
            clearInterval(quizTimerInterval);
            if (selected === correct) score += 25;
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
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest">Pidgin Scramble — Word ${currentQIndex + 1}/${currentActiveQuestions.length}</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <h3 class="text-2xl font-bold">Unscramble: <span class="text-yellow-400 tracking-widest">${item.word}</span></h3>
                    <p class="text-slate-400 text-sm">Type English meaning:</p>
                    <input type="text" id="pidginAns" placeholder="e.g. trouble" class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-center text-sm w-full max-w-xs mx-auto outline-none focus:border-yellow-400 block">
                    <button onclick="checkPidgin('${item.meaning}')" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3.5 rounded-xl shadow-lg">Submit Answer</button>
                </div>
            `;
        }

        function checkPidgin(expected) {
            const val = document.getElementById('pidginAns').value.trim().toLowerCase();
            if (val === expected) {
                score += 30;
                alert('Correct! +30 Points');
            } else {
                alert(`Incorrect! It means '${expected}'.`);
            }
            currentQIndex++;
            renderPidginGame();
        }

        function renderReflexGame() {
            document.getElementById('gameWorkspace').innerHTML = `
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest">Golden Coin Catcher</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <div class="text-center space-y-4 py-4">
                    <div id="reflexArea" class="relative h-64 bg-slate-900/60 rounded-2xl border border-yellow-500/20 overflow-hidden flex items-center justify-center cursor-pointer">
                        <button onclick="tapCoin()" id="coinBtn" class="absolute w-14 h-14 bg-yellow-400 rounded-full text-slate-950 font-bold text-xl shadow-lg flex items-center justify-center transition active:scale-90">🪙</button>
                    </div>
                    <div class="flex justify-between text-sm font-bold px-4">
                        <div>Score: <span id="refScore" class="text-yellow-400">0</span></div>
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
            score += 15;
            const sc = document.getElementById('refScore');
            if (sc) sc.innerText = score;
            moveCoinRandomly();
        }

        function endGameScreen() {
            clearInterval(refInterval);
            clearInterval(quizTimerInterval);
            
            const opponentScore = Math.floor(Math.random() * 150) + 100;
            const userWon = score >= opponentScore;

            document.getElementById('gameWorkspace').innerHTML = `
                <div class="text-center space-y-4 py-8">
                    <div class="text-4xl">${userWon ? '🏆' : '💀'}</div>
                    <h2 class="text-2xl font-extrabold ${userWon ? 'text-yellow-400' : 'text-rose-400'}">${userWon ? 'Match Won!' : 'Opponent Won!'}</h2>
                    <p class="text-slate-300">Your Score: <strong class="text-white">${score}</strong> vs Opponent: <strong class="text-slate-400">${opponentScore}</strong></p>
                    <div class="flex justify-center gap-4 pt-2">
                        <button onclick="exitGame()" class="bg-slate-900 border border-slate-700 px-6 py-3.5 rounded-xl font-bold text-sm">Back to Games</button>
                        <button onclick="openTournamentModal()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3.5 rounded-xl shadow-lg">Rematch Tournament</button>
                    </div>
                </div>
            `;
        }

        function exitGame() {
            clearInterval(refInterval);
            clearInterval(quizTimerInterval);
            document.getElementById('gameWorkspace').classList.add('hidden');
            document.getElementById('gameHubGrid').classList.remove('hidden');
        }

        function dismissInstall() {
            document.getElementById('installBanner').classList.add('hidden');
            localStorage.setItem('pwa_dismissed', 'true');
        }

        function installApp() {
            alert('To install NaijaArcade: Tap your browser menu (three dots at top right) and select "Add to Home Screen".');
            dismissInstall();
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