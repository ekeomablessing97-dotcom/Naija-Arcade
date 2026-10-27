import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Web App Manifest Route for Mobile PWA Support
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "NaijaArcade",
        "short_name": "NaijaArcade",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#030712",
        "theme_color": "#eab308",
        "description": "Nigeria's #1 Cash Tournament Arcade. Survive the Lagos hustle, play authentic board games, and win cash prizes.",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/3408/3408506.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    })

# Service Worker Route for Caching & Offline Support
@app.route('/sw.js')
def service_worker():
    sw_code = """
    self.addEventListener('install', (e) => {
        console.log('NaijaArcade Service Worker Installed');
    });
    self.addEventListener('fetch', (e) => {
        e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    });
    """
    return sw_code, 200, {'Content-Type': 'application/javascript'}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaijaArcade v3.2 - Lagos Hustle & Cash Tournament Hub</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#eab308">
    <!-- Tailwind CSS -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <!-- Paystack Inline JS SDK -->
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #030712; color: #f8fafc; }
        .glass-panel { background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(24px); border: 1px solid rgba(234, 179, 8, 0.4); box-shadow: 0 0 30px rgba(234, 179, 8, 0.15); }
        .wooden-board { background: linear-gradient(135deg, #78350f, #451a03); border: 8px solid #292524; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
        .neon-glow { text-shadow: 0 0 15px rgba(234, 179, 8, 0.6); }
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
            <button onclick="openTournamentModal()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-3.5 py-2 rounded-xl text-xs shadow-lg hover:brightness-110 transition flex items-center space-x-1 animate-pulse">
                <span>🏆 Tournaments</span>
            </button>
            <div id="authNavArea">
                <button onclick="openAuthModal()" class="bg-slate-900 border border-yellow-500/50 text-yellow-400 font-bold px-3.5 py-2 rounded-xl text-xs hover:bg-yellow-500/10 transition">Sign In</button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-4xl mx-auto px-4 py-8 w-full flex-grow space-y-8">
        
        <!-- LAGOS HUSTLE CAREER STATUS BAR -->
        <div class="glass-panel rounded-3xl p-5 md:p-6 border-l-4 border-yellow-400 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-yellow-500/20 text-yellow-400 rounded-2xl flex items-center justify-center text-2xl font-bold border border-yellow-500/40">🇳🇬</div>
                <div>
                    <div class="text-xs uppercase tracking-widest text-slate-400 font-bold">Lagos Hustle Status</div>
                    <div id="playerStatusRank" class="text-lg font-extrabold text-yellow-400">Mainland Rookie (Shomolu)</div>
                </div>
            </div>
            <div class="flex items-center gap-4 bg-slate-900/90 px-4 py-3 rounded-2xl border border-slate-800 text-xs">
                <div>
                    <div class="text-slate-400">Virtual Rent Due:</div>
                    <div class="text-rose-400 font-bold">₦45,000 (3 Days Left)</div>
                </div>
                <div class="h-8 w-px bg-slate-800"></div>
                <div>
                    <div class="text-slate-400">Hustle Wallet:</div>
                    <div id="hustleWallet" class="text-yellow-400 font-extrabold text-sm">₦1,250</div>
                </div>
            </div>
        </div>

        <!-- Hero Banner -->
        <div class="glass-panel rounded-3xl p-8 text-center space-y-4 relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-48 h-48 bg-yellow-500/10 rounded-full blur-2xl pointer-events-none"></div>
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight neon-glow">Survive the <span class="text-yellow-400">Lagos Hustle</span> & Win Big</h1>
            <p class="text-slate-400 text-sm md:text-base max-w-xl mx-auto">Play free practice games, select tournament stakes from ₦500 to ₦2,000, or battle with ₦100 mini-stakes!</p>
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
                    <p class="text-slate-400 text-xs">Authentic 10x10 wooden arcade board. Free Practice & Rent Grinding.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 2: Action / Puzzle with Mini-Stake Option -->
                <div data-category="action" class="game-card glass-panel p-6 rounded-2xl space-y-3 border-yellow-400/50 bg-yellow-500/5">
                    <div class="w-12 h-12 bg-yellow-500/20 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🧩</div>
                    <h3 class="text-lg font-bold text-white">Block-Fit Puzzle</h3>
                    <p class="text-slate-400 text-xs">Classic wooden grid box. Choose free practice or ₦100 mini-stake battle!</p>
                    <div class="flex gap-2 pt-1">
                        <button onclick="launchGame('blocks')" class="flex-1 bg-slate-900 border border-yellow-500/50 text-yellow-400 font-bold py-1.5 rounded-lg text-xs hover:bg-yellow-500/10 transition">Free Play</button>
                        <button onclick="launchStakeGame('Block-Fit', 100)" class="flex-1 bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-1.5 rounded-lg text-xs hover:brightness-110 transition">₦100 Stake ⚡</button>
                    </div>
                </div>
                <!-- Game 3: Trivia -->
                <div data-category="trivia" onclick="launchGame('trivia')" class="game-card glass-panel p-6 rounded-2xl cursor-pointer hover:border-yellow-400 transition transform hover:-translate-y-1 space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🧠</div>
                    <h3 class="text-lg font-bold text-white">Naija Mega Trivia</h3>
                    <p class="text-slate-400 text-xs">15 Expanded questions on Afrobeats & culture.</p>
                    <span class="inline-block text-xs text-yellow-400 font-bold bg-yellow-500/10 px-3 py-1 rounded-full">Play Free ➔</span>
                </div>
                <!-- Game 4: Trivia with Mini-Stake Option -->
                <div data-category="trivia" class="game-card glass-panel p-6 rounded-2xl space-y-3">
                    <div class="w-12 h-12 bg-yellow-500/10 text-yellow-400 rounded-xl flex items-center justify-center text-2xl border border-yellow-500/30">🗣️</div>
                    <h3 class="text-lg font-bold text-white">Pidgin Word Scramble</h3>
                    <p class="text-slate-400 text-xs">Decode street slang. Free or ₦200 mini-stake battle.</p>
                    <div class="flex gap-2 pt-1">
                        <button onclick="launchGame('pidgin')" class="flex-1 bg-slate-900 border border-slate-700 text-slate-300 font-bold py-1.5 rounded-lg text-xs hover:border-yellow-500 transition">Free Play</button>
                        <button onclick="launchStakeGame('Pidgin Scramble', 200)" class="flex-1 bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-1.5 rounded-lg text-xs hover:brightness-110 transition">₦200 Stake ⚡</button>
                    </div>
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
                    <span class="font-semibold text-slate-200">1. Tunde A. (Lagos Mainland)</span>
                    <span class="text-yellow-400 font-extrabold">8,450 pts</span>
                </div>
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">2. Chidi K. (Abuja VIP)</span>
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
                <p class="text-slate-400 text-sm">Save your Lagos career hustle and tournament earnings.</p>
            </div>
            <form onsubmit="handleAuthSubmit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Username or Alias</label>
                    <input type="text" id="authUsername" required placeholder="e.g. MainlandHustler" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-yellow-400 outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Password</label>
                    <input type="password" id="authPassword" required placeholder="••••••••" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-yellow-400 outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Start Your Hustle</button>
            </form>
        </div>
    </div>

    <!-- TOURNAMENTS MODAL WITH MULTI-TIER STAKES (500, 1000, 1500, 2000) -->
    <div id="tournamentModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-panel max-w-md w-full p-8 rounded-3xl space-y-6 relative text-center">
            <button onclick="closeTournamentModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            
            <div class="space-y-4" id="tournamentModalContent">
                <div class="w-16 h-16 bg-yellow-500/10 text-yellow-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-yellow-500/30">🏆</div>
                <h3 class="text-2xl font-extrabold">Select Tournament Stake</h3>
                <p class="text-slate-400 text-sm">Choose your entry tier to enter head-to-head cash battles:</p>
                
                <!-- Stake Selection Grid -->
                <div class="grid grid-cols-2 gap-3">
                    <button onclick="startMatchmaking(500)" class="bg-slate-900 border border-yellow-500/40 hover:border-yellow-400 p-3.5 rounded-2xl text-center transition group">
                        <div class="text-xs text-slate-400">Entry Fee</div>
                        <div class="text-lg font-black text-yellow-400">₦500</div>
                        <div class="text-[10px] text-emerald-400 mt-1">Win ₦1,000</div>
                    </button>
                    <button onclick="startMatchmaking(1000)" class="bg-slate-900 border border-yellow-500/40 hover:border-yellow-400 p-3.5 rounded-2xl text-center transition group">
                        <div class="text-xs text-slate-400">Entry Fee</div>
                        <div class="text-lg font-black text-yellow-400">₦1,000</div>
                        <div class="text-[10px] text-emerald-400 mt-1">Win ₦2,000</div>
                    </button>
                    <button onclick="startMatchmaking(1500)" class="bg-slate-900 border border-yellow-500/40 hover:border-yellow-400 p-3.5 rounded-2xl text-center transition group">
                        <div class="text-xs text-slate-400">Entry Fee</div>
                        <div class="text-lg font-black text-yellow-400">₦1,500</div>
                        <div class="text-[10px] text-emerald-400 mt-1">Win ₦3,000</div>
                    </button>
                    <button onclick="startMatchmaking(2000)" class="bg-slate-900 border border-yellow-500/40 hover:border-yellow-400 p-3.5 rounded-2xl text-center transition group">
                        <div class="text-xs text-slate-400">Entry Fee</div>
                        <div class="text-lg font-black text-yellow-400">₦2,000</div>
                        <div class="text-[10px] text-emerald-400 mt-1">Win ₦4,000</div>
                    </button>
                </div>

                <!-- Sponsored Free-Roll Option -->
                <div class="bg-slate-900/90 border border-emerald-500/40 p-3.5 rounded-2xl text-left space-y-1">
                    <div class="flex justify-between items-center">
                        <span class="font-extrabold text-xs text-emerald-400">🎁 Daily Sponsored Free-Roll</span>
                        <span class="text-[10px] text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded-full">₦10,000 Pot</span>
                    </div>
                    <button onclick="startFreeRollMatch()" class="w-full bg-emerald-500 text-slate-950 font-extrabold py-2 rounded-xl text-xs shadow-lg hover:brightness-110 transition mt-1">Join Free-Roll (Free)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="glass-panel border-t border-yellow-500/20 py-6 text-center text-xs text-slate-500">
        &copy; 2026 NaijaArcade v3.2. Lagos Hustle Edition. Play smart, win big.
    </footer>

    <!-- Game Scripts -->
    <script>
        // Register Service Worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW error:', err));
        }

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
        let hustleWallet = 1250;
        let activeGameType = '';
        let currentStakeAmount = 0;
        let quizTimerInterval = null;
        let timeLeft = 20;

        let snakePos = 1;
        const snakesAndLadders = { 4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 17: 7, 54: 34, 62: 19, 87: 24, 95: 75 };

        let tetrisGrid = Array(10).fill().map(() => Array(10).fill(0));
        let tetrisScore = 0;
        const tetrisShapes = [
            { name: "Square ◼️", color: "bg-amber-500", shape: [[1,1],[1,1]] },
            { name: "L-Block 📐", color: "bg-red-500", shape: [[1,0],[1,0],[1,1]] },
            { name: "T-Block ➕", color: "bg-indigo-500", shape: [[0,1,0],[1,1,1]] },
            { name: "Line 📏", color: "bg-emerald-500", shape: [[1,1,1,1]] }
        ];
        let currentShapeIdx = 0;

        window.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('naija_arcade_user');
            if (savedUser) updateNavUser(savedUser);
            const savedWallet = localStorage.getItem('naija_wallet');
            if (savedWallet) {
                hustleWallet = parseInt(savedWallet);
                document.getElementById('hustleWallet').innerText = '₦' + hustleWallet.toLocaleString();
            }
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
            alert(`Welcome to the hustle, ${username}! Let's make that money.`);
        }

        function startMatchmaking(fee) {
            const modalBody = document.getElementById('tournamentModalContent');
            modalBody.innerHTML = `
                <div class="w-16 h-16 bg-yellow-500/10 text-yellow-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-yellow-500/30 animate-spin">🔍</div>
                <h3 class="text-2xl font-extrabold">Finding ₦${fee.toLocaleString()} Opponent...</h3>
                <p class="text-slate-400 text-sm">Matching you with another Lagos hustler...</p>
            `;

            setTimeout(() => {
                const opponents = [
                    { name: "Chidi_Pro (Abuja)", banter: "Omo, I ready for this match o!" },
                    { name: "LagosChamp99", banter: "No wahala, make we see who go win!" },
                    { name: "IbadanBoy_01", banter: "E don burst! Gather here make we play." }
                ];
                const matchedOpp = opponents[Math.floor(Math.random() * opponents.length)];
                modalBody.innerHTML = `
                    <div class="w-16 h-16 bg-emerald-500/10 text-emerald-400 rounded-2xl mx-auto flex items-center justify-center text-3xl font-bold border border-emerald-500/30">⚔️</div>
                    <h3 class="text-2xl font-extrabold text-emerald-400">Opponent Found!</h3>
                    <p class="text-slate-300 text-sm">Matched against <strong class="text-white">${matchedOpp.name}</strong>!</p>
                    <p class="text-xs italic text-yellow-400 bg-slate-900 p-2 rounded-xl border border-slate-800">💬 "${matchedOpp.banter}"</p>
                    <button onclick="confirmTournamentPayment(${fee}, '${matchedOpp.name}')" class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition mt-2">Pay ₦${fee.toLocaleString()} Entry via Paystack</button>
                `;
            }, 2500);
        }

        function startFreeRollMatch() {
            closeTournamentModal();
            alert("🎁 You have successfully joined today's Sponsored Free-Roll! Play any game to set your high score for the ₦10,000 pot.");
            launchGame('trivia');
        }

        function launchStakeGame(gameName, stakeAmount) {
            currentStakeAmount = stakeAmount;
            if (hustleWallet < stakeAmount) {
                alert(`Omo! You need at least ₦${stakeAmount} in your hustle wallet to play this mini-stake battle. Win free games first!`);
                return;
            }
            hustleWallet -= stakeAmount;
            updateWallet();
            alert(`⚡ ₦${stakeAmount} deducted from wallet for ${gameName} Mini-Stake Battle! Win to double your stake.`);
            if(gameName === 'Block-Fit') launchGame('blocks');
            else launchGame('pidgin');
        }

        // PAYSTACK INLINE CHECKOUT FUNCTION WITH DYNAMIC FEE
        function confirmTournamentPayment(fee, opponent) {
            const savedUser = localStorage.getItem('naija_arcade_user') || 'NaijaHustler';
            
            let handler = PaystackPop.setup({
                key: 'pk_test_551c4e1b3d95984ab0f31a4575dc29ddf47ca9b4',
                email: savedUser + '@naijaarcade.com',
                amount: fee * 100, // Converts Naira to Kobo dynamically
                currency: 'NGN',
                channels: ['card', 'bank', 'ussd', 'bank_transfer'],
                ref: 'NAIJA_' + Math.floor((Math.random() * 1000000000) + 1),
                metadata: {
                    custom_fields: [
                        {
                            display_name: "Matched Opponent",
                            variable_name: "matched_opponent",
                            value: opponent
                        }
                    ]
                },
                callback: function(response) {
                    alert('Tournament Entry Successful! Ref: ' + response.reference);
                    hustleWallet += fee * 2;
                    updateWallet();
                    closeTournamentModal();
                },
                onClose: function() {
                    console.log('Payment popup closed.');
                }
            });
            handler.openIframe();
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
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest flex items-center gap-1.5">🐍 Lagos Snake & Ladder Hustle</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <!-- AUTHENTIC WOODEN BOARD CONTAINER -->
                <div class="wooden-board p-4 rounded-3xl max-w-lg mx-auto space-y-4">
                    <div class="flex justify-between text-[11px] font-bold text-amber-200 px-1 border-b border-amber-600/30 pb-2">
                        <span>🪜 Promotion: 4➔14, 9➔31</span>
                        <span>🐍 Police Checkpoint: 95➔75, 62➔19</span>
                    </div>
                    <div class="grid grid-cols-10 gap-1 bg-[#1a0f05] p-2.5 rounded-2xl border-4 border-amber-700 shadow-inner aspect-square">
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
                    let badge = isPlayerHere ? '<div class="w-6 h-6 bg-yellow-400 text-slate-950 rounded-full font-black text-[10px] flex items-center justify-center shadow-lg animate-bounce ring-2 ring-white">🟢</div>' : `<span class="text-[10px] text-amber-100/70 font-bold">${t}</span>`;
                    let hasLadder = snakesAndLadders[t] && snakesAndLadders[t] > t;
                    let hasSnake = snakesAndLadders[t] && snakesAndLadders[t] < t;
                    let tileStyle = hasLadder ? 'bg-emerald-950/90 border-emerald-500' : (hasSnake ? 'bg-rose-950/90 border-rose-500' : 'bg-[#29170b] border-amber-900/40');
                    boardHTML += `<div class="rounded flex items-center justify-center border ${tileStyle} relative h-7 md:h-10">${badge}</div>`;
                });
            }
            boardHTML += `</div>
                </div>
                <div class="text-center space-y-3 pt-2">
                    <div id="diceResult" class="text-lg font-bold text-yellow-400">Current Position: Tile ${snakePos} / 100</div>
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
                            alert(snakePos > old ? "🪜 Big connection! You advanced!" : "🐍 Ahh, police checkpoint delay!");
                            if (snakePos >= 100) {
                                alert("🏆 You conquered Lagos hustle & won ₦5,000 virtual cash!");
                                hustleWallet += 5000;
                                updateWallet();
                                endGameScreen();
                            }
                        }, 300);
                    } else if (snakePos >= 100) {
                        alert("🏆 You reached Tile 100 and won!");
                        hustleWallet += 5000;
                        updateWallet();
                        endGameScreen();
                    } else {
                        const rb = document.getElementById('rollBtn');
                        if(rb) rb.disabled = false;
                    }
                }
            }, 250);
        }

        function updateWallet() {
            localStorage.setItem('naija_wallet', hustleWallet);
            document.getElementById('hustleWallet').innerText = '₦' + hustleWallet.toLocaleString();
        }

        function renderTetrisPuzzle() {
            tetrisGrid = Array(10).fill().map(() => Array(10).fill(0));
            tetrisScore = 0;
            currentShapeIdx = Math.floor(Math.random() * tetrisShapes.length);
            drawTetrisBoard();
        }

        function drawTetrisBoard() {
            let shapeObj = tetrisShapes[currentShapeIdx];
            let html = `
                <div class="flex justify-between items-center border-b border-yellow-500/20 pb-3">
                    <span class="text-xs font-bold text-yellow-400 uppercase tracking-widest flex items-center gap-1.5">🧩 Lagos Block-Fit Puzzle</span>
                    <button onclick="exitGame()" class="text-xs text-slate-400 hover:text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">✕ Exit</button>
                </div>
                <div class="text-center space-y-4">
                    <div class="text-sm font-bold">Puzzle Score: <span id="tetrisScoreVal" class="text-yellow-400 text-xl">${tetrisScore}</span> pts</div>
                    
                    <!-- AUTHENTIC WOODEN BOARD CONTAINER -->
                    <div class="wooden-board p-5 rounded-3xl max-w-sm mx-auto space-y-4">
                        <div class="text-xs text-amber-200 font-semibold flex justify-between items-center px-1">
                            <span>Ready Block:</span>
                            <strong class="text-yellow-400">${shapeObj.name}</strong>
                        </div>
                        <div class="flex justify-center items-center gap-2 h-16 bg-[#1a0f05] rounded-2xl border-2 border-amber-700/60 shadow-inner">
            `;
            
            shapeObj.shape.forEach(row => {
                row.forEach(cell => {
                    let activeCol = cell === 1 ? shapeObj.color + ' shadow-md rounded scale-95' : 'opacity-0';
                    html += `<div class="w-5 h-5 ${activeCol}"></div>`;
                });
            });

            html += `       </div>

                        <!-- Visual 10x10 Wooden Grid Board -->
                        <div class="grid grid-cols-10 gap-1 bg-[#1a0f05] p-3 rounded-2xl border-4 border-amber-700 shadow-inner">
            `;

            for (let r = 0; r < 10; r++) {
                for (let c = 0; c < 10; c++) {
                    let isFilled = tetrisGrid[r][c] === 1;
                    let tileColor = isFilled ? 'bg-amber-400 border-amber-200 shadow-md scale-95' : 'bg-[#29170b] border-amber-900/30';
                    html += `<div class="w-6 h-6 md:w-7 md:h-7 rounded-sm border ${tileColor} transition-all"></div>`;
                }
            }

            html += `</div>
                    </div>
                    <button onclick="placeTetrisPiece()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Place Block on Board 🧱</button>
                </div>
            `;
            document.getElementById('gameWorkspace').innerHTML = html;
        }

        function placeTetrisPiece() {
            let placed = false;
            for (let r = 9; r >= 0; r--) {
                let slotsAvailable = 0;
                for (let c = 0; c < 10; c++) {
                    if (tetrisGrid[r][c] === 0) slotsAvailable++;
                }
                if (slotsAvailable >= 3) {
                    tetrisGrid[r][3] = 1;
                    tetrisGrid[r][4] = 1;
                    tetrisGrid[r][5] = 1;
                    placed = true;
                    break;
                }
            }

            tetrisScore += 220;
            currentShapeIdx = (currentShapeIdx + 1) % tetrisShapes.length;
            drawTetrisBoard();

            if (tetrisScore >= 1100) {
                let reward = currentStakeAmount > 0 ? currentStakeAmount * 2 : 3000;
                alert(`🏆 Awesome hustle! You cleared lines and won ₦${reward.toLocaleString()} cash!`);
                hustleWallet += reward;
                updateWallet();
                currentStakeAmount = 0;
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
                        <button onclick="openTournamentModal()" class="bg-gradient-to-r from-yellow-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3.5 rounded-lg shadow-lg">Tournaments</button>
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