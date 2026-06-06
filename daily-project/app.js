/**
 * GitHub Streak Saver - Retro Web Game Engine
 * Highly documented, fully functional canvas game.
 * Uses Web Audio API for custom synthesized SFX.
 */

// --- Audio Synthesizer System ---
class AudioSystem {
    constructor() {
        this.ctx = null;
        this.muted = false;
    }

    init() {
        if (!this.ctx) {
            try {
                this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) {
                console.error("Web Audio API not supported", e);
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playJump() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        let osc = this.ctx.createOscillator();
        let gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(180, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(550, this.ctx.currentTime + 0.12);

        gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.12);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.12);
    }

    playCollect() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        let osc = this.ctx.createOscillator();
        let gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sine';
        // Classic retro major-third chime
        osc.frequency.setValueAtTime(523.25, this.ctx.currentTime); // C5
        osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.08); // E5

        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.2);
    }

    playFreeze() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        let osc = this.ctx.createOscillator();
        let gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(300, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(900, this.ctx.currentTime + 0.25);

        gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.25);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.25);
    }

    playCollision() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        let osc = this.ctx.createOscillator();
        let gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(350, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(60, this.ctx.currentTime + 0.45);

        gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.45);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.45);
    }
}

const audio = new AudioSystem();

// --- Game Engine Setup ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state variables
let gameStarted = false;
let gameActive = false;
let score = 0;
let highscore = parseInt(localStorage.getItem('streak_saver_highscore') || '0', 10);
let freezes = 0; // Number of saved freezes
let scrollSpeed = 4;
let frameCount = 0;

// Player Agent definition
const player = {
    x: 120,
    y: 200,
    radius: 16,
    velocity: 0,
    gravity: 0.35,
    lift: -7.5,
    shieldTime: 0, // temporary invincibility frames
    rotation: 0
};

// Lists for entities
let obstacles = [];
let collectables = [];
let particles = [];

// List of funny developer bugs
const BUG_NAMES = [
    "Merge Conflict",
    "NullPointer",
    "Server Outage",
    "Legacy Code",
    "Memory Leak",
    "Bug in Prod",
    "API 500",
    "OOM Error",
    "Uncaught Exception"
];

// List of funny quotes upon game over
const GAME_OVER_QUOTES = [
    "A rogue merge conflict broke your production build. Back to refactoring!",
    "The staging environment crashed on a Saturday. No dev streak today.",
    "Your API returned 500 Internal Server Error. Time to read stack traces.",
    "You hit legacy COBOL code without a safety helmet. Streak broken!",
    "An Out-Of-Memory error occurred. Your AI clone has taken your job."
];

// Load highscore to UI
document.getElementById('highscore-val').textContent = highscore;

// Update UI stats
function updateStatsUI() {
    document.getElementById('streak-val').textContent = score;
    document.getElementById('freezes-val').textContent = freezes;
    document.getElementById('highscore-val').textContent = highscore;
}

// --- Entity Spawning Functions ---

function spawnObstacle() {
    const isTop = Math.random() > 0.5;
    const h = 70 + Math.random() * 90; // obstacle height
    const w = 90 + Math.random() * 50;  // obstacle width
    const name = BUG_NAMES[Math.floor(Math.random() * BUG_NAMES.length)];
    
    obstacles.push({
        x: canvas.width,
        y: isTop ? 0 : canvas.height - h,
        width: w,
        height: h,
        name: name,
        color: '#EF4444', // Tailwind Red 500
        isTop: isTop
    });
}

function spawnCollectable() {
    const type = Math.random() > 0.85 ? 'freeze' : 'commit';
    const radius = type === 'freeze' ? 14 : 10;
    const cy = 60 + Math.random() * (canvas.height - 120);
    
    collectables.push({
        x: canvas.width,
        y: cy,
        radius: radius,
        type: type,
        color: type === 'freeze' ? '#06B6D4' : '#22C55E', // Cyan or Green
        pulse: 0
    });
}

function createParticles(x, y, color, count = 12) {
    for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 1 + Math.random() * 4;
        particles.push({
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            radius: 2 + Math.random() * 3,
            color: color,
            alpha: 1,
            decay: 0.02 + Math.random() * 0.03
        });
    }
}

// --- Collision Math Utilities ---
function checkRectCircleCollision(rect, circle) {
    // Find closest point on rectangle to circle's center
    const closestX = Math.max(rect.x, Math.min(circle.x, rect.x + rect.width));
    const closestY = Math.max(rect.y, Math.min(circle.y, rect.y + rect.height));

    // Calculate distance between closest point and circle center
    const distanceX = circle.x - closestX;
    const distanceY = circle.y - closestY;
    const distanceSquared = (distanceX * distanceX) + (distanceY * distanceY);

    return distanceSquared < (circle.radius * circle.radius);
}

function checkCircleCollision(c1, c2) {
    const dx = c1.x - c2.x;
    const dy = c1.y - c2.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    return dist < (c1.radius + c2.radius);
}

// --- Game Control Actions ---

function playerFlap() {
    if (!gameActive) return;
    player.velocity = player.lift;
    audio.playJump();
    createParticles(player.x - player.radius, player.y, 'rgba(148, 163, 184, 0.5)', 3);
}

function useFreeze() {
    if (!gameActive) return;
    if (freezes > 0 && player.shieldTime <= 0) {
        freezes--;
        player.shieldTime = 120; // 2 seconds at 60fps
        audio.playFreeze();
        updateStatsUI();
        createParticles(player.x, player.y, '#06B6D4', 20);
    }
}

function resetGame() {
    gameActive = true;
    score = 0;
    freezes = 1; // Start with 1 freeze as buffer
    scrollSpeed = 4.5;
    frameCount = 0;
    player.y = 200;
    player.velocity = 0;
    player.shieldTime = 60; // 1 sec safe spawn buffer
    player.rotation = 0;
    obstacles = [];
    collectables = [];
    particles = [];
    
    document.getElementById('gameover-overlay').classList.add('opacity-0', 'pointer-events-none');
    updateStatsUI();
    audio.init();
}

function triggerGameOver() {
    gameActive = false;
    audio.playCollision();
    
    // Choose funny quote
    const quote = GAME_OVER_QUOTES[Math.floor(Math.random() * GAME_OVER_QUOTES.length)];
    document.getElementById('gameover-quote').textContent = `"${quote}"`;
    document.getElementById('final-score').textContent = `${score} Days`;
    
    // Show gameover panel
    document.getElementById('gameover-overlay').classList.remove('opacity-0', 'pointer-events-none');
    
    // Set highscore if beaten
    if (score > highscore) {
        highscore = score;
        localStorage.setItem('streak_saver_highscore', highscore);
        updateStatsUI();
    }
}

// --- Event Listeners and Triggers ---

// Start game button
document.getElementById('start-btn').addEventListener('click', () => {
    document.getElementById('start-overlay').classList.add('opacity-0', 'pointer-events-none');
    gameStarted = true;
    resetGame();
});

// Restart button on GameOver
document.getElementById('restart-btn').addEventListener('click', () => {
    resetGame();
});

// Control buttons
document.getElementById('ctrl-flap').addEventListener('click', (e) => {
    e.stopPropagation();
    playerFlap();
});
document.getElementById('ctrl-freeze').addEventListener('click', (e) => {
    e.stopPropagation();
    useFreeze();
});
document.getElementById('ctrl-restart').addEventListener('click', (e) => {
    e.stopPropagation();
    resetGame();
});

// Sound toggler button
const soundBtn = document.getElementById('ctrl-sound');
soundBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    audio.muted = !audio.muted;
    const soundIcon = document.getElementById('sound-icon');
    const soundStatus = document.getElementById('sound-status');
    if (audio.muted) {
        soundIcon.textContent = '🔇';
        soundStatus.textContent = 'Muted';
        soundStatus.classList.remove('text-green-500');
        soundStatus.classList.add('text-red-500');
    } else {
        soundIcon.textContent = '🔊';
        soundStatus.textContent = 'Enabled';
        soundStatus.classList.remove('text-red-500');
        soundStatus.classList.add('text-green-500');
        audio.init();
    }
});

// Twitter/X share button
document.getElementById('share-btn').addEventListener('click', () => {
    const tweetText = encodeURIComponent(`💻 I just kept my coding streak alive for ${score} days in GitHub Streak Saver! Can you beat my high score of ${highscore} days? Play now! 🚀 #GitHubStreakSaver #DeveloperHumor`);
    window.open(`https://twitter.com/intent/tweet?text=${tweetText}`, '_blank');
});

// Keyboard bindings
window.addEventListener('keydown', (e) => {
    if (!gameStarted) return;
    
    if (e.code === 'Space' || e.code === 'ArrowUp') {
        e.preventDefault();
        playerFlap();
    } else if (e.code === 'ShiftLeft' || e.code === 'ShiftRight' || e.code === 'KeyF') {
        e.preventDefault();
        useFreeze();
    } else if (e.code === 'KeyR') {
        e.preventDefault();
        resetGame();
    }
});

// Click / Tap on Canvas to flap
canvas.addEventListener('mousedown', (e) => {
    if (!gameStarted) return;
    playerFlap();
});

// Support touch taps on canvas
canvas.addEventListener('touchstart', (e) => {
    if (!gameStarted) return;
    e.preventDefault();
    playerFlap();
}, { passive: false });


// --- Main Draw & Update Core Loop ---

function update() {
    if (!gameActive) return;

    frameCount++;
    
    // Dynamic difficulty: slightly speed up as score increases
    scrollSpeed = 4.5 + Math.floor(score / 10) * 0.4;
    
    // Spawn Obstacles
    if (frameCount % 110 === 0) {
        spawnObstacle();
    }
    
    // Spawn Collectables
    if (frameCount % 85 === 0) {
        spawnCollectable();
    }

    // Decrement shielding time
    if (player.shieldTime > 0) {
        player.shieldTime--;
    }

    // Player physics
    player.velocity += player.gravity;
    player.y += player.velocity;
    
    // Smooth rotate player based on speed
    player.rotation = Math.min(Math.max(player.velocity * 0.05, -0.4), 0.4);

    // Canvas boundary collision
    if (player.y - player.radius < 0) {
        player.y = player.radius;
        player.velocity = 0;
    }
    if (player.y + player.radius > canvas.height) {
        // Fall into abyss
        if (freezes > 0) {
            freezes--;
            player.y = 200;
            player.velocity = -4;
            player.shieldTime = 120; // 2 seconds protection
            audio.playFreeze();
            updateStatsUI();
            createParticles(player.x, canvas.height - 20, '#06B6D4', 20);
        } else {
            triggerGameOver();
        }
    }

    // Update Particles
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= p.decay;
        if (p.alpha <= 0) {
            particles.splice(i, 1);
        }
    }

    // Update and collide with Collectables
    for (let i = collectables.length - 1; i >= 0; i--) {
        const col = collectables[i];
        col.x -= scrollSpeed;
        col.pulse += 0.08;

        // Collision with player
        const playerCircle = { x: player.x, y: player.y, radius: player.radius };
        const colCircle = { x: col.x, y: col.y, radius: col.radius };
        
        if (checkCircleCollision(playerCircle, colCircle)) {
            // Collect item!
            if (col.type === 'commit') {
                score++;
                audio.playCollect();
                createParticles(col.x, col.y, '#22C55E', 10);
            } else if (col.type === 'freeze') {
                freezes = Math.min(freezes + 1, 3); // Max 3 shields stock
                audio.playFreeze();
                createParticles(col.x, col.y, '#06B6D4', 15);
            }
            updateStatsUI();
            collectables.splice(i, 1);
            continue;
        }

        // Delete off-screen
        if (col.x + col.radius < 0) {
            collectables.splice(i, 1);
        }
    }

    // Update and collide with Obstacles
    for (let i = obstacles.length - 1; i >= 0; i--) {
        const obs = obstacles[i];
        obs.x -= scrollSpeed;

        // Collision detection
        const playerCircle = { x: player.x, y: player.y, radius: player.radius };
        if (player.shieldTime <= 0 && checkRectCircleCollision(obs, playerCircle)) {
            // Collision occurred!
            if (freezes > 0) {
                // Auto consume shield
                freezes--;
                player.shieldTime = 120; // 2 sec safety invincibility
                audio.playFreeze();
                updateStatsUI();
                createParticles(player.x, player.y, '#06B6D4', 25);
                // Explode obstacle!
                createParticles(obs.x + obs.width/2, obs.y + obs.height/2, '#EF4444', 15);
                obstacles.splice(i, 1);
                continue;
            } else {
                triggerGameOver();
            }
        }

        // Delete off-screen
        if (obs.x + obs.width < 0) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    // 1. Clear Screen
    ctx.fillStyle = '#090D16'; // Deep retro dark space
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw Cyber Grid Lines in background
    ctx.strokeStyle = '#1E293B';
    ctx.lineWidth = 1;
    const gridSize = 40;
    const xOffset = -(frameCount * scrollSpeed) % gridSize;
    
    // Vertical grid lines
    for (let x = xOffset; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    // Horizontal grid lines
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // 2. Draw Particles
    for (const p of particles) {
        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 3. Draw Collectables
    for (const col of collectables) {
        ctx.save();
        // Dynamic pulse scaling
        const pulseScale = 1 + Math.sin(col.pulse) * 0.15;
        ctx.fillStyle = col.color;
        
        // Add neon glow
        ctx.shadowBlur = 12;
        ctx.shadowColor = col.color;
        
        ctx.beginPath();
        if (col.type === 'freeze') {
            // Draw a diamond/star snowflake
            ctx.translate(col.x, col.y);
            ctx.scale(pulseScale, pulseScale);
            ctx.rotate(frameCount * 0.02);
            ctx.beginPath();
            for (let j = 0; j < 4; j++) {
                ctx.rotate(Math.PI / 2);
                ctx.moveTo(0, -col.radius);
                ctx.lineTo(col.radius * 0.3, -col.radius * 0.3);
                ctx.lineTo(0, 0);
                ctx.lineTo(-col.radius * 0.3, -col.radius * 0.3);
            }
            ctx.closePath();
            ctx.fill();
        } else {
            // Draw a shiny green GitHub block
            ctx.translate(col.x, col.y);
            ctx.scale(pulseScale, pulseScale);
            const r = col.radius;
            ctx.fillRect(-r, -r, r * 2, r * 2);
            
            // Subtle pixel highlights inside green commit block
            ctx.fillStyle = '#4ADE80';
            ctx.fillRect(-r + 3, -r + 3, 4, 4);
        }
        ctx.restore();
    }

    // 4. Draw Obstacles
    for (const obs of obstacles) {
        ctx.save();
        
        // Solid Red background with custom border glow
        ctx.fillStyle = '#1E1B1B'; // Charcoal dark container
        ctx.strokeStyle = obs.color;
        ctx.lineWidth = 3;
        
        ctx.shadowBlur = 10;
        ctx.shadowColor = obs.color;
        
        // Draw rounded obstacle rect
        ctx.beginPath();
        ctx.roundRect(obs.x, obs.y, obs.width, obs.height, 8);
        ctx.fill();
        ctx.stroke();
        
        // Draw tech hazard lines inside
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.2)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let k = 0; k < obs.width + obs.height; k += 15) {
            ctx.moveTo(obs.x + k, obs.y);
            ctx.lineTo(obs.x + k - obs.height, obs.y + obs.height);
        }
        ctx.stroke();

        // Write Bug Name text
        ctx.fillStyle = '#FCA5A5'; // Light red
        ctx.font = 'bold 11px monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.shadowBlur = 0; // turn off shadow for text
        ctx.fillText(obs.name, obs.x + obs.width / 2, obs.y + obs.height / 2);
        
        ctx.restore();
    }

    // 5. Draw Player Agent
    ctx.save();
    ctx.translate(player.x, player.y);
    ctx.rotate(player.rotation);

    // Apply shield neon glow
    if (player.shieldTime > 0) {
        // Flash invincibility effect
        if (Math.floor(player.shieldTime / 4) % 2 === 0) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = '#06B6D4'; // Cyan shield glow
            ctx.strokeStyle = '#22D3EE';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(0, 0, player.radius + 8, 0, Math.PI * 2);
            ctx.stroke();
        }
    }

    // Draw cute Developer Robot agent
    ctx.fillStyle = '#38BDF8'; // Sky blue shell
    ctx.beginPath();
    ctx.arc(0, 0, player.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#0284C7';
    ctx.stroke();

    // Cute retro terminal monitor screen face
    ctx.fillStyle = '#0F172A'; // Screen black
    ctx.beginPath();
    ctx.roundRect(-10, -8, 20, 14, 3);
    ctx.fill();

    // Cute glowing computer eyes
    ctx.fillStyle = player.shieldTime > 0 ? '#22D3EE' : '#22C55E'; // green eyes or shield cyan
    ctx.fillRect(-5, -4, 3, 4);
    ctx.fillRect(2, -4, 3, 4);

    // Jetpack/wings on the back
    ctx.fillStyle = '#64748B';
    ctx.fillRect(-player.radius - 5, -6, 6, 12);
    // Draw fire flame exhaust when flapping
    if (player.velocity < 0) {
        const flameLength = 8 + Math.random() * 10;
        const grad = ctx.createLinearGradient(-player.radius - 5, 0, -player.radius - 5 - flameLength, 0);
        grad.addColorStop(0, '#F59E0B'); // Orange
        grad.addColorStop(1, '#EF4444'); // Red
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(-player.radius - 5, -4);
        ctx.lineTo(-player.radius - 5 - flameLength, 0);
        ctx.lineTo(-player.radius - 5, 4);
        ctx.closePath();
        ctx.fill();
    }

    ctx.restore();

    // 6. Draw "TAP TO BOOST" text if game hasn't started yet
    if (!gameStarted) {
        ctx.save();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.font = 'bold 16px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('CLICK TO INITIATE DEVELOPER STEAK', canvas.width / 2, canvas.height / 2 + 100);
        ctx.restore();
    }
}

// Global loop callback
function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

// Start rendering loop immediately (gameplay begins after button is pressed)
loop();
