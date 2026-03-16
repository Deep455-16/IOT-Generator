/* ============================================================
   IoT FORGE — Frontend App Logic
   ============================================================ */

const API_BASE = 'http://localhost:5000';
let currentDifficulty = 'Beginner';
let savedProjects = JSON.parse(localStorage.getItem('iotforge_saved') || '[]');

// ---- Difficulty Buttons ----
document.querySelectorAll('.diff-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentDifficulty = btn.dataset.val;
  });
});

// ---- Set Topic from Chip ----
function setTopic(text) {
  document.getElementById('topicInput').value = text;
  document.getElementById('topicInput').focus();
}

// ---- Generate Project ----
document.getElementById('generateBtn').addEventListener('click', generateProject);
document.getElementById('topicInput').addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'Enter') generateProject();
});

async function generateProject() {
  const topic = document.getElementById('topicInput').value.trim();
  const category = document.getElementById('categorySelect').value;

  if (!topic) { showToast('⚠ Please enter a project topic'); return; }

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.querySelector('.btn-text').textContent = 'Generating...';

  document.getElementById('outputPlaceholder').style.display = 'none';
  document.getElementById('projectResult').style.display = 'none';
  document.getElementById('loadingState').style.display = 'flex';

  startLoaderMessages();

  // Scroll to output
  document.getElementById('outputPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });

  try {
    const res = await fetch(`${API_BASE}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, difficulty: currentDifficulty, category })
    });
    const data = await res.json();

    if (data.success) {
      renderProject(data.project);
    } else {
      showError(data.error || 'Failed to generate project');
    }
  } catch (err) {
    showError('Could not connect to the backend server. Make sure the Flask server is running on port 5000.');
  } finally {
    btn.disabled = false;
    btn.querySelector('.btn-text').textContent = 'Generate Project';
    document.getElementById('loadingState').style.display = 'none';
    stopLoaderMessages();
  }
}

// ---- Loader Messages Cycle ----
let loaderInterval;
function startLoaderMessages() {
  const msgs = document.querySelectorAll('.loader-msg');
  let i = 0;
  msgs.forEach(m => m.classList.remove('active'));
  msgs[0].classList.add('active');
  loaderInterval = setInterval(() => {
    msgs[i].classList.remove('active');
    i = (i + 1) % msgs.length;
    msgs[i].classList.add('active');
  }, 1800);
}
function stopLoaderMessages() {
  clearInterval(loaderInterval);
  document.querySelectorAll('.loader-msg').forEach(m => m.classList.remove('active'));
}

// ---- Render Project ----
function renderProject(p) {
  const result = document.getElementById('projectResult');
  result.innerHTML = `
    <div class="project-header">
      <div class="project-header-top">
        <div class="project-badges">
          <span class="badge badge-cat">${p.category}</span>
          <span class="badge badge-diff-${p.difficulty}">${p.difficulty}</span>
        </div>
        <button class="project-save-btn" id="saveProjectBtn">✦ Save Project</button>
      </div>
      <h2 class="project-title">${p.title}</h2>
      <p class="project-tagline">${p.tagline}</p>
      <div class="project-meta">
        <span class="meta-item"><span class="meta-icon">⏱</span>${p.estimated_time}</span>
        <span class="meta-item"><span class="meta-icon">💰</span>${p.estimated_cost}</span>
        <span class="meta-item"><span class="meta-icon">🔧</span>${p.components?.length || 0} Components</span>
        <span class="meta-item"><span class="meta-icon">📋</span>${p.steps?.length || 0} Steps</span>
      </div>
    </div>

    <div class="tabs-bar">
      <button class="tab-btn active" onclick="switchTab(this, 'overview')">Overview</button>
      <button class="tab-btn" onclick="switchTab(this, 'components')">Components</button>
      <button class="tab-btn" onclick="switchTab(this, 'architecture')">Architecture</button>
      <button class="tab-btn" onclick="switchTab(this, 'steps')">Steps</button>
      <button class="tab-btn" onclick="switchTab(this, 'code')">Code</button>
      <button class="tab-btn" onclick="switchTab(this, 'testing')">Testing</button>
      <button class="tab-btn" onclick="switchTab(this, 'troubleshoot')">Debug</button>
      <button class="tab-btn" onclick="switchTab(this, 'extensions')">Extensions</button>
    </div>

    ${renderOverviewTab(p)}
    ${renderComponentsTab(p)}
    ${renderArchTab(p)}
    ${renderStepsTab(p)}
    ${renderCodeTab(p)}
    ${renderTestingTab(p)}
    ${renderTroubleshootTab(p)}
    ${renderExtensionsTab(p)}
  `;
  result.style.display = 'block';
  result.style.width = '100%';

  // Attach save button
  document.getElementById('saveProjectBtn').addEventListener('click', () => saveProject(p));

  // Override output-panel centering
  document.getElementById('outputPanel').style.alignItems = 'flex-start';
  document.getElementById('outputPanel').style.justifyContent = 'flex-start';
}

function renderOverviewTab(p) {
  return `
  <div class="tab-content active" id="tab-overview">
    <div class="overview-grid">
      <div class="info-box"><div class="info-box-label">Estimated Time</div><div class="info-box-value">${p.estimated_time}</div></div>
      <div class="info-box"><div class="info-box-label">Estimated Cost</div><div class="info-box-value">${p.estimated_cost}</div></div>
      <div class="info-box"><div class="info-box-label">Difficulty</div><div class="info-box-value">${p.difficulty}</div></div>
      <div class="info-box"><div class="info-box-label">Category</div><div class="info-box-value">${p.category}</div></div>
    </div>
    <p class="overview-text">${p.overview}</p>
    ${p.prerequisites?.length ? `
    <div class="section-subtitle">Prerequisites</div>
    <ul class="list-items">${p.prerequisites.map(x => `<li>${x}</li>`).join('')}</ul>` : ''}
    ${p.learning_outcomes?.length ? `
    <div class="section-subtitle" style="margin-top:1.5rem">What You'll Learn</div>
    <ul class="list-items">${p.learning_outcomes.map(x => `<li>${x}</li>`).join('')}</ul>` : ''}
    ${p.tools_required?.length ? `
    <div class="section-subtitle" style="margin-top:1.5rem">Tools Required</div>
    <ul class="list-items">${p.tools_required.map(x => `<li>${x}</li>`).join('')}</ul>` : ''}
  </div>`;
}

function renderComponentsTab(p) {
  const comps = p.components || [];
  return `
  <div class="tab-content" id="tab-components">
    <div class="section-subtitle">Bill of Materials</div>
    <table class="components-table">
      <thead>
        <tr>
          <th>Component</th>
          <th>Qty</th>
          <th>Purpose</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        ${comps.map(c => `
        <tr>
          <td>${c.name}</td>
          <td><span class="qty-badge">×${c.quantity}</span></td>
          <td>${c.purpose}</td>
          <td><span class="cost-tag">${c.approximate_cost}</span></td>
        </tr>`).join('')}
      </tbody>
    </table>
    ${p.circuit_description ? `
    <div class="section-subtitle" style="margin-top:2rem">Circuit Description</div>
    <div class="code-explanation">${p.circuit_description}</div>` : ''}
  </div>`;
}

function renderArchTab(p) {
  const arch = p.architecture || {};
  const layers = arch.layers || [];
  return `
  <div class="tab-content" id="tab-architecture">
    ${arch.description ? `<p class="overview-text">${arch.description}</p>` : ''}
    <div class="section-subtitle">System Layers</div>
    ${layers.map((l, i) => `
    <div class="arch-layer">
      <span class="arch-layer-num">L${i+1}</span>
      <div>
        <div class="arch-layer-title">${l.name}</div>
        <div class="arch-layer-desc">${l.description}</div>
        ${l.components?.length ? `
        <div class="arch-comps">${l.components.map(c => `<span class="arch-comp-tag">${c}</span>`).join('')}</div>` : ''}
      </div>
    </div>`).join('')}
  </div>`;
}

function renderStepsTab(p) {
  const steps = p.steps || [];
  return `
  <div class="tab-content" id="tab-steps">
    <div class="section-subtitle">${steps.length} Steps to Build</div>
    <div class="steps-list">
      ${steps.map(s => `
      <div class="step-card">
        <div class="step-header" onclick="toggleStep(this)">
          <span class="step-num">STEP ${s.step_number}</span>
          <span class="step-title-text">${s.title}</span>
          <span class="step-duration">${s.duration || ''}</span>
          <span class="step-toggle">▼</span>
        </div>
        <div class="step-body">
          <p class="step-description">${s.description}</p>
          ${s.code_snippet ? `
          <div class="code-block">
            <div class="code-header">
              <span class="code-lang">Code</span>
              <button class="copy-btn" onclick="copyCode(this)">Copy</button>
            </div>
            <pre>${escapeHtml(s.code_snippet)}</pre>
          </div>` : ''}
          ${s.tips?.length ? `
          <div class="tips-list">
            ${s.tips.map(t => `<div class="tip-item"><span class="tip-icon">💡</span>${t}</div>`).join('')}
          </div>` : ''}
        </div>
      </div>`).join('')}
    </div>
  </div>`;
}

function renderCodeTab(p) {
  const code = p.code || {};
  return `
  <div class="tab-content" id="tab-code">
    <div class="section-subtitle">Full Source Code — ${code.language || 'Code'}</div>
    <div class="code-full-block">
      <div class="code-block">
        <div class="code-header">
          <span class="code-lang">${code.language || 'Code'}</span>
          <button class="copy-btn" onclick="copyCode(this)">Copy</button>
        </div>
        <pre>${escapeHtml(code.main_code || '')}</pre>
      </div>
    </div>
    ${code.explanation ? `
    <div class="section-subtitle">Code Explanation</div>
    <div class="code-explanation">${code.explanation}</div>` : ''}
  </div>`;
}

function renderTestingTab(p) {
  const t = p.testing || {};
  return `
  <div class="tab-content" id="tab-testing">
    <div class="section-subtitle">Testing Procedure</div>
    <ul class="list-items" style="margin-bottom:1.5rem">
      ${(t.steps || []).map(s => `<li>${s}</li>`).join('')}
    </ul>
    ${t.expected_output ? `
    <div class="section-subtitle">Expected Output</div>
    <div class="code-explanation">${t.expected_output}</div>` : ''}
  </div>`;
}

function renderTroubleshootTab(p) {
  const items = p.troubleshooting || [];
  return `
  <div class="tab-content" id="tab-troubleshoot">
    <div class="section-subtitle">Common Issues & Fixes</div>
    <div class="trouble-list">
      ${items.map(i => `
      <div class="trouble-item">
        <div class="trouble-problem">${i.problem}</div>
        <div class="trouble-solution">${i.solution}</div>
      </div>`).join('')}
    </div>
  </div>`;
}

function renderExtensionsTab(p) {
  const exts = p.extensions || [];
  return `
  <div class="tab-content" id="tab-extensions">
    <div class="section-subtitle">Take It Further</div>
    <p style="color:var(--text-muted);font-size:0.88rem;margin-bottom:1.5rem">Click any extension idea to generate a full project for it!</p>
    <div class="extensions-grid">
      ${exts.map(e => `
      <div class="extension-card" onclick="setTopic('${e.replace(/'/g, "\\'")}')">
        <div class="ext-icon">🚀</div>
        ${e}
      </div>`).join('')}
    </div>
  </div>`;
}

// ---- Tab Switching ----
function switchTab(btn, tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  const tabEl = document.getElementById('tab-' + tabId);
  if (tabEl) tabEl.classList.add('active');
}

// ---- Step Toggle ----
function toggleStep(header) {
  const body = header.nextElementSibling;
  const toggle = header.querySelector('.step-toggle');
  body.classList.toggle('open');
  toggle.classList.toggle('open');
}

// ---- Copy Code ----
function copyCode(btn) {
  const pre = btn.closest('.code-block').querySelector('pre');
  navigator.clipboard.writeText(pre.textContent).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}

// ---- Quick Ideas ----
document.getElementById('ideasBtn').addEventListener('click', generateIdeas);

async function generateIdeas() {
  const category = document.getElementById('ideasCategory').value;
  const difficulty = document.getElementById('ideasDifficulty').value;
  const btn = document.getElementById('ideasBtn');
  const grid = document.getElementById('ideasGrid');

  btn.disabled = true;
  btn.querySelector('span').textContent = 'Generating...';
  grid.innerHTML = '<div class="ideas-placeholder">✦ Generating ideas...</div>';

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
      grid.innerHTML = `<div class="ideas-placeholder">Error: ${data.error}</div>`;
    }
  } catch (err) {
    grid.innerHTML = '<div class="ideas-placeholder">Could not connect to backend server.</div>';
  } finally {
    btn.disabled = false;
    btn.querySelector('span').textContent = 'Spark Ideas';
  }
}

function renderIdeas(ideas) {
  const grid = document.getElementById('ideasGrid');
  grid.innerHTML = ideas.map(idea => `
    <div class="idea-card">
      <div class="idea-card-title">${idea.title}</div>
      <div class="idea-card-desc">${idea.description}</div>
      <div class="idea-card-components">
        ${(idea.components || []).map(c => `<span class="comp-tag">${c}</span>`).join('')}
      </div>
      <div class="idea-wow">✦ ${idea.wow_factor}</div>
      <button class="idea-generate-btn" onclick="generateFromIdea('${idea.title.replace(/'/g, "\\'")}')">
        Generate Full Project →
      </button>
    </div>
  `).join('');
}

function generateFromIdea(title) {
  setTopic(title);
  document.getElementById('generator').scrollIntoView({ behavior: 'smooth' });
  setTimeout(() => generateProject(), 400);
}

// ---- Save / Load Projects ----
function saveProject(projectData) {
  // If called with string (from onclick attribute)
  if (typeof projectData === 'string') {
    try { projectData = JSON.parse(projectData); } catch(e) {}
  }
  const existing = savedProjects.findIndex(p => p.title === projectData.title);
  if (existing >= 0) { showToast('Project already saved!'); return; }
  savedProjects.push({ ...projectData, savedAt: new Date().toISOString() });
  localStorage.setItem('iotforge_saved', JSON.stringify(savedProjects));
  renderSaved();
  showToast('✦ Project saved!');
}

function renderSaved() {
  const grid = document.getElementById('savedGrid');
  if (!savedProjects.length) {
    grid.innerHTML = '<div class="saved-placeholder">No saved projects yet. Generate and save your first project!</div>';
    return;
  }
  grid.innerHTML = savedProjects.map((p, i) => `
    <div class="saved-card">
      <div class="saved-card-title">${p.title}</div>
      <div class="saved-card-meta">${p.category} · ${p.difficulty} · Saved ${new Date(p.savedAt).toLocaleDateString()}</div>
      <div class="saved-card-actions">
        <button class="saved-view-btn" onclick="viewSaved(${i})">View</button>
        <button class="saved-delete-btn" onclick="deleteSaved(${i})">Delete</button>
      </div>
    </div>
  `).join('');
}

function viewSaved(index) {
  const p = savedProjects[index];
  renderProject(p);
  document.getElementById('generator').scrollIntoView({ behavior: 'smooth' });
}

function deleteSaved(index) {
  savedProjects.splice(index, 1);
  localStorage.setItem('iotforge_saved', JSON.stringify(savedProjects));
  renderSaved();
  showToast('Project deleted');
}

// ---- Error Display ----
function showError(msg) {
  const result = document.getElementById('projectResult');
  result.innerHTML = `
    <div style="padding:2rem;text-align:center">
      <div style="font-size:2rem;margin-bottom:1rem">⚠</div>
      <p style="color:var(--red);font-family:var(--font-mono);font-size:0.88rem">${msg}</p>
    </div>`;
  result.style.display = 'block';
  document.getElementById('outputPanel').style.alignItems = 'center';
  document.getElementById('outputPanel').style.justifyContent = 'center';
}

// ---- Toast ----
let toastTimeout;
function showToast(msg) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => toast.classList.remove('show'), 3000);
}

// ---- Utils ----
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ---- Init ----
renderSaved();

// Expose saveProject globally for onclick attributes
window.saveProject = function(encoded) {
  try {
    const projectData = JSON.parse(decodeURIComponent(encoded));
    saveProject(projectData);
  } catch(e) {
    // If it's already a parsed object passed directly
    saveProject(encoded);
  }
};
