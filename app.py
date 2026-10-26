import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- TRIVIA & TOURNAMENT QUESTION BANK ---
NAIJA_TRIVIA = [
    {
        "id": 1,
        "question": "Which of these cities is known as the center of excellence in Nigeria?",
        "options": ["Abuja", "Lagos", "Port Harcourt", "Kano"],
        "answer": 1,
        "funfact": "Lagos State is officially nicknamed the Centre of Excellence!"
    },
    {
        "id": 2,
        "question": "Who released the global hit album 'Made in Lagos'?",
        "options": ["Burna Boy", "Wizkid", "Davido", "Asake"],
        "answer": 1,
        "funfact": "Wizkid's 'Made in Lagos' album put Afrobeats massively on the global Billboard maps."
    },
    {
        "id": 3,
        "question": "What is the popular Nigerian street term for 'Wahala' or trouble?",
        "options": ["Gbege", "Kere", "Fela", "Oshe"],
        "answer": 0,
        "funfact": "'Gbege' or 'Puna' often describes serious trouble or drama in local parlance."
    },
    {
        "id": 4,
        "question": "Which Nigerian national team won the Africa Cup of Nations (AFCON) in 2013?",
        "options": ["Super Falcons", "Super Eagles", "Golden Eaglets", "Flying Eagles"],
        "answer": 1,
        "funfact": "Stephen Keshi led the Super Eagles to victory in South Africa in 2013."
    }
]

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
        .glass-card { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(212, 175, 55, 0.25); }
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
        <button onclick="openTournamentModal()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-4 py-2 rounded-xl text-xs shadow-lg hover:brightness-110 transition flex items-center space-x-1">
            <span>🏆 Join ₦500 Tournament</span>
        </button>
    </header>

    <!-- Main Container -->
    <main class="max-w-3xl mx-auto px-4 py-8 w-full flex-grow space-y-8">
        
        <!-- Hero Banner -->
        <div class="glass-card rounded-3xl p-8 text-center space-y-4 gold-glow relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-48 h-48 bg-amber-500/10 rounded-full blur-2xl pointer-events-none"></div>
            <span class="text-xs uppercase tracking-widest text-amber-400 font-extrabold bg-amber-500/10 px-4 py-1.5 rounded-full border border-amber-500/20">Nigeria's Ultimate Gaming & Trivia Hub</span>
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">Test Your Naija IQ & <span class="text-amber-400">Win Weekly Cash</span></h1>
            <p class="text-slate-400 text-sm md:text-base max-w-xl mx-auto">Play free trivia challenges or enter the weekly cash tournament pool to compete against top players across Nigeria.</p>
            <div class="flex flex-wrap justify-center gap-4 pt-2">
                <button onclick="startTriviaGame()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-bold px-8 py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Play Free Trivia</button>
                <button onclick="openTournamentModal()" class="bg-slate-900 border border-amber-500/40 text-amber-400 font-bold px-8 py-3.5 rounded-xl hover:bg-amber-500/10 transition">Weekly Tournament (₦500)</button>
            </div>
        </div>

        <!-- Dynamic Game Workspace -->
        <div id="gameWorkspace" class="glass-card p-6 md:p-8 rounded-3xl hidden space-y-6">
            <!-- Game content injected via JS -->
        </div>

        <!-- Live Leaderboard Preview -->
        <div class="glass-card p-6 rounded-2xl space-y-4">
            <h3 class="text-lg font-bold text-amber-400 flex items-center justify-between">
                <span>🔥 Weekly Leaderboard Champions</span>
                <span class="text-xs text-slate-400 font-normal">Prize Pool: ₦75,000</span>
            </h3>
            <div class="space-y-2">
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">1. Tunde A. (Lagos)</span>
                    <span class="text-amber-400 font-extrabold">3,450 pts</span>
                </div>
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">2. Chidi K. (Abuja)</span>
                    <span class="text-amber-400 font-extrabold">3,120 pts</span>
                </div>
                <div class="flex justify-between items-center p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sm">
                    <span class="font-semibold text-slate-200">3. Funmi O. (Ibadan)</span>
                    <span class="text-amber-400 font-extrabold">2,900 pts</span>
                </div>
            </div>
        </div>
    </main>

    <!-- TOURNAMENT MODAL -->
    <div id="tournamentModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-card max-w-md w-full p-8 rounded-3xl space-y-6 gold-glow relative">
            <button onclick="closeTournamentModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white font-bold text-lg">✕</button>
            <div class="text-center space-y-2">
                <div class="w-14 h-14 bg-amber-500/10 text-amber-400 rounded-2xl mx-auto flex items-center justify-center text-2xl font-bold border border-amber-500/30">🏆</div>
                <h3 class="text-2xl font-extrabold">Join Weekly Cash Battle</h3>
                <p class="text-slate-400 text-sm">Entry fee is <strong class="text-amber-400">₦500</strong>. Secure your spot on the live leaderboard and stand a chance to win this week's cash pool!</p>
            </div>
            
            <form onsubmit="handleTournamentEntry(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">Your Player Alias / Name</label>
                    <input type="text" id="playerName" required placeholder="e.g. LagosChampion" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-amber-400 outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase mb-1">WhatsApp / Phone Number</label>
                    <input type="tel" id="playerPhone" required placeholder="08030000000" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:border-amber-400 outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold py-3.5 rounded-xl shadow-lg hover:brightness-110 transition">Pay ₦500 & Enter Tournament</button>
            </form>
        </div>
    </div>

    <!-- Footer -->
    <footer class="glass-card border-t border-amber-500/20 py-6 text-center text-xs text-slate-500">
        &copy; 2026 NaijaArcade. Play smart, win big.
    </footer>

    <!-- Game Logic -->
    <script>
        const triviaData = [
            { q: "Which Nigerian city is known as the Centre of Excellence?", options: ["Abuja", "Lagos", "Port Harcourt", "Kano"], ans: 1 },
            { q: "Who released the global hit album 'Made in Lagos'?", options: ["Burna Boy", "Wizkid", "Davido", "Asake"], ans: 1 },
            { q: "What is the popular street term for serious trouble or drama?", options: ["Gbege", "Kere", "Fela", "Oshe"], ans: 0 },
            { q: "Which Nigerian national team won AFCON in South Africa in 2013?", options: ["Super Falcons", "Super Eagles", "Golden Eaglets", "Flying Eagles"], ans: 1 }
        ];

        let currentQIndex = 0;
        let score = 0;

        function startTriviaGame() {
            currentQIndex = 0;
            score = 0;
            document.getElementById('gameWorkspace').classList.remove('hidden');
            renderQuestion();
            window.scrollTo({ top: 300, behavior: 'smooth' });
        }

        function renderQuestion() {
            if (currentQIndex >= triviaData.length) {
                document.getElementById('gameWorkspace').innerHTML = `
                    <div class="text-center space-y-4 py-6">
                        <div class="text-4xl">🎉</div>
                        <h2 class="text-2xl font-extrabold text-amber-400">Challenge Completed!</h2>
                        <p class="text-slate-300">Your Score: <strong class="text-white text-xl">${score} / ${triviaData.length * 10}</strong></p>
                        <p class="text-slate-400 text-sm">Think you can score higher against others? Join the weekly cash tournament!</p>
                        <div class="flex justify-center gap-4 pt-4">
                            <button onclick="startTriviaGame()" class="bg-slate-900 border border-slate-700 px-6 py-3 rounded-xl font-bold text-sm">Play Again</button>
                            <button onclick="openTournamentModal()" class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-extrabold px-6 py-3 rounded-xl shadow-lg">Enter Cash Tournament</button>
                        </div>
                    </div>
                `;
                return;
            }

            const qData = triviaData[currentQIndex];
            let html = `
                <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                    <span class="text-xs font-bold text-amber-400 uppercase tracking-widest">Question ${currentQIndex + 1} of ${triviaData.length}</span>
                    <span class="text-xs text-slate-400 font-bold">Score: ${score}</span>
                </div>
                <h3 class="text-xl font-bold text-slate-100">${qData.q}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
            `;

            qData.options.forEach((opt, idx) => {
                html += `<button onclick="submitAnswer(${idx}, ${qData.ans})" class="text-left bg-slate-900 border border-slate-800 hover:border-amber-500/50 p-4 rounded-xl text-sm font-semibold transition active:scale-95">${String.fromCharCode(65 + idx)}. ${opt}</button>`;
            });

            html += `</div>`;
            document.getElementById('gameWorkspace').innerHTML = html;
        }

        function submitAnswer(selected, correct) {
            if (selected === correct) {
                score += 10;
            }
            currentQIndex++;
            renderQuestion();
        }

        function openTournamentModal() { document.getElementById('tournamentModal').classList.remove('hidden'); }
        function closeTournamentModal() { document.getElementById('tournamentModal').classList.add('hidden'); }

        function handleTournamentEntry(e) {
            e.preventDefault();
            const name = document.getElementById('playerName').value;
            const phone = document.getElementById('playerPhone').value;
            alert(`Initializing secure Paystack checkout of ₦500 for ${name} (${phone}). Redirecting to tournament gateway...`);
            window.location.href = `https://checkout.paystack.com/mock-tournament?name=${encodeURIComponent(name)}&amount=50000`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.0 if "PORT" in os.environ else 5000)
    app.run(host='0.0.0.0', port=port, debug=False)
