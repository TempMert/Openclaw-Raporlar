// OpenClaw Intelligence – Premium Site

const THEME_KEY = 'oi_theme';
const API_URL = 'data/site.json';

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
let siteData = {};
async function loadData() {
  try {
    const r = await fetch(API_URL);
    if (!r.ok) throw new Error('Network error');
    siteData = await r.json();
    render();
    animateCounters();
  } catch (e) {
    console.error('Failed to load data', e);
  }
}

// Render sections
function render() {
  // Highlights
  const hlGrid = document.getElementById('highlights-grid');
  hlGrid.innerHTML = siteData.highlights.map(h => `
    <div class="card">
      <div class="card-icon">${h.icon}</div>
      <h4>${h.title}</h4>
      <p>${h.desc}</p>
    </div>
  `).join('');

  // Projects
  const projGrid = document.getElementById('projects-grid');
  projGrid.innerHTML = siteData.showcase.map(p => `
    <article class="card project-card">
      <div class="card-icon">🖥️</div>
      <h4>${p.title}</h4>
      <p>${p.desc}</p>
      <div class="tags">${p.tags.map(t => `<span>${t}</span>`).join('')}</div>
      <a href="${p.link}" target="_blank" class="link">View Project ↗</a>
    </article>
  `).join('');

  // Trends
  const trendsList = document.getElementById('trends-list');
  trendsList.innerHTML = siteData.trends.map(t => `
    <div class="trend-item">
      <div class="trend-year">${t.year}</div>
      <div class="trend-title">${t.trend}</div>
      <div class="trend-detail">${t.detail}</div>
    </div>
  `).join('');
}

// Counter animation
function animateCounters() {
  const nums = document.querySelectorAll('.num');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = +el.dataset.target;
        let cur = 0;
        const inc = Math.ceil(target / 60);
        const step = () => {
          cur += inc;
          if (cur < target) { el.textContent = cur; requestAnimationFrame(step); }
          else { el.textContent = target; }
        };
        step();
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  nums.forEach(n => observer.observe(n));
}

// Scroll reveal for cards
const reveal = new IntersectionObserver((entries) => {
  entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.card').forEach(c => reveal.observe(c));

// Init
loadData();
