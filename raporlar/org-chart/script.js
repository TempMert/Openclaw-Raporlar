// OpenClaw Org Chart – Premium Edition

const THEME_KEY = 'org_theme';
const API_URL = '/api/agents.json';

// Theme toggle
const theme = localStorage.getItem(THEME_KEY) || 'dark';
document.body.dataset.theme = theme;
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', () => {
      const next = theme === 'dark' ? 'light' : 'dark';
      document.body.dataset.theme = next;
      localStorage.setItem(THEME_KEY, next);
    });
  }
});

// Particles canvas
(() => {
  const canvas = document.getElementById('particles');
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];
  function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
  window.addEventListener('resize', resize); resize();
  class Particle {
    constructor() { this.x = Math.random()*W; this.y = Math.random()*H; this.vx = (Math.random()-0.5)*0.4; this.vy = (Math.random()-0.5)*0.4; this.size = Math.random()*2+1; this.alpha = Math.random()*0.5+0.2; }
    update() { this.x += this.vx; this.y += this.vy; if(this.x<0) this.x=W; if(this.x>W) this.x=0; if(this.y<0) this.y=H; if(this.y>H) this.y=0; }
    draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI*2); ctx.fillStyle = `rgba(100,200,255,${this.alpha})`; ctx.fill(); }
  }
  for(let i=0;i<60;i++) particles.push(new Particle());
  function animate() { ctx.clearRect(0,0,W,H); particles.forEach(p=>{p.update();p.draw()}); requestAnimationFrame(animate); }
  animate();
})();

// Theme
const theme = localStorage.getItem(THEME_KEY) || 'dark';
document.body.dataset.theme = theme;
document.getElementById('theme-toggle').addEventListener('click', () => {
  const next = theme === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = next;
  localStorage.setItem(THEME_KEY, next);
});

// Fetch data
let agents = [];
async function loadAgents() {
  try {
    const r = await fetch(API_URL);
    if (!r.ok) throw new Error('Network response was not ok');
    const data = await r.json();
    agents = data.agents;
  } catch (e) {
    console.error('Failed to load agents JSON', e);
    // fallback static hardcoded list could go here
  }
}

// Render
function renderTree() {
  const tree = document.getElementById('org-tree');
  if (!agents.length) {
    tree.innerHTML = '<p style="text-align:center;opacity:0.6">Loading organizational data…</p>';
    return;
  }

  // Managers = first two (CEO, Manager), rest are agents
  const ceo = agents.find(a => a.id === 'ceo');
  const manager = agents.find(a => a.id === 'manager');
  const agentNodes = agents.filter(a => a.id !== 'ceo' && a.id !== 'manager');

  const createNode = (agent, level, posInSet, totalAtLevel, extraClass = '') => `
    <article class="node ${extraClass}" data-id="${agent.id}" data-level="${level}" role="treeitem" aria-level="${level}" aria-posinset="${posInSet}" aria-setsize="${totalAtLevel}" tabindex="${level===1?0:-1}" style="--c1:${agent.color.from}; --c2:${agent.color.to}">
      <div class="connector bottom" aria-hidden="true"><svg viewBox="0 0 100 60"><path class="line" d="M50 0 L50 60"/><circle class="dot" cx="50" cy="60" r="4"/></svg></div>
      <div class="node-avatar">${agent.avatar}</div>
      <div class="node-content">
        <h${level}>${agent.name}</h${level}>
        <p class="role">${agent.role}</p>
        <p class="desc">${agent.bio}</p>
      </div>
    </article>
  `;

  let html = '';

  // CEO
  html += createNode(ceo, 1, 1, 2, 'ceo');

  // Manager with connector up
  html += `
    <article class="node manager" data-level="2" role="treeitem" aria-level="2" aria-posinset="1" aria-setsize="2" tabindex="-1" style="--c1:${manager.color.from}; --c2:${manager.color.to}">
      <div class="connector" style="top:-40px"><svg viewBox="0 0 100 60"><path class="line" d="M50 0 L50 60"/><circle class="dot" cx="50" cy="60" r="4"/></svg></div>
      <div class="node-avatar">${manager.avatar}</div>
      <div class="node-content">
        <h2>${manager.name}</h2>
        <p class="role">${manager.role}</p>
        <p class="desc">${manager.bio}</p>
      </div>
      <div class="connector bottom"><svg viewBox="0 0 100 60"><path class="line" d="M50 0 L50 60"/><circle class="dot" cx="50" cy="60" r="4"/></svg></div>
    </article>
  `;

  // Agents row (flex wrap)
  html += `<div class="agents-row" style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;width:100%;">`;
  agentNodes.forEach((agent, idx) => {
    html += createNode(agent, 3, idx+1, agentNodes.length, 'agent ' + agent.id);
  });
  html += `</div>`;

  tree.innerHTML = html;

  // Staggered reveal
  requestAnimationFrame(() => {
    const nodes = tree.querySelectorAll('.node');
    nodes.forEach((n, i) => {
      setTimeout(() => n.classList.add('visible'), i * 100);
    });
  });
}

// Keyboard navigation
let focusIdx = 0;
document.addEventListener('keydown', (e) => {
  const nodes = Array.from(document.querySelectorAll('.node[tabindex="0"], .node[tabindex="-1"]'));
  if (!nodes.length) return;
  // Arrow navigation among all nodes in DOM order
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
    e.preventDefault();
    focusIdx = Math.min(focusIdx + 1, nodes.length - 1);
    nodes[focusIdx].focus();
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
    e.preventDefault();
    focusIdx = Math.max(focusIdx - 1, 0);
    nodes[focusIdx].focus();
  } else if (e.key === 'Home') {
    e.preventDefault(); focusIdx = 0; nodes[0].focus();
  } else if (e.key === 'End') {
    e.preventDefault(); focusIdx = nodes.length - 1; nodes[nodes.length-1].focus();
  }
});

// Init
loadAgents().then(renderTree);

// Optional: expose agents globally for debugging
window.orgChartAgents = agents;
