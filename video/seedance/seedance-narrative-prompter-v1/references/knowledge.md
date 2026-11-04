# Seedance Narrative Prompter — Master Knowledge Base

This document is the reference library for generating Seedance Narrative prompts. It contains the template anatomy, field guidance, camera rules, action-writing rules, lighting guidance, stability constraints, genre adaptation patterns, reference discipline, prompt density guidance, examples, pacing, audio design patterns, image-to-video behavior, video continuation handling, and multi-clip continuity rules.

---

## 1. Template Anatomy

The Narrative template has three layers. Each layer is represented in every prompt where the relevant material exists.

### Layer 1: Scene Identity

Establishes the global visual contract before the timed sequence begins.

- `[REFERENCES]` — The first field. Lists every supplied image and video reference separately and defines exactly what each reference controls.
- `[AUDIO]` — Included directly below `[REFERENCES]` when supplied audio or video controls dialogue, vocal performance, timing, music, or specific sound behavior.
- `[VISUAL STYLE]` — Defines the genre, aesthetic reference, visual philosophy, footage texture, motion character, atmosphere, depth treatment, palette, and overall lighting feel. Resolution targets such as 4K or 2K can appear here as style anchors. Rendering intentions such as subsurface scattering, volumetric fog, film grain, brushstroke boil, or bloom are appropriate when they describe visible texture rather than camera settings.
- `[DURATION]` — Exact clip length in seconds. Timing is planned from this before the detailed sequence is written.

### Layer 2: Characters and Setting

Every entity that needs visual or behavioral consistency — characters, objects, hands, creatures, props with agency — is defined before the timed sequence.

Character information can be written as compact prose or organized with optional internal labels when they improve clarity and serve a narrative function for the overall sequence.

Compact prose:

```text
NAZZ:
Adult stoic male matching @image1, with short spiky black hair, dark stubble, and a navy-purple jumpsuit. He begins seated below Oz, tired and reluctant to speak, then accepts his hand and rises.
```

Optional labels:

```text
NAZZ:
Base: Adult stoic male matching @image1.
Features: Short spiky black hair, dark stubble, and a navy-purple jumpsuit.
State in this scene: Begins seated below Oz, then accepts his hand and rises.
Emotional state: Tired and reluctant, becoming willing to speak.
```

Available labels include:

- `Base:` — What the character or entity is and which reference image controls identity, when applicable. Use `@image1`, `@image2`, etc. with no space after `@`.
- `Features:` — Physical description specific enough to render: colors by name, materials by texture, wardrobe by item, visible damage, important props.
- `Physics / personality / detail:` — How the character, body, material, clothing, hair, or entity moves, deforms, or emotes. Express personality through physicality when useful.
- `Motion anchor:` — Movement restrictions or specific movement behavior for this clip. Keep these rules beside the character description.
- `Emotional state:` — Tone and demeanor the character carries through the scene when performance needs a clear anchor.
- `State in this scene:` — Starting state for this clip: wounds, missing parts, posture, current activity, hand positions, transformation state, or other continuity information.
- `Power:` / `Power this scene:` — Mechanical behavior of an ability that activates or matters in this clip.

Use `[SETTING]` when an environment needs to remain consistent through the timed sequence. Name each setting so it can be referenced naturally inside the timed narrative. Setting information can be written as compact prose or organized with optional internal labels when they improve clarity and serve a narrative function for the overall sequence.

Compact prose:

```text
THE LAYERED ROCK CHAMBER:
Layered stained rock with fixed blue-violet and magenta illumination.
```

Optional labels:

```text
THE LAYERED ROCK CHAMBER:
Base: Environment matching @image3.
Features: Layered stained rock.
Lighting: Fixed blue-violet and magenta illumination.
```

Available labels include:

- `Base:` — What the environment is and which reference anchors it.
- `Features:` — Architecture, materials, layout, palette, surface treatment, atmosphere, important objects.
- `Physics:` — Environmental behavior when relevant.
- `Lighting:` — Stable lighting state when it carries across several shots or beats.

Define multiple settings separately when the sequence moves between environments.

### Layer 3: Timed Narrative and Final Visual Anchor

Every second of the clip is covered by explicit timestamp ranges.

A timestamp range represents a continuous visual or dramatic beat. It may contain:

- one continuous shot
- several cuts
- camera movement
- character movement
- acting and reaction
- dialogue
- foreground / midground / background staging
- rack focus or another focus change
- lighting changes
- sound events
- VFX progression
- a transition into another setting

Write events in the order the viewer experiences them.

`[FINAL VISUAL STYLE]` defines the desired finished visual output of the full sequence. It can lock style, rendering, depth and focus behavior, lighting consistency, motion behavior, spatial or character-state continuity, transition behavior, and other sequence-wide visual conditions that must remain true in the finished result.

`Avoid:` closes the prompt with stability constraints and scene-specific failure modes.

---

## 2. Timestamp Scaling and Pacing

Timing is established before detailed sequence writing. Every second of the clip must be accounted for, and time ranges are staggered according to scene rhythm.

### Duration-to-Beat Scaling

| Duration | Recommended Major Beats | Typical Seconds Per Beat |
|----------|-------------------------|--------------------------|
| 5s       | 2–3                     | 1.5–2.5s                 |
| 10s      | 3–4                     | 2.5–3.5s                 |
| 15s      | 4–7                     | 2–4s, staggered           |
| 20s      | 5–7                     | 2.5–4s                   |
| 30s      | 7–10                    | 3–4.5s                   |

These are guides rather than quotas. One beat may contain more than one cut.

### Stagger Timecodes

Use judgment according to what is happening:

- **Short beats (1–2s):** Impacts, eye-locks, slow-motion flashes, hard cuts, realization moments, sudden reactions, transition takeovers.
- **Medium beats (2.5–3.5s):** Standard action, dialogue, reactions, movement between positions, establishing a new composition.
- **Longer beats (4–5s or more):** Sustained action, longer dialogue, ritual casts, transformation sequences, magic, dance, acting, tension, atmosphere, or a phase containing several internal cuts.

Useful 15-second rhythms include:

- `0–2 / 2–4 / 4–7 / 7–8 / 8–11 / 11–13 / 13–15`
- `0–3 / 3–6 / 6–7 / 7–10 / 10–13 / 13–15`
- `0–2 / 2–5 / 5–6 / 6–9 / 9–12 / 12–15`

### Pacing Principles

- Opening beats can run longer when context needs to be established.
- Transformation or impact moments can compress to 1–2 seconds for energy.
- Dialogue-driven scenes can use longer ranges when performance needs space.
- Give spoken lines enough real time to be delivered naturally.
- Dialogue may begin in one composition and continue uninterrupted across a cut.
- Slow-motion beats stay brief unless slow motion is the central action.
- Final beats receive enough time for the chosen ending image or reaction to register.

---

## 3. Camera Discipline System

### The One-Primary Rule

Each distinct shot or cut uses one primary camera movement. Optionally add one secondary movement using `then` to sequence them.

**DO:**

```text
A low close shot slowly pushes toward him.
The handheld camera tracks beside her, then gently rises as she stops.
A fixed wide shot holds while the subject crosses the frame.
```

**DON'T:**

```text
The camera tracks, pushes, orbits, tilts and cranes around him while he runs.
```

Competing camera instructions increase jitter and reduce readability.

### Rhythm Over Specs

Seedance responds to rhythm language rather than technical camera parameters.

| Use These | Not These |
|-----------|-----------|
| slow, smooth, gentle, gradual | 24fps, f/2.8, ISO 800 |
| controlled, stable, steady | focal length 85mm |
| dynamic, swift when qualified | shutter speed 1/50 |
| imperceptible, barely moving | rack focus at 0.3m |

Technical specifications can appear in `[VISUAL STYLE]` as aesthetic anchors when they describe the visual result, but they do not drive camera behavior.

### Speed Asymmetry Rule

Fast camera movement, fast subject action, and a complex scene should not peak at the same time.

- Fast action benefits from slow or controlled camera behavior.
- Dynamic camera movement benefits from deliberate, readable subject action.
- Complex scenes with many elements, particles, or crowds benefit from reduced competing motion.

Only one speed axis should dominate at a time.

### Separate Camera from Subject

Keep it clear what the camera does and what the subject does, even when both appear in the same paragraph.

**DO:**

```text
The camera tracks beside him as he backs away, keeping his face centered.
```

The camera tracks. The character backs away.

### Supported Camera Types

| Camera Type | Best For |
|-------------|----------|
| Push-in / dolly in | Close-up emphasis, emotional focus |
| Pull-out / dolly out | Environmental reveal, context |
| Pan / lateral | Tracking, scanning |
| Tracking / follow | Action, walking |
| Orbit / arc | Product showcase, portraits, changing spatial relationship |
| Aerial / drone | Landscapes, scale |
| Handheld | Documentary feel, physical immediacy |
| Fixed / locked-off | Performance, subject action, deliberate stillness |
| Tilt | Reveals, scale emphasis |
| Crane / rise / drop | Dramatic spatial transitions |

### Position / Angle Vocabulary

Use these to establish the camera's starting position before describing movement:

- Extreme macro close-up
- Close-up
- Medium close-up
- Medium shot
- Medium-wide shot
- Wide shot
- Low tabletop angle
- Over-the-shoulder
- High-angle master shot
- Dutch angle
- First-person POV
- Low angle looking up
- Medium two-shot
- Wide establishing shot
- Overhead top-down
- 90-degree side profile at ground level
- Extreme low-angle worm's-eye
- Inverted orientation
- Lateral side-view two-shot

### Lens Effects, Depth, and Focus

Lens and focus behavior is described where it changes the image or redirects attention:

- Focus rack between subjects
- Shallow depth of field with soft bokeh
- Anamorphic streak flares
- Film grain
- Motion blur
- Lens distortion on edges

#### Depth Plane

Depth plane describes where subjects exist spatially:

- foreground
- midground
- background

Use depth to establish relationships, reveal information, create pressure, or redirect attention.

Example:

```text
Oz's rigid hand remains slightly blurred in the foreground while Nazz stays sharp in the background below him.
```

#### Rack Focus

A rack focus redirects attention. State:

1. what begins sharp
2. what begins soft
3. what changes
4. where focus ends

Example:

```text
Oz slowly tightens his fist. Nazz in the background softens while Oz's rigid hand in the foreground resolves into sharp focus.
```

---

## 4. Action Writing Rules

### 4.1 Every important verb describes visible, frame-by-frame movement.

**DO:**

- `Her eyes well up with tears. She pouts her lips excessively. She quickly grabs all three daifukus, hugging them to her chest.`
- `He pinches a single red wire protruding from a port near her jawline. He pulls it. Slowly. Six inches of red cable slides out with a faint mechanical click-click-click.`
- `The chasen tips forward and plunges its bristle head deep into the mound of matcha powder. It swirls slowly — once, twice — coating every bristle tip in vivid green.`

**DON'T:**

- `She gets upset and grabs the food.`
- `He activates her mechanism.`
- `The brush gets matcha on it.`

The difference is specific physical choreography versus narrative summary.

### 4.2 Shot Size, Angle and Cut Writing Rules

Every shot must describe a physically coherent camera view using clear, standard shot-size, angle, orientation, framing, and camera-movement language.

**DO:**

* `Front-facing medium close-up of Nazz, with Oz visible behind him on frame-right. The camera tracks backward as Nazz moves through the space.`
* `Three-quarter angle medium close-up of Nazz with Oz visible just behind him on frame-right. The camera tracks backward as Nazz moves forward.`
* `Close OTS from behind Nazz, framing Oz as he sharpens his sword with a sharpening stone. Subtle handheld drift.`
* `Hard cut to a slightly low-angle reverse OTS behind Nazz with a slow camera drift. Nazz is softly blurred in the foreground while Oz is sharp in the background, standing above him with his head bowed, gaze directed toward the ground, and rigid fist clenched.`
* `Cut to an overhead medium shot of Nazz and Oz across the table.`

**DON'T:**

* `Moving medium close-up from inside the crowd.`
* `Low cut to low canted to medium shot.`
* `Dynamic angle of Nazz and Oz.`
* `Interesting close shot from inside the room.`
* `Medium close-up on Nazz.`

Location or atmosphere does not establish a shot. Phrases such as `inside the crowd`, `in the room`, or `among the dancers` may describe where the camera is positioned, but they do not replace a clear shot size, angle, orientation, subject, or composition.

Do not invent or combine camera terminology that does not describe a clear physical viewpoint. Use the established shot-size, angle, orientation, and camera-movement vocabulary in this knowledge base.

### 4.3 Writing Cuts Inside a Timestamp Range

A timestamp range may contain one shot or multiple cuts.

Do not create a new timestamp merely because the camera cuts. Write cuts chronologically inside the same range when they belong to the same dramatic or visual beat.

**DO:**

```text
00–08 seconds:
Close OTS from behind Nazz, framing Oz as he sharpens his sword with a sharpening stone. Cut to an overhead medium shot of both characters; Oz finishes sharpening the sword and places the stone on the table. Nazz looks at him with a smirk and says, {Are you done or what?}
```

When exact cut timing or timing matters:

```text
00–08 seconds:
Close OTS from behind Nazz, framing Oz as he sharpens his sword with a sharpening stone. At 04 seconds, cut to an overhead medium shot of both characters; Oz finishes sharpening the sword and places the stone on the table.
```

```text
00–06 seconds:
In the Stained Rock Chamber, hold a close angled OTS behind Oz’s rigid hand and hip with subtle handheld motion. Oz’s rigid hand and hip sit slightly blurred in the foreground while Nazz is sharp in the background, crouched below Oz and speaking: {It shocked you awake, but that clarity won’t last. The Thrum will take you again—}

At 3 seconds, Oz slowly tightens his fist. Nazz in the background gradually softens into blur while Oz’s rigid hand in the foreground resolves into sharp focus. Nazz’s hair and clothing sway gently throughout; Oz’s visible tunic edge and loose trousers move with slow, fluid, irregular motion. Magenta edge light from behind Oz defines his foreground hand and hip while cooler blue-violet light separates Nazz in the background, with the magenta edge catching Nazz’s hair and outer contour. (No music throughout.) <Low cavern ambience and soft clothing rustle.>
```

**DON'T:**

```text
04–07 seconds:
Tight hand insert: the braided girlfriend presses a short glass into the Agent’s open palm; his fingers close around it. Cut low and canted to a medium-full shot as the women draw him into their dancing. He joins without spilling while GUY moves beside them. <Glass clink, bangles clicking.>
```

Do not write cuts as loose strings of camera modifiers such as `Cut low and canted to a medium-full shot`. Each cut must describe a clear, physically coherent new camera view.

Do not compress the Narrative into pseudo-fields using unnecessary colons and semicolons. The actions, cuts, dialogue, and sound should read as a coherent visual sequence.

When exact timing does not matter, simply write `Cut to...` or `Hard cut to...` and continue the sequence.

### Dangerous Action Words

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `epic` | no visible instruction | describe the specific visual effect |
| `amazing` / `beautiful` | adjectives without guidance | specific lighting, composition, texture |
| `lots of movement` | over-motion and jitter | one specific described motion |
| `fast` without qualification | chaos without direction | `swift single step` or another exact action |
| `cool` / `dynamic` | vague aesthetic | name the exact visual behavior or reference |

---

## 5. Lighting as a Lever

Lighting is one of the highest-leverage elements in a Seedance prompt.

### Stable Environmental Lighting

When lighting belongs to the setting and remains consistent across several shots or beats, anchor it in `[SETTING]`.

```text
Lighting: Fixed blue-violet shadow with saturated magenta-red illumination from the rear rock formations.
```

### Beat-Specific Lighting

Describe lighting inside the timed sequence when the lighting state changes, becomes part of the action, or drives the transition.

Examples:

```text
Warm golden-hour backlight through the window.
Single red overhead wash, everything else dark.
Soft overcast diffused light, even and flat.
Neon blue rim light against deep shadow.
Strobe pulses, white and violet, through haze.
```

Every distinct shot has a clear lighting state. An unchanged state can be inherited from `[SETTING]`; changes are written where they occur.

### High-Impact Lighting Keywords

| Keyword | Effect |
|---------|--------|
| golden hour | warm golden tones, long shadows |
| rim light | edge highlights separating subject from background |
| natural light | soft, realistic illumination |
| neon | colored glow, cyberpunk / urban |
| backlit | silhouette potential, dramatic depth |
| overcast | even, diffused, no harsh shadows |
| volumetric | visible light rays through fog, haze, or dust |
| practical light | visible source in frame: lamp, candle, screen |

---

## 6. Stability Constraints

Every prompt ends with `Avoid:`.

### Standard Baseline

```text
Avoid: Jitter, bent or distorted limbs.
```

### Add Based on Scene Type

| Condition | Add to Avoid |
|-----------|--------------|
| Clips over 10 seconds | temporal flicker |
| Character-driven scenes | identity drift |
| Complex scenes | chaotic composition |
| Multiple cuts with same character | inconsistent features between shots |
| Slow / contemplative scenes | unnecessary camera movement |
| Scenes using image references | character frozen in reference-image pose |
| Dialogue driven by supplied audio | inaccurate lip-sync |
| Focus choreography | abrupt focus hunting |
| 2D anime / hand-drawn styles | 3D reconstruction, CGI, photorealism |

### Words That Degrade Quality

These tend to weaken output when used without specific visual direction:

- `fast` without qualification
- `cinematic` used alone
- `epic`
- `amazing`
- `beautiful`
- `stunning`
- stacked unqualified speed words

---

## 7. Genre Adaptation Patterns

The prompt structure stays the same. Vocabulary, density, movement, sound, and emphasis shift by genre.

### Cute / Kawaii / Stop-Motion

- `[VISUAL STYLE]` can reference Laika, Aardman, Pixar short films, or another specific production language.
- Character modeling emphasizes tactile material physics: jiggles, squishes, bounces.
- Timed narrative emphasizes exaggerated expressions and held comedic beats.
- Stop-motion cadence is established in `[VISUAL STYLE]` and reinforced in `[FINAL VISUAL STYLE]` when important.
- Sound is diegetic and ASMR-forward when appropriate.
- Camera behavior is mostly fixed or slow when the characters carry the energy.

### Cyberpunk / Horror / Action

- `[VISUAL STYLE]` can reference specific films, directors, or production traditions and volumetric atmospheric effects.
- Character modeling emphasizes material science: automotive paint sheen, translucent tubing, chrome vertebrae, skin-to-hardware integration.
- Action is rapid and precisely sequenced while respecting speed asymmetry.
- Camera work can become aggressive while keeping one primary movement at a time.
- Audio can use silence as a weapon against mechanical or physical impact.

### Comedy / Dramedy / Dialogue-Driven

- `[VISUAL STYLE]` can reference specific shows, directors, or animation lineages for timing.
- Character modeling can use personality and wardrobe as comedy signals.
- Timing follows dialogue, interruption, reaction, and held beats rather than visual spectacle.
- Snap-zooms, reaction holds, and deliberate framing changes can support comedic timing.
- Subtext is carried through performance, reaction, staging, and timing.

### Anime / Moe / Japanese Healing

- `[VISUAL STYLE]` specifies the relevant anime aesthetic, line behavior, cel shading, painterly treatment, or frame-to-frame redraw.
- Character modeling includes anime-specific features when they matter.
- VFX stays stylized: painted-on effects, 2D surface animation, watercolor dissolves.
- Lighting can use warm golden-hour tones, soft-focus bokeh, or another specific established mood.
- Audio tends toward quiet ambient, room tone, wind, water, and ASMR when appropriate.

### Game / HUD / Interactive Style

- `[VISUAL STYLE]` specifies the game genre and perspective, such as TPS, FPS, or ADS transitions.
- Add `[UI OVERLAY]` when HUD elements need explicit placement.
- Add `[ANIMATION LOGIC]` when the scene needs state-machine behavior such as `start_state → mechanics → end_state`.
- Describe perspective transitions chronologically, with one primary camera movement per distinct shot or beat.

### Brutal Deity Combat / Mythological Violence

- `[VISUAL STYLE]` can reference specific anime combat lineages such as Samurai Champloo, Ninja Scroll, or Madhouse-era violence.
- Lore-grounded attacks and dialogue use actual supplied or researched mythology rather than arbitrary powers.
- Physical damage remains visible and carries forward between clips.
- Both combatants remain in constant physical motion during the fight; avoid static tableau moments mid-combat.
- Lock the spatial layout — who is on which side and which direction each combatant faces — and preserve it through the sequence.
- Audio can layer distinct vocal signatures — breathing, growls, feral laughs, pain sounds — with wet organic impacts.

---

## 8. Reference Discipline

This is one of the highest-priority systems in multi-clip production work. Reference images carry composition, pose, framing, color, design, and spatial priors into the generation.

### Rule 1: `[REFERENCES]` Comes First

Place `[REFERENCES]` before `[VISUAL STYLE]`, character descriptions, setting, and the timed sequence so reference-use instructions are established before the model processes the rest of the scene.

List each supplied image and video separately.

When `@video1` is the direct continuity reference, list it first. Otherwise list image references first, followed by video references.

### Rule 2: Define the Role of Each Reference

State exactly what each reference controls.

Examples:

```text
@image1 — Controls Nazz's identity, proportions, face, hair, stubble, and jumpsuit.
@image3 — Controls the chamber environment, palette, and stable lighting.
@image4 — Controls the confrontation composition and relative character placement.
```

A reference can control character identity, wardrobe, prop design, environment, palette, lighting, material appearance, spatial layout, composition, continuity state, or visual style.

### Rule 3: Exact Composition Is Not Preserved by Default

Do not reproduce a reference's exact original composition or framing unless the user explicitly wants it preserved.

Examples:

```text
Nazz @image1 controls his identity, proportions, face, hair, stubble, and jumpsuit.

Oz @image2 controls his identity, proportions, face, hair, clothing, and single red rigid arm.

Do not reproduce the character's reference poses or layouts.

The Layered Rock Chamber @image3 controls the environment, palette, and lighting. Do not reproduce its exact original composition or framing.

The hand-clasp reference @image5 controls the appearance of the hands and their firm completed clasp. Do not reproduce its exact original composition or background.

@image6 controls the shot composition and relative character placement.
```

### Rule 4: Use Spatially Incompatible Framing When Needed

A strong unwanted pose prior can be broken with a composition the reference cannot naturally fit into, when that composition also serves the scene.

Examples:

- Extreme macro close-up on a specific body part
- Overhead top-down
- 90-degree horizontal side profile at ground level
- Over-the-shoulder from directly behind
- Inverted close-up
- First-person POV from another character's eyes
- Extreme low-angle worm's-eye
- Close-up on a specific detail such as a hand, wound, weapon edge, droplet, or clawed foot

Rotate through these framings across the shots of a clip. Do not repeat the same framing twice within the clip. Varied angles create kinetic rhythm and reduce the chance of collapsing back into a reference pose.

### Rule 5: Use `Motion anchor:` Inside the Character Block

Character-specific movement rules stay beside the character description.

```text
RAKTABIJA:
Base: Massive red-skinned asura matching @image2.
Features: [...]
Motion anchor: Raktabija stays in close-range combat — grappling, slamming, and swinging at close range. His mouth snarls, bites, roars, and closes rather than remaining fixed open.
```

### Rule 6: Carry Visible Physical Damage Forward

Persistent damage becomes part of `Features:` or `State in this scene:`.

```text
RAKTABIJA:
Features: Bald domed head with one curved horn; the other is gone, leaving a bloody bone stump. One of the four yellow eyes is ruptured and empty, oozing yellow fluid and blood.
```

This preserves narrative continuity and gives the model a more specific current design to lock onto.

### Rule 7: Reference Tag Formatting

Use:

- `@image1`, `@image2`, etc.
- `@video1`, `@video2`, etc.
- `@audio1`, `@audio2`, etc.

Use no space after `@`.

### Rule 8: Reinforce High-Risk Reference Rules Where They Matter

Repeat a high-priority reference rule once at the point where it directly controls generation:

- movement restrictions in `Motion anchor:`
- environment or lighting constraints in `[SETTING]`
- shot-specific composition constraints inside the relevant timed beat

---

## 9. Prompt Density Awareness

The bracketed setup and timed narrative give director-level control, but density still has diminishing returns and can introduce conflicting instructions.

### Guidelines

- Keep each camera instruction concise: one primary movement, optionally one secondary.
- Timed narrative can be longer when choreographic or performance specificity is doing real work.
- Keep `[VISUAL STYLE]` tight and specific rather than stacking adjectives.
- Keep lighting descriptions brief and specific when stated inside the timed sequence.
- Keep `[REFERENCES]` concise. State shared exclusions once and keep reference-specific exclusions only where needed.
- Keep the full prompt within the applicable platform or user-specified character limit.

### The Redundancy Test

Before finalizing, ask:

`Does this sentence control something the model can render, hear, preserve, interpret, or time?`

If not, cut it.

Reference-use instructions and concise directorial subtext can contain non-renderable information when they materially guide interpretation.

---

## 10. Example Prompts

### Example A — Cave Flash-Bloom Transition

```text
[REFERENCES]
@image1 — Cave-approach reference. Use it for the rear-view cave setting, the four imposing disciples moving deeper inside, the bright opening in the distance, the faint cave-dweller silhouettes, and the painterly brushstroke language. Do not hold on its exact still composition.
@image2 — Struggle reference. Use it for the low close confrontation, the imposing figure pressing forward from the bright opening, the foreground cave-dwellers resisting him, the strong backlight, and the same painterly style. Do not reveal it as a still image before motion begins.

[VISUAL STYLE]
Fluid 16fps hand-drawn 2D anime with visible brushstrokes and painterly backgrounds. Dark indigo-violet cave atmosphere, pale white-lavender backlight, soft cave haze, natural figure movement, and subtle frame-to-frame brush redraw.

[DURATION]
8 seconds

00–04 seconds:
Wide shot, rear view, slightly low angle, with a slow tracking push behind the four imposing disciples @image1. The four figures stride naturally deeper into the cave. In the far backdrop, faint silhouettes of cave-dwellers move near the bright cave opening.

04–05 seconds:
The four disciples keep moving forward as the camera continues tracking behind them. The cave-opening light swells brighter and begins to pulse, with a subtle shake running through the image as the bloom builds. The pulse suddenly surges into a fast white-lavender flash-bloom that overtakes the frame and whips the scene into the next shot.

05–08 seconds:
Low, close shot with slight handheld camera shake as the flash-bloom clears into @image2, with the struggle already in motion. The people in front struggle to resist the imposing figures. The tall figure with glowing magenta eyes tightens his existing hold on the man at frame right, twists his arm down, and forces him onto his knees beside the kneeling man in the center.

[FINAL VISUAL STYLE]
Fluid 16fps hand-drawn 2D anime with visible brushstroke boil, painterly cave haze, rough shadow texture, and a bloom that starts at the cave opening, builds with a subtle shake and pulse, then snaps into a fast white-lavender flash-bloom.

Avoid: Jitter, bent or distorted limbs, temporal flicker, chaotic composition, static reveal of the second shot, characters frozen in reference-image poses, 3D reconstruction, cutout motion.
```

### Example B — The Clarity Won’t Last

```text
[REFERENCES]
Nazz @image1 controls his identity, proportions, face, hair, stubble, and jumpsuit.

Oz @image3 controls his identity, proportions, face, hair, clothing, and single red rigid arm. Oz has no demonic or transformed features.

Character references define design. Do not reproduce their reference poses or layouts.

The Stained Rock Chamber @image4 controls the stained rock environment, layered stone textures, and blue-violet to magenta lighting. Do not reproduce its exact original composition or framing.

[AUDIO]
Use @audio1 as the dialogue reference. Lip-sync Nazz’s speech to the exact timing and delivery from the audio reference. Oz remains silent.

[VISUAL STYLE]
Fluid 1990s hand-drawn dramatic anime with crisp ink contours and flat cel shading. A held close OTS with a gradual transfer of sharp focus, followed by one deliberate hard cut to a low reverse OTS. Hair and clothing sway gently with fluid, irregular motion throughout.

[DURATION]
10 seconds

[CHARACTERS]
NAZZ:
Base: Adult stoic male matching @image1.
Features: Short spiky black hair, short dark stubble along his jaw and chin, dark navy-purple fitted work jumpsuit with long sleeves.
State in this scene: Crouched below Oz, speaking steadily with exact lip-sync.
Emotional state: Calm, grave, and certain of his warning.

OZ:
Base: Young man matching @image3.
Features: Messy spiky black hair, sharp dark blue-grey eyes, lean youthful build, high-collared short-sleeved tunic, loose cropped trousers, fitted boots, and one red rigid arm.
State in this scene: Standing over Nazz with his head bowed and gaze directed toward the ground. Oz remains silent.
Emotional state: Shaken by the possibility that he could hurt more people.

[SETTING]
STAINED ROCK CHAMBER:
Base: Environment matching @image4.
Features: Close layered rock walls, broad mineral bands, dark vertical stains and fissures.
Lighting: Deep blue-violet shadow with saturated magenta-red illumination.

00–06 seconds:
In the Stained Rock Chamber, hold a close angled OTS behind Oz’s rigid hand and hip with subtle handheld motion. Oz’s rigid hand and hip sit slightly blurred in the foreground while Nazz is sharp in the background, crouched below Oz and speaking: {It shocked you awake, but that clarity won’t last. The Thrum will take you again—}

At 3 seconds, Oz slowly tightens his fist. Nazz in the background gradually softens into blur while Oz’s rigid hand in the foreground resolves into sharp focus. Nazz’s hair and clothing sway gently throughout; Oz’s visible tunic edge and loose trousers move with slow, fluid, irregular motion. Magenta edge light from behind Oz defines his foreground hand and hip while cooler blue-violet light separates Nazz in the background, with the magenta edge catching Nazz’s hair and outer contour. (No music throughout.) <Low cavern ambience and soft clothing rustle.>

06–10 seconds:
Hard cut to a slightly low-angle reverse OTS behind Nazz with a slow camera drift. Nazz is softly blurred in the foreground while Oz is sharp in the background, standing above him with his head bowed, gaze directed toward the ground, and rigid fist clenched. Nazz raises his head slightly toward Oz as he finishes: {—and when it does, more people will die.} Their hair and clothing continue swaying gently with fluid, irregular motion. Magenta backlight behind Oz outlines his silhouette and catches Nazz’s hair and outer contour. <Low cavern ambience and soft clothing rustle.>

[FINAL VISUAL STYLE]
Fluid 1990s hand-drawn dramatic anime with crisp ink contours and flat cel shading. Maintain controlled layered depth, deliberate focus transitions, fixed blue-violet and magenta lighting, and gentle irregular movement in hair and clothing across the sequence.

Avoid: Static framing, digital zoom, abrupt focus hunting, moving light sources, visible wind effects, frozen reference poses, identity drift, jitter, temporal flicker, inaccurate lip-sync, subtitles, bent or distorted limbs, 3D reconstruction, CGI, photorealism.
```

---

## 11. Audio Design Patterns

Use `[AUDIO]` when supplied audio or video controls dialogue, vocal performance, music, or specific sound behavior. Moment-specific sound can also be written directly into the timed sequence where it occurs.

### Seedance 2.5 Inline Audio and Text Syntax

| Content | Syntax |
|---------|--------|
| Music or no-music instruction | `()` |
| SFX, ambience, room tone, and nonverbal vocal sounds | `<>` |
| Spoken dialogue | `{}` |
| Subtitles | `【】` |

The markers classify only the enclosed content. The surrounding narrative still controls timing, delivery, progression, mixing, interaction, and visual performance. Silence is a directional state and remains in the surrounding prose. Group related sounds inside one `<>` when they share timing and treatment; separate them when their timing or treatment differs.

Use specific sensory audio language such as:

- muffled
- echoing
- crunchy
- reverberant
- sharp
- wet
- distant
- low drone
- dead silence

### Reference Audio

When `@audio1`, `@audio2`, etc. define dialogue performance, preserve the relevant:

- wording
- timing
- pauses
- cadence
- vocal strain or restraint
- emotional delivery
- breath pattern
- lip-sync

An uninterrupted line can continue across camera cuts without resetting the performance.

### Genre Audio Patterns

| Genre | Audio Approach |
|-------|----------------|
| Macro / ASMR | wet textures, contact sounds, amplified material interaction |
| Horror / Cyberpunk | silence, sub-bass, metallic impacts, low drones |
| Comedy / Dramedy | ambient room tone, punctuation sounds, dialogue timing |
| Anime / Healing | soft ambient, wind, water, kitchen sounds, gentle musical cues |
| Action / Fantasy | layered SFX, environmental response, orchestral swells, bass drops |
| Stop-Motion | tactile diegetic sound, score only when specified |
| Brutal Deity Combat | distinct vocal signatures, wet organic impacts, silence beats |

---

## 12. Common Critical Constraints

These are recurring constraints that may apply depending on the scene type. Include only the relevant constraints.

- **Surface animation:** "All animation stays flat and embedded on the physical surface — painted-on aesthetic, never 3D pop-out."

- **Handheld realism:** "Camera maintains handheld micro-shake throughout. Never stabilizes to tripod smoothness."

- **Stop-motion cadence:** "Stop-motion with intentional frame-to-frame jitter. No smooth interpolation. Characters move in holds and pops."

- **Material integrity:** "Physical objects maintain real-world reflections, weight, and surface properties even when stylized animation occurs on or within them."

- **No breaking the plane:** "Animated elements within a contained surface never extend beyond the physical boundary of that surface."

- **Spatial layout lock:** "[Character A] on the LEFT, [Character B] on the RIGHT, facing each other across the [aisle/space] throughout. Neither character crosses behind the other at any point."

- **Reference pose exclusion:** "Character references define design. Do not reproduce their reference poses or layouts."

---

## 13. Image-to-Video vs. Text-to-Video Prompting

When generating from a supplied starting image, the prompt shifts toward what changes.

| Element | Text-to-Video | Image-to-Video |
|---------|---------------|----------------|
| Subject description | detailed | can be shorter because identity is already visible |
| Motion description | full choreography | focus on dynamic change and movement |
| Composition | establish it | preserve the starting composition when requested |
| Camera movement | flexible | align with the existing composition |

For image-to-video, establish the starting image's role in `[REFERENCES]`, make the starting-frame relationship explicit (`Starting from @image1...` or equivalent), and spend more of the prompt on what changes: movement, performance, focus, camera behavior, environmental response, and transformation.

---

## 14. Video Reference for Continuation

When `@video1` is the direct continuation reference, list it first inside `[REFERENCES]`.

Example:

```text
[REFERENCES]
@video1 — Direct continuation reference. Continue from its final visible character positions, environment state, damage, lighting state, and ongoing motion.
@image1 — ...
@image2 — ...
```

The continuation reference helps preserve the generation boundary mechanically. Character identity, environment, wardrobe, damage, and important spatial state are still established explicitly when they matter.

---

## 15. Multi-Clip Sequence Discipline

When writing a sequence of clips that tell a continuous story:

1. **Every clip fully re-establishes its current state.** Character identity, environment, wardrobe, materials, props, physical damage, and important spatial relationships are established again where needed.

2. **Carry visible physical damage forward.** Wounds, missing body parts, broken features, and damaged clothing become part of the current character description.

3. **Lock spatial relationships across clips.** Preserve important left/right, foreground/background, standing/crouched, facing, and distance relationships by stating them in the setup or opening timed beat.

4. **Use clip endings deliberately.** Pre-strike tension, mid-motion cuts, held reactions, dialogue crossing a cut, transitions, stillness, impacts, and resolved beats can all serve as endings depending on the sequence.

5. **Re-establish transformed environments.** When an earlier clip changes the environment, describe the resulting environment as the current `[SETTING]`.

---

## 16. Final Visual Style

`[FINAL VISUAL STYLE]` defines the desired finished visual output after the full timed sequence.

Use it to lock the sequence-wide visual conditions that must survive the generation, such as:

- animation language and rendering behavior
- line quality, cel shading, painterly treatment, or material rendering
- depth and focus behavior
- lighting consistency
- motion behavior
- spatial relationships and character-state continuity
- VFX or transition behavior
- other visual conditions that define the intended finished clip

The opening `[VISUAL STYLE]` establishes the visual direction before the sequence begins. `[FINAL VISUAL STYLE]` states what the finished output must preserve after the sequence has introduced cuts, performance, focus changes, lighting changes, VFX, transitions, and continuity demands.
