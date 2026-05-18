# Project: "Sadia's Quest" - 2D RPG Scavenger Hunt

## Objective
Act as an expert HTML5 Canvas Game Developer and Python Engineer. Build a Streamlit application that hosts a fully playable, top-down 2D RPG game (similar to classic Pokémon/Zelda). Streamlit is only the wrapper; the entire game must be built using HTML, CSS, and JavaScript injected via `st.components.v1.html(..., height=800)`.

## Game Engine & Technical Architecture (CRITICAL)
- **The Engine:** Build a tile-based HTML5 Canvas game. 
- **Mobile First Controls:** Since she will play this on her phone while walking around NYC, you MUST implement an on-screen CSS/JS D-Pad (Up, Down, Left, Right) that controls the player character, alongside keyboard arrow support.
- **Save State:** Use browser `window.localStorage.setItem` and `getItem` to track `gameProgress` (Stage 1 to 7) and `playerX`/`playerY` coordinates. If she refreshes the page on her phone, she must spawn exactly where she left off with her progress intact.
- **The Sprite:** Use Canvas `fillRect` or base64 encoded pixel art to draw the player sprite: a cute, 16x16 or 32x32 pixel-art girl with tan skin. Implement simple 2-frame walking animations if possible.
- **Collision & Blocking:** Implement a 2D array tilemap. 0 = walkable, 1 = wall/water, 2 = Snorlax/Gate. The map must feature "Gates" (blocked paths). For example, the bridge from LIC to Manhattan is blocked by an NPC or barrier that only disappears when Stage 1 is cleared.

## Map Design (Pixelated New York)
The tilemap should represent a miniaturized NYC:
- **Starting Area (Right side):** Long Island City.
- **Middle Barrier:** A river of blue tiles with a single path (The Ferry/Bridge).
- **Main Area (Left side):** Manhattan. Contains various distinct zones for the remaining Dungeons.
- **Dungeon Entrances:** Visually distinct tiles (like a glowing square or a building door). When the player steps on a Dungeon tile, it triggers an HTML/CSS overlay Modal for the puzzle.

---

## The 7 Dungeons (Interactive Modals)
When the player triggers a Dungeon, pause the Canvas game and show a stylized HTML/CSS modal. The player must clear it to update `gameProgress` and remove the map barriers.

### Stage 1: The Ferry (LIC side)
- **UI:** A dialog box with two input fields. 
- **Prompt:** "What was the earliest mode of transportation to Manhattan from LIC?" (Requires `ferry`). "When was regular ferry service first established?" (Requires `1642` or `1600s`).
- **Success:** Trigger a CSS animation of a ship sailing across the modal. The map barrier blocking the river is removed.

### Stage 2: Brunch (Manhattan Side)
- **UI:** An interactive keypad or multiple-choice buttons: `85`, `90`, `97`, `112`.
- **Prompt:** "What is the pier that we went to for our first date?"
- **Success:** Selecting `97` turns green, plays a success chime, unlocks the path to the West Side.

### Stage 3: Pier 97
- **UI:** An arcade-style terminal.
- **Prompt:** "Collaborate to clear 3 rounds of Project Makeover. Enter the confirmation code."
- **Success:** She types `cleared`. Trigger CSS glowing "LEVEL CLEAR" text. Unlocks the path back to the LIC apartment area.

### Stage 4: The Birthday Rites (LIC Apartment)
- **UI:** An RPG inventory screen. 
- **Prompt:** "What is the snack that is mandatory to consume to celebrate one’s birthday in Bangladeshi culture?" (Requires `paayesh` or `payesh`).
- **Success:** Render a pulsing pixel-art Treasure Chest. When she taps it, it opens to reveal: *"Save Point Unlocked. Find the golden item hidden in the apartment and EQUIP NEW ARMOR. Rest, and change into evening wear."*

### Stage 5: Kono (The Bowery)
- **UI:** CSS Interactive Flip-Cards. Three cards showing facts: 1. The Gizzard (Rocks), 2. Chicken Tax (1963 tariff), 3. Retinal Physics. She must click to flip them.
- **Prompt:** "What rare state of matter describes the layout of a chicken's retina?" (Requires `hyperuniformity`). 
- **Success:** Unlocks the path to the Park.

### Stage 6: Washington Square Park
- **UI:** A moody, typewriter-effect screen.
- **Prompt:** Use JS to slowly type out: *"Some greet me as a friend, some flee me as a foe... I have no lungs, yet I will take your breath..."*
- **Success:** Input requires `death`. Unlocks the final map tile.

### Stage 7: Death & Co (Final Boss)
- **UI:** A text area for her favorite memory. 
- **Success (Cinematic Ending):** When submitted, fade the entire Canvas and HTML wrapper to black using a slow CSS transition. Fade in elegant gold text:
  > *"Happy Birthday Sadia."*
  > *"You are the most wonderful thing that has ever happened to me."*
  > *"Open the physical letter."*