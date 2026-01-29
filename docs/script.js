// Game State
const gameState = {
    timed: false,
    category: null,
    difficulty: null,
    questionCount: 10,
    currentQuestion: 0,
    score: 0,
    points: 0,
    streak: 0,
    bestStreak: 0,
    questions: [],
    timerInterval: null
};

// Screen Management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function showMenu() {
    showScreen('menu-screen');
}

// Category Selection
function showCategorySelect(timed) {
    gameState.timed = timed;
    const categories = ['All Categories', ...getCategories()];
    const container = document.getElementById('category-options');
    container.innerHTML = categories.map(cat =>
        `<button class="option-btn" onclick="selectCategory('${cat === 'All Categories' ? '' : cat}')">${cat}</button>`
    ).join('');
    showScreen('category-screen');
}

function selectCategory(category) {
    gameState.category = category || null;
    showDifficultySelect();
}

// Difficulty Selection
function showDifficultySelect() {
    showScreen('difficulty-screen');
}

function selectDifficulty(difficulty) {
    gameState.difficulty = difficulty;
    showCountSelect();
}

// Question Count Selection
function showCountSelect() {
    const available = filterQuestions(questions, gameState.category, gameState.difficulty).length;
    document.getElementById('available-questions').textContent = available;
    gameState.questionCount = Math.min(10, available);
    document.getElementById('question-count').textContent = gameState.questionCount;
    showScreen('count-screen');
}

function changeCount(delta) {
    const available = filterQuestions(questions, gameState.category, gameState.difficulty).length;
    gameState.questionCount = Math.max(5, Math.min(available, gameState.questionCount + delta));
    document.getElementById('question-count').textContent = gameState.questionCount;
}

// Start Quiz
function startQuiz() {
    // Reset state
    gameState.currentQuestion = 0;
    gameState.score = 0;
    gameState.points = 0;
    gameState.streak = 0;
    gameState.bestStreak = 0;

    // Get questions
    const pool = filterQuestions(questions, gameState.category, gameState.difficulty);
    gameState.questions = shuffleArray(pool).slice(0, gameState.questionCount);

    // Show countdown
    showCountdown();
}

function showCountdown() {
    showScreen('countdown-screen');
    let count = 3;
    document.getElementById('countdown-number').textContent = count;

    const interval = setInterval(() => {
        count--;
        if (count > 0) {
            document.getElementById('countdown-number').textContent = count;
        } else if (count === 0) {
            document.getElementById('countdown-number').textContent = 'GO!';
        } else {
            clearInterval(interval);
            showQuestion();
        }
    }, 600);
}

// Show Question
function showQuestion() {
    showScreen('quiz-screen');

    const q = gameState.questions[gameState.currentQuestion];

    // Update header
    document.getElementById('current-q').textContent = gameState.currentQuestion + 1;
    document.getElementById('total-q').textContent = gameState.questions.length;

    const badge = document.getElementById('q-difficulty');
    badge.textContent = q.difficulty.toUpperCase();
    badge.className = 'difficulty-badge ' + q.difficulty;

    // Update question
    document.getElementById('question-text').textContent = q.text;

    // Update choices
    const choicesContainer = document.getElementById('choices');
    choicesContainer.innerHTML = q.choices.map((choice, i) =>
        `<button class="choice-btn" onclick="selectAnswer(${i})">${String.fromCharCode(65 + i)}. ${choice}</button>`
    ).join('');

    // Update score bar
    updateScoreBar();

    // Timer
    if (gameState.timed) {
        document.getElementById('timer-bar').classList.remove('hidden');
        startTimer();
    } else {
        document.getElementById('timer-bar').classList.add('hidden');
    }
}

function startTimer() {
    const timerFill = document.getElementById('timer-fill');
    let timeLeft = 15000;
    const startTime = Date.now();

    timerFill.style.width = '100%';

    gameState.timerInterval = setInterval(() => {
        const elapsed = Date.now() - startTime;
        timeLeft = Math.max(0, 15000 - elapsed);
        timerFill.style.width = (timeLeft / 15000 * 100) + '%';

        if (timeLeft <= 0) {
            clearInterval(gameState.timerInterval);
            timeUp();
        }
    }, 50);
}

function timeUp() {
    const buttons = document.querySelectorAll('.choice-btn');
    buttons.forEach(btn => btn.disabled = true);

    const q = gameState.questions[gameState.currentQuestion];
    buttons[q.answer].classList.add('correct');

    gameState.streak = 0;

    showFeedback(false, "Time's Up!");
}

// Answer Selection
function selectAnswer(index) {
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
    }

    const q = gameState.questions[gameState.currentQuestion];
    const correct = index === q.answer;

    // Disable all buttons and show result
    const buttons = document.querySelectorAll('.choice-btn');
    buttons.forEach(btn => btn.disabled = true);
    buttons[index].classList.add(correct ? 'correct' : 'wrong');
    if (!correct) {
        buttons[q.answer].classList.add('correct');
    }

    // Calculate points
    let pointsEarned = 0;
    let difficultyBonus = 0;
    let streakBonus = 0;

    if (correct) {
        gameState.score++;
        gameState.streak++;
        gameState.bestStreak = Math.max(gameState.bestStreak, gameState.streak);

        // Base points
        pointsEarned = 10;

        // Difficulty bonus
        const multipliers = { easy: 1, medium: 2, hard: 3 };
        difficultyBonus = 10 * (multipliers[q.difficulty] - 1);
        pointsEarned += difficultyBonus;

        // Streak bonus
        if (gameState.streak >= 3) {
            streakBonus = Math.min(25, (gameState.streak - 2) * 5);
            pointsEarned += streakBonus;
        }

        gameState.points += pointsEarned;
    } else {
        gameState.streak = 0;
    }

    showFeedback(correct, null, pointsEarned, difficultyBonus, streakBonus, q.choices[q.answer]);
}

function showFeedback(correct, customMessage, points, diffBonus, streakBonus, correctAnswer) {
    const content = document.getElementById('feedback-content');

    if (customMessage) {
        content.innerHTML = `
            <div class="feedback-wrong">
                <div class="feedback-title">${customMessage}</div>
                <div class="feedback-answer">The correct answer was: ${gameState.questions[gameState.currentQuestion].choices[gameState.questions[gameState.currentQuestion].answer]}</div>
            </div>
        `;
    } else if (correct) {
        let bonusText = '';
        if (diffBonus > 0) bonusText += `difficulty +${diffBonus} `;
        if (streakBonus > 0) bonusText += `streak x${gameState.streak} +${streakBonus}`;

        content.innerHTML = `
            <div class="feedback-correct">
                <div class="feedback-title">CORRECT!</div>
                <div class="feedback-points">+${points} points${bonusText ? ` (${bonusText.trim()})` : ''}</div>
            </div>
        `;
    } else {
        content.innerHTML = `
            <div class="feedback-wrong">
                <div class="feedback-title">WRONG!</div>
                <div class="feedback-answer">The correct answer was: ${correctAnswer}</div>
            </div>
        `;
    }

    // Update button text
    const isLast = gameState.currentQuestion >= gameState.questions.length - 1;
    document.getElementById('next-btn').textContent = isLast ? 'See Results' : 'Next Question';

    showScreen('feedback-screen');
}

function nextQuestion() {
    gameState.currentQuestion++;

    if (gameState.currentQuestion >= gameState.questions.length) {
        showResults();
    } else {
        showQuestion();
    }
}

function updateScoreBar() {
    document.getElementById('current-score').textContent = gameState.score;
    document.getElementById('score-total').textContent = gameState.currentQuestion;
    document.getElementById('points').textContent = gameState.points;

    const streakDisplay = document.getElementById('streak-display');
    if (gameState.streak > 1) {
        streakDisplay.classList.remove('hidden');
        document.getElementById('streak').textContent = gameState.streak;
    } else {
        streakDisplay.classList.add('hidden');
    }
}

// Results
function showResults() {
    const total = gameState.questions.length;
    const percentage = Math.round((gameState.score / total) * 100);

    // Stars and grade
    let stars, grade, gradeColor;
    if (percentage >= 80) {
        stars = '⭐⭐⭐⭐⭐';
        grade = 'EXCELLENT!';
        gradeColor = '#00b894';
    } else if (percentage >= 60) {
        stars = '⭐⭐⭐⭐☆';
        grade = 'GREAT JOB!';
        gradeColor = '#00d4ff';
    } else if (percentage >= 40) {
        stars = '⭐⭐⭐☆☆';
        grade = 'GOOD EFFORT!';
        gradeColor = '#f39c12';
    } else if (percentage >= 20) {
        stars = '⭐⭐☆☆☆';
        grade = 'KEEP TRYING!';
        gradeColor = '#9b59b6';
    } else {
        stars = '⭐☆☆☆☆';
        grade = 'STUDY MORE!';
        gradeColor = '#e94560';
    }

    document.getElementById('stars').textContent = stars;
    document.getElementById('grade').textContent = grade;
    document.getElementById('grade').style.color = gradeColor;

    document.getElementById('final-score').textContent = gameState.score;
    document.getElementById('final-total').textContent = total;
    document.getElementById('percentage').textContent = percentage;
    document.getElementById('final-points').textContent = gameState.points;
    document.getElementById('final-streak').textContent = gameState.bestStreak;

    document.getElementById('player-name').value = '';

    showScreen('results-screen');
}

// Leaderboard
function saveScore() {
    const name = document.getElementById('player-name').value.trim();
    if (!name) {
        alert('Please enter your name!');
        return;
    }

    const scores = getScores();
    scores.push({
        name: name,
        score: gameState.score,
        total: gameState.questions.length,
        points: gameState.points,
        bestStreak: gameState.bestStreak,
        percentage: Math.round((gameState.score / gameState.questions.length) * 100),
        category: gameState.category || 'All Categories',
        date: new Date().toISOString()
    });

    // Sort by points, then percentage
    scores.sort((a, b) => b.points - a.points || b.percentage - a.percentage);

    // Keep top 100
    localStorage.setItem('quizScores', JSON.stringify(scores.slice(0, 100)));

    alert('Score saved!');
    showLeaderboard();
}

function getScores() {
    try {
        return JSON.parse(localStorage.getItem('quizScores')) || [];
    } catch {
        return [];
    }
}

function showLeaderboard() {
    const scores = getScores().slice(0, 10);
    const container = document.getElementById('leaderboard-list');

    if (scores.length === 0) {
        container.innerHTML = '<div class="no-scores">No scores yet. Be the first to play!</div>';
    } else {
        container.innerHTML = scores.map((s, i) => {
            const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i + 1);
            return `
                <div class="leaderboard-item">
                    <div class="leaderboard-rank">${medal}</div>
                    <div class="leaderboard-info">
                        <div class="leaderboard-name">${s.name}</div>
                        <div class="leaderboard-details">${s.score}/${s.total} | ${s.category}</div>
                    </div>
                    <div class="leaderboard-points">${s.points}</div>
                </div>
            `;
        }).join('');
    }

    showScreen('leaderboard-screen');
}

function showHelp() {
    showScreen('help-screen');
}

// Helper Functions
function getCategories() {
    return [...new Set(questions.map(q => q.category))].sort();
}

function filterQuestions(qs, category, difficulty) {
    return qs.filter(q =>
        (!category || q.category === category) &&
        (!difficulty || q.difficulty === difficulty)
    );
}

function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

// PWA Support
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
}
