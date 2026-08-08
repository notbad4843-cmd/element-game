import os

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>원소술사 아카데미 (원소 게임 모음)</title>
    <link rel="manifest" href="./manifest.json">
    <meta name="theme-color" content="#090a0f">
    <style>
        /* CSS reset & variables */
        :root {
            --bg-color: #0b0f19;
            --text-main: #f0f4f8;
            --accent-glow: 0 0 10px rgba(100, 200, 255, 0.8);
            --gold: #FFD700;
            --silver: #C0C0C0;
            --bronze: #CD7F32;
        }

        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
            color: var(--text-main);
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            overflow: hidden; /* Prevent scrolling */
            touch-action: none;
        }

        /* Starry background effect */
        .stars {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1;
            pointer-events: none;
        }

        .screen {
            display: none;
            width: 100%;
            height: 100%;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: absolute;
            top: 0; left: 0;
        }
        .screen.active {
            display: flex;
        }

        h1 {
            font-size: 3rem;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            margin-bottom: 2rem;
            text-align: center;
        }
        h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        .subtitle {
            margin-bottom: 20px; font-size: 1.2rem; color: #aaa; text-align: center;
        }

        .btn {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 15px 30px;
            font-size: 1.2rem;
            border-radius: 30px;
            margin: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: var(--accent-glow);
            transform: translateY(-2px);
        }
        .btn.primary {
            background: rgba(0, 150, 255, 0.2);
            border-color: rgba(0, 150, 255, 0.5);
        }
        .btn.secondary {
            background: rgba(255, 100, 150, 0.2);
            border-color: rgba(255, 100, 150, 0.5);
        }

        .input-field {
            padding: 10px 20px;
            font-size: 1.2rem;
            border-radius: 30px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            text-align: center;
            margin-bottom: 20px;
            outline: none;
            width: 250px;
            backdrop-filter: blur(5px);
        }
        .input-field::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        .input-field:focus {
            border-color: rgba(0, 150, 255, 0.8);
            box-shadow: var(--accent-glow);
        }

        /* Game 1 UI (Falling Stars) */
        #game-ui {
            position: absolute;
            top: 0; left: 0; width: 100%;
            padding: 20px;
            box-sizing: border-box;
            display: flex;
            justify-content: space-between;
            font-size: 1.5rem;
            pointer-events: none;
            z-index: 10;
        }
        #target-display {
            position: absolute;
            top: 80px;
            width: 100%;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #ffeb3b;
            text-shadow: 0 0 20px rgba(255, 235, 59, 0.8);
            pointer-events: none;
            z-index: 10;
        }
        #game-area {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            overflow: hidden;
        }
        .bubble {
            position: absolute;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.8), rgba(255,255,255,0.1));
            border: 1px solid rgba(255,255,255,0.4);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px black;
            cursor: pointer;
            user-select: none;
            box-shadow: 0 0 15px rgba(255,255,255,0.2);
            transform-origin: center;
        }
        .bubble:active {
            transform: scale(0.9) !important;
        }

        /* Result & Panels */
        .panel {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 30px;
            max-width: 600px;
            width: 90%;
            max-height: 85vh;
            overflow-y: auto;
            backdrop-filter: blur(10px);
            text-align: center;
        }
        .panel::-webkit-scrollbar { width: 8px; }
        .panel::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); border-radius: 10px; }
        .panel::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }

        .correct-list { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
        .correct-item { background: rgba(76, 175, 80, 0.2); border: 1px solid #4CAF50; padding: 5px 10px; border-radius: 20px; font-size: 0.9rem; }
        .wrong-item { background: rgba(244, 67, 54, 0.2); border: 1px solid #F44336; padding: 5px 10px; border-radius: 20px; font-size: 0.9rem; }

        /* Hall of Fame */
        #hof-content { padding: 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 10px; }
        #hof-content h2 { color: #FFD700; text-shadow: 0 0 10px rgba(255,215,0,0.5); }
        .rank-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; margin-bottom: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; font-size: 1.2rem; text-align: left; }
        .rank-1 { border: 2px solid var(--gold); box-shadow: 0 0 15px rgba(255,215,0,0.3); }
        .rank-2 { border: 2px solid var(--silver); }
        .rank-3 { border: 2px solid var(--bronze); }
        .medal { font-size: 1.5rem; margin-right: 15px; }
        
        .feedback-text { position: absolute; font-size: 2rem; font-weight: bold; pointer-events: none; animation: floatUp 1s ease-out forwards; z-index: 20; }
        .feedback-text.correct { color: #4CAF50; text-shadow: 0 0 10px #4CAF50; }
        .feedback-text.wrong { color: #F44336; text-shadow: 0 0 10px #F44336; }

        @keyframes floatUp { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-50px); } }
        
        /* Game 2 (Memory Card) UI */
        .memory-game-header {
            position: absolute;
            top: 20px;
            width: 100%;
            text-align: center;
            pointer-events: none;
            z-index: 10;
        }
        #game2-stage-info {
            font-size: 2rem;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255,215,0,0.8);
        }
        #game2-matches-info {
            font-size: 1.2rem;
            color: #fff;
            margin-top: 5px;
        }
        .memory-grid-container {
            width: 100%;
            height: 100%;
            padding: 100px 20px 20px 20px;
            box-sizing: border-box;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .memory-grid {
            display: grid;
            gap: 10px;
            width: 100%;
            max-width: 600px;
            perspective: 1000px;
        }
        .memory-grid.cols-4 { grid-template-columns: repeat(4, 1fr); max-width: 400px; }
        .memory-grid.cols-5 { grid-template-columns: repeat(5, 1fr); max-width: 500px; }
        .memory-grid.cols-6 { grid-template-columns: repeat(6, 1fr); max-width: 600px; }

        .memory-card {
            width: 100%;
            aspect-ratio: 3/4;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.5s;
            cursor: pointer;
        }
        .memory-card.flipped { transform: rotateY(180deg); }
        .memory-card-front, .memory-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-sizing: border-box;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            text-align: center;
            word-break: keep-all;
        }
        .memory-card-back {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            border: 2px solid #5a7b9c;
            font-size: 2rem;
            color: rgba(255,255,255,0.2);
        }
        .memory-card-back::after { content: '★'; }
        .memory-card-front {
            background: linear-gradient(135deg, #fff, #f0f0f0);
            color: #111;
            transform: rotateY(180deg);
            border: 2px solid #fff;
            font-weight: bold;
            font-size: 1.2rem;
            padding: 5px;
        }
        .memory-card-front.symbol {
            font-size: 2.2rem;
            color: #e91e63;
        }
        .memory-card-front.name {
            font-size: 1.3rem;
            color: #1976d2;
        }
        .memory-card-front.matched {
            background: linear-gradient(135deg, #4caf50, #81c784);
            color: white;
            border-color: #a5d6a7;
        }
        .memory-card-front.matched.symbol, .memory-card-front.matched.name {
            color: white;
        }

        /* Main Menu Layout */
        .menu-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            max-width: 600px;
            width: 90%;
            margin-top: 30px;
        }
        .game-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(5px);
        }
        .game-card:hover {
            background: rgba(255,255,255,0.15);
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .game-card.g1:hover { border-color: rgba(0, 150, 255, 0.8); box-shadow: 0 0 15px rgba(0, 150, 255, 0.5); }
        .game-card.g2:hover { border-color: rgba(255, 100, 150, 0.8); box-shadow: 0 0 15px rgba(255, 100, 150, 0.5); }

        @media (max-width: 600px) {
            h1 { font-size: 2.2rem; }
            #target-display { font-size: 2.2rem; }
            .bubble { width: 55px; height: 55px; font-size: 1.3rem; }
            .memory-grid { gap: 5px; }
            .memory-card-front { font-size: 0.9rem; }
            .memory-card-front.symbol { font-size: 1.5rem; }
            .memory-card-front.name { font-size: 1rem; }
            #game2-stage-info { font-size: 1.5rem; }
        }
    </style>
</head>
<body>

    <!-- Background Stars -->
    <canvas class="stars" id="star-canvas"></canvas>

    <!-- [APP] Main Menu -->
    <div id="screen-main-menu" class="screen active">
        <h1>원소술사 아카데미</h1>
        <p class="subtitle">원소 기호를 완벽하게 마스터하세요!</p>
        
        <div class="menu-grid">
            <div class="game-card g1" onclick="showScreen('screen-game1-start')">
                <h2>1. 별을 따는 원소술사</h2>
                <p style="color:#aaa;">떨어지는 별 중에서 정답 기호를 잡아라!</p>
            </div>
            <div class="game-card g2" onclick="showScreen('screen-game2-start')">
                <h2>2. 기억의 원소술사</h2>
                <p style="color:#aaa;">원소 이름과 기호 카드의 짝을 맞춰라!</p>
            </div>
        </div>

        <div style="margin-top: 30px;">
            <button class="btn" onclick="showScreen('screen-learn')">원소 기호 사전 📖</button>
            <button class="btn" onclick="showScreen('screen-hof')">명예의 전당 🏆 (게임1)</button>
        </div>
    </div>

    <!-- [APP] Learning Screen -->
    <div id="screen-learn" class="screen">
        <div class="panel" style="max-width: 800px; width: 95%;">
            <h2>원소 기호 사전 📖</h2>
            <p class="subtitle">게임을 시작하기 전에 30개의 원소 기호를 익혀보세요!</p>
            
            <div id="learn-list" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 20px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                <!-- Filled by JS -->
            </div>
            
            <button class="btn" onclick="showScreen('screen-main-menu')">메인으로</button>
        </div>
    </div>

    <!-- [GAME 1] Start Screen -->
    <div id="screen-game1-start" class="screen">
        <h2>별을 따는 원소술사</h2>
        <p class="subtitle">제한시간 60초 안에 최대한 많은 원소를 모으세요.</p>
        
        <input type="text" id="nickname-input" class="input-field" placeholder="별명을 입력하세요" autocomplete="off" maxlength="15">
        
        <div>
            <button class="btn primary" onclick="startGame1('easy')">쉬움 모드 시작</button>
            <button class="btn primary" onclick="startGame1('hard')">어려움 모드 시작</button>
        </div>
        <div style="margin-top: 20px;">
            <button class="btn" onclick="showScreen('screen-main-menu')">뒤로 가기</button>
        </div>
    </div>

    <!-- [GAME 1] Play Screen -->
    <div id="screen-game1-play" class="screen">
        <div id="game-ui">
            <div id="score-display">점수: <span id="score">0</span></div>
            <div id="time-display">시간: <span id="time">60</span>s</div>
        </div>
        <div id="target-display">수소</div>
        <div id="game-area"></div>
    </div>

    <!-- [GAME 1] Result Screen -->
    <div id="screen-game1-result" class="screen">
        <div class="panel">
            <h2>게임 종료!</h2>
            <h1 id="final-score" style="margin: 10px 0; color: #00bcd4;">0 점</h1>
            <p id="result-mode" style="color: #aaa;"></p>
            
            <div style="display: flex; flex-direction: column; gap: 20px; text-align: left; margin: 20px 0; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
                <div>
                    <h3 style="margin: 0 0 5px 0; color: #4CAF50; font-size: 1.1rem;">✅ 맞춘 원소들</h3>
                    <div id="correct-list-container" class="correct-list"></div>
                </div>
                <div>
                    <h3 style="margin: 0 0 5px 0; color: #F44336; font-size: 1.1rem;">❌ 틀린 원소들</h3>
                    <div id="wrong-list-container" class="correct-list"></div>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="btn primary" onclick="saveScoreAndShowHoF()">명예의 전당 등록</button>
                <button class="btn" onclick="showScreen('screen-main-menu')">메인으로</button>
            </div>
        </div>
    </div>

    <!-- [GAME 1] Hall of Fame Screen -->
    <div id="screen-hof" class="screen">
        <div class="panel" style="padding: 0; background: transparent; border: none;">
            <div id="hof-content">
                <h2>🏆 명예의 전당 🏆</h2>
                <p style="margin-bottom: 20px; font-size: 0.9rem; color: #ccc;">올림픽 챔피언 원소술사들 (별 따기)</p>
                <div id="hof-list">
                    <!-- Ranks here -->
                </div>
                <div style="margin-top: 20px; color:#888; font-size:0.8rem;">
                    * 기록은 현재 기기에만 저장됩니다.
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="btn" onclick="showScreen('screen-main-menu')">메인으로</button>
            </div>
        </div>
    </div>

    <!-- [GAME 2] Start Screen -->
    <div id="screen-game2-start" class="screen">
        <h2>기억의 원소술사</h2>
        <p class="subtitle">원소 기호와 이름 카드의 짝을 맞추어 보세요.<br>총 3개의 단계로 진행됩니다.</p>
        
        <div style="margin-top: 20px;">
            <button class="btn secondary" style="font-size: 1.5rem; padding: 15px 40px;" onclick="startGame2(1)">도전 시작!</button>
        </div>
        <div style="margin-top: 20px;">
            <button class="btn" onclick="showScreen('screen-main-menu')">뒤로 가기</button>
        </div>
    </div>

    <!-- [GAME 2] Play Screen -->
    <div id="screen-game2-play" class="screen">
        <div class="memory-game-header">
            <div id="game2-stage-info">1단계 (4x4)</div>
            <div id="game2-matches-info">찾은 쌍: 0 / 8</div>
        </div>
        <div class="memory-grid-container">
            <div id="memory-grid" class="memory-grid cols-4">
                <!-- Cards injected here -->
            </div>
        </div>
    </div>

    <!-- [GAME 2] Result Screen -->
    <div id="screen-game2-result" class="screen">
        <div class="panel">
            <h2 id="g2-result-title">단계 클리어!</h2>
            <p id="g2-result-desc" class="subtitle">모든 원소의 짝을 찾았습니다!</p>
            
            <div style="margin-top: 30px;">
                <button id="g2-next-btn" class="btn secondary" onclick="startGame2(g2CurrentStage + 1)">다음 단계로</button>
                <button class="btn" onclick="showScreen('screen-main-menu')">메인으로</button>
            </div>
        </div>
    </div>

    <script>
        // --- Data (Exactly 30 Elements) ---
        const elementsData = [
            { symbol: 'H', name: '수소' }, { symbol: 'He', name: '헬륨' }, { symbol: 'Li', name: '리튬' },
            { symbol: 'Be', name: '베릴륨' }, { symbol: 'B', name: '붕소' }, { symbol: 'C', name: '탄소' },
            { symbol: 'N', name: '질소' }, { symbol: 'O', name: '산소' }, { symbol: 'F', name: '플루오린' },
            { symbol: 'Ne', name: '네온' }, { symbol: 'Na', name: '나트륨' }, { symbol: 'Mg', name: '마그네슘' },
            { symbol: 'Al', name: '알루미늄' }, { symbol: 'Si', name: '규소' }, { symbol: 'P', name: '인' },
            { symbol: 'S', name: '황' }, { symbol: 'Cl', name: '염소' }, { symbol: 'Ar', name: '아르곤' },
            { symbol: 'K', name: '칼륨' }, { symbol: 'Ca', name: '칼슘' },
            { symbol: 'Fe', name: '철' }, { symbol: 'Cu', name: '구리' }, { symbol: 'Zn', name: '아연' },
            { symbol: 'Ag', name: '은' }, { symbol: 'Au', name: '금' }, { symbol: 'Pb', name: '납' },
            { symbol: 'Hg', name: '수은' }, { symbol: 'I', name: '아이오딘' }, 
            { symbol: 'Ba', name: '바륨' }, { symbol: 'Mn', name: '망가니즈' }
        ];

        // --- Starry Background Effect ---
        function initStars() {
            const canvas = document.getElementById('star-canvas');
            const ctx = canvas.getContext('2d');
            let w, h;
            
            function resize() {
                w = canvas.width = window.innerWidth;
                h = canvas.height = window.innerHeight;
            }
            window.addEventListener('resize', resize);
            resize();

            const stars = Array(200).fill().map(() => ({
                x: Math.random() * w,
                y: Math.random() * h,
                size: Math.random() * 2 + 0.5,
                speed: Math.random() * 0.5 + 0.1,
                alpha: Math.random()
            }));

            function animateStars() {
                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = 'white';
                stars.forEach(star => {
                    star.y -= star.speed;
                    star.alpha += (Math.random() - 0.5) * 0.05;
                    if (star.alpha < 0) star.alpha = 0;
                    if (star.alpha > 1) star.alpha = 1;
                    
                    if (star.y < 0) {
                        star.y = h;
                        star.x = Math.random() * w;
                    }
                    
                    ctx.globalAlpha = star.alpha;
                    ctx.beginPath();
                    ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                    ctx.fill();
                });
                requestAnimationFrame(animateStars);
            }
            animateStars();
        }
        initStars();

        // --- Screen Management ---
        function showScreen(screenId) {
            // Clean up game1 if running
            clearInterval(gameInterval);
            cancelAnimationFrame(animationFrameId);

            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById(screenId).classList.add('active');
            
            if (screenId === 'screen-hof') {
                renderHoF();
            } else if (screenId === 'screen-learn') {
                renderLearnScreen();
            }
        }

        // --- Learn Screen ---
        function renderLearnScreen() {
            const listDiv = document.getElementById('learn-list');
            if (listDiv.children.length === 0) {
                elementsData.forEach(el => {
                    const card = document.createElement('div');
                    card.style.background = 'rgba(255,255,255,0.1)';
                    card.style.border = '1px solid rgba(255,255,255,0.3)';
                    card.style.borderRadius = '10px';
                    card.style.padding = '10px';
                    card.style.width = '80px';
                    card.style.textAlign = 'center';
                    
                    card.innerHTML = `
                        <div style="font-size: 1.8rem; font-weight: bold; color: #FFD700; text-shadow: 0 0 10px rgba(255,215,0,0.3);">${el.symbol}</div>
                        <div style="font-size: 0.9rem; margin-top: 5px; color: #ddd;">${el.name}</div>
                    `;
                    listDiv.appendChild(card);
                });
            }
        }

        // ==========================================
        // GAME 1: 별을 따는 원소술사
        // ==========================================
        let currentMode = 'easy'; // 'easy' or 'hard'
        let score = 0;
        let timeLeft = 60;
        let gameInterval = null;
        let animationFrameId = null;
        let targetElement = null;
        let bubbles = []; 
        let correctElementsThisGame = [];
        let wrongElementsThisGame = [];
        let playerNickname = '이름 없는 원소술사';
        const GAME_DURATION = 60; 

        function startGame1(mode) {
            const nameInput = document.getElementById('nickname-input').value.trim();
            playerNickname = nameInput ? nameInput : '이름 없는 원소술사';

            currentMode = mode;
            score = 0;
            timeLeft = GAME_DURATION;
            correctElementsThisGame = [];
            wrongElementsThisGame = [];
            
            document.getElementById('score').innerText = score;
            document.getElementById('time').innerText = timeLeft;
            document.getElementById('game-area').innerHTML = '';
            
            showScreen('screen-game1-play');
            
            nextQuestion1();
            
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(() => {
                timeLeft--;
                document.getElementById('time').innerText = timeLeft;
                if (timeLeft <= 0) {
                    endGame1();
                }
            }, 1000);

            if (animationFrameId) cancelAnimationFrame(animationFrameId);
            lastTime = performance.now();
            updateBubbles(lastTime);
        }

        function endGame1() {
            clearInterval(gameInterval);
            cancelAnimationFrame(animationFrameId);
            
            document.getElementById('final-score').innerText = `${score} 점`;
            const modeText = currentMode === 'easy' ? '쉬움 모드' : '어려움 모드';
            document.getElementById('result-mode').innerText = modeText;
            
            const correctContainer = document.getElementById('correct-list-container');
            correctContainer.innerHTML = '';
            if (correctElementsThisGame.length === 0) {
                correctContainer.innerHTML = '<span style="color:#888;">없음</span>';
            } else {
                correctElementsThisGame.forEach(el => {
                    const span = document.createElement('span');
                    span.className = 'correct-item';
                    span.innerText = `${el.name} (${el.symbol})`;
                    correctContainer.appendChild(span);
                });
            }

            const wrongContainer = document.getElementById('wrong-list-container');
            wrongContainer.innerHTML = '';
            if (wrongElementsThisGame.length === 0) {
                wrongContainer.innerHTML = '<span style="color:#888;">없음</span>';
            } else {
                wrongElementsThisGame.forEach(el => {
                    const span = document.createElement('span');
                    span.className = 'wrong-item';
                    span.innerText = `${el.name} (${el.symbol})`;
                    wrongContainer.appendChild(span);
                });
            }
            
            showScreen('screen-game1-result');
        }

        function nextQuestion1() {
            targetElement = elementsData[Math.floor(Math.random() * elementsData.length)];
            document.getElementById('target-display').innerText = targetElement.name;
            
            const area = document.getElementById('game-area');
            area.innerHTML = '';
            bubbles = [];

            const baseSpeed = currentMode === 'hard' ? 220 : 80; 
            const numOptions = currentMode === 'hard' ? 8 : 4;
            
            const options = [targetElement];
            while (options.length < numOptions) {
                const randomEl = elementsData[Math.floor(Math.random() * elementsData.length)];
                if (!options.includes(randomEl)) {
                    options.push(randomEl);
                }
            }
            
            options.sort(() => Math.random() - 0.5);

            const bubbleSize = window.innerWidth <= 600 ? 55 : 80;

            options.forEach(opt => {
                const el = document.createElement('div');
                el.className = 'bubble';
                el.innerText = opt.symbol;
                
                const startX = Math.random() * (window.innerWidth - bubbleSize - 20) + 10;
                const startY = Math.random() * (window.innerHeight - 200 - bubbleSize) + 150;
                
                const angle = Math.random() * Math.PI * 2;
                const speed = baseSpeed + (Math.random() * 50 - 25);
                const vx = Math.cos(angle) * speed;
                const vy = Math.sin(angle) * speed;

                area.appendChild(el);

                const bubbleObj = {
                    dom: el,
                    x: startX,
                    y: startY,
                    vx: vx,
                    vy: vy,
                    radius: bubbleSize / 2,
                    data: opt
                };

                el.addEventListener('pointerdown', (e) => {
                    e.preventDefault(); 
                    handleBubbleClick(bubbleObj, e.clientX, e.clientY);
                });

                bubbles.push(bubbleObj);
            });
        }

        function handleBubbleClick(bubbleObj, clickX, clickY) {
            const feedback = document.createElement('div');
            feedback.className = 'feedback-text';
            feedback.style.left = `${clickX}px`;
            feedback.style.top = `${clickY}px`;

            if (bubbleObj.data.symbol === targetElement.symbol) {
                const points = currentMode === 'hard' ? 2 : 1;
                score += points;
                feedback.innerText = `+${points}`;
                feedback.classList.add('correct');
                
                if (!correctElementsThisGame.some(el => el.symbol === targetElement.symbol)) {
                    correctElementsThisGame.push(targetElement);
                }
                setTimeout(nextQuestion1, 100);
            } else {
                score -= 1;
                feedback.innerText = '-1';
                feedback.classList.add('wrong');
                
                if (!wrongElementsThisGame.some(el => el.symbol === targetElement.symbol)) {
                    wrongElementsThisGame.push(targetElement);
                }
                bubbleObj.dom.style.opacity = '0';
                bubbleObj.dom.style.pointerEvents = 'none';
                bubbleObj.active = false; 
            }

            document.getElementById('score').innerText = score;
            document.body.appendChild(feedback);
            
            setTimeout(() => {
                if(document.body.contains(feedback)) {
                    document.body.removeChild(feedback);
                }
            }, 1000);
        }

        let lastTime = 0;
        function updateBubbles(time) {
            const dt = (time - lastTime) / 1000;
            lastTime = time;
            const maxDt = Math.min(dt, 0.1);
            const w = window.innerWidth;
            const h = window.innerHeight;
            const uiHeight = 150; 

            bubbles.forEach(b => {
                if (b.active === false) return;
                b.x += b.vx * maxDt;
                b.y += b.vy * maxDt;
                const r = b.radius;
                
                if (b.x < 0) { b.x = 0; b.vx *= -1; }
                else if (b.x + r*2 > w) { b.x = w - r*2; b.vx *= -1; }

                if (b.y < uiHeight) { b.y = uiHeight; b.vy *= -1; }
                else if (b.y + r*2 > h) { b.y = h - r*2; b.vy *= -1; }

                b.dom.style.transform = `translate(${b.x}px, ${b.y}px)`;
            });

            if (timeLeft > 0) {
                animationFrameId = requestAnimationFrame(updateBubbles);
            }
        }

        // Game 1 HoF
        const HOF_KEY = 'element_game_hof';
        function saveScoreAndShowHoF() {
            const records = JSON.parse(localStorage.getItem(HOF_KEY) || '[]');
            const newRecord = {
                nickname: playerNickname,
                score: score,
                mode: currentMode === 'easy' ? '쉬움' : '어려움',
                date: new Date().toLocaleDateString('ko-KR')
            };
            records.push(newRecord);
            records.sort((a, b) => b.score - a.score);
            const topRecords = records.slice(0, 10);
            localStorage.setItem(HOF_KEY, JSON.stringify(topRecords));
            showScreen('screen-hof');
        }
        function renderHoF() {
            const listDiv = document.getElementById('hof-list');
            listDiv.innerHTML = '';
            const records = JSON.parse(localStorage.getItem(HOF_KEY) || '[]');
            
            if (records.length === 0) {
                listDiv.innerHTML = '<div style="padding: 20px;">아직 등록된 기록이 없습니다.</div>';
                return;
            }

            records.forEach((record, index) => {
                const div = document.createElement('div');
                div.className = `rank-item ${index < 3 ? 'rank-' + (index + 1) : ''}`;
                
                let medalStr = `${index + 1}위`;
                if (index === 0) medalStr = '<span class="medal">🥇</span>';
                else if (index === 1) medalStr = '<span class="medal">🥈</span>';
                else if (index === 2) medalStr = '<span class="medal">🥉</span>';
                
                const displayName = record.nickname || '이름 없는 원소술사';

                div.innerHTML = `
                    <div style="display:flex; align-items:center;">
                        ${medalStr}
                        <div style="margin-left:10px;">
                            <span style="font-weight:bold;">${displayName}</span>
                            <span style="color: #00bcd4; font-weight:bold; margin-left: 5px;">${record.score} 점</span>
                        </div>
                    </div>
                    <div style="font-size:0.9rem; color:#aaa;">
                        [${record.mode}] ${record.date}
                    </div>
                `;
                listDiv.appendChild(div);
            });
        }


        // ==========================================
        // GAME 2: 기억의 원소술사 (Memory Card Match)
        // ==========================================
        const GAME2_STAGES = [
            { level: 1, name: '1단계 (4x4)', cols: 4, pairs: 8 },  // 16 cards
            { level: 2, name: '2단계 (4x5)', cols: 4, pairs: 10 }, // 20 cards (wait, 4x5 or 5x4 layout. Using 4 columns for 20 cards works)
            { level: 3, name: '3단계 (6x6)', cols: 6, pairs: 18 }  // 36 cards
        ];

        let g2CurrentStage = 1;
        let g2Cards = [];
        let g2FlippedIndices = [];
        let g2MatchedPairs = 0;
        let g2IsAnimating = false;

        function startGame2(stageLevel) {
            g2CurrentStage = stageLevel;
            const stageConfig = GAME2_STAGES[stageLevel - 1];
            
            if (!stageConfig) {
                // Game completely cleared
                document.getElementById('g2-result-title').innerText = "🎉 아카데미 졸업! 🎉";
                document.getElementById('g2-result-desc').innerText = "모든 기억의 원소술사 단계를 완벽하게 클리어하셨습니다!";
                document.getElementById('g2-next-btn').style.display = 'none';
                showScreen('screen-game2-result');
                return;
            }

            // Setup UI
            document.getElementById('game2-stage-info').innerText = stageConfig.name;
            g2MatchedPairs = 0;
            updateG2MatchesInfo();
            showScreen('screen-game2-play');

            // Generate Cards
            const grid = document.getElementById('memory-grid');
            grid.className = `memory-grid cols-${stageConfig.cols}`;
            grid.innerHTML = '';

            // Randomly select elements for this stage
            let shuffledElements = [...elementsData].sort(() => Math.random() - 0.5);
            let selectedElements = shuffledElements.slice(0, stageConfig.pairs);

            g2Cards = [];
            selectedElements.forEach(el => {
                g2Cards.push({ type: 'symbol', value: el.symbol, elementId: el.symbol });
                g2Cards.push({ type: 'name', value: el.name, elementId: el.symbol });
            });

            // Shuffle cards
            g2Cards.sort(() => Math.random() - 0.5);

            // Render cards
            g2Cards.forEach((card, index) => {
                const cardEl = document.createElement('div');
                cardEl.className = 'memory-card';
                cardEl.dataset.index = index;
                
                const cardFront = document.createElement('div');
                cardFront.className = `memory-card-front ${card.type}`;
                cardFront.innerText = card.value;
                
                const cardBack = document.createElement('div');
                cardBack.className = 'memory-card-back';
                
                cardEl.appendChild(cardFront);
                cardEl.appendChild(cardBack);
                
                cardEl.addEventListener('click', () => handleCardClick(index));
                grid.appendChild(cardEl);
            });

            g2FlippedIndices = [];
            g2IsAnimating = false;
        }

        function updateG2MatchesInfo() {
            const stageConfig = GAME2_STAGES[g2CurrentStage - 1];
            document.getElementById('game2-matches-info').innerText = `찾은 쌍: ${g2MatchedPairs} / ${stageConfig.pairs}`;
        }

        function handleCardClick(index) {
            if (g2IsAnimating) return;
            if (g2FlippedIndices.includes(index)) return; // Already flipped
            
            const cardEl = document.querySelector(`.memory-card[data-index="${index}"]`);
            if (cardEl.classList.contains('matched')) return; // Already matched

            // Flip
            cardEl.classList.add('flipped');
            g2FlippedIndices.push(index);

            if (g2FlippedIndices.length === 2) {
                checkG2Match();
            }
        }

        function checkG2Match() {
            g2IsAnimating = true;
            const idx1 = g2FlippedIndices[0];
            const idx2 = g2FlippedIndices[1];
            const card1 = g2Cards[idx1];
            const card2 = g2Cards[idx2];
            
            const el1 = document.querySelector(`.memory-card[data-index="${idx1}"]`);
            const el2 = document.querySelector(`.memory-card[data-index="${idx2}"]`);

            if (card1.elementId === card2.elementId) {
                // Match!
                setTimeout(() => {
                    el1.classList.add('matched');
                    el2.classList.add('matched');
                    el1.querySelector('.memory-card-front').classList.add('matched');
                    el2.querySelector('.memory-card-front').classList.add('matched');
                    
                    g2MatchedPairs++;
                    updateG2MatchesInfo();
                    
                    g2FlippedIndices = [];
                    g2IsAnimating = false;

                    const stageConfig = GAME2_STAGES[g2CurrentStage - 1];
                    if (g2MatchedPairs === stageConfig.pairs) {
                        setTimeout(() => endG2Stage(), 800);
                    }
                }, 400); // Wait for flip animation
            } else {
                // Not a match, flip back
                setTimeout(() => {
                    el1.classList.remove('flipped');
                    el2.classList.remove('flipped');
                    g2FlippedIndices = [];
                    g2IsAnimating = false;
                }, 800); // View time before flipping back
            }
        }

        function endG2Stage() {
            document.getElementById('g2-result-title').innerText = `${g2CurrentStage}단계 클리어!`;
            document.getElementById('g2-result-desc').innerText = "모든 원소의 짝을 찾았습니다!";
            document.getElementById('g2-next-btn').style.display = 'inline-block';
            showScreen('screen-game2-result');
        }

        // --- PWA Service Worker Registration ---
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js').then(registration => {
                    console.log('ServiceWorker registration successful with scope: ', registration.scope);
                }).catch(err => {
                    console.log('ServiceWorker registration failed: ', err);
                });
            });
        }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
