import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sadia's Quest",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
      .stApp {background: #0a0a14;}
      iframe {display: block; margin: 0 auto; border: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Sadia's Quest</title>
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body {
    margin: 0; padding: 0; background: #0a0a14;
    font-family: 'Courier New', monospace; color: #fff;
    touch-action: none; overflow: hidden; user-select: none;
    -webkit-user-select: none; height: 100%;
  }
  #app {
    display: flex; flex-direction: column; align-items: center;
    gap: 8px; padding: 6px 0; min-height: 100vh;
  }
  #hud {
    display: flex; justify-content: space-between; align-items: center;
    width: 360px; max-width: 96vw; padding: 6px 10px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 8px; font-size: 11px; letter-spacing: 1px;
  }
  #hud .stage { font-weight: bold; color: #ffd966; }
  #hud .zone { color: #b9bcff; }
  #hud .actions { display: flex; gap: 6px; }
  #hud button {
    background: transparent; border: 1px solid rgba(255,255,255,0.3);
    color: #fff; padding: 3px 8px; border-radius: 4px; cursor: pointer;
    font-family: inherit; font-size: 10px; letter-spacing: 1px;
  }
  #hud button:hover { background: rgba(255,255,255,0.1); }
  #canvas-wrap { position: relative; }
  #gameCanvas {
    display: block; background: #2a4f2a; border: 3px solid #ffd966;
    border-radius: 6px; image-rendering: pixelated; image-rendering: crisp-edges;
    box-shadow: 0 0 24px rgba(255,217,102,0.25);
  }
  #toast {
    position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%);
    background: rgba(0,0,0,0.78); padding: 4px 12px; border-radius: 4px;
    font-size: 10px; letter-spacing: 1px; opacity: 0;
    transition: opacity 0.4s; pointer-events: none; white-space: nowrap;
    border: 1px solid #ffd966; color: #ffd966;
  }
  #toast.show { opacity: 1; }
  #dpad {
    display: grid; grid-template-columns: 56px 56px 56px;
    grid-template-rows: 56px 56px 56px; gap: 6px;
    margin-top: 4px; touch-action: none;
  }
  .btn {
    background: rgba(255,255,255,0.12);
    border: 2px solid rgba(255,255,255,0.4);
    border-radius: 12px; color: #fff; font-size: 22px;
    display: flex; justify-content: center; align-items: center;
    user-select: none; cursor: pointer; touch-action: none;
    transition: background 0.08s, border-color 0.08s;
  }
  .btn.pressed { background: rgba(255,217,102,0.4); border-color: #ffd966; }
  #up { grid-column: 2; grid-row: 1; }
  #left { grid-column: 1; grid-row: 2; }
  #right { grid-column: 3; grid-row: 2; }
  #down { grid-column: 2; grid-row: 3; }

  /* ===== Modal ===== */
  #modal-root {
    position: fixed; inset: 0; display: none;
    align-items: center; justify-content: center;
    background: rgba(0,0,0,0.88); z-index: 100; padding: 14px;
    overflow-y: auto;
  }
  #modal-root.show { display: flex; animation: fadeIn 0.3s; }
  @keyframes fadeIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }
  .modal {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    border: 3px solid #ffd966; border-radius: 12px;
    padding: 20px; max-width: 360px; width: 100%;
    box-shadow: 0 0 40px rgba(255,217,102,0.4);
    animation: fadeIn 0.3s;
  }
  .modal h2 {
    margin: 0 0 6px; color: #ffd966; font-size: 15px;
    letter-spacing: 2px; text-transform: uppercase;
  }
  .modal .sub { color: #b9bcff; font-size: 10px; letter-spacing: 1.5px; margin-bottom: 10px; }
  .modal p { margin: 8px 0; font-size: 13px; line-height: 1.5; }
  .modal .prompt { color: #b9bcff; font-style: italic; }
  .modal input[type=text], .modal textarea {
    width: 100%; padding: 9px; margin: 4px 0;
    background: #0a0a14; border: 2px solid #ffd966; color: #fff;
    font-family: inherit; font-size: 14px; border-radius: 4px;
    outline: none;
  }
  .modal input[type=text]:focus, .modal textarea:focus {
    border-color: #ff77aa; box-shadow: 0 0 8px rgba(255,119,170,0.4);
  }
  .modal textarea { resize: vertical; min-height: 80px; }
  .modal label { display: block; font-size: 11px; color: #b9bcff; margin-top: 8px; letter-spacing: 1px; }
  .modal button.submit {
    background: #ffd966; color: #000; border: none;
    padding: 10px 16px; font-family: inherit; font-weight: bold;
    font-size: 13px; border-radius: 4px; cursor: pointer;
    margin-top: 10px; width: 100%; letter-spacing: 2px;
  }
  .modal button.submit:hover { background: #ffe88a; }
  .modal .error { color: #ff6b6b; font-size: 11px; min-height: 14px; margin-top: 4px; }
  .modal .ok { color: #6bff8d; font-weight: bold; font-size: 13px; }

  /* Stage 2 — choices */
  .choices { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 14px 0; }
  .choice-btn {
    padding: 18px; font-size: 22px; font-weight: bold;
    background: #2a2a3e; border: 2px solid #b9bcff; color: #fff;
    border-radius: 6px; cursor: pointer; font-family: inherit;
    transition: all 0.15s;
  }
  .choice-btn:hover { background: #3a3a4e; }
  .choice-btn.wrong { background: #5a1a1a; border-color: #ff6b6b; animation: shake 0.4s; }
  .choice-btn.right { background: #1a5a2a; border-color: #6bff8d; }
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-6px); }
    75% { transform: translateX(6px); }
  }

  /* Stage 3 — terminal */
  .terminal {
    background: #000; color: #00ff41; padding: 12px;
    font-family: 'Courier New', monospace; font-size: 12px;
    border: 1px solid #00ff41; border-radius: 4px;
    min-height: 80px;
  }
  .terminal .line { line-height: 1.5; }
  .terminal input {
    background: transparent; color: #00ff41; border: none;
    outline: none; font-family: inherit; font-size: 13px; width: 80%;
  }
  .terminal .caret::after { content: '_'; animation: blink 0.9s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  .neon {
    color: #ffd966; text-shadow: 0 0 8px #ffd966, 0 0 16px #ff77aa;
    animation: neonPulse 0.6s ease-in-out infinite alternate;
    text-align: center; font-size: 22px; font-weight: bold;
    letter-spacing: 4px; margin: 16px 0;
  }
  @keyframes neonPulse {
    from { text-shadow: 0 0 6px #ffd966; }
    to { text-shadow: 0 0 24px #ffd966, 0 0 40px #ff77aa, 0 0 60px #ff77aa; }
  }

  /* Stage 4 — treasure */
  .inventory {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 6px; margin: 12px 0;
  }
  .slot {
    aspect-ratio: 1; background: #2a2a3e; border: 2px solid #5a5a7e;
    border-radius: 4px; display: flex; align-items: center;
    justify-content: center; font-size: 20px;
  }
  .slot.filled { background: #3a3a5e; border-color: #ffd966; }
  .chest-wrap { display: flex; justify-content: center; padding: 16px 0; }
  .chest {
    width: 80px; height: 60px;
    background: #8b5a2b; border: 4px solid #5a3812;
    border-radius: 4px; position: relative; cursor: pointer;
    animation: chestPulse 1.2s ease-in-out infinite alternate;
  }
  .chest::before {
    content: ''; position: absolute; top: -16px; left: -4px; right: -4px;
    height: 22px; background: #8b5a2b; border: 4px solid #5a3812;
    border-radius: 40px 40px 0 0; border-bottom: none;
  }
  .chest::after {
    content: ''; position: absolute; top: 8px; left: 50%;
    transform: translateX(-50%); width: 10px; height: 16px;
    background: #ffd966; border: 2px solid #5a3812; z-index: 2;
  }
  @keyframes chestPulse {
    from { box-shadow: 0 0 8px #ffd966; transform: scale(1); }
    to   { box-shadow: 0 0 28px #ffd966, 0 0 50px #ff77aa; transform: scale(1.05); }
  }

  /* Stage 5 — memory match */
  .memory-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 6px; margin: 14px 0;
  }
  .tile {
    aspect-ratio: 1; perspective: 600px; cursor: pointer;
  }
  .tile .inner {
    width: 100%; height: 100%; position: relative;
    transform-style: preserve-3d; transition: transform 0.4s;
  }
  .tile.flipped .inner, .tile.matched .inner { transform: rotateY(180deg); }
  .tile .face {
    position: absolute; inset: 0; backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 6px; display: flex; align-items: center;
    justify-content: center; font-size: 24px;
    border: 2px solid #ffd966;
  }
  .tile .front { background: #2a2a3e; color: #b9bcff; }
  .tile .back  { background: #1a3a3a; transform: rotateY(180deg); }
  .tile.matched .back { background: #1a5a2a; border-color: #6bff8d; }
  .match-counter { text-align: center; color: #b9bcff; font-size: 11px; letter-spacing: 1px; margin-top: 4px; }

  /* Stage 6 — typewriter */
  .typewriter {
    background: #000; color: #d4d4f0;
    padding: 16px; font-family: 'Courier New', monospace;
    font-size: 13px; line-height: 1.6; min-height: 110px;
    border: 1px solid #444; border-radius: 4px;
    white-space: pre-wrap; font-style: italic;
  }
  .typewriter::after { content: '▎'; animation: blink 0.9s steps(1) infinite; color: #ffd966; }
  .typewriter.done::after { content: ''; }

  /* Ferry stage */
  .ferry-stage {
    height: 64px; background: linear-gradient(180deg, #87ceeb 0%, #4a90e2 60%, #2e5f9e 100%);
    border-radius: 4px; position: relative; overflow: hidden; margin: 12px 0;
    border: 2px solid #1a3a5a;
  }
  .ship {
    position: absolute; bottom: 14px; left: -50px; width: 40px; height: 30px;
    animation: sail 3.2s ease-in-out forwards;
  }
  .ship .hull {
    position: absolute; bottom: 0; width: 100%; height: 14px;
    background: #6b3a1a; border-radius: 0 0 12px 12px;
  }
  .ship .sail {
    position: absolute; bottom: 14px; left: 50%;
    transform: translateX(-50%);
    width: 0; height: 0;
    border-left: 10px solid transparent; border-right: 10px solid transparent;
    border-bottom: 16px solid #fff;
  }
  .ship .mast {
    position: absolute; bottom: 14px; left: 50%;
    transform: translateX(-50%);
    width: 2px; height: 18px; background: #2a1a0e;
  }
  @keyframes sail { to { left: calc(100% + 50px); } }
  .waves {
    position: absolute; bottom: 0; left: 0; right: 0; height: 10px;
    background: repeating-linear-gradient(90deg, transparent 0 6px, rgba(255,255,255,0.3) 6px 8px);
    animation: waves 1.6s linear infinite;
  }
  @keyframes waves { to { background-position: -28px 0; } }

  /* Final ending */
  #ending {
    position: fixed; inset: 0; background: #000;
    display: none; flex-direction: column; align-items: center;
    justify-content: center; z-index: 200;
    color: #ffd966; text-align: center; padding: 30px;
    font-family: 'Georgia', 'Times New Roman', serif;
    opacity: 0; transition: opacity 4s ease-in;
  }
  #ending.show { display: flex; opacity: 1; }
  #ending p { font-size: 20px; margin: 14px 0; letter-spacing: 1px; line-height: 1.5; opacity: 0; transition: opacity 1.8s; }
  #ending p.small { font-size: 13px; opacity: 0; margin-top: 36px; color: #b9bcff; letter-spacing: 2px; }
  #ending.show p.visible { opacity: 1; }
  #ending.show p.small.visible { opacity: 0.85; }

  /* Black fade overlay used for stage 7 → ending */
  #fade-black {
    position: fixed; inset: 0; background: #000;
    opacity: 0; pointer-events: none; z-index: 180;
    transition: opacity 3.6s ease-in;
  }
  #fade-black.show { opacity: 1; pointer-events: all; }

  @media (max-width: 380px) {
    #hud { width: 96vw; font-size: 10px; }
    #gameCanvas { width: 96vw; height: auto; }
  }
</style>
</head>
<body>
<div id="app">
  <div id="hud">
    <span class="stage">STAGE <span id="stageNum">0</span>/7</span>
    <span class="zone" id="zoneName">LIC</span>
    <span class="actions">
      <button id="muteBtn">SOUND ON</button>
      <button id="resetBtn">RESET</button>
    </span>
  </div>
  <div id="canvas-wrap">
    <canvas id="gameCanvas" width="360" height="264"></canvas>
    <div id="toast"></div>
  </div>
  <div id="dpad">
    <div class="btn" id="up">▲</div>
    <div class="btn" id="left">◀</div>
    <div class="btn" id="right">▶</div>
    <div class="btn" id="down">▼</div>
  </div>
</div>

<div id="fade-black"></div>
<div id="modal-root"></div>
<div id="ending">
  <p id="end1">Happy Birthday, Sadia.</p>
  <p id="end2">You are the most wonderful thing that has ever happened to me.</p>
  <p id="end3" class="small">Open the physical letter.</p>
</div>

<script>
'use strict';

// =================== CONSTANTS ===================
const TILE = 24;
const VIEW_W = 15;
const VIEW_H = 11;
const MAP_W = 20;
const MAP_H = 25;
const STATE_KEY = 'sadiaQuestState_v2';

// Tile codes
const T_GRASS  = 0;
const T_WATER  = 1;
const T_BRIDGE = 2;
const T_WALL   = 3;
const T_ROAD   = 4;
const T_PARK   = 5;
const T_PIER   = 6;
const T_SAND   = 7;
const T_D1 = 11, T_D2 = 12, T_D3 = 13, T_D4 = 14, T_D5 = 15, T_D6 = 16, T_D7 = 17;
const T_CLEARED = 20;

const DUNGEON_TILES = new Set([T_D1, T_D2, T_D3, T_D4, T_D5, T_D6, T_D7]);
const DUNGEON_INDEX = { [T_D1]:0, [T_D2]:1, [T_D3]:2, [T_D4]:3, [T_D5]:4, [T_D6]:5, [T_D7]:6 };
const BLOCKING = new Set([T_WATER, T_WALL]);

// Build the NYC tilemap procedurally
function buildMap() {
  const m = [];
  for (let r = 0; r < MAP_H; r++) {
    m.push([]);
    for (let c = 0; c < MAP_W; c++) {
      let t = T_GRASS;
      // Border walls
      if (r === 0 || r === MAP_H - 1 || c === 0 || c === MAP_W - 1) t = T_WALL;
      // East River (cols 9-10), except bridge row 12
      else if ((c === 9 || c === 10) && r !== 12) t = T_WATER;
      // Bridge tiles
      else if (r === 12 && (c === 9 || c === 10)) t = T_BRIDGE;
      // LIC zone gets a road grid feel
      else if (c >= 11 && c <= 18 && (r % 4 === 2)) t = T_ROAD;
      // Manhattan grid
      else if (c >= 1 && c <= 8 && (r % 4 === 0) && r > 0 && r < 24) t = T_ROAD;
      // Park around D6 (cols 3-5, rows 9-11)
      if (r >= 9 && r <= 11 && c >= 3 && c <= 5) t = T_PARK;
      // Pier sand around D3
      if (r >= 3 && r <= 5 && c >= 2 && c <= 4) t = T_PIER;
      m[r][c] = t;
    }
  }
  // Dungeon entrances
  m[12][11] = T_D1; // ferry (LIC side of bridge)
  m[14][6]  = T_D2; // brunch (Manhattan, south of bridge)
  m[4][3]   = T_D3; // pier 97 (Manhattan north)
  m[7][16]  = T_D4; // LIC apartment (birthday rites)
  m[17][5]  = T_D5; // Kono / Bowery
  m[10][4]  = T_D6; // Washington Square Park
  m[22][4]  = T_D7; // Death & Co
  // Building enclosures around gated dungeons — the gate is the ONLY entrance.
  // Each entry is [row, col]. Dungeon interior tile is NOT listed.
  const blocks = [
    // D3 building (rows 3-5, cols 2-4); gate at (5,3), interior at (4,3)
    [3,2],[3,3],[3,4],[4,2],[4,4],[5,2],[5,4],
    // D4 building (rows 6-8, cols 15-17); gate at (7,15), interior at (7,16)
    [6,15],[6,16],[6,17],[7,17],[8,15],[8,16],[8,17],
    // D5 building (rows 16-18, cols 4-6); gate at (16,5), interior at (17,5)
    [16,4],[16,6],[17,4],[17,6],[18,4],[18,5],[18,6],
    // D6 building (rows 9-11, cols 3-5); gate at (11,4), interior at (10,4)
    [9,3],[9,4],[9,5],[10,3],[10,5],[11,3],[11,5],
    // D7 building (rows 21-23, cols 3-5); gate at (21,4), interior at (22,4)
    [21,3],[21,5],[22,3],[22,5],[23,3],[23,4],[23,5],
  ];
  for (const [r,c] of blocks) m[r][c] = T_WALL;
  // Tall apartment cluster decor in LIC
  const lic_buildings = [[2,12],[2,15],[2,17],[3,13],[3,16]];
  for (const [r,c] of lic_buildings) m[r][c] = T_WALL;
  // Bowery decor
  m[19][2] = T_WALL; m[19][6] = T_WALL; m[20][3] = T_WALL;
  return m;
}

const MAP = buildMap();

// Gates: { r, c, unlocksAtStage, kind }
// Active when state.stage < unlocksAtStage. Each rendered with a unique sprite.
const GATES = [
  { r: 12, c: 8,  unlocksAtStage: 1, kind: 'npc'     },
  { r: 5,  c: 3,  unlocksAtStage: 2, kind: 'rope'    },
  { r: 7,  c: 15, unlocksAtStage: 3, kind: 'door'    },
  { r: 16, c: 5,  unlocksAtStage: 4, kind: 'fence'   },
  { r: 11, c: 4,  unlocksAtStage: 5, kind: 'lantern' },
  { r: 21, c: 4,  unlocksAtStage: 6, kind: 'shadow'  },
];
function gateAt(r, c) {
  for (const g of GATES) if (g.r === r && g.c === c) return g;
  return null;
}

const ZONES = [
  { rMin: 0,  rMax: 6,  cMin: 11, cMax: 18, name: 'LIC · Apartments' },
  { rMin: 7,  rMax: 11, cMin: 11, cMax: 18, name: 'LIC · Center' },
  { rMin: 12, rMax: 18, cMin: 11, cMax: 18, name: 'LIC · Docks' },
  { rMin: 19, rMax: 23, cMin: 11, cMax: 18, name: 'LIC · South' },
  { rMin: 0,  rMax: 6,  cMin: 1,  cMax: 8,  name: 'Pier 85-97' },
  { rMin: 7,  rMax: 11, cMin: 1,  cMax: 8,  name: 'Washington Sq Park' },
  { rMin: 12, rMax: 16, cMin: 1,  cMax: 8,  name: 'Midtown · Brunch' },
  { rMin: 17, rMax: 19, cMin: 1,  cMax: 8,  name: 'The Bowery' },
  { rMin: 20, rMax: 23, cMin: 1,  cMax: 8,  name: 'East Village' },
];
function zoneFor(r, c) {
  for (const z of ZONES) if (r>=z.rMin && r<=z.rMax && c>=z.cMin && c<=z.cMax) return z.name;
  return '— — —';
}

// =================== STATE ===================
function defaultState() {
  return {
    x: 13, y: 7,         // tile coords (col, row) in LIC apartments
    facing: 'down',
    stage: 0,
    cleared: [false,false,false,false,false,false,false],
    muted: false,
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (!raw) return defaultState();
    const s = JSON.parse(raw);
    const d = defaultState();
    return Object.assign(d, s);
  } catch (e) { return defaultState(); }
}
function saveState() {
  try { localStorage.setItem(STATE_KEY, JSON.stringify(state)); } catch (e) {}
}
let state = loadState();

// =================== AUDIO ===================
const audio = {
  ctx: null,
  bgmGain: null,
  bgmTimer: null,
  bgmStep: 0,
  init() {
    if (this.ctx) return;
    try {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) { return; }
    this.bgmGain = this.ctx.createGain();
    this.bgmGain.gain.value = state.muted ? 0 : 0.04;
    this.bgmGain.connect(this.ctx.destination);
    this.startBgm();
  },
  setMuted(m) {
    state.muted = m;
    if (this.bgmGain) this.bgmGain.gain.value = m ? 0 : 0.04;
    saveState();
  },
  // 16-step C major melody + bass, ~120bpm
  startBgm() {
    if (!this.ctx) return;
    if (this.bgmTimer) clearInterval(this.bgmTimer);
    const lead = [523.25, 0, 659.25, 0, 783.99, 659.25, 523.25, 0,
                  587.33, 0, 698.46, 0, 880.00, 698.46, 587.33, 0];
    const bass = [130.81, 0, 0, 0, 196.00, 0, 0, 0,
                  146.83, 0, 0, 0, 220.00, 0, 0, 0];
    const stepMs = 220;
    this.bgmTimer = setInterval(() => {
      if (state.muted || !this.ctx || this.ctx.state !== 'running') return;
      const i = this.bgmStep % 16;
      this.bgmStep++;
      if (lead[i]) this.tone(lead[i], stepMs/1000 * 0.95, 'triangle', 0.6);
      if (bass[i]) this.tone(bass[i], stepMs/1000 * 1.5, 'sine', 0.9);
    }, stepMs);
  },
  tone(freq, dur, type, vol) {
    if (!this.ctx) return;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type; o.frequency.value = freq;
    g.gain.value = 0;
    o.connect(g); g.connect(this.bgmGain);
    const now = this.ctx.currentTime;
    g.gain.setValueAtTime(0, now);
    g.gain.linearRampToValueAtTime(vol, now + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, now + dur);
    o.start(now); o.stop(now + dur + 0.02);
  },
  sfx(name) {
    if (!this.ctx || state.muted) return;
    if (name === 'step')    this.tone(220, 0.05, 'square', 0.18);
    if (name === 'bump')    this.tone(110, 0.12, 'square', 0.5);
    if (name === 'success') {
      this.tone(523.25, 0.12, 'triangle', 0.7);
      setTimeout(() => this.tone(659.25, 0.12, 'triangle', 0.7), 110);
      setTimeout(() => this.tone(783.99, 0.18, 'triangle', 0.8), 220);
      setTimeout(() => this.tone(1046.5, 0.30, 'triangle', 0.9), 360);
    }
    if (name === 'fail') {
      this.tone(330, 0.12, 'sawtooth', 0.4);
      setTimeout(() => this.tone(220, 0.20, 'sawtooth', 0.5), 100);
    }
    if (name === 'enter')   this.tone(660, 0.15, 'triangle', 0.5);
  },
};

// =================== RENDER ===================
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

let frameTick = 0;
let isMoving = false;
let stepAnim = 0;

function camera() {
  // Centered camera, clamped to map bounds
  let camX = state.x - Math.floor(VIEW_W / 2);
  let camY = state.y - Math.floor(VIEW_H / 2);
  camX = Math.max(0, Math.min(MAP_W - VIEW_W, camX));
  camY = Math.max(0, Math.min(MAP_H - VIEW_H, camY));
  return { camX, camY };
}

function tileColor(t, r, c) {
  switch (t) {
    case T_GRASS:   return '#3b8b3b';
    case T_WATER:   return '#3a78d8';
    case T_BRIDGE:  return '#8b5a2b';
    case T_WALL:    return '#4a4a5e';
    case T_ROAD:    return '#5a5a64';
    case T_PARK:    return '#2f6b2f';
    case T_PIER:    return '#c8a878';
    case T_SAND:    return '#d8b88a';
    default: return '#3b8b3b';
  }
}

function drawTile(r, c, sx, sy) {
  const t = MAP[r][c];
  // Background base
  ctx.fillStyle = tileColor(t, r, c);
  ctx.fillRect(sx, sy, TILE, TILE);

  // Decorative overlays per type
  if (t === T_GRASS) {
    // grass dots
    ctx.fillStyle = '#4fa44f';
    ctx.fillRect(sx + 4 + ((r*7+c*3)%6), sy + 6, 2, 2);
    ctx.fillRect(sx + 14, sy + 16 + ((c*5+r)%4), 2, 2);
  } else if (t === T_WATER) {
    ctx.fillStyle = '#5a98e8';
    const w = (frameTick / 8) | 0;
    ctx.fillRect(sx + ((w + c) % 4) * 4, sy + 8, 6, 2);
    ctx.fillRect(sx + ((w + r) % 5) * 3, sy + 18, 5, 2);
  } else if (t === T_BRIDGE) {
    ctx.fillStyle = '#6b3a1a';
    for (let i = 0; i < 4; i++) ctx.fillRect(sx, sy + i*6, TILE, 1);
  } else if (t === T_WALL) {
    ctx.fillStyle = '#2a2a3e';
    ctx.fillRect(sx + 2, sy + 2, TILE - 4, TILE - 4);
    ctx.fillStyle = '#6a6a7e';
    ctx.fillRect(sx + 4, sy + 4, 4, 4);
    ctx.fillRect(sx + 14, sy + 6, 4, 4);
    ctx.fillRect(sx + 6, sy + 14, 4, 4);
    ctx.fillRect(sx + 16, sy + 16, 4, 4);
  } else if (t === T_ROAD) {
    ctx.fillStyle = '#7a7a84';
    ctx.fillRect(sx + 10, sy + 2, 2, 6);
    ctx.fillRect(sx + 10, sy + 16, 2, 6);
  } else if (t === T_PARK) {
    ctx.fillStyle = '#4fb04f';
    ctx.fillRect(sx + 6, sy + 6, 4, 4);
    ctx.fillStyle = '#8b5a2b';
    ctx.fillRect(sx + 7, sy + 10, 2, 4);
  } else if (t === T_PIER) {
    ctx.fillStyle = '#a88858';
    ctx.fillRect(sx, sy, TILE, 1);
    ctx.fillRect(sx, sy + 11, TILE, 1);
    ctx.fillRect(sx, sy + 22, TILE, 1);
  } else if (DUNGEON_TILES.has(t)) {
    drawDungeonTile(t, sx, sy);
  }

  // Cleared marker
  const dIdx = DUNGEON_INDEX[t];
  if (dIdx !== undefined && state.cleared[dIdx]) {
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.fillRect(sx + 2, sy + 2, TILE - 4, TILE - 4);
    ctx.fillStyle = '#6bff8d';
    ctx.font = 'bold 16px monospace';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('✓', sx + TILE/2, sy + TILE/2 + 1);
  }

  // Gate overlay
  const g = gateAt(r, c);
  if (g && state.stage < g.unlocksAtStage) drawGate(g, sx, sy);
}

function drawDungeonTile(t, sx, sy) {
  // Glowing portal-like square
  const pulse = (Math.sin(frameTick / 8) + 1) / 2;
  const glow = 0.5 + pulse * 0.5;
  // Stage-specific accent color
  const accents = {
    [T_D1]: '#5ad8ff', // ferry blue
    [T_D2]: '#ffb46b', // brunch orange
    [T_D3]: '#6bff8d', // pier green
    [T_D4]: '#ff77aa', // birthday pink
    [T_D5]: '#ffd966', // kono gold
    [T_D6]: '#b9bcff', // wash sq lavender
    [T_D7]: '#ff5a5a', // death red
  };
  const col = accents[t] || '#ffd966';
  ctx.fillStyle = '#1a1a2e';
  ctx.fillRect(sx + 3, sy + 3, TILE - 6, TILE - 6);
  ctx.strokeStyle = col;
  ctx.lineWidth = 2;
  ctx.strokeRect(sx + 4, sy + 4, TILE - 8, TILE - 8);
  ctx.fillStyle = `rgba(${hexRgb(col)},${glow})`;
  ctx.fillRect(sx + 8, sy + 8, TILE - 16, TILE - 16);
  // Stage number label
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 10px monospace';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(String((DUNGEON_INDEX[t] ?? 0) + 1), sx + TILE/2, sy + TILE/2 + 1);
}

function hexRgb(hex) {
  const h = hex.replace('#','');
  const r = parseInt(h.slice(0,2),16);
  const g = parseInt(h.slice(2,4),16);
  const b = parseInt(h.slice(4,6),16);
  return `${r},${g},${b}`;
}

function drawGate(g, sx, sy) {
  if (g.kind === 'npc') {
    // Friendly NPC sprite (dock master) — light blue uniform, hat
    ctx.fillStyle = '#1e3a5f'; ctx.fillRect(sx + 7, sy + 4, 10, 4);   // hat
    ctx.fillStyle = '#2a4f8a'; ctx.fillRect(sx + 6, sy + 6, 12, 2);   // brim
    ctx.fillStyle = '#d2a679'; ctx.fillRect(sx + 8, sy + 8, 8, 6);    // face
    ctx.fillStyle = '#000';    ctx.fillRect(sx + 10, sy + 11, 1, 1); ctx.fillRect(sx + 13, sy + 11, 1, 1);
    ctx.fillStyle = '#1e3a5f'; ctx.fillRect(sx + 6, sy + 14, 12, 8);  // body
    ctx.fillStyle = '#ffd966'; ctx.fillRect(sx + 11, sy + 16, 2, 2);  // badge
  } else if (g.kind === 'rope') {
    ctx.fillStyle = '#6b3a1a'; ctx.fillRect(sx + 2, sy + 4, 2, 16);
    ctx.fillRect(sx + 20, sy + 4, 2, 16);
    ctx.fillStyle = '#a85a2a';
    for (let i = 4; i <= 20; i += 4) ctx.fillRect(sx + i, sy + 11, 4, 2);
    ctx.fillStyle = '#ff6b6b'; ctx.fillRect(sx + 10, sy + 9, 4, 6);
  } else if (g.kind === 'door') {
    ctx.fillStyle = '#5a3812'; ctx.fillRect(sx + 4, sy + 2, 16, 20);
    ctx.fillStyle = '#8b5a2b'; ctx.fillRect(sx + 6, sy + 4, 12, 16);
    ctx.fillStyle = '#ffd966'; ctx.fillRect(sx + 15, sy + 12, 2, 2);
  } else if (g.kind === 'fence') {
    ctx.fillStyle = '#3a3a3e';
    for (let i = 2; i <= 18; i += 4) ctx.fillRect(sx + i, sy + 2, 2, 20);
    ctx.fillRect(sx + 2, sy + 8, 20, 1);
    ctx.fillRect(sx + 2, sy + 16, 20, 1);
  } else if (g.kind === 'lantern') {
    ctx.fillStyle = '#2a2a3e'; ctx.fillRect(sx + 10, sy + 4, 4, 14);
    const flick = (Math.sin(frameTick / 5) + 1) / 2;
    ctx.fillStyle = `rgba(255, 215, 100, ${0.5 + flick * 0.5})`;
    ctx.fillRect(sx + 7, sy + 4, 10, 8);
    ctx.fillStyle = '#ffd966'; ctx.fillRect(sx + 10, sy + 6, 4, 4);
  } else if (g.kind === 'shadow') {
    const wobble = Math.sin(frameTick / 6) * 1.5;
    ctx.fillStyle = '#1a0a1a';
    ctx.fillRect(sx + 4 + wobble, sy + 4, 16, 18);
    ctx.fillStyle = '#5a1a3a';
    ctx.fillRect(sx + 8 + wobble, sy + 8, 8, 12);
    ctx.fillStyle = '#ff5a5a';
    ctx.fillRect(sx + 10 + wobble, sy + 10, 1, 1);
    ctx.fillRect(sx + 13 + wobble, sy + 10, 1, 1);
  }
}

function drawPlayer(sx, sy) {
  // 24x24 pixel-art tan girl with pink shirt, dark hair, 2-frame walk
  const walking = isMoving && (stepAnim % 16 < 8);
  // Hair (back layer)
  ctx.fillStyle = '#2a1a0e';
  ctx.fillRect(sx + 5, sy + 2, 14, 5);   // top of head
  ctx.fillRect(sx + 4, sy + 5, 3, 9);    // left side
  ctx.fillRect(sx + 17, sy + 5, 3, 9);   // right side
  ctx.fillRect(sx + 5, sy + 13, 14, 2);  // back hair
  // Face
  ctx.fillStyle = '#d2a679';
  ctx.fillRect(sx + 7, sy + 5, 10, 8);
  // Eyes (depend on facing)
  ctx.fillStyle = '#1a0a0e';
  if (state.facing === 'left') {
    ctx.fillRect(sx + 8, sy + 9, 2, 2);
    ctx.fillRect(sx + 12, sy + 9, 2, 2);
  } else if (state.facing === 'right') {
    ctx.fillRect(sx + 10, sy + 9, 2, 2);
    ctx.fillRect(sx + 14, sy + 9, 2, 2);
  } else {
    ctx.fillRect(sx + 9, sy + 9, 2, 2);
    ctx.fillRect(sx + 13, sy + 9, 2, 2);
  }
  // Blush
  ctx.fillStyle = '#e89a9a';
  ctx.fillRect(sx + 8, sy + 11, 1, 1);
  ctx.fillRect(sx + 15, sy + 11, 1, 1);
  // Shirt (pink)
  ctx.fillStyle = '#ff77aa';
  ctx.fillRect(sx + 5, sy + 14, 14, 6);
  ctx.fillStyle = '#ff558b';
  ctx.fillRect(sx + 5, sy + 19, 14, 1);
  // Arms
  ctx.fillStyle = '#d2a679';
  ctx.fillRect(sx + 4, sy + 15, 1, 4);
  ctx.fillRect(sx + 19, sy + 15, 1, 4);
  // Pants — two legs with walking offset
  ctx.fillStyle = '#3a5da8';
  const lY = walking ? sy + 19 : sy + 20;
  const rY = walking ? sy + 20 : sy + 19;
  ctx.fillRect(sx + 7, lY, 4, 4);
  ctx.fillRect(sx + 13, rY, 4, 4);
  // Shoes
  ctx.fillStyle = '#1a1a2e';
  ctx.fillRect(sx + 7, lY + 3, 4, 1);
  ctx.fillRect(sx + 13, rY + 3, 4, 1);
}

function render() {
  const { camX, camY } = camera();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Map tiles
  for (let vy = 0; vy < VIEW_H; vy++) {
    for (let vx = 0; vx < VIEW_W; vx++) {
      const r = camY + vy, c = camX + vx;
      if (r < 0 || r >= MAP_H || c < 0 || c >= MAP_W) {
        ctx.fillStyle = '#0a0a14';
        ctx.fillRect(vx * TILE, vy * TILE, TILE, TILE);
        continue;
      }
      drawTile(r, c, vx * TILE, vy * TILE);
    }
  }
  // Player
  const px = (state.x - camX) * TILE;
  const py = (state.y - camY) * TILE;
  drawPlayer(px, py);
}

// =================== INPUT / MOVEMENT ===================
const stageNumEl = document.getElementById('stageNum');
const zoneEl = document.getElementById('zoneName');

function updateHud() {
  stageNumEl.textContent = state.stage;
  zoneEl.textContent = zoneFor(state.y, state.x);
}

function blockedAt(r, c) {
  if (r < 0 || r >= MAP_H || c < 0 || c >= MAP_W) return true;
  const t = MAP[r][c];
  if (BLOCKING.has(t)) return true;
  const g = gateAt(r, c);
  if (g && state.stage < g.unlocksAtStage) return true;
  return false;
}

let gameRunning = true;
let movementCooldown = 0;

function tryMove(dx, dy) {
  if (!gameRunning) return;
  if (movementCooldown > 0) return;
  audio.init();
  // Update facing
  if (dx === 1) state.facing = 'right';
  else if (dx === -1) state.facing = 'left';
  else if (dy === 1) state.facing = 'down';
  else if (dy === -1) state.facing = 'up';

  const nx = state.x + dx;
  const ny = state.y + dy;
  if (blockedAt(ny, nx)) {
    audio.sfx('bump');
    isMoving = false;
    movementCooldown = 8;
    saveState();
    return;
  }
  state.x = nx; state.y = ny;
  audio.sfx('step');
  isMoving = true;
  stepAnim = (stepAnim + 8) % 32;
  movementCooldown = 6;
  saveState();
  updateHud();

  // Auto-trigger dungeon
  const t = MAP[state.y][state.x];
  if (DUNGEON_TILES.has(t)) {
    const idx = DUNGEON_INDEX[t];
    if (!state.cleared[idx]) {
      setTimeout(() => openDungeon(idx), 120);
    }
  }
}

// Keyboard
const keysHeld = {};
window.addEventListener('keydown', (e) => {
  const k = e.key.toLowerCase();
  if (['arrowup','arrowdown','arrowleft','arrowright'].includes(k)) {
    e.preventDefault();
    keysHeld[k] = true;
  }
});
window.addEventListener('keyup', (e) => {
  const k = e.key.toLowerCase();
  keysHeld[k] = false;
});

function pollKeyboard() {
  if (keysHeld['arrowup'])         tryMove(0, -1);
  else if (keysHeld['arrowdown'])  tryMove(0, 1);
  else if (keysHeld['arrowleft'])  tryMove(-1, 0);
  else if (keysHeld['arrowright']) tryMove(1, 0);
  else { isMoving = false; }
}

// D-pad with held repeat
function bindDpad(id, dx, dy) {
  const el = document.getElementById(id);
  let timer = null;
  const start = (e) => {
    if (e) e.preventDefault();
    el.classList.add('pressed');
    tryMove(dx, dy);
    if (timer) clearInterval(timer);
    timer = setInterval(() => tryMove(dx, dy), 140);
  };
  const stop = (e) => {
    if (e) e.preventDefault();
    el.classList.remove('pressed');
    if (timer) { clearInterval(timer); timer = null; }
    isMoving = false;
  };
  el.addEventListener('pointerdown', start);
  el.addEventListener('pointerup', stop);
  el.addEventListener('pointerleave', stop);
  el.addEventListener('pointercancel', stop);
  el.addEventListener('touchstart', (e) => e.preventDefault(), { passive: false });
}
bindDpad('up', 0, -1);
bindDpad('down', 0, 1);
bindDpad('left', -1, 0);
bindDpad('right', 1, 0);

// =================== TOAST ===================
const toastEl = document.getElementById('toast');
let toastTimer = null;
function toast(msg, dur = 2400) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove('show'), dur);
}

// =================== MODAL / DUNGEONS ===================
const modalRoot = document.getElementById('modal-root');
let currentDungeon = null;

function closeModal() {
  modalRoot.classList.remove('show');
  modalRoot.innerHTML = '';
  currentDungeon = null;
  gameRunning = true;
}

function clearDungeon(idx) {
  state.cleared[idx] = true;
  state.stage = Math.max(state.stage, idx + 1);
  saveState();
  updateHud();
  audio.sfx('success');
  toast(`STAGE ${idx + 1} CLEARED`, 2800);
}

function openDungeon(idx) {
  if (currentDungeon !== null) return;
  if (state.cleared[idx]) return;
  gameRunning = false;
  currentDungeon = idx;
  audio.init();
  audio.sfx('enter');
  modalRoot.innerHTML = DUNGEONS[idx].html;
  modalRoot.classList.add('show');
  if (DUNGEONS[idx].onOpen) DUNGEONS[idx].onOpen();
}

// Helper: normalize input
function norm(s) { return (s || '').trim().toLowerCase(); }

// =================== 7 DUNGEONS ===================
const DUNGEONS = [
  // -------- Stage 1: Ferry --------
  {
    html: `
      <div class="modal">
        <h2>The Ferry</h2>
        <div class="sub">LIC Pier · Stage 1 of 7</div>
        <p class="prompt">The dock master blocks the bridge. "Before you cross, prove you know the river's history."</p>
        <div class="ferry-stage" id="ferryStage"><div class="waves"></div></div>
        <label>What was the earliest mode of transportation from LIC to Manhattan?</label>
        <input id="d1a" type="text" autocomplete="off" placeholder="..." />
        <label>What year was regular service first established?</label>
        <input id="d1b" type="text" autocomplete="off" placeholder="YYYY" />
        <div class="error" id="d1err"></div>
        <button class="submit" id="d1submit">SET SAIL</button>
      </div>`,
    onOpen() {
      document.getElementById('d1submit').addEventListener('click', () => {
        const a = norm(document.getElementById('d1a').value);
        const b = norm(document.getElementById('d1b').value);
        const okA = (a === 'ferry');
        const yearNum = parseInt(b, 10);
        const isExact = (b === '1642');
        const isClose = !isExact && !isNaN(yearNum) && yearNum >= 1600 && yearNum <= 1680;
        const okB = isExact || isClose;
        if (okA && okB) {
          const stage = document.getElementById('ferryStage');
          stage.insertAdjacentHTML('beforeend', '<div class="ship"><div class="mast"></div><div class="sail"></div><div class="hull"></div></div>');
          document.getElementById('d1submit').disabled = true;
          document.getElementById('d1err').innerHTML = isClose
            ? '<span class="ok">Close enough! It was 1642.</span>'
            : '<span class="ok">All aboard.</span>';
          setTimeout(() => { clearDungeon(0); closeModal(); }, 3200);
        } else {
          document.getElementById('d1err').textContent =
            !okA ? 'Try again — earliest mode...' : 'Try again — earlier than that.';
          audio.sfx('fail');
        }
      });
    }
  },

  // -------- Stage 2: Brunch --------
  {
    html: `
      <div class="modal">
        <h2>Brunch</h2>
        <div class="sub">Manhattan West Side · Stage 2 of 7</div>
        <p class="prompt">Sun on the water. A waiter holds out a menu. "Which pier do you remember?"</p>
        <div class="choices">
          <button class="choice-btn" data-v="85">85</button>
          <button class="choice-btn" data-v="90">90</button>
          <button class="choice-btn" data-v="97">97</button>
          <button class="choice-btn" data-v="112">112</button>
        </div>
        <div class="error" id="d2err"></div>
      </div>`,
    onOpen() {
      document.querySelectorAll('#modal-root .choice-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const v = btn.dataset.v;
          if (v === '97') {
            btn.classList.add('right');
            document.getElementById('d2err').innerHTML = '<span class="ok">Yes — pier 97.</span>';
            setTimeout(() => { clearDungeon(1); closeModal(); }, 900);
          } else {
            btn.classList.add('wrong');
            audio.sfx('fail');
            document.getElementById('d2err').textContent = 'Not that one. Try again.';
            setTimeout(() => btn.classList.remove('wrong'), 500);
          }
        });
      });
    }
  },

  // -------- Stage 3: Pier 97 Terminal --------
  {
    html: `
      <div class="modal">
        <h2>Pier 97</h2>
        <div class="sub">Project Makeover Arcade · Stage 3 of 7</div>
        <p class="prompt">An arcade terminal flickers. The screen reads: "COLLAB ROUNDS 3/3 COMPLETE. ENTER CONFIRMATION CODE."</p>
        <div class="terminal">
          <div class="line">&gt; status: rounds_cleared = 3</div>
          <div class="line">&gt; awaiting confirmation code...</div>
          <div class="line">&gt; <span class="caret"></span><input id="d3in" type="text" autocomplete="off" autocapitalize="off" /></div>
        </div>
        <div class="error" id="d3err"></div>
        <button class="submit" id="d3submit">SUBMIT</button>
      </div>`,
    onOpen() {
      const submit = () => {
        const v = norm(document.getElementById('d3in').value);
        if (v === 'cleared') {
          document.querySelector('#modal-root .terminal').insertAdjacentHTML(
            'beforeend',
            '<div class="line">&gt; <span class="ok">CODE ACCEPTED</span></div><div class="neon">LEVEL CLEAR</div>'
          );
          document.getElementById('d3submit').disabled = true;
          setTimeout(() => { clearDungeon(2); closeModal(); }, 2400);
        } else {
          document.getElementById('d3err').textContent = 'Invalid code. Try the one we always say.';
          audio.sfx('fail');
        }
      };
      document.getElementById('d3submit').addEventListener('click', submit);
      document.getElementById('d3in').addEventListener('keydown', (e) => { if (e.key === 'Enter') submit(); });
      document.getElementById('d3in').focus();
    }
  },

  // -------- Stage 4: Birthday Rites --------
  {
    html: `
      <div class="modal">
        <h2>The Birthday Rites</h2>
        <div class="sub">LIC Apartment · Stage 4 of 7</div>
        <p class="prompt">The kitchen is warm. The recipe is ancient.</p>
        <div class="inventory">
          <div class="slot filled">🍚</div>
          <div class="slot filled">🥛</div>
          <div class="slot filled">🍯</div>
          <div class="slot">?</div>
        </div>
        <label>What snack is mandatory on a Bangladeshi birthday?</label>
        <input id="d4in" type="text" autocomplete="off" placeholder="..." />
        <div class="error" id="d4err"></div>
        <button class="submit" id="d4submit">OFFER</button>
      </div>`,
    onOpen() {
      const submit = () => {
        const v = norm(document.getElementById('d4in').value);
        if (v === 'paayesh' || v === 'payesh' || v === 'payash' || v === 'paayash') {
          document.querySelector('#modal-root .inventory .slot:last-child').textContent = '🍮';
          document.querySelector('#modal-root .inventory .slot:last-child').classList.add('filled');
          // Show treasure
          setTimeout(() => {
            const modal = document.querySelector('#modal-root .modal');
            modal.innerHTML = `
              <h2>Save Point Unlocked</h2>
              <div class="sub">LIC Apartment</div>
              <div class="chest-wrap"><div class="chest" id="chest"></div></div>
              <p id="chestMsg" style="display:none;" class="prompt">
                A treasure chest pulses with light. Tap to open.
              </p>
              <p id="chestReveal" style="display:none;">
                <span class="ok">EQUIP NEW ARMOR.</span><br>
                Find the golden item hidden in the apartment.<br>
                Rest, and change into evening wear.
              </p>
              <button class="submit" id="d4close" style="display:none;">CONTINUE</button>
            `;
            document.getElementById('chestMsg').style.display = 'block';
            const chest = document.getElementById('chest');
            chest.addEventListener('click', () => {
              document.getElementById('chestMsg').style.display = 'none';
              document.getElementById('chestReveal').style.display = 'block';
              const closeBtn = document.getElementById('d4close');
              closeBtn.style.display = 'block';
              chest.style.animation = 'none';
              audio.sfx('success');
              closeBtn.addEventListener('click', () => { clearDungeon(3); closeModal(); });
            });
          }, 700);
        } else {
          document.getElementById('d4err').textContent = 'The kitchen is silent. Try another spelling.';
          audio.sfx('fail');
        }
      };
      document.getElementById('d4submit').addEventListener('click', submit);
      document.getElementById('d4in').addEventListener('keydown', (e) => { if (e.key === 'Enter') submit(); });
    }
  },

  // -------- Stage 5: Kono --------
  {
    html: `
      <div class="modal">
        <h2>Kono</h2>
        <div class="sub">The Bowery · Stage 5 of 7</div>
        <p class="prompt">The chef sends out a memory game on the omakase counter. Match all four pairs.</p>
        <div class="memory-grid" id="d5grid"></div>
        <div class="match-counter" id="d5count">0 / 4 PAIRS</div>
      </div>`,
    onOpen() {
      const icons = ['🐔','🪨','👁️','🚛'];
      const deck = [...icons, ...icons]
        .map(v => ({ v, k: Math.random() }))
        .sort((a, b) => a.k - b.k)
        .map(o => o.v);
      const grid = document.getElementById('d5grid');
      grid.innerHTML = deck.map((icon, i) =>
        `<div class="tile" data-i="${i}" data-v="${icon}">
           <div class="inner">
             <div class="face front">?</div>
             <div class="face back">${icon}</div>
           </div>
         </div>`
      ).join('');
      const counter = document.getElementById('d5count');
      let firstPick = null;
      let busy = false;
      let matched = 0;
      grid.querySelectorAll('.tile').forEach(tile => {
        tile.addEventListener('click', () => {
          if (busy) return;
          if (tile.classList.contains('flipped') || tile.classList.contains('matched')) return;
          tile.classList.add('flipped');
          audio.sfx('step');
          if (firstPick === null) {
            firstPick = tile;
            return;
          }
          if (firstPick.dataset.v === tile.dataset.v) {
            firstPick.classList.add('matched');
            tile.classList.add('matched');
            firstPick = null;
            matched += 1;
            counter.textContent = `${matched} / 4 PAIRS`;
            audio.sfx('enter');
            if (matched === 4) {
              setTimeout(() => { clearDungeon(4); closeModal(); }, 900);
            }
          } else {
            busy = true;
            const a = firstPick, b = tile;
            firstPick = null;
            audio.sfx('fail');
            setTimeout(() => {
              a.classList.remove('flipped');
              b.classList.remove('flipped');
              busy = false;
            }, 850);
          }
        });
      });
    }
  },

  // -------- Stage 6: Washington Square --------
  {
    html: `
      <div class="modal">
        <h2>Washington Square</h2>
        <div class="sub">Under the Arch · Stage 6 of 7</div>
        <div class="typewriter" id="tw"></div>
        <div id="d6gate" style="display:none;">
          <label>Your answer:</label>
          <input id="d6in" type="text" autocomplete="off" placeholder="..." />
          <div class="error" id="d6err"></div>
          <button class="submit" id="d6submit">SPEAK</button>
        </div>
      </div>`,
    onOpen() {
      const text =
        'Some greet me as a friend, some flee me as a foe,\n' +
        'But I am the final destination everyone must know.\n' +
        'I bring an end to sorrow, but also end your glee,\n' +
        'Kings and beggars both must yield their time to me.\n' +
        'I have no lungs, yet I will take your breath,\n' +
        'And leave you sleeping soundly where there is nothing left.\n' +
        'What am I?';
      const el = document.getElementById('tw');
      let i = 0;
      const tick = setInterval(() => {
        if (i >= text.length) {
          clearInterval(tick);
          el.classList.add('done');
          document.getElementById('d6gate').style.display = 'block';
          return;
        }
        el.textContent = text.slice(0, ++i);
      }, 55);
      const submit = () => {
        const v = norm(document.getElementById('d6in').value);
        if (v === 'death') {
          document.getElementById('d6err').innerHTML = '<span class="ok">...the answer was always so.</span>';
          setTimeout(() => { clearDungeon(5); closeModal(); }, 1400);
        } else {
          document.getElementById('d6err').textContent = 'The riddle waits. One word.';
          audio.sfx('fail');
        }
      };
      document.getElementById('d6submit').addEventListener('click', submit);
      document.getElementById('d6in').addEventListener('keydown', (e) => { if (e.key === 'Enter') submit(); });
    }
  },

  // -------- Stage 7: Death & Co --------
  {
    html: `
      <div class="modal">
        <h2>Death &amp; Co</h2>
        <div class="sub">East Village · Final Stage 7 of 7</div>
        <p class="prompt">The bartender pours something amber. "One last thing before the cocktail. Tell me a favorite memory of ours."</p>
        <textarea id="d7in" placeholder="Type slowly. There is no wrong answer."></textarea>
        <div class="error" id="d7err"></div>
        <button class="submit" id="d7submit">REMEMBER</button>
      </div>`,
    onOpen() {
      document.getElementById('d7submit').addEventListener('click', () => {
        const v = (document.getElementById('d7in').value || '').trim();
        if (v.length < 5) {
          document.getElementById('d7err').textContent = 'Tell me a little more.';
          audio.sfx('fail');
          return;
        }
        // Save memory for posterity
        try { localStorage.setItem('sadiaFinalMemory', v); } catch (e) {}
        clearDungeon(6);
        closeModal();
        playEnding();
      });
    }
  },
];

// =================== ENDING ===================
function playEnding() {
  const fade = document.getElementById('fade-black');
  const ending = document.getElementById('ending');
  gameRunning = false;
  fade.classList.add('show');
  setTimeout(() => {
    ending.classList.add('show');
    setTimeout(() => document.getElementById('end1').classList.add('visible'), 800);
    setTimeout(() => document.getElementById('end2').classList.add('visible'), 3200);
    setTimeout(() => document.getElementById('end3').classList.add('visible'), 6000);
  }, 3400);
}

// =================== HUD CONTROLS ===================
const muteBtn = document.getElementById('muteBtn');
function refreshMuteBtn() { muteBtn.textContent = state.muted ? 'SOUND OFF' : 'SOUND ON'; }
refreshMuteBtn();
muteBtn.addEventListener('click', () => {
  audio.init();
  audio.setMuted(!state.muted);
  refreshMuteBtn();
});

document.getElementById('resetBtn').addEventListener('click', () => {
  if (confirm('Reset all progress? This wipes your save.')) {
    try { localStorage.removeItem(STATE_KEY); } catch (e) {}
    location.reload();
  }
});

// =================== GAME LOOP ===================
function loop() {
  frameTick++;
  if (movementCooldown > 0) movementCooldown--;
  if (gameRunning) pollKeyboard();
  if (isMoving) stepAnim = (stepAnim + 1) % 32;
  render();
  requestAnimationFrame(loop);
}

// Init
updateHud();
render();
requestAnimationFrame(loop);

// If save indicates ending already played, show map with all cleared — no auto replay
// (player can keep walking after the finale)

// Unlock audio on first interaction (mobile)
function unlockAudio() {
  audio.init();
  if (audio.ctx && audio.ctx.state === 'suspended') audio.ctx.resume();
  window.removeEventListener('pointerdown', unlockAudio);
  window.removeEventListener('keydown', unlockAudio);
}
window.addEventListener('pointerdown', unlockAudio);
window.addEventListener('keydown', unlockAudio);
</script>
</body>
</html>"""

components.html(GAME_HTML, height=820, scrolling=False)
