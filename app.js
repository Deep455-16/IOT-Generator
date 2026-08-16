/* ============================================================
   IOTech — Industrial IoT Generator
   App Logic
   ============================================================ */

const API_BASE = window.location.origin.includes('localhost') ? 'http://localhost:5000' : 'https://iot-generator.onrender.com';
let currentDifficulty = 'Beginner';
let savedProjects = JSON.parse(localStorage.getItem('iotech_saved') || '[]');

/* ============================================================
   INITIALIZATION
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initMobileMenu();
  
  // Page specific initialization
  if (document.getElementById('generatorPage')) {
    initGenerator();
  }
  if (document.getElementById('ideasPage')) {
    initIdeas();
    // Auto-fetch ideas on load
    document.getElementById('ideasBtn').click();
  }
  if (document.getElementById('savedPage')) {
    renderSaved();
  }
});

/* ============================================================
   THEME MANAGEMENT
   ============================================================ */
function initTheme() {
  const toggleBtn = document.getElementById('themeToggle');
  const html = document.documentElement;
  
  // Check local storage or system preference
  const savedTheme = localStorage.getItem('iotech_theme');
  if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    html.setAttribute('data-theme', 'dark');
  } else {
    html.setAttribute('data-theme', 'light');
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('iotech_theme', next);
    });
  }
}

/* ============================================================
   MOBILE MENU
   ============================================================ */
function initMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const nav = document.getElementById('mobileNav');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      nav.classList.toggle('hidden');
    });
  }
}

/* ============================================================
   GENERATOR PAGE LOGIC
   ============================================================ */
function initGenerator() {
  // Difficulty buttons
  document.querySelectorAll('.diff-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.diff-btn').forEach(b => {
        b.classList.remove('active', 'border-accent-light', 'bg-accent-light/10', 'text-accent-light', 'dark:text-accent-dark');
        b.classList.add('border-industrial-300', 'dark:border-industrial-700', 'bg-industrial-50', 'dark:bg-industrial-800', 'text-industrial-600', 'dark:text-industrial-400');
      });
      btn.classList.remove('border-industrial-300', 'dark:border-industrial-700', 'bg-industrial-50', 'dark:bg-industrial-800', 'text-industrial-600', 'dark:text-industrial-400');
      btn.classList.add('active', 'border-accent-light', 'bg-accent-light/10', 'text-accent-light', 'dark:text-accent-dark');
      currentDifficulty = btn.dataset.val;
    });
  });

  const genBtn = document.getElementById('generateBtn');
  const topicInput = document.getElementById('topicInput');
  
  if (genBtn) genBtn.addEventListener('click', generateProject);
  if (topicInput) {
    topicInput.addEventListener('keydown', e => {
      if (e.ctrlKey && e.key === 'Enter') generateProject();
    });
    // Check if we navigated from ideas with a predefined topic
    const params = new URLSearchParams(window.location.search);
    const ideaParam = params.get('topic');
    if (ideaParam) {
      topicInput.value = ideaParam;
      generateProject();
    }
  }
}

async function generateProject() {
  const topic = document.getElementById('topicInput').value.trim();
  const category = document.getElementById('categorySelect').value;

  if (!topic) { showToast('Please enter a project concept'); return; }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.querySelector('.btn-text').textContent = 'Generating...';

  document.getElementById('outputPlaceholder').classList.add('hidden');
  document.getElementById('projectResult').classList.add('hidden');
  document.getElementById('loadingState').classList.remove('hidden');

  startLoaderMessages();
  startProgressBar();

  try {
    const res = await fetch(`${API_BASE}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, difficulty: currentDifficulty, category })
    });
    const data = await res.json();

    if (data.success) {
      renderProject(data.project, 'projectResult');
    } else {
      showError(data.error || 'Failed to generate project');
    }
  } catch (err) {
    showError('Could not connect to the backend server. Please try again later.');
  } finally {
    btn.disabled = false;
    btn.querySelector('.btn-text').textContent = 'Generate Blueprint';
    document.getElementById('loadingState').classList.add('hidden');
    stopLoaderMessages();
    stopProgressBar();
  }
}

let loaderInterval, progressInterval;
function startLoaderMessages() {
  const msgs = document.querySelectorAll('.loader-msg');
  if(!msgs.length) return;
  let i = 0;
  msgs.forEach(m => { m.classList.remove('active'); m.classList.add('hidden'); });
  msgs[0].classList.add('active'); msgs[0].classList.remove('hidden');
  loaderInterval = setInterval(() => {
    msgs[i].classList.remove('active'); msgs[i].classList.add('hidden');
    i = (i + 1) % msgs.length;
    msgs[i].classList.add('active'); msgs[i].classList.remove('hidden');
  }, 1800);
}
function stopLoaderMessages() { clearInterval(loaderInterval); }
function startProgressBar() {
  const fill = document.getElementById('progressFill');
  if(!fill) return;
  let progress = 0;
  fill.style.width = '0%';
  progressInterval = setInterval(() => {
    progress += Math.random() * 12 + 3;
    if (progress > 90) progress = 90;
    fill.style.width = progress + '%';
  }, 600);
}
function stopProgressBar() {
  clearInterval(progressInterval);
  const fill = document.getElementById('progressFill');
  if(fill) {
    fill.style.width = '100%';
    setTimeout(() => { fill.style.width = '0%'; }, 500);
  }
}

/* ============================================================
   IDEAS PAGE LOGIC
   ============================================================ */
function initIdeas() {
  const btn = document.getElementById('ideasBtn');
  if (btn) btn.addEventListener('click', generateIdeas);
}

async function generateIdeas() {
  const category = document.getElementById('ideasCategory').value;
  const difficulty = document.getElementById('ideasDifficulty').value;
  const btn = document.getElementById('ideasBtn');
  const grid = document.getElementById('ideasGrid');

  btn.disabled = true;
  grid.innerHTML = '<div class="col-span-full text-center py-12 text-industrial-500 font-mono">Fetching inspiration...</div>';

  try {
    const res = await fetch(`${API_BASE}/api/quick-ideas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, difficulty })
    });
    const data = await res.json();

    if (data.success) {
      renderIdeas(data.ideas);
    } else {
      grid.innerHTML = `<div class="col-span-full text-center py-12 text-red-500 font-mono">Error: ${data.error}</div>`;
    }
  } catch (err) {
    grid.innerHTML = '<div class="col-span-full text-center py-12 text-red-500 font-mono">Could not connect to backend server.</div>';
  } finally {
    btn.disabled = false;
  }
}

function renderIdeas(ideas) {
  const grid = document.getElementById('ideasGrid');
  grid.innerHTML = ideas.map(idea => `
    <div class="bg-white dark:bg-industrial-900 border border-industrial-200 dark:border-industrial-700 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow flex flex-col">
      <h3 class="text-xl font-bold text-industrial-900 dark:text-white mb-2">${escapeHtml(idea.title)}</h3>
      <p class="text-sm text-industrial-600 dark:text-industrial-400 mb-4 flex-grow">${escapeHtml(idea.description)}</p>
      
      <div class="flex flex-wrap gap-2 mb-4">
        ${(idea.components || []).map(c => `<span class="bg-industrial-100 dark:bg-industrial-800 text-industrial-600 dark:text-industrial-300 text-xs px-2 py-1 rounded border border-industrial-200 dark:border-industrial-700 font-mono">${escapeHtml(c)}</span>`).join('')}
      </div>
      
      <div class="text-xs text-accent-warning font-bold uppercase tracking-wide mb-4">
        <span class="material-symbols-outlined text-[14px] align-middle">star</span> ${escapeHtml(idea.wow_factor)}
      </div>
      
      <button onclick="window.location.href='generator.html?topic=${encodeURIComponent(idea.title)}'" class="w-full bg-industrial-100 hover:bg-industrial-200 dark:bg-industrial-800 dark:hover:bg-industrial-700 text-industrial-800 dark:text-industrial-200 py-2 rounded-md text-sm font-bold flex items-center justify-center gap-1 transition-colors">
        <span class="material-symbols-outlined text-sm">precision_manufacturing</span> Generate Blueprint
      </button>
    </div>
  `).join('');
}

/* ============================================================
   SAVED PAGE LOGIC
   ============================================================ */
function renderSaved() {
  const grid = document.getElementById('savedGrid');
  if (!grid) return;
  
  if (!savedProjects.length) {
    grid.innerHTML = '<div class="col-span-full text-center py-12 text-industrial-500 font-mono bg-white dark:bg-industrial-900 border border-dashed border-industrial-300 dark:border-industrial-700 rounded-lg">No saved blueprints.</div>';
    return;
  }
  
  grid.innerHTML = savedProjects.map((p, i) => `
    <div class="bg-white dark:bg-industrial-900 border border-industrial-200 dark:border-industrial-700 rounded-lg shadow-sm flex flex-col overflow-hidden">
      <div class="bg-industrial-100 dark:bg-industrial-950 px-4 py-3 border-b border-industrial-200 dark:border-industrial-800 flex justify-between items-center">
        <span class="text-xs font-mono font-bold text-industrial-500 uppercase">${escapeHtml(p.category)}</span>
        <span class="text-xs font-mono font-bold text-accent-light dark:text-accent-dark uppercase">${escapeHtml(p.difficulty)}</span>
      </div>
      <div class="p-6 flex-grow">
        <h3 class="text-xl font-bold text-industrial-900 dark:text-white mb-2">${escapeHtml(p.title)}</h3>
        <p class="text-xs text-industrial-500 font-mono">Saved: ${new Date(p.savedAt).toLocaleDateString()}</p>
      </div>
      <div class="px-6 py-4 bg-industrial-50 dark:bg-industrial-950/50 border-t border-industrial-100 dark:border-industrial-800 flex gap-2">
        <button onclick="viewSaved(${i})" class="flex-1 bg-white hover:bg-industrial-100 dark:bg-industrial-800 dark:hover:bg-industrial-700 text-industrial-800 dark:text-industrial-200 py-2 rounded-md text-sm font-bold border border-industrial-200 dark:border-industrial-700 transition-colors">
          View
        </button>
        <button onclick="deleteSaved(${i})" class="px-4 bg-red-50 hover:bg-red-100 dark:bg-red-900/20 dark:hover:bg-red-900/40 text-red-600 dark:text-red-400 py-2 rounded-md text-sm font-bold border border-red-200 dark:border-red-900/50 transition-colors flex items-center justify-center">
          <span class="material-symbols-outlined text-sm">delete</span>
        </button>
      </div>
    </div>
  `).join('');
}

function viewSaved(index) {
  const p = savedProjects[index];
  const modal = document.getElementById('viewModal');
  const content = document.getElementById('modalContent');
  
  if (modal && content) {
    modal.classList.remove('hidden');
    renderProject(p, 'modalContent');
    
    // Setup close
    document.getElementById('closeModalBtn').onclick = () => modal.classList.add('hidden');
    document.getElementById('viewModalBg').onclick = () => modal.classList.add('hidden');
    
    // Hide save button inside modal since it's already saved
    const saveBtn = content.querySelector('#saveProjectBtn');
    if (saveBtn) saveBtn.style.display = 'none';
  }
}

function deleteSaved(index) {
  savedProjects.splice(index, 1);
  localStorage.setItem('iotech_saved', JSON.stringify(savedProjects));
  renderSaved();
  showToast('Blueprint deleted');
}

/* ============================================================
   PROJECT RENDERING LOGIC (Shared)
   ============================================================ */
function renderProject(p, targetId) {
  const result = document.getElementById(targetId);
  if (!result) return;
  
  result.innerHTML = `
    <div class="project-header">
      <div class="project-header-top">
        <div class="project-badges">
          <span class="badge badge-cat">${escapeHtml(p.category)}</span>
          <span class="badge badge-diff-${escapeHtml(p.difficulty)}">${escapeHtml(p.difficulty)}</span>
        </div>
        <button class="project-save-btn" id="saveProjectBtn">
          <span class="material-symbols-outlined text-[18px]">bookmark</span> Save
        </button>
      </div>
      <h2 class="project-title">${escapeHtml(p.title)}</h2>
      <p class="project-tagline">${escapeHtml(p.tagline || '')}</p>
      <div class="project-meta">
        <span class="meta-item"><span class="material-symbols-outlined meta-icon text-[18px]">schedule</span> ${escapeHtml(p.estimated_time || 'N/A')}</span>
        <span class="meta-item"><span class="material-symbols-outlined meta-icon text-[18px]">payments</span> ${escapeHtml(p.estimated_cost || 'N/A')}</span>
        <span class="meta-item"><span class="material-symbols-outlined meta-icon text-[18px]">memory</span> ${p.components?.length || 0} Components</span>
        <span class="meta-item"><span class="material-symbols-outlined meta-icon text-[18px]">format_list_numbered</span> ${p.steps?.length || 0} Steps</span>
      </div>
    </div>

    <div class="tabs-bar">
      <button class="tab-btn active" onclick="switchTab(this, 'overview', '${targetId}')">Overview</button>
      <button class="tab-btn" onclick="switchTab(this, 'components', '${targetId}')">Components</button>
      <button class="tab-btn" onclick="switchTab(this, 'architecture', '${targetId}')">Architecture</button>
      <button class="tab-btn" onclick="switchTab(this, 'steps', '${targetId}')">Steps</button>
      <button class="tab-btn" onclick="switchTab(this, 'code', '${targetId}')">Code</button>
      <button class="tab-btn" onclick="switchTab(this, 'testing', '${targetId}')">Testing</button>
      <button class="tab-btn" onclick="switchTab(this, 'troubleshoot', '${targetId}')">Debug</button>
    </div>

    ${renderOverviewTab(p)}
    ${renderComponentsTab(p)}
    ${renderArchTab(p)}
    ${renderStepsTab(p)}
    ${renderCodeTab(p)}
    ${renderTestingTab(p)}
    ${renderTroubleshootTab(p)}
  `;
  result.classList.remove('hidden');

  const saveBtn = result.querySelector('#saveProjectBtn');
  if (saveBtn) saveBtn.addEventListener('click', () => saveProject(p));
}

function renderOverviewTab(p) {
  return `
  <div class="tab-content active" id="tab-overview">
    <div class="overview-grid">
      <div class="info-box"><div class="info-box-label">Time</div><div class="info-box-value">${escapeHtml(p.estimated_time || 'N/A')}</div></div>
      <div class="info-box"><div class="info-box-label">Cost</div><div class="info-box-value">${escapeHtml(p.estimated_cost || 'N/A')}</div></div>
      <div class="info-box"><div class="info-box-label">Difficulty</div><div class="info-box-value">${escapeHtml(p.difficulty)}</div></div>
      <div class="info-box"><div class="info-box-label">Category</div><div class="info-box-value">${escapeHtml(p.category)}</div></div>
    </div>
    <div class="section-subtitle">Abstract</div>
    <p class="overview-text">${escapeHtml(p.overview || p.description || '')}</p>
  </div>`;
}

function renderComponentsTab(p) {
  const comps = p.components || [];
  return `
  <div class="tab-content" id="tab-components">
    <div class="section-subtitle">Bill of Materials</div>
    <div class="overflow-x-auto">
      <table class="components-table">
        <thead>
          <tr><th>Component</th><th>Qty</th><th>Purpose</th><th>Cost</th></tr>
        </thead>
        <tbody>
          ${comps.map(c => {
            const name = typeof c === 'string' ? c : c.name;
            const qty = c.quantity || 1;
            const purpose = c.purpose || '-';
            const cost = c.approximate_cost || '-';
            return `
            <tr>
              <td>${escapeHtml(name)}</td>
              <td><span class="qty-badge">&times;${qty}</span></td>
              <td>${escapeHtml(purpose)}</td>
              <td><span class="cost-tag">${escapeHtml(cost)}</span></td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>
  </div>`;
}

function renderArchTab(p) {
  const arch = p.architecture || {};
  const layers = arch.layers || [];
  return `
  <div class="tab-content" id="tab-architecture">
    <div class="section-subtitle">System Layers</div>
    ${layers.length ? layers.map((l, i) => `
    <div class="arch-layer">
      <span class="arch-layer-num">L${i + 1}</span>
      <div>
        <div class="arch-layer-title">${escapeHtml(l.name)}</div>
        <div class="arch-layer-desc">${escapeHtml(l.description)}</div>
      </div>
    </div>`).join('') : '<p class="text-industrial-500 font-mono text-sm">Architecture data not available.</p>'}
  </div>`;
}

function renderStepsTab(p) {
  const steps = p.steps || [];
  return `
  <div class="tab-content" id="tab-steps">
    <div class="section-subtitle">Assembly & Instructions</div>
    ${steps.length ? steps.map(s => `
    <div class="step-card">
      <div class="step-header" onclick="toggleStep(this)">
        <span class="step-num">STEP ${s.step_number}</span>
        <span class="step-title-text">${escapeHtml(s.title)}</span>
        <span class="step-toggle material-symbols-outlined">expand_more</span>
      </div>
      <div class="step-body">
        <p class="step-description">${escapeHtml(s.description)}</p>
        ${s.code_snippet ? `
        <div class="code-block">
          <div class="code-header"><span class="code-lang">Snippet</span></div>
          <pre>${escapeHtml(s.code_snippet)}</pre>
        </div>` : ''}
      </div>
    </div>`).join('') : '<p class="text-industrial-500 font-mono text-sm">No steps provided.</p>'}
  </div>`;
}

function renderCodeTab(p) {
  const code = p.code || {};
  return `
  <div class="tab-content" id="tab-code">
    <div class="section-subtitle">Main Firmware</div>
    <div class="code-block">
      <div class="code-header">
        <span class="code-lang">${escapeHtml(code.language || 'Code')}</span>
        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
      </div>
      <pre>${escapeHtml(code.main_code || '# Code not available')}</pre>
    </div>
    ${code.explanation ? `
    <div class="mt-4">
      <div class="font-bold text-sm text-industrial-900 dark:text-white mb-2">Explanation:</div>
      <p class="text-sm text-industrial-600 dark:text-industrial-400 leading-relaxed">${escapeHtml(code.explanation)}</p>
    </div>` : ''}
  </div>`;
}

function renderTestingTab(p) {
  const t = p.testing || {};
  return `
  <div class="tab-content" id="tab-testing">
    <div class="section-subtitle">Testing Procedure</div>
    ${t.steps?.length ? `
    <ul class="list-items mb-6">
      ${t.steps.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
    </ul>` : '<p class="text-industrial-500 font-mono text-sm mb-4">No specific testing steps provided.</p>'}
    
    <div class="font-bold text-sm text-industrial-900 dark:text-white mb-2">Expected Output:</div>
    <div class="bg-industrial-100 dark:bg-industrial-800 p-4 rounded-md font-mono text-sm text-industrial-800 dark:text-industrial-200 border-l-4 border-accent-light">
      ${escapeHtml(t.expected_output || 'System should operate normally.')}
    </div>
  </div>`;
}

function renderTroubleshootTab(p) {
  const items = p.troubleshooting || [];
  return `
  <div class="tab-content" id="tab-troubleshoot">
    <div class="section-subtitle">Common Issues</div>
    ${items.length ? items.map(i => `
    <div class="trouble-item">
      <div class="trouble-problem">${escapeHtml(i.problem)}</div>
      <div class="trouble-solution">${escapeHtml(i.solution)}</div>
    </div>`).join('') : '<p class="text-industrial-500 font-mono text-sm">No troubleshooting data available.</p>'}
  </div>`;
}

/* ============================================================
   UI HELPERS
   ============================================================ */
window.switchTab = function(btn, tabId, targetId) {
  const container = document.getElementById(targetId);
  if (!container) return;
  container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  container.querySelectorAll('.tab-content').forEach(t => {
    t.classList.remove('active');
  });
  btn.classList.add('active');
  const tabEl = container.querySelector('#tab-' + tabId);
  if (tabEl) tabEl.classList.add('active');
}

window.toggleStep = function(header) {
  const body = header.nextElementSibling;
  const toggle = header.querySelector('.step-toggle');
  body.classList.toggle('open');
  if (body.classList.contains('open')) {
    toggle.textContent = 'expand_less';
  } else {
    toggle.textContent = 'expand_more';
  }
}

window.copyCode = function(btn) {
  const pre = btn.closest('.code-block').querySelector('pre');
  navigator.clipboard.writeText(pre.textContent).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}

function saveProject(projectData) {
  const existing = savedProjects.findIndex(p => p.title === projectData.title);
  if (existing >= 0) { showToast('Blueprint already in library!'); return; }
  savedProjects.push({ ...projectData, savedAt: new Date().toISOString() });
  localStorage.setItem('iotech_saved', JSON.stringify(savedProjects));
  showToast('Blueprint saved to library!');
}

function showError(msg) {
  const result = document.getElementById('projectResult');
  if (!result) return;
  result.innerHTML = `
    <div class="text-center py-12">
      <span class="material-symbols-outlined text-red-500 text-5xl mb-4">error</span>
      <p class="text-red-500 font-mono">${escapeHtml(msg)}</p>
    </div>`;
  result.classList.remove('hidden');
}

function showToast(msg) {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">info</span> ${escapeHtml(msg)}</div>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
