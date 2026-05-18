# Sadia's Quest — Project Notes

A birthday-gift game for Sadia. Started as a 2D top-down Pokémon-style RPG, then evolved into a real-world walking scavenger hunt across NYC. Multiple variants live on parallel git branches so any version is always playable.

---

## Current state at a glance

| Branch | Variant | Status | Use it for |
|--------|---------|--------|------------|
| `main` | 2D top-down RPG | ✅ Complete, playable | Couch fallback if AR fails |
| `ar-walk` | Real-world GPS scavenger hunt | ✅ Complete, **production target** | The actual birthday day |
| `3d-pov` | First-person 3D dungeon-crawler | 🟡 Branch created, not built | Optional future direction |

Remote: https://github.com/jasonan0609/528_sadia

Same single-file architecture in all variants: `app.py` is a thin Streamlit wrapper that injects one massive inline HTML/CSS/JS string via `st.components.v1.html(...)`. Streamlit is just a host; the game is pure browser code.

---

## The 7 puzzles (current answer key)

These are identical across both built variants — the puzzle layer is renderer-agnostic.

| # | Name | Mechanic | Correct answer |
|---|------|----------|----------------|
| 1 | The Ferry | Two text inputs + CSS ship-sail animation | `ferry` + `1642` (1600–1680 also accepted with a "close enough" message) |
| 2 | Brunch | Four multiple-choice buttons (85 / 90 / 97 / 112) | Tap `97` |
| 3 | Pier 97 | Retro green terminal with blinking caret | Type `cleared` |
| 4 | Birthday Rites | RPG inventory + text input → pulsing treasure chest | `paayesh` / `payesh` / `payash` / `paayash`, then tap chest |
| 5 | Kono | 4×2 memory-match game (🐔 🪨 👁️ 🚛, two of each, shuffled) | Match all 4 pairs |
| 6 | Washington Square | Typewriter riddle (7-line poem about death) | Type `death` |
| 7 | Death & Co | Textarea for favorite memory | Any text ≥ 5 chars → triggers fade-to-gold ending |

**Riddle text (Stage 6) — verbatim, do not change without checking with the user:**

```
Some greet me as a friend, some flee me as a foe,
But I am the final destination everyone must know.
I bring an end to sorrow, but also end your glee,
Kings and beggars both must yield their time to me.
I have no lungs, yet I will take your breath,
And leave you sleeping soundly where there is nothing left.
What am I?
```

**Ending text** (after Stage 7 submit, fades in over black):

> Happy Birthday, Sadia.
> You are the most wonderful thing that has ever happened to me.
>
> *Open the physical letter.*

---

## `main` — 2D top-down build

Classic Pokémon/Zelda feel.

- 20×25 tile map: LIC on the right, East River with bridge in the middle, Manhattan on the left (Pier 85-97, Washington Sq, Bowery, East Village).
- Camera-scrolling viewport (15×11 tiles visible at 24px each = 360×264 canvas).
- Pixel-art tan girl sprite: dark hair, pink shirt, blue pants, 2-frame leg-shuffle walk. Drawn entirely with `fillRect` — no asset files.
- Each gated dungeon (D3–D7) is enclosed in a 3×3 building of wall tiles; the gate is the only way in.
- Dungeon trigger: step on the dungeon tile → modal opens (auto, no button press).
- Gates render with a themed sprite per kind: NPC dock master, rope, door, fence, lantern, shadow.
- Controls: arrow keys (no WASD — removed because it conflicted with text inputs) + on-screen D-pad (`pointerdown`/`pointerup` with 140ms held-repeat).
- Procedural Web Audio bgm: 16-step C-major lead+bass at ~120bpm. SFX: bump / step / success / fail / enter.
- localStorage key: `sadiaQuestState_v2` (single JSON blob — replaces the original scattered `sadiaX`/`sadiaY` keys).
- HUD: stage counter, live zone name, mute, RESET (with `confirm()`).

---

## `ar-walk` — real-world GPS scavenger hunt (production)

She physically walks across NYC. Each of the 7 dungeons is pinned to a real address; arriving within ~60m auto-triggers the puzzle. **Same 7 puzzles, same correct answers — only the trigger mechanism changed.**

### Architecture
- Leaflet 1.9.4 + OpenStreetMap tiles (free, no API key) loaded from unpkg CDN.
- `navigator.geolocation.watchPosition` for live tracking.
- Haversine distance from player → current target.
- Sequential gating: only the current `state.stage` pin can trigger.
- Intro modal with **BEGIN** button — required so first GPS request fires from a user gesture (iOS Safari rule).
- Manual override: always-visible **I'M HERE** button with confirm dialog. Use case: indoor stages where GPS dies, or just-arrived-but-game-hasn't-updated.
- Screen wake-lock API (iOS 16.4+ / modern Android) to fight auto-lock during long walks.
- Pixel-art tan girl from 2D is now the GPS marker — rendered as inline SVG with a leg-bob walk animation, iconAnchor at her feet so her shoes sit on her actual coordinate.
- Map pin states: cleared = green ✓, current = pulsing gold, future = faint grey ?.
- HUD: stage counter, live `Next: <name> · <distance>m`, mute, RESET.
- localStorage key: `sadiaQuestAR_v1`. No x/y (GPS provides it). Stores `stage`, `cleared[]`, `muted`, `manualOverrides[]`, `startedAt`.

### Coordinates config
Top of the inline `<script>` in `app.py`, look for `const DUNGEON_LOCATIONS = [...]`. Seven entries with `lat`, `lng`, `name`, `short`, `hint`. Public spots (Pier 97, Washington Sq, Kono on Bowery, Death & Co, LIC Ferry terminal) are seeded with approximate real coords. **Two are marked `← REPLACE`**:
- D2 Brunch (Manhattan-side brunch spot) — needs the actual brunch venue's coords
- D4 Birthday Rites (LIC apartment) — needs the apartment coords

To grab a precise coord: right-click in Google Maps → click the lat/lng readout at the top of the popup → copy.

`TRIGGER_RADIUS_M = 60` is tunable per spot if any location's GPS is flaky in NYC's urban-canyon zones.

### Hosting
- Local dev: `streamlit run app.py` works on localhost. Browser geolocation requires HTTPS *or* localhost.
- Phone testing: `ngrok http 8501` from a second terminal gives a temporary HTTPS URL.
- Production (for the actual birthday): **Streamlit Community Cloud**, pointed at the `ar-walk` branch (not main). Free, HTTPS, no Mac dependency once deployed.

### Desktop trigger simulation
Chrome DevTools → ⋮ → More tools → **Sensors** → **Location** → "Other..." → paste any pin's lat/lng. Modal fires within ~5 seconds. Lets you walk through all 7 stages from the couch.

---

## `3d-pov` — first-person 3D (unbuilt)

Branch exists at the same baseline commit as `main`. Plan was: Three.js scene with smooth free movement, fog-of-war mini-map top-right. Never started — pivoted to AR instead. Plan file: `~/.claude/plans/so-i-want-you-serialized-pudding.md` (current version reflects AR, prior 3D plan was overwritten).

---

## Decisions made along the way

These are worth knowing if you tweak anything:

- **Stage 5 was originally a typed riddle ("hyperuniformity")** — replaced with a 4×2 memory-match game because she couldn't reasonably guess it.
- **Stage 6 riddle was rewritten** to point more clearly at "death" (original was vague). User provided the exact 7-line text.
- **Stage 1 year** accepts `1642` exactly OR any year 1600–1680 with a "Close enough! It was 1642." message.
- **WASD was removed** from keyboard input — it was intercepting key presses inside the text-input modals (typing "w" in the memory textarea would prevent default). Arrow keys only.
- **No camera/AR overlay** in `ar-walk` — pure map-based. WebXR is a non-starter on iOS Safari.
- **No external asset files** anywhere. All sprites: SVG/canvas `fillRect`. All audio: Web Audio oscillators. All textures: procedural canvas.

---

## How to run

```bash
cd /Users/junghyunan/Projects/birthday
git checkout ar-walk          # or main for the 2D version
streamlit run app.py
```

First install: `pip install -r requirements.txt` (just `streamlit`).

---

## Open items before her birthday

- [ ] Paste real coords into `DUNGEON_LOCATIONS` for D2 (brunch spot) and D4 (apartment).
- [ ] Verify the 5 seeded coords actually point at the right doorway in Google Maps.
- [ ] Deploy `ar-walk` to Streamlit Community Cloud, get a permanent `https://….streamlit.app` URL.
- [ ] On her phone: open the URL once, allow location, set Auto-Lock → Never, charge to 100%, bring a charger.
- [ ] Walk-test the full route at least once before the day to catch any GPS dead zones.
- [ ] Write and seal the "physical letter" the ending refers to.
