/* ═══════════════════════════════════════════════
   IoT FORGE — main.css  (3-D Edition)
   Palette: #0a0e1a (obsidian) · #00f5a0 (emerald) · #0ff (cyan)
   Fonts: Orbitron (display) · Space Grotesk (body) · JetBrains Mono (code)
═══════════════════════════════════════════════ */

/* ─── RESET & BASE ─── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #0a0e1a;
  --bg2:      #0f1423;
  --bg3:      #141929;
  --surface:  #181f30;
  --surface2: #1e273d;
  --border:   #ffffff0f;
  --border2:  #ffffff18;
  --em:       #00f5a0;
  --em2:      #00c8ff;
  --em3:      #7b5ea7;
  --text:     #e8ecf4;
  --text2:    #8b93a8;
  --text3:    #545e74;
  --red:      #ff4d6d;
  --amber:    #fbbf24;

  --r-sm: 8px;
  --r-md: 12px;
  --r-lg: 18px;
  --r-xl: 24px;

  --shadow-sm: 0 2px 8px #00000040;
  --shadow-md: 0 8px 32px #00000060;
  --shadow-lg: 0 24px 64px #00000080;
  --glow-em:  0 0 24px #00f5a030, 0 0 80px #00f5a010;
  --glow-em2: 0 0 24px #00c8ff30;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

html { scroll-behavior: smooth; }

body {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  line-height: 1.65;
  color: var(--text);
  background: var(--bg);
  overflow-x: hidden;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--em); }

/* ─── BG CANVAS ─── */
.bg-canvas {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  overflow: hidden;
}
#particleCanvas { position: absolute; inset: 0; width: 100%; height: 100%; }

.grid-overlay {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(var(--border) 1px, transparent 1px),
    linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 100%);
}

.glow-orb {
  position: absolute; border-radius: 50%;
  filter: blur(120px); opacity: 0.18;
  animation: orbFloat 12s ease-in-out infinite alternate;
}
.glow-1 { width: 600px; height: 600px; background: var(--em); top: -200px; right: -150px; animation-delay: 0s; }
.glow-2 { width: 500px; height: 500px; background: var(--em2); bottom: -150px; left: -100px; animation-delay: -4s; }
.glow-3 { width: 400px; height: 400px; background: var(--em3); top: 40%; left: 30%; animation-delay: -8s; }

@keyframes orbFloat {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(40px, 30px) scale(1.1); }
}

/* ─── NAVBAR ─── */
.navbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  padding: 0 2rem;
  background: #0a0e1a88;
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border);
  transition: var(--transition);
}
.navbar.scrolled {
  background: #0a0e1acc;
  box-shadow: 0 4px 32px #00000060;
}
.nav-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; gap: 2rem;
  height: 64px;
}
.logo {
  display: flex; align-items: center; gap: 10px;
  text-decoration: none; color: inherit;
  flex-shrink: 0;
}
.logo-icon {
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  background: #00f5a010;
  border: 1px solid #00f5a030;
  border-radius: 8px;
  transition: var(--transition);
}
.logo:hover .logo-icon { background: #00f5a020; box-shadow: var(--glow-em); }
.logo-text {
  font-family: 'Orbitron', monospace;
  font-size: 15px; font-weight: 400; letter-spacing: 1px;
}
.logo-text strong { color: var(--em); font-weight: 700; }

.nav-links {
  display: flex; align-items: center; gap: 0.25rem;
  margin-left: auto;
}
.nav-link {
  padding: 6px 14px;
  color: var(--text2); font-size: 13px; font-weight: 500;
  text-decoration: none; border-radius: 6px;
  transition: var(--transition);
}
.nav-link:hover { color: var(--text); background: var(--surface); }

.nav-badge {
  margin-left: 8px; padding: 4px 10px;
  background: #00f5a015; border: 1px solid #00f5a030;
  border-radius: 99px; color: var(--em);
  font-size: 11px; font-family: 'JetBrains Mono', monospace;
  font-weight: 500; letter-spacing: 0.5px;
}

.nav-menu-btn {
  display: none; flex-direction: column; gap: 5px;
  background: none; border: none; cursor: pointer; padding: 4px;
}
.nav-menu-btn span {
  width: 20px; height: 1.5px; background: var(--text2); border-radius: 2px;
  transition: var(--transition);
}

/* ─── HERO ─── */
.hero {
  position: relative; z-index: 1;
  min-height: 100vh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  padding: 8rem 2rem 6rem;
}

.hero-label {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px;
  background: #00f5a010; border: 1px solid #00f5a025;
  border-radius: 99px;
  font-size: 12px; font-weight: 500;
  color: var(--em); letter-spacing: 0.5px;
  margin-bottom: 2rem;
  font-family: 'JetBrains Mono', monospace;
}
.pulse-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--em);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.7); }
}

.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(2.4rem, 6vw, 5rem);
  font-weight: 700; line-height: 1.1;
  letter-spacing: -1px;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 80px #00f5a010;
}
.hero-accent {
  background: linear-gradient(135deg, var(--em) 0%, var(--em2) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.05rem; color: var(--text2);
  max-width: 560px; margin: 0 auto 3rem;
  line-height: 1.7;
}

.hero-stats {
  display: flex; align-items: center; gap: 0;
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: var(--r-lg);
  padding: 1.5rem 2.5rem;
  margin-bottom: 2.5rem;
  box-shadow: var(--shadow-md), inset 0 1px 0 #ffffff08;
  /* 3D card effect */
  transform: perspective(600px) rotateX(3deg);
  transition: transform 0.4s ease;
}
.hero-stats:hover { transform: perspective(600px) rotateX(0deg); }

.stat-card { text-align: center; padding: 0 2rem; }
.stat-num {
  font-family: 'Orbitron', monospace;
  font-size: 2rem; font-weight: 700;
  color: var(--em);
}
.stat-plus { display: inline; font-size: 1.4rem; color: var(--em); font-weight: 700; }
.stat-sym {
  font-family: 'Orbitron', monospace;
  font-size: 2rem; font-weight: 700;
  color: var(--em2);
}
.stat-label { font-size: 12px; color: var(--text3); letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }
.stat-divider { width: 1px; height: 60px; background: var(--border2); flex-shrink: 0; }

.hero-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 28px;
  background: var(--em); color: #000;
  border-radius: var(--r-sm); font-weight: 600; font-size: 14px;
  text-decoration: none;
  transition: var(--transition);
  box-shadow: var(--glow-em);
}
.hero-cta:hover {
  background: #00ffaa;
  transform: translateY(-2px);
  box-shadow: 0 8px 32px #00f5a040;
}

/* ─── FLOATING CHIPS ─── */
.chip {
  position: absolute;
  padding: 6px 14px;
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: 99px;
  font-size: 11px; font-weight: 500;
  color: var(--text2);
  font-family: 'JetBrains Mono', monospace;
  pointer-events: none;
  animation: chipFloat 6s ease-in-out infinite;
}
.chip-1 { top: 20%; left: 8%; animation-delay: 0s; color: var(--em); border-color: #00f5a030; }
.chip-2 { top: 35%; right: 7%; animation-delay: -1.5s; color: var(--em2); border-color: #00c8ff30; }
.chip-3 { bottom: 30%; left: 5%; animation-delay: -3s; }
.chip-4 { bottom: 25%; right: 9%; animation-delay: -4.5s; }
.chip-5 { top: 55%; left: 12%; animation-delay: -2s; }

@keyframes chipFloat {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-12px); }
}

/* ─── SECTIONS ─── */
.section { position: relative; z-index: 1; padding: 6rem 0; }
.section-alt { background: var(--bg2); }

.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }

.section-header {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 0.5rem;
}
.section-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: var(--em);
}
.section-label {
  font-size: 11px; font-weight: 600; letter-spacing: 2px;
  text-transform: uppercase; color: var(--text3);
}
.section-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(1.6rem, 3vw, 2.4rem);
  font-weight: 700; margin-bottom: 3rem;
  letter-spacing: -0.5px;
}

/* ─── GENERATOR LAYOUT ─── */
.generator-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* ─── PANELS ─── */
.panel {
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: var(--r-xl);
  padding: 2rem;
  position: relative; overflow: hidden;
  /* 3D lift */
  box-shadow: var(--shadow-md),
              inset 0 1px 0 #ffffff08,
              0 1px 0 #ffffff05;
  transform: perspective(800px) rotateY(-1deg) rotateX(1deg);
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.panel:hover {
  transform: perspective(800px) rotateY(0deg) rotateX(0deg);
  box-shadow: var(--shadow-lg), inset 0 1px 0 #ffffff10;
}
.panel-output {
  transform: perspective(800px) rotateY(1deg) rotateX(1deg);
  min-height: 420px;
}
.panel-output:hover { transform: perspective(800px) rotateY(0deg) rotateX(0deg); }

.panel-glow {
  position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(ellipse 60% 40% at 80% 0%, #00c8ff08 0%, transparent 70%);
}
.panel-glow-green {
  background: radial-gradient(ellipse 60% 40% at 20% 100%, #00f5a008 0%, transparent 70%);
}

/* ─── FORM FIELDS ─── */
.field-group { display: flex; flex-direction: column; gap: 8px; margin-bottom: 1.25rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.field-label {
  font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--text3);
}

.input-wrapper { position: relative; }
.field-textarea {
  width: 100%; min-height: 110px; resize: vertical;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--r-md);
  padding: 12px 14px;
  color: var(--text); font-family: 'Space Grotesk', sans-serif; font-size: 14px;
  line-height: 1.6; outline: none;
  transition: border-color var(--transition), box-shadow var(--transition);
}
.field-textarea::placeholder { color: var(--text3); }
.field-textarea:focus {
  border-color: #00f5a050;
  box-shadow: 0 0 0 3px #00f5a010;
}

.select-wrapper { position: relative; }
.field-select {
  width: 100%; appearance: none;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--r-sm);
  padding: 10px 36px 10px 12px;
  color: var(--text); font-family: 'Space Grotesk', sans-serif; font-size: 14px;
  cursor: pointer; outline: none;
  transition: border-color var(--transition), box-shadow var(--transition);
}
.field-select:focus { border-color: #00f5a050; box-shadow: 0 0 0 3px #00f5a010; }
.select-arrow {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  color: var(--text3); pointer-events: none;
}

/* ─── GENERATE BUTTON ─── */
.btn-generate {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--em) 0%, #00d4aa 100%);
  color: #000; font-weight: 700; font-size: 14px; font-family: 'Space Grotesk', sans-serif;
  border: none; border-radius: var(--r-md); cursor: pointer;
  position: relative; overflow: hidden;
  transition: var(--transition);
  box-shadow: var(--glow-em);
  letter-spacing: 0.3px;
}
.btn-generate:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px #00f5a050;
}
.btn-generate:active { transform: translateY(0); }

.btn-shimmer {
  position: absolute; inset: 0;
  background: linear-gradient(105deg, transparent 40%, #ffffff30 50%, transparent 60%);
  transform: translateX(-100%);
  animation: shimmer 3s ease-in-out infinite;
}
@keyframes shimmer {
  0%   { transform: translateX(-100%); }
  60%  { transform: translateX(100%); }
  100% { transform: translateX(100%); }
}

/* ─── QUICK TRIES ─── */
.quick-tries {
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
  margin-top: 1rem;
}
.tries-label { font-size: 11px; color: var(--text3); font-weight: 500; white-space: nowrap; }
.try-pill {
  padding: 4px 12px;
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: 99px;
  font-size: 11px; color: var(--text2); font-family: 'Space Grotesk', sans-serif;
  cursor: pointer; transition: var(--transition); white-space: nowrap;
}
.try-pill:hover { border-color: #00f5a040; color: var(--em); background: #00f5a008; }

/* ─── OUTPUT IDLE ─── */
.output-idle {
  height: 100%; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; gap: 12px; padding: 3rem 1rem;
}
.idle-icon { animation: idlePulse 3s ease-in-out infinite; }
@keyframes idlePulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50%       { opacity: 0.9; transform: scale(1.05); }
}
.idle-title { font-size: 15px; font-weight: 600; color: var(--text); }
.idle-sub { font-size: 13px; color: var(--text3); }

/* ─── LOADING ─── */
.output-loading {
  padding: 2rem 1rem; display: flex; flex-direction: column; gap: 1.5rem;
}
.loading-steps { display: flex; flex-direction: column; gap: 12px; }
.load-step {
  display: flex; align-items: center; gap: 12px;
  font-size: 13px; color: var(--text3);
  transition: var(--transition);
}
.load-step.active { color: var(--text); }
.load-step.done   { color: var(--em); }
.load-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--text3); flex-shrink: 0;
  transition: var(--transition);
}
.load-step.active .load-dot { background: var(--em2); animation: pulse 1s infinite; }
.load-step.done   .load-dot { background: var(--em); }

.loading-bar {
  height: 3px; background: var(--bg3);
  border-radius: 99px; overflow: hidden;
}
.loading-fill {
  height: 100%; width: 0%;
  background: linear-gradient(90deg, var(--em), var(--em2));
  border-radius: 99px; transition: width 0.5s ease;
}

/* ─── RESULT ─── */
.output-result { display: flex; flex-direction: column; gap: 1rem; }
.result-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.result-title-row { display: flex; flex-direction: column; gap: 6px; }
.result-project-title { font-family: 'Orbitron', monospace; font-size: 15px; font-weight: 600; }
.result-badges { display: flex; gap: 6px; }
.result-badge {
  padding: 3px 9px; border-radius: 99px;
  font-size: 10px; font-weight: 600; letter-spacing: 0.5px;
  text-transform: uppercase; font-family: 'JetBrains Mono', monospace;
}
.badge-diff { background: #00c8ff15; color: var(--em2); border: 1px solid #00c8ff30; }
.badge-cat  { background: #00f5a015; color: var(--em); border: 1px solid #00f5a030; }

.result-actions { display: flex; gap: 6px; flex-shrink: 0; }
.icon-btn {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: var(--r-sm); color: var(--text2);
  cursor: pointer; transition: var(--transition);
}
.icon-btn:hover { border-color: #00f5a040; color: var(--em); }

.result-tabs { display: flex; gap: 2px; border-bottom: 1px solid var(--border); padding-bottom: 0; }
.rtab {
  padding: 7px 14px; border-bottom: 2px solid transparent; margin-bottom: -1px;
  font-size: 12px; font-weight: 500; color: var(--text3);
  background: none; border-top: none; border-left: none; border-right: none;
  cursor: pointer; transition: var(--transition);
  font-family: 'Space Grotesk', sans-serif;
}
.rtab:hover { color: var(--text); }
.rtab.active { color: var(--em); border-bottom-color: var(--em); }

.result-content {
  font-size: 13px; line-height: 1.7; color: var(--text2);
  max-height: 320px; overflow-y: auto;
}
.result-content h4 { font-family: 'Orbitron', monospace; font-size: 12px; color: var(--em); margin: 1rem 0 0.5rem; }
.result-content ul { padding-left: 1.2rem; }
.result-content li { margin-bottom: 4px; }
.result-content pre {
  background: var(--bg); padding: 1rem;
  border-radius: var(--r-sm); border: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace; font-size: 12px;
  overflow-x: auto; color: var(--em);
  white-space: pre-wrap;
}
.result-content .step-item {
  display: flex; gap: 10px; margin-bottom: 10px;
}
.step-num {
  width: 22px; height: 22px; border-radius: 50%;
  background: #00f5a020; border: 1px solid #00f5a040;
  color: var(--em); font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px;
}

/* ─── FILTERS ─── */
.ideas-filters {
  display: flex; flex-wrap: wrap; gap: 1.5rem;
  align-items: flex-end; margin-bottom: 2rem;
}
.filter-group { display: flex; flex-direction: column; gap: 8px; }
.filter-label {
  font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--text3);
}
.filter-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.fpill {
  padding: 5px 12px;
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: 99px; font-size: 12px; color: var(--text2);
  cursor: pointer; transition: var(--transition);
  font-family: 'Space Grotesk', sans-serif;
}
.fpill:hover  { border-color: #00f5a040; color: var(--em); }
.fpill.active { background: #00f5a015; border-color: #00f5a050; color: var(--em); }

.btn-spark {
  padding: 10px 22px;
  background: linear-gradient(135deg, var(--em2) 0%, #0080ff 100%);
  color: #fff; font-weight: 600; font-size: 13px;
  border: none; border-radius: var(--r-sm); cursor: pointer;
  position: relative; overflow: hidden;
  transition: var(--transition); margin-left: auto;
  font-family: 'Space Grotesk', sans-serif;
  box-shadow: var(--glow-em2);
}
.btn-spark:hover { transform: translateY(-2px); box-shadow: 0 8px 32px #00c8ff40; }

/* ─── IDEAS GRID ─── */
.ideas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}
.ideas-placeholder {
  grid-column: 1/-1; text-align: center; padding: 3rem;
  color: var(--text3); font-size: 14px;
}
.ideas-placeholder strong { color: var(--em2); }

.idea-card {
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: var(--r-lg); padding: 1.25rem;
  cursor: pointer; transition: var(--transition);
  /* 3D card effect */
  transform: perspective(500px) rotateX(2deg);
  box-shadow: var(--shadow-sm), inset 0 1px 0 #ffffff06;
  position: relative; overflow: hidden;
}
.idea-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, #00f5a005 0%, transparent 60%);
  opacity: 0; transition: var(--transition);
}
.idea-card:hover {
  border-color: #00f5a030;
  transform: perspective(500px) rotateX(0deg) translateY(-4px);
  box-shadow: var(--shadow-md), var(--glow-em);
}
.idea-card:hover::before { opacity: 1; }

.idea-badges { display: flex; gap: 6px; margin-bottom: 10px; }
.idea-cat { font-size: 10px; padding: 3px 8px; border-radius: 99px; }
.diff-beginner     { background: #00f5a010; color: var(--em); border: 1px solid #00f5a025; }
.diff-intermediate { background: #fbbf2410; color: var(--amber); border: 1px solid #fbbf2425; }
.diff-advanced     { background: #ff4d6d10; color: var(--red); border: 1px solid #ff4d6d25; }

.idea-title { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
.idea-desc { font-size: 12px; color: var(--text3); line-height: 1.55; }
.idea-action {
  display: flex; align-items: center; gap: 4px;
  font-size: 11px; color: var(--em2); margin-top: 10px;
  opacity: 0; transition: var(--transition);
}
.idea-card:hover .idea-action { opacity: 1; }

/* ─── SAVED GRID ─── */
.saved-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem; min-height: 200px;
}
.saved-empty {
  grid-column: 1/-1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 8px; padding: 4rem; text-align: center;
}
.empty-icon { margin-bottom: 8px; }
.saved-empty p { color: var(--text2); font-size: 15px; }
.saved-empty small { color: var(--text3); font-size: 13px; }

.saved-card {
  background: var(--surface); border: 1px solid var(--border2);
  border-radius: var(--r-lg); padding: 1.25rem;
  transition: var(--transition);
  transform: perspective(500px) rotateX(2deg);
  box-shadow: var(--shadow-sm), inset 0 1px 0 #ffffff06;
}
.saved-card:hover {
  border-color: #7b5ea730; transform: perspective(500px) rotateX(0deg) translateY(-3px);
  box-shadow: var(--shadow-md), 0 0 24px #7b5ea720;
}
.saved-card-title { font-weight: 600; font-size: 13px; margin-bottom: 6px; }
.saved-card-meta { font-size: 11px; color: var(--text3); margin-bottom: 12px; }
.saved-card-actions { display: flex; gap: 6px; }
.sc-btn {
  flex: 1; padding: 6px 10px;
  background: var(--bg3); border: 1px solid var(--border2);
  border-radius: 6px; color: var(--text2); font-size: 11px;
  cursor: pointer; transition: var(--transition); text-align: center;
  font-family: 'Space Grotesk', sans-serif;
}
.sc-btn:hover { border-color: #00f5a040; color: var(--em); }
.sc-btn-del:hover { border-color: #ff4d6d40; color: var(--red); }

/* ─── FOOTER ─── */
.footer {
  position: relative; z-index: 1;
  padding: 2rem;
  border-top: 1px solid var(--border);
  background: var(--bg);
}
.footer-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; gap: 1.5rem;
  flex-wrap: wrap;
}
.footer-tagline { font-size: 13px; color: var(--text3); }

/* ─── TOAST ─── */
.toast {
  position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
  padding: 12px 20px;
  background: var(--surface); border: 1px solid var(--border2);
  border-radius: var(--r-md);
  font-size: 13px; color: var(--text);
  box-shadow: var(--shadow-md);
  opacity: 0; transform: translateY(8px);
  transition: all 0.3s ease;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.toast.success { border-color: #00f5a040; color: var(--em); }

/* ─── RESPONSIVE ─── */
@media (max-width: 900px) {
  .generator-layout { grid-template-columns: 1fr; }
  .hero-stats {
    flex-direction: column; gap: 1rem; padding: 1.5rem;
    transform: none;
  }
  .stat-divider { width: 60px; height: 1px; }
  .chip { display: none; }
  .nav-links { display: none; }
  .nav-menu-btn { display: flex; }
  .panel { transform: none; }
  .panel:hover { transform: none; }
  .idea-card { transform: none; }
  .idea-card:hover { transform: translateY(-3px); }
}

@media (max-width: 600px) {
  .hero { padding: 6rem 1.5rem 4rem; }
  .section { padding: 4rem 0; }
  .field-row { grid-template-columns: 1fr; }
  .ideas-filters { flex-direction: column; }
  .btn-spark { margin-left: 0; width: 100%; }
}
