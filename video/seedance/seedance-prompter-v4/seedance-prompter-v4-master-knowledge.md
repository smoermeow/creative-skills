# Seedance 2.0 Prompter — Master Knowledge Base v4

This document is the reference library for generating Seedance 2.0 cinematic prompts. It contains the template anatomy, field-by-field guidance, model-specific rules derived from the official ByteDance prompt guide, reference-image discipline (hard-won from production), genre adaptation patterns, and full example prompts.

---

## 1. Template Anatomy

The prompt template has four layers. Each layer must be present in every prompt.

### Layer 1: Scene Identity
Establishes the global visual contract. Everything in the shot sequence is filtered through this.

- `[TITLE]` — Short, evocative name for the scene.
- `[REFERENCES]` — **REQUIRED AS THE SECOND FIELD.** Governs how reference images are used. See Section 7 for full rules.
- `[STYLE]` — The genre, aesthetic reference, and visual philosophy. This is the single most important stylistic field. Be specific: name cinematic references, art movements, production styles. Resolution targets (4K, 2K) belong here as style anchors, not as technical specs.
- `[VISUAL FEEL]` — Describe the visual rhythm and texture of the footage using sensory language. Prioritize words like "slow," "smooth," "warm," "gritty," "stable," "dreamy," "handheld," "gentle." Technical camera specs (f-stops, ISO, focal length in mm) should be avoided — the model responds to rhythmic feel descriptors, not photography jargon. Rendering intentions (subsurface scattering, volumetric fog, film grain) are acceptable here because they describe visible texture, not camera settings.
- `[DURATION]` — Clip length in seconds. Drives the shot-sequence segmentation.

### Layer 2: Characters and Setting
Every entity that appears on screen — characters, objects, hands, creatures, props with agency — must be defined here before the shot sequence begins.

Required fields per character:
- `Base:` — What it is and which reference image it matches (if any). Format: `"matching reference @image1"` with NO space between @ and image number.
- `Features:` — Physical description. Specific enough to render: colors by name, materials by texture, wardrobe by item.
- `Physics / personality / detail:` — How it moves, deforms, or emotes. Material behavior (jiggles, flexes, glows). Personality expressed through physicality, not adjectives.

Conditionally included fields (use when relevant):
- `Motion anchor:` — Use this field INSIDE the character block to specify movement restrictions for that character in this specific clip. Example: *"Leans toward the orb without stepping, casually raises a loose fist, then lowers it and settles back when the orb recoils. Never strikes or touches it."* This places movement rules adjacent to the character description where the model parses them together, rather than buried in the `avoid` list at the bottom.
- `Emotional state:` — For character-heavy dramatic scenes, use this to specify the tone and demeanor the character carries throughout. Example: *"Composed menace snaps into startled disgust; her panic contrasts with the boy’s and ghost’s restrained, deadpan reactions."*
- `State in this scene:` — For multi-clip sequences, use this to specify the character's starting state in this clip (wounds, missing parts, posture, current activity). See Section 7 on damage continuity. Example from Slime Panic: *"Holding the completed landing pose, coated in clear, slightly cloudy saliva with a faint blue-gray tint."*
- `Power:` or `Power this scene:` — For characters with specific abilities that activate in this clip, describe the mechanical behavior of the power so the model can render it.

Use `[SETTING]` when the environment needs to be defined before the shot sequence. Name the setting, then describe it with relevant fields such as `Base:`, `Features:`, or `Physics:`.

### Layer 3: Shot Sequence
The shot-by-shot timeline. Every second of the clip must be accounted for in discrete timestamp ranges. **Stagger shot durations based on scene rhythm — do not default to evenly split intervals.** See Section 10.

Timestamp format: `XX–YY — SHOT NAME:` where XX is start second and YY is end second.

Required per shot:
- `Camera:` — One primary movement instruction. Optionally one secondary. Never more than two. Describe using rhythm words rather than technical parameters. See Section 2 for the full camera discipline system.
- `Action:` — Specific physical movements. Choreography, not summary. Every action should be visually renderable.
- `Lighting:` — Brief per-shot lighting note. Even 3–5 words here has outsized impact on output quality.

Conditionally included per shot:
- `Dialogue:` — Exact lines if spoken. Use a semicolon after the speaker name: `Dialogue: Character; "Line."`
- `VFX:` — Particle effects, material transformations, physics events.
- `Reaction:` — Character response if separate from main action.
- `SFX:` — Sound effects tied to this specific beat.

### Layer 4: Production Notes
Contextual information that applies across the whole scene but lives outside the timeline.

Common sub-fields:
- `Audio design:` — Sound philosophy, music cues, silence, ambient tone.
- `Lighting:` — Overall lighting strategy and shifts across the clip. Per-shot lighting notes in the shot sequence override this for their specific beat.
- `Subtext:` — What the scene is really about. Emotional thesis. Comedic logic. Lore grounding.
- `Critical constraint:` — Hard creative rules the model must respect. Spatial continuity rules for multi-character scenes (e.g., "both characters face each other across the aisle throughout"). Repeat key reference-handling rules here for extra enforcement.
- `Avoid:` — Model stability constraints. Standard baseline: "avoid jitter and bent limbs." See Section 5.
- `Animation style:` — Frame rate cadence, interpolation rules, stop-motion holds.

---

## 2. Camera Discipline System

### The One-Primary Rule
Every `Camera:` field must have **one primary movement instruction.** Optionally add **one secondary instruction** using "then" to sequence them. Never stack three or more.

**DO:**
```text
Camera: Slow push-in, low angle.
Camera: Handheld tracking shot, then gentle rise.
Camera: Static wide shot. Hold.
```

**DON'T:**
```text
Camera: Handheld over-the-shoulder tracking shot from behind and slightly below, pushing through the crowd with anamorphic streak flares and focus hunting.
```
That's four competing instructions. The model will jitter trying to satisfy all of them.

### Rhythm Over Specs
The model responds to rhythm language, not technical parameters.

| Use These (Rhythm) | Not These (Specs) |
|---------------------|-------------------|
| slow, smooth, gentle, gradual | 24fps, f/2.8, ISO 800 |
| controlled, stable, steady | focal length 85mm |
| dynamic, swift (use sparingly) | shutter speed 1/50 |
| imperceptible, barely moving | rack focus at 0.3m |

Technical specs can appear in `[STYLE]` as aesthetic anchors ("35mm film tone") but should not drive camera behavior.

### Speed Asymmetry Rule
**Never combine fast camera movement + fast subject action + complex scene.** This is the #1 cause of artifacts and jitter.

- If the action is fast → camera should be slow/stable.
- If the camera is dynamic → action should be controlled/deliberate.
- Complex scenes (many elements, particles, crowd) → both camera and action should be slow.

Only one speed axis can be "fast" at a time.

### Separate Camera from Subject
Camera movement and subject movement must be described independently. Don't blend them.

**DO:**
```text
Camera: Fixed wide shot. Hold.
Action: The dancer spins slowly across the frame.
```

**DON'T:**
```text
Camera: Spinning camera around a dancing person.
```

### Supported Camera Types

| Camera Type | Best For |
|-------------|----------|
| Push-in / dolly in | Close-up emphasis, emotional focus |
| Pull-out / dolly out | Environmental reveal, context |
| Pan / lateral | Tracking, scanning |
| Tracking / follow | Action, walking |
| Orbit / arc | Product showcase, portraits |
| Aerial / drone | Landscapes, scale |
| Handheld | Documentary, realism |
| Fixed / locked-off | Focus on subject action |
| Tilt | Reveals, scale emphasis |
| Crane | Dramatic transitions |

### Position/Angle Vocabulary
Use these to set the camera's starting position before describing its movement:

- Extreme macro close-up
- Low tabletop angle
- Over-the-shoulder
- High-angle master shot
- Dutch angle (tilted frame)
- First-person POV
- Low angle looking up
- Medium two-shot
- Wide establishing shot
- Overhead top-down
- 90-degree side profile at ground level
- Extreme low-angle worm's-eye
- Inverted orientation (upside-down)
- Lateral side-view two-shot

### Lens Effects
These belong in `[VISUAL FEEL]` or `VFX:` — not crammed into the `Camera:` field:

- Focus rack between subjects
- Shallow DOF with soft bokeh
- Anamorphic streak flares
- Film grain
- Motion blur
- Lens distortion on edges

---

## 3. Action Writing Rules

Every verb should describe a visible, frame-by-frame movement.

**DO:**
- "Her eyes well up with tears. She pouts her lips excessively. She quickly grabs all three daifukus, hugging them to her chest."
- "It rotates right, glides toward the socket and unfolds its manipulator. The arm recedes diagonally from the large foreground shell toward the smaller socket, reinforced by converging wall seams. Its probe inserts and turns; small hover corrections keep it connected while processing."
- "A robot lunges. Eldric lands on its forearm, slides to its chest, and sweeps one open hand through the torso in one cyan-black arc. The machine separates into upper and lower halves as he passes."

**DON'T:**
- "She gets upset and grabs the food."
- "The orb activates the mechanism."
- "Eldric defeats a robot."

The difference: specific physical choreography vs. narrative summary. Every verb should describe a visible, frame-by-frame movement.

### Dangerous Action Words
Avoid vague intensity modifiers that give the model no visual instruction:

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| "epic" | Model doesn't know what it means | Describe the specific visual effect |
| "amazing" / "beautiful" | Adjectives without guidance | Specific lighting, composition, texture |
| "lots of movement" | Causes jitter from over-motion | One specific, described motion |
| "fast" (unqualified) | Causes chaos without direction | "swift single step" or keep action slow |
| "cool" / "dynamic" | Vague aesthetic | Name the exact aesthetic reference |

---

## 4. Lighting as a Lever

The official Seedance guide identifies lighting description as the **highest-leverage single element** in any prompt. One lighting line does more for output quality than ten adjectives.

### Per-Shot Lighting
Every shot block should include a `Lighting:` field, even if it's brief. Examples:

```text
Lighting: Warm golden-hour backlight through window.
Lighting: Single red overhead wash, everything else dark.
Lighting: Soft overcast diffused light, even and flat.
Lighting: Neon blue rim light against deep shadow.
Lighting: Strobe pulses, white and violet, through haze.
```

### High-Impact Lighting Keywords

| Keyword | Effect |
|---------|--------|
| golden hour | Warm golden tones, long shadows |
| rim light | Edge highlights separating subject from background |
| natural light | Soft, realistic illumination |
| neon | Colored glow, cyberpunk/urban |
| backlit | Silhouette potential, dramatic depth |
| overcast | Even, diffused, no harsh shadows |
| volumetric | Light rays visible through fog/haze/dust |
| practical light | Light source visible in frame (lamp, candle, screen) |

### Overall Lighting Strategy
Still include in `[PRODUCTION NOTES]` → `Lighting:` for the global philosophy. Per-shot notes override for their specific beat.

---

## 5. Stability Constraints (Negative Prompts)

Include an `Avoid:` field in `[PRODUCTION NOTES]` on every prompt.

### Standard Baseline (include on every prompt):
```text
Avoid: Jitter, bent or distorted limbs.
```

### Add Based on Scene Type:

| Condition | Add to Avoid |
|-----------|-------------|
| Clips over 10 seconds | "temporal flicker" |
| Character-driven scenes | "identity drift" |
| Complex scenes (crowd, particles, many elements) | "chaotic composition" |
| Multi-shot with same character | "inconsistent features between shots" |
| Slow/contemplative scenes | "unnecessary camera movement" |
| Scenes with reference images | "Character frozen in reference-image pose" (see Section 7) |

### Words That Degrade Quality
These keywords in any field tend to produce worse output:

- "fast" without qualification
- "cinematic" used alone (too vague — always pair with a specific reference)
- "epic" (meaningless to the model)
- "amazing" / "beautiful" / "stunning" (adjectives without visual instruction)
- Stacking multiple unqualified speed words

---

## 6. Genre Adaptation Patterns

The template skeleton stays the same. The vocabulary, density, and emphasis shift by genre.

### Cute / Kawaii / Stop-Motion
- `[STYLE]` references Laika, Aardman, Pixar short films. Names material textures (clay, felt, dough).
- Character modeling emphasizes tactile material physics (jiggles, squishes, bounces).
- Action lines lean into exaggerated expressions and held comedic beats.
- Production notes specify animation cadence ("stop-motion holds and pops, no smooth tweening").
- SFX are diegetic and ASMR-forward.
- Camera should be mostly fixed or slow. Let the characters carry the energy.

### Cyberpunk / Horror / Action
- `[STYLE]` references specific films or directors, volumetric atmospheric effects.
- Character modeling emphasizes material science (automotive paint sheen, translucent tubing, chrome vertebrae).
- Action lines are rapid and precisely sequenced — but apply the speed asymmetry rule.
- Camera work can be aggressive but must still follow the one-primary rule.
- Audio design often uses silence as a weapon — contrast between chaos and dead quiet.

### Comedy / Dramedy / Dialogue-Driven
- `[STYLE]` references specific shows or directors for comedic timing.
- Character modeling includes personality and wardrobe as comedy signals.
- The shot sequence is paced around dialogue beats, not visual spectacle.
- Camera work uses snap-zooms and held reaction shots for comedic timing.
- Production notes include a `Subtext:` field explaining the joke's underlying logic.

### Anime / Moe / Japanese Healing
- `[STYLE]` references specific anime aesthetics (4K Moe, healing genre, ukiyo-e).
- Character modeling includes anime-specific features (ahoge, chibi proportions, star-highlights in eyes).
- VFX stays stylized — painted-on effects, 2D surface animation, watercolor dissolves.
- Lighting is warm, golden-hour, with soft-focus bokeh. Per-shot lighting notes matter here.
- Audio tends toward quiet ambient and ASMR.

### Game / HUD / Interactive Style
- `[STYLE]` specifies game genre and perspective (TPS, FPS, ADS transitions).
- Adds a `[UI OVERLAY]` section with HUD element placement.
- Adds `[ANIMATION LOGIC]` with state machines (start_state → mechanics → end_state).
- Camera describes perspective transitions as single primary instructions per beat.

### Cyberpunk Anime / Comedy-Thriller
- `[STYLE]` defines retro OVA cel animation, mechanical grime, hard shadows, and held comic reactions.
- Character movement rules preserve the ghost’s compact scale and the hunter’s transition from composed menace to exaggerated panic.
- Keep room geography or foreground/midground staging explicit, using the relevant scene rather than mixing locations.
- Build comedy through contrasting performances: the hunter panics while the boy and ghost remain restrained.
- Preserve dialogue and delivery order; in Slime Panic, the boy speaks only after the hunter reaches the water.
- Audio uses the specified machine hum, bag crinkle, breach impacts, drips, footsteps, and splashes where those actions occur; no music in these examples.

---

## 7. Reference Image Discipline

**This section is the most important one in this document for multi-clip production work. The failures that happen early in any project are almost always failures of reference discipline. Apply these rules from the first prompt and cold-start drift disappears.**

### The Core Problem
Reference images are labeled `@image1`, `@image2`, etc. The model reads them first, processes their compositions, poses, and framings, and uses that visual information as a prior for how the scene should look. If the prompt's anti-reference language is buried at the bottom in `Avoid:` or `Critical constraint:`, the model sees the image composition before it sees the instruction not to reproduce it. The result is scene drift back toward the reference image pose.

### Rule 1: `[REFERENCES]` is the second field, always
Place a `[REFERENCES]` field immediately after `[TITLE]` and before `[STYLE]`. This ensures the model parses the reference-use instructions before processing character descriptions or the shot sequence. Non-negotiable for any prompt using reference images.

### Rule 2: Name the specific reference-image composition to avoid
A general disclaimer like "reference image is for character design only" does not work. The model needs the failure mode described by name. Open the reference image, identify the specific pose/framing/composition elements that would cause drift, and name them directly.

**Weak (ineffective):**
```text
[REFERENCES]
The reference image is for character design only, not scene composition.
```

**Strong (effective), adapted from Ceiling Breach:**

Reference tags are local to this excerpt: ghost `@image1`, safehouse `@image2`, alien `@image3`, boy `@image4`.

```text
[REFERENCES]
@image1: Ghost design only; never copy its static frontal couch portrait.
@image2: Teal safehouse, neon sign, worn couch, table, pipes and ceiling; never show the room empty.
@image3: Alien hunter design only; never copy her frontal low-angle portrait.
@image4: Boy design only; never copy his top-down pose.
```

The specificity is what makes it work. Name the pose. Name the framing. Name the body position. Name the angle relationship to the camera.

### Rule 3: Describe framings that are spatially incompatible with the reference images
The most powerful anti-drift technique is choosing shot compositions that the reference image physically cannot fit into. If the reference shows a character standing frontally in a medium shot, an extreme macro on their hand, an overhead top-down, a 90-degree side profile at ground level, an inverted upside-down close-up, or an over-the-shoulder from behind all make it geometrically impossible for the model to retreat into the reference pose.

**Incompatible framing examples:**
- Extreme macro close-up on a specific body part (hands, eyes, wound, weapon edge)
- Overhead top-down looking straight down
- 90-degree horizontal side profile at ground level
- Over-the-shoulder from directly behind
- Inverted / upside-down close-up
- First-person POV from another character's eyes
- Extreme low-angle worm's-eye looking up past feet
- Close-up on a specific detail (a saliva droplet, a coated hand, a chip falling through dust)

Rotate through these framings across the shots of a clip. No repeated framing twice within the same clip. Varied angles create kinetic rhythm and prevent any single frame from slipping into reference pose.

### Rule 4: Use `Motion anchor:` inside the character block
When a character's movement in this specific clip is restricted or shaped differently than their general behavior, put the rule inside the character block as a `Motion anchor:` field. Example:

```text
CALEN:
Base: One hooded humanoid matching @image3.
Features: Pale hood, burnt-orange outfit, black chest armor, dark gloves and heavy boots; blond hair covered.
Motion anchor: Leans toward the orb without stepping, casually raises a loose fist, then lowers it and settles back when the orb recoils. Never strikes or touches it.
```

The model parses character movement rules alongside the character description, not as a separate constraint layer. Much more effective than putting the same restriction in the `Avoid:` list at the bottom.

### Rule 5: Carry visible physical damage forward between clips
For multi-clip sequences where a character sustains damage in a previous clip, describe the damage explicitly in this clip's character block via the `Features:` or `State in this scene:` fields. Example from Malfoid Prompt 2:

```text
MALE 1:
State in this scene: Bruised and exhausted, cheek cut and blood at the mouth corner. On the ground, partly supported on his left arm; brown wooden wand in his right hand.
Continuity: The mouth-corner blood is visibly wiped in Shot 16 and must not return afterward.
```

Carrying damage forward does two things:
1. Prevents narrative reset between clips (no model memory across generations, so you must re-establish).
2. Gives the model a sharper, more specific character design to lock onto — a damaged character is more unique than a clean one, which reduces drift back toward the reference image.

This rule is especially important for sequences longer than three clips. By clip five, your characters should look visibly battered if the story has been escalating.

### Rule 6: Reference tag formatting
- No space between @ and the image number: `@image1` not `@ image1`.
- Use `@image1`, `@image2`, `@video1` as the standard labels in the order received.
- When citing a video reference for direct continuation, the prompt can open with a `[PROMPT START]` field containing `Continue from @video1.` as the first field before `[TITLE]`.

### Rule 7: Repeat key reference rules in `Critical constraint:`
Even with `[REFERENCES]` at the top, restating the most important anti-drift rules in `Critical constraint:` at the bottom creates redundant enforcement. The model reads the rule at parse-time (top) and again at generation-time (bottom). Redundancy is not noise here — it is reinforcement.

---

## 8. Prompt Density Awareness

The official Seedance guide recommends 60–100 words for flat-text prompts. Our bracketed structure is intentionally denser — it gives director-level control. But density has diminishing returns and can introduce conflicting instructions.

### Guidelines:
- **`Camera:` field:** Keep under 20 words. One primary instruction, optionally one secondary.
- **`Action:` field:** Can be longer (30–80 words per shot) because choreographic specificity is our competitive advantage. But every sentence must describe a visible movement.
- **`[STYLE]` field:** 15–30 words. Tight. Specific references, not stacked adjectives.
- **`[VISUAL FEEL]` field:** 15–25 words. Rhythm and texture, not specs.
- **`Lighting:` per shot:** 5–15 words. Brief and specific.
- **`[REFERENCES]` field:** Can be longer (30–80 words) — specificity is the entire point.
- **Overall prompt:** Target under 5,000 characters unless otherwise specified.

### The Redundancy Test
Before finalizing, ask: "Does this sentence describe something the model can render in a video frame?" If not, cut it. The model ignores narrative context, emotional subtext, and abstract concepts — those are for the human reading the prompt, not for the model executing it.

**Exception:** `Subtext:` and `[REFERENCES]` are allowed to contain non-renderable information because they serve as directorial guidance for the model's interpretation, not render targets.

---

## 9. Example Prompts


### Example A — E01: Ensemble Dialogue and Mechanical Performance (The Reluctant Accomplice)

Source: The Acolyte, `documents/scripts/base-heist-clip-01-v22.prompt.md`. Full prompt preserved verbatim.

```text
[TITLE]
The Reluctant Accomplice

[REFERENCES]
@image1: Otto's character design. Do not reproduce his three standing turnaround views or two bordered hooded-face panels.
@image2: Orb drone design. Do not reproduce the labeled side/front/back panels, underside view, probe and eye close-ups, or lens-mood strip as a scene layout.
@image3: Calen's character design. Do not reproduce his frontal diagonal sword display, side-view lowered sword, or stacked portraits including the hood-down blond portrait. His hood stays up.
@image4: Local facade and approach architecture from the wide door view.
@image5: Actual segmented door and yellow-lit left-edge recess from the closer view. Architecture follows these images; camera placement follows the shots below.

[STYLE]
Japanese sci-fi anime matching the references: bold ink, sharp cel shadows, matte cloth and weathered machinery. Assertive perspective drawing and expressive full-body acting; consistent adult proportions.

[VISUAL FEEL]
Quiet infiltration, sinister teasing and nervous mechanical reactions. Enlarged foreground gestures, receding architectural diagonals and subtle action-responsive handheld motion create depth.

[DURATION]
15 seconds.

[CHARACTERS]
OTTO:
Base: One hooded humanoid matching @image1.
Features: Worn crimson cloak, lavender bangs, violet eyes, shadow-dark face, black outfit, pale panels and utility belt.
Personality: Economical gestures and steady eye contact.
Emotional state: Patient with the orb, calmly dismissive of Calen's teasing threat.
State in this scene: Hood up; standing close to the wall, to Calen's right and the orb's left.
Motion anchor: Holds his place, opens a gloved hand toward the orb and nods toward the socket.

CALEN:
Base: One hooded humanoid matching @image3.
Features: Pale hood, burnt-orange outfit, black chest armor, dark gloves and heavy boots; blond hair covered.
Personality: Cocked shoulders, loose elbows and a crooked grin make his threatening jokes look effortless.
Emotional state: Sinisterly amused; enjoys watching the orb wonder whether he means it.
State in this scene: Hood up, shadow-dark face; beside Otto on his left.
Motion anchor: Leans toward the orb without stepping, casually raises a loose fist, then lowers it and settles back when the orb recoils. Never strikes or touches it.

DRONE:
Base: One hovering utility orb matching @image2.
Features: Chipped cream shell, dark gray underside, dusty pink plates, circular lens, thin top antenna and folding articulated probe.
Physics: Lens green while cooperative, red when alarmed. Hovering body dips and rises; probe joints unfold mechanically without changing shell geometry.
Emotional state: Startled by Calen, then reluctantly reassured by Otto.
State in this scene: Already hovering to Otto's right, between him and the socket; probe folded, lens green.
Motion anchor: Starts toward the socket, stops and turns toward Calen at the threat, then directs its lens toward Otto. After reassurance, acknowledges him, turns back and connects.

[SETTING]
BASE SIDE:
Base: Facade and approach matching @image4.
Features: Marked metal apron; floor seams converge toward the monumental entrance.
ACTUAL DOOR:
Base: Segmented blue-gray metal door matching @image5.
Features: Closed door, yellow wall light and left-edge recess. Calen stands left, Otto beside him closer to the wall, orb farther right before the adjacent socket. Entrance centre clear.

[SHOT SEQUENCE]
00–02 — SMALL FIGURES:
Camera: Static deck-level wide from the oblique approach, looking upward toward the entrance.
Action: Calen @image3 stands left in his orange outfit and pale hood; Otto @image1 stands beside him in crimson. Orb @image2 hovers to Otto's right between him and the socket. Otto faces the orb, which faces left toward him. Foreground deck seams converge beneath the small figures; the door rises above them.
Lighting: Cool blue ambient, distant red accents and yellow door markers.
SFX: Low ventilation rumble.

02–06 — A LITTLE ENCOURAGEMENT:
Camera: Overhead medium group shot from above the approach; subtle handheld reframing follows Calen @image3's gesture.
Action: Calen @image3 fills left foreground, Otto @image1 stands close beside him at centre, and orb @image2 hovers right near the socket. Upper bodies, orb and socket fill the overhead frame. Orb @image2 turns right and starts toward the socket. Calen cocks his shoulders, leans into the group and raises a loose fist toward the lens as he jokes. His glove appears larger than his torso through foreshortening; his shoulders and lean carry the threat beneath his hood. Orb @image2 brakes, bobs upward and turns its red lens left toward Calen. Calen lowers his fist and settles back, watching the recoil without laughing.
Dialogue: Calen @image3; "開けるのか？少し壊してやろうか。"
Lighting: Yellow practical light catches the glove, pale hood and crimson cloak.
SFX: Startled electronic chirp immediately after Calen's complete line.

06–10 — OTTO INTERVENES:
Camera: Low oblique close-up below orb height from the approach side; subtle handheld reframing follows Otto @image1's hand.
Action: Otto @image1 occupies left and centre, orb @image2 edges the right foreground. The orb turns its lens from Calen toward Otto. Otto opens his glove toward it in the lower foreground, palm below its body, and nods right toward the socket. The nearby glove appears larger than his face behind it; his violet eyes remain visible above the hand. Calen @image3 stays offscreen left. 
Dialogue: Otto @image1; "大丈夫。手は出させない。今、開けてくれ。"
Lighting: Cool edge on crimson hood; amber catches glove and orb shell.

10–15 — RELUCTANT COOPERATION:
Camera: Low diagonal close-up along the wall below socket height; restrained handheld following tracks orb @image2's approach.
Action: After Otto's complete line, orb @image2 fills near-left foreground, facing Otto offscreen left; the socket sits farther away at upper-right. The orb dips once, its lens turning green, and gives a subdued response. It rotates right, glides toward the socket and unfolds its manipulator. The arm recedes diagonally from the large foreground shell toward the smaller socket, reinforced by converging wall seams. Its probe inserts and turns; small hover corrections keep it connected while processing. Otto @image1 and Calen @image3 remain offscreen left. Door stays closed.
Lighting: Amber practical light across chipped shell and recessed socket metal.
SFX: Reluctant digital warble, servo clicks, connector click and quiet processing pulses.

[PRODUCTION NOTES]
Audio design: Japanese human dialogue; orb sounds entirely non-vocal. Calen uses a teasing lilt with a quietly threatening warmth, no reassuring laugh. Otto speaks calmly and directly. Continuous machinery ambience; no music, narration or subtitles.
Lighting: Cool ambient with consistent yellow door practicals; faces and colored clothing remain readable.
Subtext: Calen knows he is joking; Otto knows it too. The orb is not convinced.
Critical constraint: Start at 00.0 with exactly one Otto @image1, one orb @image2 and one Calen @image3. Preserve Calen left, Otto centre, orb and socket right; all cameras remain on the approach side without reversing the layout. The threat is overhead medium, not wide; preserve left-to-right positions. Foreshortening comes from foreground hands and receding depth, not enlarged anatomy. Opening camera static; later handheld motion responds to action, no decorative zooms or drifting. Both hoods stay up; clothing retains reference colors. Show threat, orb recoil, Otto reassurance, orb acknowledgment and approach before connection. Exclude Otto's turnaround and face panels, the orb's labeled diagram and mood strip, and Calen's sword displays and hood-down portrait. Cut outside complete spoken lines.
Avoid: Uncontrolled camera jitter, bent limbs, temporal flicker, identity drift, duplicate characters, inconsistent features, frozen reference poses and photorealistic live-action rendering.
```

### Example B — E02: Video Continuation and Restrained Acting (Malfoid Takes Control)

Source: Malfoid Prompt 2, `02_reversal_malfoid_takes_control_seedance_v4_continuation_v5.md`. Full fenced prompt preserved verbatim; upload instructions and revision notes are not part of the prompt.

```text
[PROMPT START]
Continue from @video1.

[TITLE]
Reversal / Malfoid Takes Control

[REFERENCES]
@video1: Video continuation reference for character state, environment, spatial continuity, visual style and established voices.
@image1: Male 1.
@image2: Male 2.
@image3: Female 1.
@image4: Malfoid.
@image5: Evil Lord.
@image6: Wizards — six other masked followers; Male 3 is a separate character.
@image7: Courtyard ground-level.
@image8: Courtyard overhead.
@image9: Male 3 — Malfoid’s father; hood-on appearance only.

Character references define identity, clothing, colors, and equipment, not staging. Do not reproduce Male 1's repeated turnaround figures, the Wizards' side-by-side costume lineup, or the upright full-body display poses and pale backgrounds of the other references. Environment references define the ruined courtyard's architecture and materials; the shot sequence defines camera placement and action. For @image9, use only the right-hand hood-on, silver-masked appearance. Do not reproduce the paired full-body sheet, the unmasked face or the hood-off appearance.

[STYLE]
Retro anime, bold linework, Shirow meets Frieren. Mature proportions, detailed hand-drawn environments, restrained facial acting, graphic silhouettes, selective perspective exaggeration. Strong impact frames only for the blitz and curse.

[VISUAL FEEL]
A sharp rupture in held tension, followed by increasingly intimate stillness. Heavy cloth, green afterimage, drifting dust, dark painted backgrounds.

[DURATION]
30.0 seconds.

[CHARACTERS]
MALE 1:
Base: Young man matching @image1.
Features: Tousled black hair, green eyes, dark rounded-rectangular glasses. Dirt-marked black robe with burgundy lining, off-white shirt, loosened burgundy tie, charcoal sweater and trousers, brown lace-up shoes.
State in this scene: Bruised and exhausted, cheek cut and blood at the mouth corner. On the ground, partly supported on his left arm; brown wooden wand in his right hand.
Motion anchor: Never stands. His wand rises only slightly when Malfoid approaches. He stays physically guarded, then freezes at her closeness.
Voice: Young male, clear and natural, exhaustion slightly roughening a grounded mid-range tone; emotionally direct, restrained intensity.

MALFOID:
Base: Young woman matching @image4.
Features: Long straight platinum-white hair, pale gray-blue eyes. Black forest-green-lined robe, ivory shirt, green-and-silver striped tie, charcoal V-neck sweater, pleated skirt, dark tights and black loafers.
State in this scene: Initially among the surrounding followers, Male 3 directly behind her with one hand on each shoulder; composed, uninjured, brown wand in her right hand.
Physics / personality / detail: Explosive entry followed by measured steps, precise hands and an unreadable face.
Motion anchor: Her wand remains in her right hand. She uses her free left hand for Male 1's chin and mouth. No kiss.
Voice: Young female, cool and composed, smooth and slightly low-pitched; precise articulation, understated confidence, dry lightly teasing edge rather than softness.

MALE 3 — MALFOID’S FATHER:
Base: Tall, lean male matching the hood-on appearance in @image9.
Features: Raised black hood; elongated full-face silver mask with narrow black eye openings, central nose ridge and symmetrical engraved ornament. Pale silver-blond hair falls beside the mask. Long black robe with broad sleeves, dark diamond-patterned front trim, small silver chest fittings and a weathered ragged hem; dark high-collared shirt, fitted black waistcoat, black trousers and tall black boots. Bare pale hands; no gloves.
State in this scene: Within the surrounding ring at the opening, directly behind Malfoid with one hand on each of her shoulders. When the battlefield is revealed in Shot 12, he is down and motionless among the six other masked Wizards.
Motion anchor: Does not accompany Malfoid’s blitz. Shoulder contact does not persist after she moves away. His takedown is not shown; hood and full-face silver mask remain on.

EVIL LORD:
Base: Slender bald male matching @image5.
Features: Pale gray-green skin, hollow angular face, slit-nostril nose, narrow red eyes, bony fingers. Matte dark charcoal-olive robe, dark boots, pale tan wand in his right hand.
State in this scene: Standing over grounded Male 1 with wand raised toward him.
Voice: Low male, smooth and controlled, aristocratic and precise, cold resonant presence; forceful attack followed by a quiet break of disbelief.

MALE 2:
Base: Young man matching @image2.
Features: Ginger hair, pale freckled face, burgundy-lined dark robe, pale shirt, dark-red tie, charcoal sweater, worn trousers and black lace-up shoes.
Motion anchor: Remains down nearby throughout; no intervention.

FEMALE 1:
Base: Young woman matching @image3.
Features: Voluminous chestnut hair, brown eyes, scratched cheeks, burgundy-lined black robe, white shirt, burgundy tie, gray-purple sweater vest, dark pleated skirt, tights and black lace-up shoes.
Motion anchor: Remains down nearby throughout; no intervention.

WIZARDS:
Base: Exactly six other masked followers using six distinct costume variants from @image6; Male 3 is additional and uses his own reference.
Features: Varied dark hooded robes in charcoal, blue-gray, green, olive, plum and teal; decorated ivory-gray masks, dark gloves, boots, belts and selected metal bracers.
State in this scene: Standing in an enclosing ring at the opening. All are down and motionless when the battlefield is revealed in Shot 12.
Motion anchor: Their takedown is not shown. No added battle or explanatory attack.

[SETTING]
RUINED CASTLE COURTYARD:
Base: Architecture and paving grounded in @image7 and @image8.
Features: Broken Gothic arcades, jagged roofless walls, cracked blue-gray slabs, central paving damage, perimeter rubble and weak side fires. Layered smoke obscures parts of the ring.
Blocking: Male 1 is grounded near the centre. The Evil Lord faces him at close range. Male 2 and Female 1 lie nearby. Malfoid begins within the followers, Male 3 behind her with one hand on each shoulder. She appears directly behind the Evil Lord, then approaches Male 1 across his fallen body.
Lighting: Cold blue moonlight, weak orange fires, hard shadows and silver rims; the curse briefly replaces these with green.

[SHOT SEQUENCE]
00.0–07.5 — SHOT 10:
Camera: Hard cut at 00.0; static tight frontal medium close-up on the Evil Lord from Male 1's eyeline.
Action: The Evil Lord begins the killing curse. On “アバダ――”, Malfoid blitzes into frame directly behind him in a teleport-like anime burst, already holding her right-hand wand to his temple. Her face is readable beyond his shoulder. He freezes, recognizes her, and quietly speaks. She delivers her incantation without hesitation and fires immediately at its completion.
Lighting: Cold moonlight on the Evil Lord; hard silver rim on Malfoid's arrival, then the frame floods green.
Dialogue: EVIL LORD; 「アバダ――」
Delivery: Suddenly forceful and lethal, all previous restraint snapping into the attack; interrupted before completing the curse.
Dialogue: EVIL LORD; 「……ドラコ。」
Delivery: Very quiet, breath caught slightly, disbelief entering his voice.
Dialogue: MALFOID; 「アバダ・ケダブラ。」
Delivery: Calm and absolute, level volume, no hesitation or anger.
VFX: High-speed smear/blitz entry, brief held reveal, then point-blank green impact flash and shadow inversion.
SFX: Sharp blitz impact, wand tap against skin, point-blank curse discharge.

07.5–09.5 — SHOT 11:
Duration: 2.0s
Camera: Ground-level medium shot from Male 1’s side; static.
Action: The Evil Lord’s wand slips from his hand and he collapses heavily. Malfoid remains standing behind him.
Dialogue: —
SFX: CLACK. THUD.
Lighting: Green afterglow fades back into cold moonlight.
VFX: Small impact shake and dust kick.

09.5–12.5 — SHOT 12:
Camera: High-angle wide shot, slowly pulling back over the courtyard.
Action: The Evil Lord is down beside Male 1. Male 3 and the other six masked Wizards who had surrounded them are now down across the courtyard while Malfoid remains the only standing figure.
Dialogue: —
SFX: Wind returns into the silence.
Lighting: Moonlight opens the entire battlefield while scattered fires continue to flicker.
VFX: Smoke clears in layers, gradually exposing the changed battlefield.

12.5–14.0 — SHOT 13:
Camera: Static tight three-quarter frontal close-up on Male 1.
Action: Male 1 looks screen-left, then slowly scans toward screen-right. Shock shifts into deeper confusion.
Lighting: Cold moonlight catches both eyes behind his glasses.
VFX: Minimal held animation.
SFX: His breathing.

14.0–16.5 — SHOT 14:
Camera: Static low-angle Male 1 POV, medium-full on Malfoid; fallen Evil Lord across the lower foreground.
Action: Malfoid lowers her wand, steps over the Evil Lord and walks directly toward camera.
Lighting: She crosses alternating moonlight and orange fire spill.
VFX: Smoke parallax separates her from the background.
SFX: Slow measured footsteps.

16.5–19.0 — SHOT 15:
Camera: Static over-the-shoulder medium shot behind Male 1, his wand enlarged in the near foreground.
Action: Male 1 raises his right-hand wand slightly. Malfoid notices without slowing, stops directly in front of him and crouches.
Lighting: Cool rim light outlines her; Male 1 remains darker in the foreground.
VFX: Background detail softens as she comes closer.
SFX: Footsteps stop; fabric folds as she crouches.

19.0–22.0 — SHOT 16:
Camera: Static tight side-profile two-shot at their eye level; Male 1 frame-left, Malfoid frame-right.
Action: Keeping her wand lowered in her right hand, Malfoid places her left hand beneath Male 1's chin and turns his face slightly toward her. She studies his cheek cut, then wipes the blood from the corner of his mouth with her left thumb.
Lighting: Moonlight falls across his face as she turns it.
VFX: Background simplifies into dark painted shapes.
SFX: Male 1 takes a short breath.

22.0–24.5 — SHOT 17:
Camera: Over-the-shoulder close-up behind Malfoid on Male 1's face; slow push-in.
Action: Male 1 watches her closely, unable to read her. His mouth opens as he finally tries to speak.
Lighting: A narrow moonlit reflection crosses his glasses without hiding his eyes.
Dialogue: MALE 1; 「どうして――」
Delivery: Quiet and bewildered, weakened by exhaustion; the unfinished question slips out before he composes himself.
VFX: Background falls progressively darker.
SFX: His voice breaks the silence.

24.5–30.0 — SHOT 18:
Camera: Tight side-profile two-shot; slow push-in.
Action: Malfoid leans toward Male 1 until their faces nearly touch, then deliberately moves past his mouth toward his ear. Male 1 freezes. She speaks close to his ear; their lips never touch.
Lighting: A thin silver rim traces both profiles.
Dialogue: MALFOID; 「相変わらず質問が多いのね、ポッター。」
Delivery: Low and close, dry and lightly amused; confident teasing without tenderness.
VFX: Background reduces to near-black, with restrained eye highlights.
SFX: Her voice sits almost alone in the mix.

[PRODUCTION NOTES]
Audio design: NO MUSIC, no score, no musical stings. Exact Japanese dialogue only. Physical blitz, wand contact, discharge, clack, thud, footsteps, fabric, breathing, wind and distant fire. Reduce ambience around the final exchange without introducing a musical tone.
Continuity: Preserve Male 1's bruises and cheek cut. The mouth-corner blood is visibly wiped in Shot 16 and must not return afterward. Both protagonists retain their wands in their right hands. Preserve Male 1 frame-left and Malfoid frame-right across the intimate profile shots.
Critical constraint: Begin Shot 10 immediately after the final shot of @video1, with no replay, overlap or added opening shot. Exactly seven masked Wizards surround the central group: Male 3 plus six others, not seven others. In Shot 12 all seven are down and Malfoid is the only standing figure. Male 3 retains his raised hood and full-face silver mask. Shot 11 is exactly the specified two-second ground-level collapse. No alternative fall, disintegration or additional action. The Evil Lord never completes his curse. The followers' defeat is revealed, not explained. No kiss, tenderness, added combat or extra dialogue. Reference display poses never replace staging.
Animation style: Stable camera during the blitz. Impact frames are confined to the entry and discharge; subsequent performance uses restrained cel-anime acting.
Avoid: Jitter, bent or distorted limbs, malformed hands, temporal flicker, identity drift, chaotic composition, inconsistent features, duplicated wands, hand swapping, reference-image display poses and subtitles.
```

### Example C — E03: Multi-Opponent Action and Impact Pacing (Break Point)

Source: Dark Eldric, `_workspace/flova-break-point-23s-exact/prompt.txt`. Full prompt preserved verbatim.

```text
[TITLE]
Break Point

[REFERENCES]
@image1/@image2 anchor Eldric; @image3 the city; @image4 samurai; @image5 robots; @image6 soldiers. Use design only. Exclude @image1’s forward palm, @image2’s sheet, @image3’s street-canyon view, @image4’s posed trio, @image5’s low-angle pair, and @image6’s frontal lineup.

[STYLE]
Premium dark supernatural action anime, sharp cel linework, painted city, polished 4K finish.

[VISUAL FEEL]
Nonstop combat, hard inserts, extreme foreshortening, impact holds, disciplined smears, debris parallax, stable anatomy.

[DURATION]
23 seconds

[CHARACTERS]
DARK ELDRIC:
Base: Tall lean skeletal sovereign matching @image1 and @image2.
Features: Rose-bone skull, cyan eyes and cracks; gunmetal skeletal armor, cyan chest core, black-violet magenta-lined cape, claw hands, asymmetric red/black legs, heavy boots, blue-violet aura.
Physics / personality / detail: Barehanded redirects, open-hand cuts, elbows, aerial pivots; cape drags heavily.
Motion anchor: Never use the reaching pose or sheet stance. Remain in continuous close combat until the final strike.

SAMURAI:
Base: Three @image4 samurai: red horned, black with red scarf, and white high-collared armor; blue energy katanas.

ROBOTS:
Base: @image5 robots: worn gray plates, black mechanics, twin cyan optics, red center sensors, piston limbs; one breacher has a rocket forearm.

SOLDIERS:
Base: @image6 soldiers: worn gray armor, cyan visors, orange details, ribbed hoses, heavy rifles, shields, restraint cables.

[SETTING]
ELEVATED CITY INTERSECTION:
Base: @image3’s near-future towers, aerial rails, signs, barricades, and a concrete commercial building.
Features: Reflective pavement and smoke; keep the building on Eldric’s screen-right.

[SHOT SEQUENCE]
00–03 — MID-IMPACT:
Camera: Controlled low-wide lateral track parallel to the melee.
Action: Eldric ducks a black samurai’s blade, elbows a robot sensor, catches a soldier’s shield, and pivots it into the crimson samurai’s descending strike. Blade, shield, and piston fist collide behind his cape.
Lighting: Cyan signs and white muzzle flashes.

03–05 — LAUNCH INSERT:
Camera: Locked extreme close-up on Eldric’s boot and fractured pavement.
Action: A katana spears down beside his heel. He stamps it flat, crouches, and launches; pavement caves as the samurai is dragged off balance.
Lighting: Cyan reflection cut by violet aura.

05–07 — AIRBORNE INTERLOCK:
Camera: Smooth inverted orbit beneath the airborne fighters.
Action: Eldric rises between two jumping samurai and a robot. He folds around one blade; the second blade blocks the robot’s fist above him while a soldier’s shield catches his descending heel. Every attack path intersects clearly.
Lighting: Eclipse backlight, magenta tower rims.

07–09 — ONE CUT:
Camera: Locked 90-degree side profile at rooftop height.
Action: A robot lunges. Eldric lands on its forearm, slides to its chest, and sweeps one open hand through the torso in one cyan-black arc. The machine separates into upper and lower halves as he passes.
Lighting: Cyan edge flare against black sky.

09–11 — IMPACT INSERTS:
Camera: Locked extreme-close inserts, hard-cutting on each contact.
Action: Fingers catch a katana’s flat; heel crushes a rifle receiver; skull slips past a piston fist; palm cracks an ivory mask. Each contact freezes for one readable impact frame.
Lighting: White flashes over cyan shadows.

11–14 — CLOSING THE SKY:
Camera: Controlled overhead spiral descending toward Eldric.
Action: Eldric vaults again. Three samurai jump around him, crossing blades above and below; two robots block his exits while soldiers fire through the gaps. He redirects blade into fist, steps across a robot shoulder, and tears two cables, but a third hooks his cape.
Lighting: Searchlights rotate through smoke.

14–16 — THE OPENING:
Camera: Rapid first-person rush along the breacher robot’s rocket forearm.
Action: The cable arrests Eldric for half a beat. A samurai braces against his back and shields seal below. The breacher’s fist accelerates through the only open lane toward his ribs.
Lighting: Orange exhaust against cyan armor rims.

16–18 — THROUGH THE WALL:
Camera: Locked ground-level profile facing the screen-right building.
Action: One punch folds Eldric sideways. A pressure ring leads him across the avenue and through the concrete façade, then three interior walls collapse behind him.
Lighting: White impact core, then interior darkness.
VFX: Deep wall tunnel; layered debris follows his path.
18–23 — ANGER:
Camera: Inverted crater close-up, slowly rotating upright.
Action: Eldric remains completely still under rubble for one full beat. Then his claw slowly presses down and he rises with cold, deliberate weight as frame levels. Once upright, both sockets build to a contained menacing blue-white glow; skull cracks answer dimly. Hold his evil stare to cut.
Lighting: Dim neon; contained eye glow only.

[PRODUCTION NOTES]
Audio design: No music. Continuous impacts; silence only on impact holds and the rubble beat.
Critical constraint: Start mid-fight. Keep the building screen-right. Eldric bisects one robot with exactly one open-hand slash. One breacher punch sends him through the building; he lies still for one beat, rises, and his eyes glow last;  No flare, burst, shockwave, or expanding aura.  Preserve reference identity without reference poses.
Avoid: Jitter, distorted limbs, flicker, identity drift, crowd blending, duplicates, merged weapons, unreadable impacts, gore, extra slashes.
Animation style: High-budget cel action, selective impact holds, disciplined smears, stable geometry.
```

---

## 10. Timestamp Scaling and Pacing

### Duration-to-Shot Scaling

| Duration | Recommended Shots | Avg Seconds Per Shot |
|----------|-------------------|----------------------|
| 5s       | 2–3               | 1.5–2.5s            |
| 10s      | 3–4               | 2.5–3.5s            |
| 15s      | 4–7               | 2–4s (staggered)    |
| 20s      | 5–7               | 2.5–4s              |
| 30s      | 7–10              | 3–4.5s              |

### Stagger Timecodes — Do Not Default to Even Intervals

Do not default to evenly split 3-second intervals. Staggering shot durations based on scene rhythm is required. Even-interval pacing flattens scenes and removes kinetic shape.

Use judgment per beat:
- **Short beats (1–2s):** Impacts, eye-locks, slow-mo flashes, hard cuts, realization moments, ceiling ruptures.
- **Medium beats (2.5–3.5s):** Standard action, dialogue, reactions.
- **Longer beats (4–5s):** Sustained action, ritual casts, transformation sequences, magic, dance.

**Good 15-second staggered pacing examples:**
- 0–2s / 2–4s / 4–7s / 7–8s / 8–11s / 11–13s / 13–15s (seven-shot variable rhythm)
- 0–3s / 3–6s / 6–7s / 7–10s / 10–13s / 13–15s (six-shot rhythm with a one-second impact flash)
- 0–2s / 2–5s / 5–6s / 6–9s / 9–12s / 12–15s (six-shot rhythm with impact flash)

### Pacing Principles
- Opening shots can run longer (establishing context).
- Transformation or impact moments should be compressed (1–2s) for energy.
- Final shots benefit from a held beat — let the image breathe before the clip ends.
- Dialogue-driven scenes may use longer shots; action scenes use shorter cuts.
- Slow-motion beats should be brief (1 second) unless the slow-motion IS the scene — extended slow-motion beats deflate clip energy.

---

## 11. Audio Design Patterns

Audio is always specified in production notes, never left to default. Use specific sensory audio keywords — "muffled," "echoing," "crunchy," "reverb," "sharp" — rather than generic descriptors. The model matches audio vibration to these words.

| Genre | Audio Approach |
|-------|---------------|
| Macro / ASMR | Wet textures, contact sounds, amplified material interaction |
| Horror / Cyberpunk | Silence as weapon, sub-bass detonations, metallic impacts |
| Comedy / Dramedy | Ambient room tone, sharp punctuation sounds (pen click, door shut), dialogue pacing |
| Anime / Healing | Soft ambient, wind, water, kitchen sounds, gentle musical stings |
| Action / Fantasy | Layered SFX (impact + reverb + environmental), orchestral swells, bass drops |
| Stop-Motion | Diegetic only, tactile material sounds, no score unless specified |
| Anime Comedy-Thriller | Separate voice identity from delivery; tactile diegetic sounds, restrained reaction beats, and silence under dialogue where specified |

---

## 12. Common Critical Constraints

These are recurring rules that may apply depending on the scene type. Include the relevant constraint in `[PRODUCTION NOTES]` → `Critical constraint:` when applicable:

- **Surface animation:** "All animation stays flat and embedded on the physical surface — painted-on aesthetic, never 3D pop-out."
- **Handheld realism:** "Camera maintains handheld micro-shake throughout. Never stabilizes to tripod smoothness."
- **Stop-motion cadence:** "Stop-motion with intentional frame-to-frame jitter. No smooth interpolation. Characters move in holds and pops."
- **Material integrity:** "Physical objects maintain real-world reflections, weight, and surface properties even when stylized animation occurs on or within them."
- **No breaking the plane:** "Animated elements within a contained surface (teeth, screen, painting) never extend beyond the physical boundary of that surface."
- **Spatial layout lock (multi-character):** "[Character A] on the LEFT, [Character B] on the RIGHT, facing each other across the [aisle/space] throughout. Neither character crosses behind the other at any point."
- **Reference pose exclusion:** "Reference images are STRICTLY character design anchors. [Character] NEVER shown in the frontal display pose from @image1. [Character] NEVER shown in the forward-charge pose from @image2."

---

## 13. Image-to-Video vs. Text-to-Video Prompting

When generating from a reference image (image-to-video mode), the prompt structure shifts:

| Element | Text-to-Video | Image-to-Video |
|---------|---------------|----------------|
| Subject description | Must be detailed | Already in the image — can be shortened |
| Motion description | Full choreography | Focus on dynamic changes and movement |
| Composition | Describe fully | Add "preserve composition and colors" |
| Camera movement | Flexible | Must align with the image's existing composition |

For image-to-video, front-load with "Animate the provided image" or "Starting from the reference composition" and focus the prompt on what *changes* — not what the image already shows.

---

## 14. Video Reference for Continuation

When a previous clip serves as direct continuation reference (labeled `@video1`), the prompt can open with a `[PROMPT START]` field BEFORE the `[TITLE]` field:

```text
[PROMPT START]
Continue from @video1.

[TITLE]
[Scene Title]

[REFERENCES]
[...]
```

This explicit continuation cue helps the model preserve character state, environment, and spatial positioning from the previous clip. Still re-describe everything fully within the character blocks — the model has no memory across generations, so the `[PROMPT START]` cue aids continuity but does not replace full re-establishment.

---

## 15. Multi-Clip Sequence Discipline

When writing a sequence of clips that tell a continuous story:

1. **Every clip must fully re-establish the character, environment, wardrobe, materials, and scene state as if it is the only prompt the model will ever see.** No "same character from Part 1," no "continuation narrative," no "escalated stakes from before."

2. **Carry visible physical damage forward.** Wounds, missing body parts, broken features from previous rounds become part of the character's design in this clip. See Section 7, Rule 5.

3. **Lock spatial relationships across clips.** If two characters face each other across an aisle in clip 3, they face each other across that same aisle in clip 4. State the spatial layout explicitly in `Critical constraint:`.

4. **Let each clip end on a hook, not a resolution.** Pre-strike tension, mid-motion cuts, held frames on a reaction — these are stronger clip closers than resolved action. Resolution happens inside the next clip, establishing continuity.

5. **Environmental transformations must be re-described in full.** If clip 3 summoned a new environment, clip 4's character block must describe that environment from scratch as the established setting — not reference that it was summoned previously.
