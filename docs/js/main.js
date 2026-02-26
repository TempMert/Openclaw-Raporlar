// ══════════════════════════════════════════
// EMAILJS KURULUMU — Şu 4 değeri doldur:
// ══════════════════════════════════════════
const EJ_KEY = "d-nHLonUZ-g8WVUBW";        // Account > Public Key
const EJ_SERVICE = "service_ob6wtws";        // Email Services
const EJ_WELCOME = "template_vyd0bd2";  // Hoşgeldin template ID
const EJ_RESET = "template_hc0hwk2";    // Şifre sıfırlama template ID
// ══════════════════════════════════════════
const EJ_ON = EJ_KEY !== "BURAYA_PUBLIC_KEY";
if (EJ_ON) emailjs.init(EJ_KEY);

function mailWelcome(name, email) {
  if (!EJ_ON) return;
  emailjs.send(EJ_SERVICE, EJ_WELCOME, { to_name: name, to_email: email }).catch(e => console.log(e));
}
function mailReset(name, email, code) {
  if (!EJ_ON) return Promise.resolve();
  return emailjs.send(EJ_SERVICE, EJ_RESET, { to_name: name || 'Müşterimiz', to_email: email, reset_code: code });
}

// ═══ PRODUCTS DATA ═══
const products = [
  { id: 1, name: "En İyi Arkadaşlar Serisi Kuromi ve My Melody", brand: "BUNDLE", category: "bundle sanrio", price: 599.99, oldPrice: 1198, discount: 50, emoji: "🎀", soldOut: true, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/7fc7759b-c7d1-459c-aafd-cefd1e4cbcb1/image_720.webp", stars: 5, reviews: 87, stock: 0 },
  { id: 2, name: "En İyi Arkadaşlar Serisi Squidward ve Mr. Krebs", brand: "BUNDLE", category: "bundle spongebob", price: 499.99, oldPrice: 978.99, discount: 49, emoji: "🦑", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/58cf3086-cf8d-42fa-a478-b5a2adb61259/image_720.webp", stars: 5, reviews: 54, stock: 5 },
  { id: 3, name: "Kuromi Sanrio Brick", brand: "BRICKS", category: "sanrio", price: 399.99, oldPrice: 599, discount: 33, emoji: "🖤", soldOut: true, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/ead57cec-85a2-4f24-9584-4d31ca189abb/image_720.webp", stars: 5, reviews: 112, stock: 0 },
  { id: 4, name: "My Melody Sanrio Brick", brand: "BRICKS", category: "sanrio", price: 399.99, oldPrice: 599, discount: 33, emoji: "🎀", soldOut: true, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/ec600b69-7a60-482c-94c8-8490fbcc1c89/image_720.webp", stars: 5, reviews: 98, stock: 0 },
  { id: 5, name: "Mickey Mouse Mini Brick", brand: "BRICKS", category: "disney", price: 299.99, oldPrice: 489, discount: 39, emoji: "🐭", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/05d9172f-1d7d-46e2-be78-399611019773/image_720.webp", stars: 4.5, reviews: 76, stock: 14 },
  { id: 6, name: "Mr. Krebs Mini Brick", brand: "BRICKS", category: "spongebob", price: 299.99, oldPrice: 489, discount: 39, emoji: "🦀", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/c9adebe1-3b09-4b21-a970-2844c06b3b65/image_720.webp", stars: 5, reviews: 143, stock: 8 },
  { id: 7, name: "My Melody Mini Brick", brand: "BRICKS", category: "sanrio", price: 299.99, oldPrice: 489, discount: 39, emoji: "🎀", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/889fad65-2f6e-4813-9c4c-5d18305e108d/image_720.webp", stars: 5, reviews: 89, stock: 11 },
  { id: 8, name: "Squidward Mini Brick", brand: "BRICKS", category: "spongebob", price: 299.99, oldPrice: 489, discount: 39, emoji: "🦑", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/0007a624-5437-4ec4-b1ba-5ac93ed2a07a/image_720.webp", stars: 4.5, reviews: 61, stock: 17 },
  { id: 9, name: "Piglet Mini Brick", brand: "BRICKS", category: "disney", price: 299.99, oldPrice: 489, discount: 39, emoji: "🐷", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/1efe2869-f4be-41a0-8a9e-9a152081c4fd/image_720.webp", stars: 4.5, reviews: 44, stock: 20 },
  { id: 10, name: "Goofy Mini Brick", brand: "BRICKS", category: "disney", price: 299.99, oldPrice: 489, discount: 39, emoji: "🐶", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/f7228794-d1f2-4580-bdb5-0208f267654c/image_720.webp", stars: 5, reviews: 58, stock: 12 },
  { id: 11, name: "Pamuk Prenses Mini Brick", brand: "BRICKS", category: "disney", price: 299.99, oldPrice: 489, discount: 39, emoji: "🍎", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/1e75778f-5eb2-4323-a6a0-884e83ec01e4/image_720.webp", stars: 5, reviews: 72, stock: 9 },
  { id: 12, name: "Sindirella Mini Brick", brand: "BRICKS", category: "disney", price: 299.99, oldPrice: 489, discount: 39, emoji: "👠", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/fb54c506-8882-4203-84ce-97502afd0b18/image_720.webp", stars: 5, reviews: 67, stock: 15 },
  { id: 13, name: "Chibiusa Mini Brick", brand: "BRICKS", category: "anime", price: 299.99, oldPrice: 489, discount: 39, emoji: "🌙", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/11c0ce4f-052d-45e2-87cc-ebf4a8e18334/image_720.webp", stars: 5, reviews: 93, stock: 7 },
  { id: 14, name: "Alien Mini Brick", brand: "BRICKS", category: "anime", price: 299.99, oldPrice: 489, discount: 39, emoji: "👽", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/bb07aa3d-c247-48dc-8cc5-518f838c5fa1/image_720.webp", stars: 4, reviews: 38, stock: 22 },
  { id: 15, name: "Cookie Ann Mini Brick", brand: "BRICKS", category: "sanrio", price: 299.99, oldPrice: 489, discount: 39, emoji: "🍪", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/38740c39-3751-4bfb-b8eb-b5c39e164a41/image_720.webp", stars: 4.5, reviews: 51, stock: 18 },
  { id: 16, name: "Cinnamoroll Mini Brick", brand: "BRICKS", category: "sanrio", price: 299.99, oldPrice: 489, discount: 39, emoji: "☁️", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/0882587d-59ed-4fa7-a7ba-62851e7cc2a6/image_720.webp", stars: 5, reviews: 108, stock: 6 },
  { id: 17, name: "Flying Cats Grey Cat", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🐈", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/45aee070-e1e2-4af3-8e4b-797c6d9ac654/image_720.webp", stars: 4.5, reviews: 42, stock: 13 },
  { id: 18, name: "Flying Dogs Brown Dog", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🐕", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/999e4add-b571-425c-867b-a380fc063a22/image_720.webp", stars: 4.5, reviews: 35, stock: 19 },
  { id: 19, name: "Flying Dogs Orange Dog", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🟠", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/fa441354-f2cb-4550-a641-f4b01ef5ad0b/image_720.webp", stars: 4, reviews: 29, stock: 25 },
  { id: 20, name: "Flying Dogs Cream Dog", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🤍", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/eacc02e8-5835-4be1-a449-c82f58aa3e5b/image_720.webp", stars: 4.5, reviews: 31, stock: 16 },
  { id: 21, name: "Flying Dogs White Pink Dog", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🐾", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/78e40ff9-59d8-4470-8006-257a296fcd42/image_720.webp", stars: 5, reviews: 46, stock: 4 },
  { id: 22, name: "Flying Cats Black Cat", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🐈⬛", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/13934652-32ec-47dd-a34a-e1583bccc487/image_720.webp", stars: 5, reviews: 63, stock: 10 },
  { id: 23, name: "Flying Dogs White Dog", brand: "MEKANSM", category: "flying", price: 324.99, oldPrice: 449, discount: 28, emoji: "🐩", soldOut: false, img: "https://cdn.myikas.com/images/8056384c-a086-458c-a400-f7587740fcdf/4deee969-8cfd-4c64-9136-ce3f4fbc64fc/image_720.webp", stars: 4.5, reviews: 40, stock: 21 }
];

// ═══ AUTH ═══
let users = JSON.parse(localStorage.getItem('plp_users') || '[]');
let me = JSON.parse(localStorage.getItem('plp_me') || 'null');
const saveU = () => localStorage.setItem('plp_users', JSON.stringify(users));
const saveMe = () => localStorage.setItem('plp_me', JSON.stringify(me));

function updateNav() {
  const nr = document.getElementById('navRight');
  if (me) {
    nr.innerHTML = `<button class="nbtn nbtn-ghost" onclick="openProfile()">👤 ${me.name}</button>
    <button class="cart-nbtn" onclick="toggleCart()">🛒 Sepet <span class="cart-badge" id="cartCount">0</span></button>`;
  } else {
    nr.innerHTML = `<button class="nbtn nbtn-ghost" onclick="openModal('login')">Giriş Yap</button>
    <button class="nbtn nbtn-fill" onclick="openModal('register')">Kayıt Ol</button>
    <button class="cart-nbtn" onclick="toggleCart()">🛒 Sepet <span class="cart-badge" id="cartCount">0</span></button>`;
  }
  renderCart();
}

function openModal(t) {
  document.getElementById('authModal').classList.add('open');
  showV(t === 'login' ? 'vLogin' : t === 'register' ? 'vReg' : 'vForgot');
  ['fEmail', 'fCode', 'fNewPass', 'lEmail', 'lPass', 'rName', 'rSurname', 'rEmail', 'rPass'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  pwdStrength('');
  activeResetEmail = '';
  activeResetCode = '';
}
function closeModal() { document.getElementById('authModal').classList.remove('open'); }
function closeModalOutside(e) { if (e.target.id === 'authModal') closeModal(); }
function showV(id) {
  ['vLogin', 'vReg', 'vForgot'].forEach(v => document.getElementById(v).style.display = v === id ? 'block' : 'none');
  ['errLogin', 'errReg', 'errForgot', 'okForgot'].forEach(x => { const el = document.getElementById(x); if (el) { el.classList.remove('show'); el.textContent = ''; } });
  if (id === 'vForgot') {
    document.getElementById('forgotStep1').style.display = 'block';
    document.getElementById('forgotStep2').style.display = 'none';
  }
}
function setErr(id, msg) { const el = document.getElementById(id); el.textContent = msg; el.classList.add('show'); }

function doLogin() {
  const email = document.getElementById('lEmail').value.trim(), pass = document.getElementById('lPass').value;
  if (!email || !pass) return setErr('errLogin', 'E-posta ve şifre zorunludur.');
  const u = users.find(x => x.email === email && x.password === pass);
  if (!u) return setErr('errLogin', 'E-posta veya şifre hatalı.');
  me = u; saveMe(); closeModal(); updateNav(); showToast(`🎉 Hoşgeldin ${u.name}!`);
}

function doRegister() {
  const name = document.getElementById('rName').value.trim(), surname = document.getElementById('rSurname').value.trim();
  const email = document.getElementById('rEmail').value.trim(), pass = document.getElementById('rPass').value;
  if (!name || !surname || !email || !pass) return setErr('errReg', 'Tüm alanları doldurun.');
  if (pass.length < 6) return setErr('errReg', 'Şifre en az 6 karakter olmalıdır.');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return setErr('errReg', 'Geçerli bir e-posta girin.');
  if (users.find(u => u.email === email)) return setErr('errReg', 'Bu e-posta zaten kayıtlı.');
  const nu = { id: Date.now(), name, surname, email, password: pass, orders: [], since: new Date().toLocaleDateString('tr-TR') };
  users.push(nu); saveU(); me = nu; saveMe();
  mailWelcome(name, email);
  closeModal(); updateNav(); showToast(`🎉 Hoşgeldin ${name}! Hesabın oluşturuldu.`);
}

let activeResetEmail = '';
let activeResetCode = '';

function doForgot() {
  const email = document.getElementById('fEmail').value.trim();
  if (!email) return setErr('errForgot', 'E-posta adresinizi girin.');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return setErr('errForgot', 'Geçerli bir e-posta girin.');
  document.getElementById('errForgot').classList.remove('show');

  const u = users.find(x => x.email === email);
  if (!u) return setErr('errForgot', 'Bu e-posta adresine ait hesap bulunamadı.');

  const ok = document.getElementById('okForgot');
  const code = Math.random().toString(36).slice(2, 8).toUpperCase();
  activeResetEmail = email;
  activeResetCode = code;

  if (EJ_ON) {
    mailReset(u.name, email, code)
      .then(() => {
        ok.textContent = `✅ ${email} adresine sıfırlama maili gönderildi!`;
        ok.classList.add('show');
        document.getElementById('forgotStep1').style.display = 'none';
        document.getElementById('forgotStep2').style.display = 'block';
      })
      .catch(() => {
        ok.textContent = `✅ ${email} adresine sıfırlama maili gönderildi!`;
        ok.classList.add('show');
        document.getElementById('forgotStep1').style.display = 'none';
        document.getElementById('forgotStep2').style.display = 'block';
      });
  } else {
    ok.textContent = `✅ Mail gönderildi! Kod: ${code}`;
    ok.classList.add('show');
    document.getElementById('forgotStep1').style.display = 'none';
    document.getElementById('forgotStep2').style.display = 'block';
  }
}

function doResetPassword() {
  const code = document.getElementById('fCode').value.trim().toUpperCase();
  const pass = document.getElementById('fNewPass').value;

  if (!code || !pass) return setErr('errForgot', 'Lütfen kodu ve yeni şifrenizi girin.');
  if (code !== activeResetCode) return setErr('errForgot', 'Girdiğiniz kod hatalı.');
  if (pass.length < 6) return setErr('errForgot', 'Şifreniz en az 6 karakter olmalıdır.');

  const u = users.find(x => x.email === activeResetEmail);
  if (u) {
    u.password = pass;
    saveU();
    showToast('🎉 Şifreniz başarıyla değiştirildi! Giriş yapabilirsiniz.');
    showV('vLogin');
  }
}

function pwdStrength(v) {
  const bar = document.getElementById('pwdBar'), hint = document.getElementById('pwdHint');
  if (!v) { bar.style.width = '0'; hint.textContent = ''; return; }
  let s = 0;
  if (v.length >= 6) s++; if (v.length >= 10) s++; if (/[A-Z]/.test(v)) s++; if (/[0-9]/.test(v)) s++; if (/[^A-Za-z0-9]/.test(v)) s++;
  const c = ['#e84040', '#f59e0b', '#fbbf24', '#22c55e', '#22c55e'];
  const l = ['Çok zayıf', 'Zayıf', 'Orta', 'Güçlü', 'Çok güçlü'];
  bar.style.width = (s * 20) + '%'; bar.style.background = c[s - 1] || '#e84040';
  hint.textContent = l[s - 1] || ''; hint.style.color = c[s - 1] || '#e84040';
}

function doLogout() { me = null; localStorage.removeItem('plp_me'); toggleProfile(); updateNav(); showToast('👋 Çıkış yapıldı.'); }

// ═══ PROFILE ═══
function openProfile() { if (!me) { openModal('login'); return; } renderProfile(); document.getElementById('profileOverlay').classList.add('open'); document.getElementById('profilePanel').classList.add('open'); }
function toggleProfile() { document.getElementById('profileOverlay').classList.remove('open'); document.getElementById('profilePanel').classList.remove('open'); }
const demoOrders = [
  { id: '#PLP-2401', status: 'delivered', label: 'Teslim Edildi', items: 'Mr. Krebs Mini Brick × 1', total: '₺299.99', date: '15 Oca 2025' },
  { id: '#PLP-2389', status: 'shipping', label: 'Kargoda', items: 'Flying Cats Black Cat × 2', total: '₺649.98', date: '20 Oca 2025' }
];
function renderProfile() {
  const u = me, orders = u.orders && u.orders.length ? u.orders : demoOrders;
  document.getElementById('profileBody').innerHTML = `
    <div class="p-user-card">
      <div class="p-av">${u.name[0]}${u.surname ? u.surname[0] : ''}</div>
      <div><div class="p-nm">${u.name} ${u.surname || ''}</div><div class="p-em">${u.email}</div><div class="p-sc">Üye: ${u.since || 'Bugün'}</div></div>
    </div>
    <div class="p-sec">📦 Siparişlerim</div>
    ${orders.map(o => `
      <div class="o-card">
        <div class="o-head"><span class="o-id">${o.id}</span><span class="o-status s-${o.status}">${o.label}</span></div>
        <div class="o-items">${o.items}</div>
        <div class="o-meta"><span class="o-total">${o.total}</span><span class="o-date">${o.date}</span></div>
      </div>`).join('')}
    ${!orders.length ? '<div style="text-align:center;padding:32px;color:var(--text2);font-weight:600">Henüz sipariş verilmedi.</div>' : ''}
    <div class="p-sec" style="margin-top:20px">⚙️ Hesap</div>
    <ul class="p-menu">
      <li onclick="showToast('Profil düzenleme yakında!')">✏️ Profili Düzenle</li>
      <li onclick="showToast('Adresler yakında!')">📍 Adreslerim</li>
      <li onclick="showToast('Favoriler yakında!')">❤️ Favorilerim</li>
      <li onclick="openModal('forgot');toggleProfile()">🔑 Şifre Değiştir</li>
    </ul>
    <button class="logout-btn" onclick="doLogout()">Çıkış Yap</button>`;
}

// ═══ PRODUCTS ═══
function stars(n) { let s = ''; for (let i = 1; i <= 5; i++)s += i <= n || n >= i - 0.5 ? '★' : '☆'; return s; }
function renderProducts(list) {
  const g = document.getElementById('prodGrid');
  if (!list.length) { g.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--text2);font-weight:700">Bu kategoride ürün bulunamadı.</div>'; return; }
  g.innerHTML = list.map(p => {
    const pct = Math.min(100, Math.round((p.stock / 25) * 100));
    const low = p.stock > 0 && p.stock <= 5;
    const sl = p.stock === 0 ? null : p.stock <= 5 ? `🔥 Son ${p.stock} ürün!` : p.stock <= 10 ? `⚡ ${p.stock} adet kaldı` : null;
    return `<div class="prod-card" onclick="openImageModal('${p.img}', '${p.name}')">
      <div class="prod-img">
        <img src="${p.img}" alt="${p.name}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="prod-img-ph" style="display:none">${p.emoji}</div>
        ${p.soldOut ? `<span class="prod-badge b-sold">Tükendi</span>` : p.discount >= 45 ? `<span class="prod-badge b-hot">🔥 %${p.discount} İndirim</span>` : `<span class="prod-badge b-off">%${p.discount} İndirim</span>`}
        <button class="wish-btn" onclick="event.stopPropagation();toggleWish(this)">♡</button>
        ${p.soldOut ? `<div class="sold-overlay"><div class="sold-tag">Tükendi</div></div>` : ''}
      </div>
      ${!p.soldOut && sl ? `<div class="stock-wrap"><div class="stock-lbl">${sl}</div><div class="stock-bar"><div class="stock-fill ${low ? 'low' : ''}" style="width:${pct}%"></div></div></div>` : ''}
      <div class="prod-body">
        <div class="prod-brand">${p.brand}</div>
        <div class="prod-name">${p.name}</div>
        <div class="prod-stars">${stars(p.stars)}<span>(${p.reviews})</span></div>
        <div class="prod-footer">
          <div><div class="price-now">₺${p.price.toFixed(2)}</div><div class="price-old">₺${p.oldPrice.toLocaleString('tr')}</div></div>
          ${!p.soldOut ? `<button class="add-btn" onclick="event.stopPropagation(); addToCart(${p.id})">+</button>` : `<button class="add-btn" style="opacity:0.3;cursor:not-allowed" disabled onclick="event.stopPropagation();">+</button>`}
        </div>
      </div>
    </div>`;
  }).join('');
}

function openImageModal(imgSrc, title) {
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImageDisplay');
  const modalTitle = document.getElementById('modalImageTitle');

  if (modal && modalImg) {
    modalImg.src = imgSrc;
    if (modalTitle) modalTitle.textContent = title;
    modal.classList.add('open');
  }
}
function closeImageModal() {
  const modal = document.getElementById('imageModal');
  if (modal) modal.classList.remove('open');
}

function toggleWish(btn) {
  if (btn.dataset.on) { btn.textContent = '♡'; btn.classList.remove('on'); delete btn.dataset.on; showToast('Favorilerden çıkarıldı'); }
  else { btn.textContent = '♥'; btn.classList.add('on'); btn.dataset.on = '1'; showToast('❤️ Favorilere eklendi!'); }
}
function fp(cat, btn) {
  document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderProducts(cat === 'all' ? products : products.filter(p => p.category.includes(cat)));
}
function filterAndScroll(cat) {
  const btn = [...document.querySelectorAll('.filter-pill')].find(b => b.textContent.toLowerCase().includes(cat === 'flying' ? 'flying' : cat));
  if (btn) { fp(cat, btn); document.getElementById('products').scrollIntoView({ behavior: 'smooth' }); }
}

// ═══ CART ═══
let cart = [];
function addToCart(id) {
  const p = products.find(x => x.id === id); if (!p || p.soldOut) return;
  const ex = cart.find(x => x.id === id); if (ex) ex.qty++; else cart.push({ ...p, qty: 1 });
  renderCart(); showToast(`✅ ${p.emoji} Sepete eklendi!`);
}
function changeQty(id, d) { const item = cart.find(x => x.id === id); if (!item) return; item.qty += d; if (item.qty <= 0) cart = cart.filter(x => x.id !== id); renderCart(); }
function removeItem(id) { cart = cart.filter(x => x.id !== id); renderCart(); }
function renderCart() {
  const cnt = cart.reduce((s, i) => s + i.qty, 0);
  const el = document.getElementById('cartCount'); if (el) el.textContent = cnt;
  const body = document.getElementById('cartBody'), foot = document.getElementById('cartFoot'); if (!body) return;
  if (!cart.length) { body.innerHTML = `<div class="cart-empty"><span class="ee">🛒</span><p>Sepetiniz boş</p></div>`; foot.innerHTML = ''; return; }
  body.innerHTML = cart.map(i => `
    <div class="cart-item">
      <div class="ci-img"><img src="${i.img}" alt="${i.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div style="display:none;width:100%;height:100%;align-items:center;justify-content:center;font-size:1.5rem">${i.emoji}</div></div>
      <div class="ci-info">
        <div class="ci-name">${i.name}</div>
        <div class="ci-price">₺${(i.price * i.qty).toFixed(2)}</div>
        <div class="ci-controls"><div class="ci-btn" onclick="changeQty(${i.id},-1)">−</div><span class="ci-qty">${i.qty}</span><div class="ci-btn" onclick="changeQty(${i.id},1)">+</div></div>
      </div>
      <button class="ci-del" onclick="removeItem(${i.id})">🗑</button>
    </div>`).join('');
  const sub = cart.reduce((s, i) => s + i.price * i.qty, 0);
  foot.innerHTML = `
    <div class="total-rows">
      <div class="total-row"><span>Ara Toplam</span><span>₺${sub.toFixed(2)}</span></div>
      <div class="total-row"><span>Kargo</span><span style="color:var(--green);font-weight:800">Ücretsiz 🎁</span></div>
      <div class="total-row final"><span>Toplam</span><span class="tv">₺${sub.toFixed(2)}</span></div>
    </div>
    <div class="free-ship">🎁 Tüm siparişlerde kargo ücretsiz!</div>
    <button class="checkout-btn" onclick="doCheckout()">Ödemeye Geç →</button>`;
}
function doCheckout() {
  if (!me) { toggleCart(); openModal('login'); showToast('⚠️ Ödeme için giriş yapmalısınız'); return; }
  const order = { id: '#PLP-' + Date.now().toString().slice(-4), status: 'processing', label: 'Hazırlanıyor', items: cart.map(i => `${i.name} × ${i.qty}`).join(', '), total: '₺' + cart.reduce((s, i) => s + i.price * i.qty, 0).toFixed(2), date: new Date().toLocaleDateString('tr-TR') };
  me.orders = [order, ...(me.orders || [])];
  users = users.map(u => u.id === me.id ? me : u); saveU(); saveMe();
  cart = []; renderCart(); toggleCart();
  showToast('🎉 Siparişiniz alındı! Hesabınızdan takip edebilirsiniz.');
}
function toggleCart() { document.getElementById('cartOverlay').classList.toggle('open'); document.getElementById('cartPanel').classList.toggle('open'); }

// ═══ CONTACT ═══
function submitContact() {
  const n = document.getElementById('cName').value.trim(), e = document.getElementById('cEmail').value.trim(), m = document.getElementById('cMsg').value.trim();
  if (!n || !e || !m) { showToast('⚠️ Lütfen tüm alanları doldurun'); return; }
  ['cName', 'cSurname', 'cEmail', 'cMsg'].forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
  showToast('✅ Mesajınız iletildi! En kısa sürede geri döneceğiz.');
}

// ═══ POPUP ═══
function closePopup() { const p = document.getElementById('popupBanner'); p.style.transform = 'translateX(-140%)'; setTimeout(() => p.style.display = 'none', 500); }
setTimeout(() => document.getElementById('popupBanner').classList.add('show'), 2500);

// ═══ TOAST ═══
let toastTimer;
function showToast(msg) { const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 3500); }

// ═══ INIT ═══
renderProducts(products);
updateNav();
