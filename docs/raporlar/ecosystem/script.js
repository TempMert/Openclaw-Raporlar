// OpenClaw Ecosystem Explorer

const THEME_KEY = 'ecosystem_theme';
const API_URL = 'repos.json';

// Particles
(() => {
  const canvas = document.getElementById('particles');
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];
  const resize = () => { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; };
  window.addEventListener('resize', resize); resize();
  class Particle {
    constructor() { this.x = Math.random()*W; this.y = Math.random()*H; this.vx = (Math.random()-0.5)*0.5; this.vy = (Math.random()-0.5)*0.5; this.size = Math.random()*2+1; this.alpha = Math.random()*0.5+0.2; }
    update() { this.x += this.vx; this.y += this.vy; if(this.x<0) this.x=W; if(this.x>W) this.x=0; if(this.y<0) this.y=H; if(this.y>H) this.y=0; }
    draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI*2); ctx.fillStyle = `rgba(100,200,255,${this.alpha})`; ctx.fill(); }
  }
  for(let i=0;i<80;i++) particles.push(new Particle());
  const animate = () => { ctx.clearRect(0,0,W,H); particles.forEach(p=>{p.update();p.draw()}); requestAnimationFrame(animate); };
  animate();
})();

// Theme
const saved = localStorage.getItem(THEME_KEY) || 'dark';
document.body.dataset.theme = saved;
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('theme-toggle');
  btn.addEventListener('click', () => {
    const next = saved === 'dark' ? 'light' : 'dark';
    document.body.dataset.theme = next;
    localStorage.setItem(THEME_KEY, next);
  });
});

// Load data
let reposData = { categories: [] };
async function loadData() {
  try {
    const r = await fetch(API_URL);
    if (!r.ok) throw new Error('Network error');
    reposData = await r.json();
    document.getElementById('last-updated').textContent = reposData.updated;
    renderCategories();
    renderRepos(reposData.categories.flatMap(c => c.repos));
  } catch (e) {
    console.error('Failed to load repos.json', e);
  }
}

// Render category buttons
function renderCategories() {
  const nav = document.getElementById('categories');
  const allBtn = `<button class="cat-btn on" data-cat="all">All</button>`;
  const cats = reposData.categories.map(c => `
    <button class="cat-btn" data-cat="${c.id}">
      ${c.icon} ${c.title}
    </button>
  `).join('');
  nav.innerHTML = allBtn + cats;

  nav.addEventListener('click', e => {
    if (!e.target.matches('.cat-btn')) return;
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('on'));
    e.target.classList.add('on');
    const cat = e.target.dataset.cat;
    if (cat === 'all') {
      renderRepos(reposData.categories.flatMap(c => c.repos));
    } else {
      const category = reposData.categories.find(c => c.id === cat);
      renderRepos(category ? category.repos : []);
    }
  });
}

// Render repo cards
function renderRepos(repos) {
  const query = document.getElementById('search').value.trim().toLowerCase();
  const filtered = repos.filter(r => 
    r.name.toLowerCase().includes(query) || 
    r.desc.toLowerCase().includes(query)
  );

  const grid = document.getElementById('repos-grid');
  if (!filtered.length) {
    grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;opacity:.6">No repositories match your search.</p>';
    return;
  }

  grid.innerHTML = filtered.map(r => `
    <article class="card">
      <div class="card-header">
        <div class="card-icon">📦</div>
        <div class="card-title">${r.name.split('/')[1]}</div>
      </div>
      <div class="card-desc">${r.desc}</div>
      <div class="card-meta">
        <span class="star">⭐ ${r.stars}</span>
        <span class="lang">${r.language}</span>
      </div>
      <a href="${r.url}" target="_blank" class="card-link">View on GitHub ↗</a>
    </article>
  `).join('');
}

// Search
document.getElementById('search').addEventListener('input', () => {
  const activeCat = document.querySelector('.cat-btn.on').dataset.cat;
  if (activeCat === 'all') {
    renderRepos(reposData.categories.flatMap(c => c.repos));
  } else {
    const category = reposData.categories.find(c => c.id === activeCat);
    renderRepos(category ? category.repos : []);
  }
});

// Init
loadData();
