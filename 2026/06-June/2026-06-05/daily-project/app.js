/* ============================================================
 * Daily Coding Streak Dashboard — App Logic
 * Friday Daily Project (JS/TS) — June 5, 2026
 *
 * Features:
 * - Streak calendar heatmap for the current month
 * - Stats summary (current streak, total days, completion rate)
 * - Today's coding challenges placeholder
 * - Activity log with mock data refreshed daily
 * - LocalStorage persistence for streak data
 * ============================================================ */

(function () {
  'use strict';

  const STORAGE_KEY = 'dailyCodingStreak';
  const TODAY = new Date();
  const CURRENT_YEAR = TODAY.getFullYear();
  const CURRENT_MONTH = TODAY.getMonth();
  const DAYS_IN_MONTH = new Date(CURRENT_YEAR, CURRENT_MONTH + 1, 0).getDate();

  function loadStreakData() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try { return JSON.parse(raw); } catch (e) { /* fall through */ }
    }
    return generateSeedData();
  }

  function saveStreakData(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }

  function generateSeedData() {
    const data = { days: {} };
    const today = TODAY.getDate();
    for (let d = 1; d <= today; d++) {
      if (d < today && Math.random() > 0.7) continue;
      data.days[d] = {
        date: `${CURRENT_YEAR}-${String(CURRENT_MONTH + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`,
        solved: Math.floor(Math.random() * 3) + 1,
        project: Math.random() > 0.5,
        refactor: Math.random() > 0.7,
      };
    }
    return data;
  }

  function calculateStats(data) {
    let currentStreak = 0;
    const today = TODAY.getDate();
    for (let d = today; d >= 1; d--) {
      if (data.days[d]) currentStreak++;
      else break;
    }
    const totalActive = Object.keys(data.days).length;
    const completionRate = Math.round((totalActive / today) * 100);
    let totalSolved = 0;
    Object.values(data.days).forEach(entry => {
      totalSolved += entry.solved || 0;
    });
    return { currentStreak, totalActive, completionRate, totalSolved };
  }

  function renderStats(stats) {
    document.getElementById('streak-count').textContent = stats.currentStreak;
    document.getElementById('total-days').textContent = stats.totalActive;
    document.getElementById('completion-rate').textContent = `${stats.completionRate}%`;
    document.getElementById('total-solved').textContent = stats.totalSolved;
  }

  function renderStreakCalendar(data) {
    const grid = document.getElementById('streak-grid');
    const monthLabel = document.getElementById('month-label');
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'];
    monthLabel.textContent = `${monthNames[CURRENT_MONTH]} ${CURRENT_YEAR}`;
    grid.innerHTML = '';

    const firstDay = new Date(CURRENT_YEAR, CURRENT_MONTH, 1).getDay();
    const today = TODAY.getDate();

    for (let i = 0; i < firstDay; i++) {
      const empty = document.createElement('div');
      empty.className = 'streak-day';
      empty.style.visibility = 'hidden';
      grid.appendChild(empty);
    }

    for (let d = 1; d <= DAYS_IN_MONTH; d++) {
      const dayEl = document.createElement('div');
      dayEl.className = 'streak-day';
      const entry = data.days[d];
      if (entry) {
        dayEl.classList.add('active');
        const intensity = Math.min((entry.solved || 1) / 4, 1);
        dayEl.style.setProperty('--day-active', `rgba(34, 197, 94, ${0.3 + intensity * 0.5})`);
      }
      if (d === today) dayEl.classList.add('today');

      const tooltip = document.createElement('span');
      tooltip.className = 'tooltip';
      tooltip.textContent = entry ? `${entry.solved} problem(s) solved` : 'No activity';
      dayEl.appendChild(tooltip);

      if (d === today || d === 1 || d === DAYS_IN_MONTH) dayEl.textContent = d;
      grid.appendChild(dayEl);
    }
  }

  function renderChallenges() {
    const container = document.getElementById('challenges-container');
    const challenges = [
      {
        platform: 'LeetCode',
        title: 'Total Waviness of Numbers in Range II',
        difficulty: 'Hard',
        badgeClass: 'badge-hard',
        link: 'https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/',
        description: 'Calculate total sum of peak/valley waviness for all numbers in a range up to 10^15 using Digit DP.'
      },
      {
        platform: 'HackerRank',
        title: 'Staircase',
        difficulty: 'Easy',
        badgeClass: 'badge-easy',
        link: 'https://www.hackerrank.com/challenges/staircase/problem',
        description: 'Print a right-aligned staircase of size n using # characters and spaces.'
      }
    ];
    container.innerHTML = challenges.map(c => `
      <div class="challenge-card">
        <div class="challenge-header">
          <span class="badge ${c.badgeClass}">${c.platform} &bull; ${c.difficulty}</span>
        </div>
        <h3>${c.title}</h3>
        <p>${c.description}</p>
        <a href="${c.link}" target="_blank" rel="noopener" class="challenge-link">View Challenge &rarr;</a>
      </div>
    `).join('');
  }

  function renderActivityLog(data) {
    const list = document.getElementById('activity-list');
    const entries = data.days[TODAY.getDate()];
    const activities = [];
    if (entries) {
      if (entries.solved > 0) activities.push({ type: 'solved', text: `Solved ${entries.solved} coding challenge(s)` });
      if (entries.project) activities.push({ type: 'project', text: 'Built daily mini-project (JS/TS)' });
      if (entries.refactor) activities.push({ type: 'refactor', text: 'Refactored code in portfolio repository' });
    }
    if (activities.length === 0) {
      activities.push({ type: 'solved', text: 'No activity recorded yet today &mdash; start coding!' });
    }
    list.innerHTML = activities.map(a => `
      <div class="activity-item">
        <div class="activity-dot ${a.type}"></div>
        <div>
          <div>${a.text}</div>
          <div class="activity-time">Today at ${String(TODAY.getHours()).padStart(2, '0')}:${String(TODAY.getMinutes()).padStart(2, '0')}</div>
        </div>
      </div>
    `).join('');
  }

  function markTodayActive() {
    const data = loadStreakData();
    const today = TODAY.getDate();
    if (!data.days) data.days = {};
    if (!data.days[today]) {
      data.days[today] = {
        date: `${CURRENT_YEAR}-${String(CURRENT_MONTH + 1).padStart(2, '0')}-${String(today).padStart(2, '0')}`,
        solved: 2,
        project: true,
        refactor: true,
      };
      saveStreakData(data);
    }
    return data;
  }

  function init() {
    const data = markTodayActive();
    const stats = calculateStats(data);
    renderStats(stats);
    renderStreakCalendar(data);
    renderChallenges();
    renderActivityLog(data);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();