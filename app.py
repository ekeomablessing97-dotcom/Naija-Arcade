import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- GAME WEBSITE HTML & JAVASCRIPT TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaijaArcade - Play & Win Daily</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass-card { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(212, 175, 55, 0.25); }
        .gold-glow { box-shadow: 0 0 30px rgba(212, 175, 55, 0.2); }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-amber-500 selection:text-slate-950">

    <!-- Navbar -->
    <header class="glass-card border-b border-amber-500/20 sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-amber-400 flex items-center justify-center font-black text-slate-950 text-xl gold-glow">🎮</div>
            <span class="text-2xl font-black tracking-wider bg-gradient-to-r from-amber-400 via-amber-200 to-amber-500 bg-clip-text text-transparent">NaijaArcade</span>
        </div>
        <div class="flex items-center space-x-4">
            <span class="text-xs bg-amber-500/10 text-amber-400 px-3 py-1.5 rounded-full border border-amber-500/30 font-bold">🏆 High Score: <span id="topScore">0</span></span>
        </div>
    </header>

    <!-- Main Game Container -->
    <main class="max-w-xl mx-auto px-4 py-8 w-full flex-grow flex flex-col justify-center">
        <div class="glass-card rounded-3xl p-6 md:p-8 text-center space-y-6 gold-glow">
            
            <!-- Game Header -->
            <div>
                <span class="text-xs uppercase tracking-widest text-amber-400 font-extrabold bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">Quick Reflex Challenge</span>
                <h1 class="text-3xl font-extrabold mt-3">Catch the Golden Coin!</h1>
                <p class="text-slate-400 text-sm mt-1">Tap the falling gold coins as fast as you can before the 30-second timer runs out!</p>
            </div>

            <!-- Score & Timer Bar -->
            <div class="flex justify-between items-center bg-slate-900/80 px-6 py-3 rounded-2xl border border-slate-800 font-bold">
                <div>Score: <span id="currentScore" class="text-amber-400 text-xl">0</span></div>
                <div>Time Left: <span id="timeLeft" class="text-rose-400 text-xl">30</span>s</div>
            </div>

            <!-- Play Area Canvas / Box -->
            <div id="gameArea" class="relative h-64 bg-slate-900/50 rounded-2xl border border-slate-800 overflow-hidden flex items-center justify-center cursor-pointer select-none">
                <div id="startScreen" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/80 backdrop-blur-sm z-10 space-y-4">
                    <p class="text-slate-300 font-semibold text-sm">Ready to test your speed?</p>
                    <button onclick="startGame()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Start Game</button>
                </div>
                <!-- Dynamic Target -->
                <div id="coin" onclick="hitCoin()" class="hidden absolute w-12 h-12 bg-gradient-to-tr from-amber-500 to-amber-300 rounded-full shadow-lg cursor-pointer flex items-center justify-center text-slate-950 font-bold text-lg gold-glow transition-transform active:scale-90">🪙</div>
            </div>

            <!-- Controls / Info -->
            <p class="text-xs text-slate-500">Share your high score with friends and challenge them to beat your record!</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="glass-card border-t border-amber-500/20 py-6 text-center text-xs text-slate-500">
        &copy; 2026 NaijaArcade. Built for instant browser entertainment.
    </footer>

    <!-- Game Logic Script -->
    <script>
        let score = 0;
        let timeLeft = 30;
        let gameInterval = null;
        let coinTimer = null;
        let isPlaying = false;

        function startGame() {
            score = 0;
            timeLeft = 30;
            isPlaying = true;
            document.getElementById('currentScore').innerText = score;
            document.getElementById('timeLeft').innerText = timeLeft;
            document.getElementById('startScreen').classList.add('hidden');
            document.getElementById('coin').classList.remove('hidden');
            
            moveCoin();

            gameInterval = setInterval(() => {
                timeLeft--;
                document.getElementById('timeLeft').innerText = timeLeft;
                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
        }

        function moveCoin() {
            if (!isPlaying) return;
            const area = document.getElementById('gameArea');
            const coin = document.getElementById('coin');
            
            const maxX = area.clientWidth - 60;
            const maxY = area.clientHeight - 60;
            
            const randomX = Math.floor(Math.random() * maxX);
            const randomY = Math.floor(Math.random() * maxY);
            
            coin.style.left = randomX + 'px';
            coin.style.top = randomY + 'px';

            // Auto jump coin every 900ms if missed
            clearTimeout(coinTimer);
            coinTimer = setTimeout(moveCoin, 900);
        }

        function hitCoin() {
            if (!isPlaying) return;
            score += 10;
            document.getElementById('currentScore').innerText = score;
            moveCoin(); // jump immediately to new spot
        }

        function endGame() {
            isPlaying = false;
            clearInterval(gameInterval);
            clearTimeout(coinTimer);
            document.getElementById('coin').classList.add('hidden');
            
            let topScore = localStorage.getItem('naija_arcade_top') || 0;
            if (score > topScore) {
                topScore = score;
                localStorage.setItem('naija_arcade_top', topScore);
            }
            document.getElementById('topScore').innerText = topScore;

            const startScreen = document.getElementById('startScreen');
            startScreen.querySelector('h3, h1')?.remove();
            startScreen.innerHTML = `
                <div class="space-y-2">
                    <h3 class="text-2xl font-extrabold text-amber-400">Time's Up!</h3>
                    <p class="text-slate-300 text-sm">Your Final Score: <strong class="text-white text-lg">${score}</strong></p>
                    <button onclick="startGame()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3 rounded-xl shadow-lg hover:brightness-110 transition mt-2">Play Again</button>
                </div>
            `;
            startScreen.classList.remove('hidden');
        }

        // Load initial high score
        document.getElementById('topScore').innerText = localStorage.getItem('naija_arcade_top') || 0;
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
