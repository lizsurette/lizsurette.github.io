---
layout: default
title: Games
permalink: /games/
---

<div class="games-container">
  <h1>Games</h1>
  <hr />
  
  <div class="games-grid">
    <div class="game-card">
      <h2>Snake Game</h2>
      <p>A classic snake game where you control a snake to eat food and grow longer. Avoid hitting the walls or yourself!</p>
      <a href="/game/" class="game-link">Play Now</a>
    </div>
    
    <!-- More games can be added here in the future -->
  </div>
</div>

<style>
.games-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.game-card {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.game-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.game-card h2 {
  color: #333;
  margin-top: 0;
}

.game-card p {
  color: #666;
  margin-bottom: 20px;
}

.game-link {
  display: inline-block;
  background-color: #3fa757;
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.game-link:hover {
  background-color: #2d7a41;
  text-decoration: none;
  color: white;
}
</style> 