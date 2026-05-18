import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Sadia's Quest — Walking Edition",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
      .stApp {background: #0a0a14;}
      iframe {display: block; margin: 0 auto; border: none; width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Sadia's Quest — Walking Edition</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body {
    margin: 0; padding: 0; background: #0a0a14;
    font-family: 'Courier New', monospace; color: #fff;
    overflow: hidden; user-select: none; -webkit-user-select: none;
    height: 100%; width: 100%;
  }
  #app { display: flex; flex-direction: column; height: 100vh; max-height: 100vh; }
  #hud {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 12px; background: linear-gradient(180deg, #1a1a2e, #0f0f1e);
    border-bottom: 2px solid #ffd966; flex-shrink: 0;
    font-size: 11px; letter-spacing: 1px;
  }
  #hud .left { display: flex; flex-direction: column; gap: 2px; }
  #hud .stage { font-weight: bold; color: #ffd966; font-size: 13px; letter-spacing: 2px; }
  #hud .target { color: #b9bcff; font-size: 10px; }
  #hud .actions { display: flex; gap: 6px; }
  #hud button {
    background: transparent; border: 1px solid rgba(255,255,255,0.3);
    color: #fff; padding: 4px 8px; border-radius: 4px; cursor: pointer;
    font-family: inherit; font-size: 10px; letter-spacing: 1px;
  }
  #hud button:hover { background: rgba(255,255,255,0.1); }
  #map { flex: 1; width: 100%; background: #2a2a3e; }
  #hint-bar {
    padding: 10px 12px; background: linear-gradient(180deg, #0f0f1e, #1a1a2e);
    border-top: 2px solid #ffd966; flex-shrink: 0;
    display: flex; flex-direction: column; gap: 6px;
  }
  #hintText { margin: 0; font-size: 12px; color: #b9bcff; font-style: italic; line-height: 1.4; }
  #imHere {
    background: #ffd966; color: #000; border: none;
    padding: 10px 12px; font-family: inherit; font-weight: bold;
    font-size: 12px; border-radius: 4px; cursor: pointer;
    letter-spacing: 2px; width: 100%;
  }
  #imHere:hover { background: #ffe88a; }
  #imHere:disabled { background: #5a5a64; color: #999; cursor: not-allowed; }

  /* ===== Intro modal ===== */
  #intro-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.92);
    display: flex; align-items: center; justify-content: center;
    z-index: 50; padding: 16px;
  }
  #intro-overlay .modal {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    border: 3px solid #ffd966; border-radius: 12px;
    padding: 24px; max-width: 380px; width: 100%;
    box-shadow: 0 0 40px rgba(255,217,102,0.4);
  }
  #intro-overlay h1 {
    margin: 0 0 4px; color: #ffd966; font-size: 18px;
    letter-spacing: 3px; text-transform: uppercase; text-align: center;
  }
  #intro-overlay .sub { color: #b9bcff; font-size: 11px; letter-spacing: 2px; text-align: center; margin-bottom: 18px; }
  #intro-overlay p { font-size: 13px; line-height: 1.6; margin: 10px 0; }
  #intro-overlay .tips { color: #b9bcff; font-size: 11px; line-height: 1.5; margin: 14px 0; }
  #intro-overlay .tips li { margin: 4px 0; }
  #intro-overlay button {
    background: #ffd966; color: #000; border: none;
    padding: 12px 16px; font-family: inherit; font-weight: bold;
    font-size: 14px; border-radius: 4px; cursor: pointer;
    margin-top: 12px; width: 100%; letter-spacing: 3px;
  }

  /* ===== Modal layer (reused from 2D) ===== */
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
    padding: 20px; max-width: 380px; width: 100%;
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
  @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-6px); } 75% { transform: translateX(6px); } }

  .terminal { background: #000; color: #00ff41; padding: 12px;
    font-family: 'Courier New', monospace; font-size: 12px;
    border: 1px solid #00ff41; border-radius: 4px; min-height: 80px; }
  .terminal .line { line-height: 1.5; }
  .terminal input { background: transparent; color: #00ff41; border: none;
    outline: none; font-family: inherit; font-size: 13px; width: 80%; }
  .terminal .caret::after { content: '_'; animation: blink 0.9s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  .neon { color: #ffd966; text-shadow: 0 0 8px #ffd966, 0 0 16px #ff77aa;
    animation: neonPulse 0.6s ease-in-out infinite alternate;
    text-align: center; font-size: 22px; font-weight: bold;
    letter-spacing: 4px; margin: 16px 0; }
  @keyframes neonPulse {
    from { text-shadow: 0 0 6px #ffd966; }
    to { text-shadow: 0 0 24px #ffd966, 0 0 40px #ff77aa, 0 0 60px #ff77aa; }
  }

  .inventory { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 12px 0; }
  .slot { aspect-ratio: 1; background: #2a2a3e; border: 2px solid #5a5a7e;
    border-radius: 4px; display: flex; align-items: center;
    justify-content: center; font-size: 20px; }
  .slot.filled { background: #3a3a5e; border-color: #ffd966; }
  .chest-wrap { display: flex; justify-content: center; padding: 16px 0; }
  .chest { width: 80px; height: 60px; background: #8b5a2b; border: 4px solid #5a3812;
    border-radius: 4px; position: relative; cursor: pointer;
    animation: chestPulse 1.2s ease-in-out infinite alternate; }
  .chest::before { content: ''; position: absolute; top: -16px; left: -4px; right: -4px;
    height: 22px; background: #8b5a2b; border: 4px solid #5a3812;
    border-radius: 40px 40px 0 0; border-bottom: none; }
  .chest::after { content: ''; position: absolute; top: 8px; left: 50%;
    transform: translateX(-50%); width: 10px; height: 16px;
    background: #ffd966; border: 2px solid #5a3812; z-index: 2; }
  @keyframes chestPulse {
    from { box-shadow: 0 0 8px #ffd966; transform: scale(1); }
    to   { box-shadow: 0 0 28px #ffd966, 0 0 50px #ff77aa; transform: scale(1.05); }
  }

  .memory-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 14px 0; }
  .tile { aspect-ratio: 1; perspective: 600px; cursor: pointer; }
  .tile .inner { width: 100%; height: 100%; position: relative;
    transform-style: preserve-3d; transition: transform 0.4s; }
  .tile.flipped .inner, .tile.matched .inner { transform: rotateY(180deg); }
  .tile .face { position: absolute; inset: 0; backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 6px; display: flex; align-items: center;
    justify-content: center; font-size: 24px; border: 2px solid #ffd966; }
  .tile .front { background: #2a2a3e; color: #b9bcff; }
  .tile .back  { background: #1a3a3a; transform: rotateY(180deg); }
  .tile.matched .back { background: #1a5a2a; border-color: #6bff8d; }
  .match-counter { text-align: center; color: #b9bcff; font-size: 11px; letter-spacing: 1px; margin-top: 4px; }

  .typewriter { background: #000; color: #d4d4f0; padding: 16px;
    font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.6;
    min-height: 110px; border: 1px solid #444; border-radius: 4px;
    white-space: pre-wrap; font-style: italic; }
  .typewriter::after { content: '▎'; animation: blink 0.9s steps(1) infinite; color: #ffd966; }
  .typewriter.done::after { content: ''; }

  .ferry-stage { height: 64px; background: linear-gradient(180deg, #87ceeb 0%, #4a90e2 60%, #2e5f9e 100%);
    border-radius: 4px; position: relative; overflow: hidden; margin: 12px 0;
    border: 2px solid #1a3a5a; }
  .ship { position: absolute; bottom: 14px; left: -50px; width: 40px; height: 30px;
    animation: sail 3.2s ease-in-out forwards; }
  .ship .hull { position: absolute; bottom: 0; width: 100%; height: 14px;
    background: #6b3a1a; border-radius: 0 0 12px 12px; }
  .ship .sail { position: absolute; bottom: 14px; left: 50%;
    transform: translateX(-50%); width: 0; height: 0;
    border-left: 10px solid transparent; border-right: 10px solid transparent;
    border-bottom: 16px solid #fff; }
  .ship .mast { position: absolute; bottom: 14px; left: 50%;
    transform: translateX(-50%); width: 2px; height: 18px; background: #2a1a0e; }
  @keyframes sail { to { left: calc(100% + 50px); } }
  .waves { position: absolute; bottom: 0; left: 0; right: 0; height: 10px;
    background: repeating-linear-gradient(90deg, transparent 0 6px, rgba(255,255,255,0.3) 6px 8px);
    animation: waves 1.6s linear infinite; }
  @keyframes waves { to { background-position: -28px 0; } }

  /* ===== Custom Leaflet markers ===== */
  .pin {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-family: 'Courier New', monospace;
    color: #fff; box-shadow: 0 0 12px rgba(0,0,0,0.6);
    border: 3px solid #fff;
  }
  .pin.current {
    background: #ffd966; color: #000;
    animation: pinPulse 1s ease-in-out infinite alternate;
    border-color: #fff;
  }
  @keyframes pinPulse {
    from { box-shadow: 0 0 8px #ffd966; transform: scale(1); }
    to   { box-shadow: 0 0 32px #ffd966, 0 0 56px #ff77aa; transform: scale(1.15); }
  }
  .pin.cleared { background: #2a8a2a; }
  .pin.future  { background: #4a4a64; opacity: 0.55; }
  .player-sprite {
    width: 32px; height: 42px;
    filter: drop-shadow(0 0 6px rgba(255,217,102,0.7));
    image-rendering: pixelated; image-rendering: crisp-edges;
  }
  .player-sprite .leg-l { animation: legBob 0.42s steps(1) infinite alternate; }
  .player-sprite .leg-r { animation: legBob 0.42s steps(1) infinite alternate-reverse; }
  @keyframes legBob { from { transform: translateY(0); } to { transform: translateY(-1px); } }
  .player-sprite .body { animation: bodyBob 0.42s steps(1) infinite alternate; }
  @keyframes bodyBob { from { transform: translateY(0); } to { transform: translateY(-0.4px); } }
  /* Leaflet default attribution prettier */
  .leaflet-control-attribution { font-size: 9px !important; background: rgba(0,0,0,0.5) !important; color: #aaa !important; }
  .leaflet-control-attribution a { color: #b9bcff !important; }

  /* ===== Final ending (reused) ===== */
  #ending { position: fixed; inset: 0; background: #000;
    display: none; flex-direction: column; align-items: center;
    justify-content: center; z-index: 200;
    color: #ffd966; text-align: center; padding: 30px;
    font-family: 'Georgia', 'Times New Roman', serif;
    opacity: 0; transition: opacity 4s ease-in; }
  #ending.show { display: flex; opacity: 1; }
  #ending p { font-size: 20px; margin: 14px 0; letter-spacing: 1px; line-height: 1.5; opacity: 0; transition: opacity 1.8s; }
  #ending p.small { font-size: 13px; opacity: 0; margin-top: 36px; color: #b9bcff; letter-spacing: 2px; }
  #ending.show p.visible { opacity: 1; }
  #ending.show p.small.visible { opacity: 0.85; }

  #fade-black { position: fixed; inset: 0; background: #000;
    opacity: 0; pointer-events: none; z-index: 180;
    transition: opacity 3.6s ease-in; }
  #fade-black.show { opacity: 1; pointer-events: all; }
</style>
</head>
<body>

<!-- Intro / permissions gate -->
<div id="intro-overlay">
  <div class="modal">
    <h1>Sadia's Quest</h1>
    <div class="sub">Walking Edition</div>
    <p>Seven stops across NYC. Walk to each one to unlock its puzzle.</p>
    <p>Stage 1 starts where the East River meets Long Island City.</p>
    <ul class="tips">
      <li>📍 Allow location when prompted.</li>
      <li>🔆 Keep your screen on (consider Auto-Lock → Never).</li>
      <li>🔋 Bring a charger — GPS is hungry.</li>
      <li>👟 Wear comfortable shoes.</li>
    </ul>
    <button id="beginBtn">BEGIN</button>
  </div>
</div>

<div id="app">
  <div id="hud">
    <span class="left">
      <span class="stage">STAGE <span id="stageNum">0</span>/7</span>
      <span class="target" id="targetLine">Next: —</span>
    </span>
    <span class="actions">
      <button id="muteBtn">SOUND ON</button>
      <button id="resetBtn">RESET</button>
    </span>
  </div>
  <div id="map"></div>
  <div id="hint-bar">
    <p id="hintText">Tap BEGIN to start.</p>
    <button id="imHere">I'M HERE (manual unlock)</button>
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

// =====================================================================
// CONFIG — replace lat/lng with the actual GPS coordinates for each spot.
// Use Google Maps: right-click any location → click the lat,lng readout
// to copy it, then paste below.
// =====================================================================
const DUNGEON_LOCATIONS = [
  { id: 0, name: 'The Ferry',          short: 'LIC Ferry',
    lat: 40.7411, lng: -73.9579,
    hint: 'Walk to the LIC ferry terminal at the East River.' },
  { id: 1, name: 'Brunch',             short: 'Brunch spot',
    lat: 40.7589, lng: -73.9851,   // ← REPLACE with your actual brunch spot
    hint: 'Cross to Manhattan. Head to the brunch spot.' },
  { id: 2, name: 'Pier 97',            short: 'Pier 97',
    lat: 40.7707, lng: -73.9956,
    hint: 'North along the Hudson. Pier 97 is waiting.' },
  { id: 3, name: 'Birthday Rites',     short: 'LIC apartment',
    lat: 40.7461, lng: -73.9501,   // ← REPLACE with the apartment coords
    hint: 'Back home to the LIC apartment.' },
  { id: 4, name: 'Kono',               short: 'Kono · Bowery',
    lat: 40.7234, lng: -73.9907,
    hint: 'The Bowery. Find Kono.' },
  { id: 5, name: 'Washington Square',  short: 'Washington Sq',
    lat: 40.7308, lng: -73.9973,
    hint: 'Under the arch in Washington Square Park.' },
  { id: 6, name: 'Death & Co',         short: 'Death & Co',
    lat: 40.7263, lng: -73.9886,
    hint: 'East Village. The final stop.' },
];
const TRIGGER_RADIUS_M = 60;   // meters — bump up if GPS is flaky in any spot
const DEFAULT_CENTER = [40.7461, -73.9501];
const DEFAULT_ZOOM = 13;
const STATE_KEY = 'sadiaQuestAR_v1';

// =====================================================================
// STATE
// =====================================================================
function defaultState() {
  return {
    stage: 0,
    cleared: [false,false,false,false,false,false,false],
    muted: false,
    manualOverrides: [],
    startedAt: null,
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (!raw) return defaultState();
    return Object.assign(defaultState(), JSON.parse(raw));
  } catch (e) { return defaultState(); }
}
function saveState() {
  try { localStorage.setItem(STATE_KEY, JSON.stringify(state)); } catch (e) {}
}
let state = loadState();

// =====================================================================
// AUDIO (reused from 2D)
// =====================================================================
const audio = {
  ctx: null, bgmGain: null, bgmTimer: null, bgmStep: 0,
  init() {
    if (this.ctx) return;
    try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch (e) { return; }
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
    o.connect(g); g.connect(this.bgmGain);
    const now = this.ctx.currentTime;
    g.gain.setValueAtTime(0, now);
    g.gain.linearRampToValueAtTime(vol, now + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, now + dur);
    o.start(now); o.stop(now + dur + 0.02);
  },
  sfx(name) {
    if (!this.ctx || state.muted) return;
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
    if (name === 'step')    this.tone(220, 0.05, 'square', 0.18);
  },
};

// =====================================================================
// MAP (Leaflet)
// =====================================================================
let map = null;
let playerMarker = null;
let accuracyCircle = null;
let dungeonMarkers = [];     // index = stage id
let userPannedRecently = false;
let userPanTimer = null;

function pinIcon(stageIdx, status) {
  const label = status === 'cleared' ? '✓' : status === 'future' ? '?' : String(stageIdx + 1);
  return L.divIcon({
    className: '',
    html: `<div class="pin ${status}">${label}</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });
}

function initMap() {
  map = L.map('map', { zoomControl: true, attributionControl: true })
        .setView(DEFAULT_CENTER, DEFAULT_ZOOM);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
  }).addTo(map);
  // Place dungeon pins
  DUNGEON_LOCATIONS.forEach((d, i) => {
    const status = state.cleared[i] ? 'cleared' : (i === state.stage ? 'current' : 'future');
    const marker = L.marker([d.lat, d.lng], { icon: pinIcon(i, status) })
                     .bindPopup(`<b>${d.name}</b><br>${d.hint}`)
                     .addTo(map);
    dungeonMarkers.push(marker);
  });
  // Track user pans so we don't fight them when auto-centering
  map.on('dragstart', () => {
    userPannedRecently = true;
    clearTimeout(userPanTimer);
    userPanTimer = setTimeout(() => { userPannedRecently = false; }, 8000);
  });
}

function refreshMarkers() {
  DUNGEON_LOCATIONS.forEach((d, i) => {
    const status = state.cleared[i] ? 'cleared' : (i === state.stage ? 'current' : 'future');
    dungeonMarkers[i].setIcon(pinIcon(i, status));
  });
}

const PLAYER_SVG = `
<svg class="player-sprite" viewBox="0 0 24 30" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
  <ellipse cx="12" cy="27" rx="7" ry="1.6" fill="rgba(0,0,0,0.35)"/>
  <g class="body">
    <rect x="5"  y="2"  width="14" height="5" fill="#2a1a0e"/>
    <rect x="4"  y="5"  width="3"  height="9" fill="#2a1a0e"/>
    <rect x="17" y="5"  width="3"  height="9" fill="#2a1a0e"/>
    <rect x="5"  y="13" width="14" height="2" fill="#2a1a0e"/>
    <rect x="7"  y="5"  width="10" height="8" fill="#d2a679"/>
    <rect x="9"  y="9"  width="2"  height="2" fill="#1a0a0e"/>
    <rect x="13" y="9"  width="2"  height="2" fill="#1a0a0e"/>
    <rect x="8"  y="11" width="1"  height="1" fill="#e89a9a"/>
    <rect x="15" y="11" width="1"  height="1" fill="#e89a9a"/>
    <rect x="5"  y="14" width="14" height="6" fill="#ff77aa"/>
    <rect x="5"  y="19" width="14" height="1" fill="#ff558b"/>
    <rect x="4"  y="15" width="1"  height="4" fill="#d2a679"/>
    <rect x="19" y="15" width="1"  height="4" fill="#d2a679"/>
  </g>
  <g class="leg-l">
    <rect x="7"  y="20" width="4" height="3" fill="#3a5da8"/>
    <rect x="7"  y="23" width="4" height="1" fill="#1a1a2e"/>
  </g>
  <g class="leg-r">
    <rect x="13" y="20" width="4" height="3" fill="#3a5da8"/>
    <rect x="13" y="23" width="4" height="1" fill="#1a1a2e"/>
  </g>
</svg>`;

function setPlayer(lat, lng, accuracy) {
  if (!playerMarker) {
    playerMarker = L.marker([lat, lng], {
      icon: L.divIcon({ className: '', html: PLAYER_SVG, iconSize: [32, 42], iconAnchor: [16, 38] })
    }).addTo(map);
    accuracyCircle = L.circle([lat, lng], {
      radius: accuracy || 30,
      color: '#ffd966', fillColor: '#ffd966', fillOpacity: 0.08, weight: 1
    }).addTo(map);
    // First fix: center on player
    map.setView([lat, lng], Math.max(map.getZoom(), 15));
  } else {
    playerMarker.setLatLng([lat, lng]);
    accuracyCircle.setLatLng([lat, lng]);
    if (accuracy) accuracyCircle.setRadius(accuracy);
    // Auto-recenter if she's near the edge of the visible map and hasn't panned recently
    if (!userPannedRecently) {
      const bounds = map.getBounds();
      const pad = bounds.pad(-0.25);
      if (!pad.contains([lat, lng])) map.panTo([lat, lng]);
    }
  }
}

// =====================================================================
// GEOLOCATION
// =====================================================================
let watchId = null;
let lastPos = null;
let triggerLocked = false;   // prevents retrigger while standing in zone

function startWatching() {
  if (!navigator.geolocation) {
    document.getElementById('hintText').textContent =
      '⚠️ Your browser does not support location. Tap I\'M HERE at each spot.';
    return;
  }
  watchId = navigator.geolocation.watchPosition(onPos, onPosError, {
    enableHighAccuracy: true, maximumAge: 5000, timeout: 15000
  });
}

function onPos(pos) {
  const { latitude, longitude, accuracy } = pos.coords;
  lastPos = { lat: latitude, lng: longitude, acc: accuracy };
  if (!state.startedAt) { state.startedAt = new Date().toISOString(); saveState(); }
  setPlayer(latitude, longitude, accuracy);

  if (state.stage >= 7) {
    updateHud(null);
    return;
  }
  const target = DUNGEON_LOCATIONS[state.stage];
  const distM = haversineM(latitude, longitude, target.lat, target.lng);
  updateHud(distM);

  // Check trigger
  if (distM <= TRIGGER_RADIUS_M && !triggerLocked && !state.cleared[state.stage] && !modalOpen()) {
    triggerLocked = true;
    openDungeon(state.stage);
  } else if (distM > TRIGGER_RADIUS_M + 15) {
    // exited the zone — unlock so future arrivals can retrigger (after closing without solving)
    triggerLocked = false;
  }
}

function onPosError(err) {
  const map = { 1: 'Location permission denied.', 2: 'Position unavailable.', 3: 'Location timeout.' };
  const msg = map[err.code] || 'GPS unavailable.';
  document.getElementById('hintText').textContent = `⚠️ ${msg} Tap I'M HERE when you arrive.`;
}

function haversineM(lat1, lng1, lat2, lng2) {
  const R = 6371000;
  const toRad = (d) => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng/2)**2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

// =====================================================================
// HUD
// =====================================================================
const stageNumEl = document.getElementById('stageNum');
const targetLineEl = document.getElementById('targetLine');
const hintTextEl = document.getElementById('hintText');

function updateHud(distM) {
  stageNumEl.textContent = state.stage;
  if (state.stage >= 7) {
    targetLineEl.textContent = 'COMPLETE ★';
    hintTextEl.textContent = 'You finished. Open the letter.';
    return;
  }
  const target = DUNGEON_LOCATIONS[state.stage];
  if (distM == null) {
    targetLineEl.textContent = `Next: ${target.short}`;
  } else if (distM < 1000) {
    targetLineEl.textContent = `Next: ${target.short} · ${Math.round(distM)}m`;
  } else {
    targetLineEl.textContent = `Next: ${target.short} · ${(distM/1000).toFixed(2)}km`;
  }
  hintTextEl.textContent = target.hint;
}

// =====================================================================
// MODAL / DUNGEONS
// =====================================================================
const modalRoot = document.getElementById('modal-root');
let currentDungeon = null;
function modalOpen() { return currentDungeon !== null; }

function closeModal() {
  modalRoot.classList.remove('show');
  modalRoot.innerHTML = '';
  currentDungeon = null;
}

function clearDungeon(idx) {
  state.cleared[idx] = true;
  state.stage = Math.max(state.stage, idx + 1);
  saveState();
  refreshMarkers();
  audio.sfx('success');
  triggerLocked = false;
  // Update HUD immediately even if we don't have a fresh GPS fix
  if (lastPos) {
    if (state.stage < 7) {
      const t = DUNGEON_LOCATIONS[state.stage];
      updateHud(haversineM(lastPos.lat, lastPos.lng, t.lat, t.lng));
    } else updateHud(null);
  } else updateHud(null);
}

function openDungeon(idx) {
  if (currentDungeon !== null) return;
  if (state.cleared[idx]) return;
  currentDungeon = idx;
  audio.init();
  audio.sfx('enter');
  modalRoot.innerHTML = DUNGEONS[idx].html;
  modalRoot.classList.add('show');
  if (DUNGEONS[idx].onOpen) DUNGEONS[idx].onOpen();
}

function norm(s) { return (s || '').trim().toLowerCase(); }

// =====================================================================
// 7 DUNGEONS — verbatim from 2D build
// =====================================================================
const DUNGEONS = [
  // Stage 1: Ferry
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

  // Stage 2: Brunch
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

  // Stage 3: Pier 97 Terminal
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

  // Stage 4: Birthday Rites
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

  // Stage 5: Kono memory match
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
          if (firstPick === null) { firstPick = tile; return; }
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

  // Stage 6: Washington Square
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

  // Stage 7: Death & Co
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
        try { localStorage.setItem('sadiaFinalMemory', v); } catch (e) {}
        clearDungeon(6);
        closeModal();
        playEnding();
      });
    }
  },
];

// =====================================================================
// ENDING
// =====================================================================
function playEnding() {
  const fade = document.getElementById('fade-black');
  const ending = document.getElementById('ending');
  fade.classList.add('show');
  setTimeout(() => {
    ending.classList.add('show');
    setTimeout(() => document.getElementById('end1').classList.add('visible'), 800);
    setTimeout(() => document.getElementById('end2').classList.add('visible'), 3200);
    setTimeout(() => document.getElementById('end3').classList.add('visible'), 6000);
  }, 3400);
}

// =====================================================================
// HUD BUTTONS
// =====================================================================
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

document.getElementById('imHere').addEventListener('click', () => {
  if (state.stage >= 7) return;
  const target = DUNGEON_LOCATIONS[state.stage];
  if (!confirm(`Open the puzzle for "${target.name}"? Only use this if you have arrived but GPS hasn't triggered.`)) return;
  state.manualOverrides.push({ idx: state.stage, ts: Date.now() });
  saveState();
  openDungeon(state.stage);
});

// =====================================================================
// SCREEN WAKE LOCK (best effort)
// =====================================================================
let wakeLock = null;
async function requestWakeLock() {
  try {
    if ('wakeLock' in navigator) {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeLock.addEventListener('release', () => { wakeLock = null; });
    }
  } catch (e) {}
}
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && !wakeLock) requestWakeLock();
});

// =====================================================================
// BOOT
// =====================================================================
document.getElementById('beginBtn').addEventListener('click', () => {
  document.getElementById('intro-overlay').style.display = 'none';
  audio.init();
  initMap();
  startWatching();
  requestWakeLock();
  updateHud(null);
  // If audio context is suspended (autoplay policy), tap will resume
  if (audio.ctx && audio.ctx.state === 'suspended') audio.ctx.resume();
});

// If she's already started before (save exists), still show the intro once per session
// but pre-fill state so she can continue from where she left off.
updateHud(null);
</script>
</body>
</html>"""

components.html(GAME_HTML, height=820, scrolling=False)
