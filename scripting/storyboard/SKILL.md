---
name: storyboard
description: Create validated storyboard JSON from raw idea text using confrontation extraction, beat planning, pacing, and cinematic QA.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [prompt-library, chain, confrontation, storyboard, hermes-native]
---

# Storyboard

Purpose
Convert raw ideation/blueprint text into production-usable storyboard JSON through two dependent prompt stages.

Internal stages
1) confrontation extraction stage
2) storyboard expansion stage

Stage 1 output is never a final deliverable by itself.

## Lookup note

This portable package is registered as `storyboard`. Load this package’s `SKILL.md`.

## Stage 1 — Confrontation Extraction

Extract the core dramatic tensions from the blueprint. For each tension, produce:

```json
{
  "id": "T1",
  "label": "Entity vs. Village",
  "type": "external|internal|interpersonal|supernatural|existential|structural",
  "description": "One-sentence description of the tension.",
  "weight": "hook|core|escalation|climax|resolution|bridge",
  "scenes": [1, 2, 3]
}
```

Rules:
- Weight `hook` = first thing the audience feels. `core` = carries the middle. `escalation` = raises stakes mid-act. `climax` = the point of irreversible action. `resolution` = aftermath. `bridge` = connects to next chapter.
- `scenes` maps each tension to which scene numbers it lives in.
- Include an `escalationPath` array listing tension IDs in the order they activate.
- Include `thematicCore` as a string array of 3-5 statements the blueprint argues for.
- Typical output: 5-8 tensions. Fewer = thin story. More = unfocused.

## Stage 2 — Storyboard Expansion

Each scene from the blueprint becomes a scene object. Each scene gets 3 keyframes (A/B/C pattern):

```json
{
  "sceneNumber": 1,
  "title": "Scene title",
  "durationSec": "8-12",
  "confrontations": ["T1"],
  "purpose": "What this scene does narratively",
  "keyframes": [
    {
      "kf": "1A",
      "timing": "0.0s",
      "shot": "Shot description — framing, distance, subject",
      "blocking": "Who occupies frame-left, center, frame-right, foreground, midground, and background",
      "visual": "Color palette, lighting, composition details",
      "motion": "What moves, how fast, direction",
      "continuity": "Position, direction, physical state, and props inherited from this shot and handed to the next",
      "dramaticChange": "What meaningfully changes between the beginning and end of the shot",
      "audio": "Sound design — diegetic first, then score/ambience"
    }
  ]
}
```

Keyframe conventions:
- A = establish (what we see first)
- B = develop (what changes or reveals)
- C = land (the beat that closes the moment)
- Timing is cumulative from scene start.
- Audio is concrete — name specific sounds, not "tense music."
- 3 keyframes per scene is the standard. Use 2 only for very short bridge scenes.

### Production fields for every shot/keyframe

Keep the existing keyframe/shot structure. Add these three concise production fields to every shot/keyframe:

- `blocking`: Describe principal characters and important objects relative to the camera using frame-left, center, frame-right, foreground, midground, and background. Include facing direction when relevant. Never locate a subject only as "left of the hero" or "beside the boss."
- `continuity`: State the position, screen direction, eyeline, entry or exit position, physical state, restraints, wounds, costume state, and important prop placement or ownership that must connect with adjacent shots. Include only what matters for the handoff; do not repeat the complete blocking description.
- `dramaticChange`: State what meaningfully changes between the beginning and end of the shot: physical situation, audience understanding, power relationship, or visibly expressed character control or emotion. Do not merely repeat `motion`.

Before writing shots, establish the location's stable geography internally: entrances and exits, fixed landmarks, character starting positions, movement routes, and axis of action. This is a planning rule, not an additional required output field.

## Output contract

```json
{
  "confrontation_blueprint": {
    "projectTitle": "string",
    "premise": "string",
    "tensions": [...],
    "escalationPath": ["T1", "T3", ...],
    "thematicCore": ["...", "..."]
  },
  "storyboard": {
    "videoTitle": "string",
    "format": "string",
    "estimatedRuntime": "string",
    "tone": ["...", "..."],
    "scenes": [...]
  }
}
```

## Validation
- videoTitle: string — required
- scenes: array, length >= 1 — required
- Each scene has keyframes: array, length >= 1 — required
- Run `json.load()` to verify parseable JSON before writing to disk.

## Cheap-model reliability layer (required)

Use this layer when quality drops on smaller or cheaper models. Treat it as mandatory default behavior, not optional style guidance.

### Stage 1.5 — Beat decomposition (between confrontation extraction and storyboard expansion)
Before writing keyframes, decompose each scene into atomic beats.

Per scene create a temporary plan object:
```json
{
  "sceneNumber": 1,
  "durationSec": "10-14",
  "beats": [
    {"id": "B1", "function": "orient", "subject": "Kiba", "action": "enters frame and scans room"},
    {"id": "B2", "function": "reveal", "subject": "book", "action": "book appears under cloth"},
    {"id": "B3", "function": "reaction", "subject": "Kiba", "action": "stillness after discovery"}
  ]
}
```
Rules:
- One beat = one camera intention.
- If two characters react in sequence, that is two beats.
- No keyframes until beat list is complete.

### Deterministic pacing map
Convert scene duration into target keyframe count first, then write keyframes.

- 6-8s scene → 3-4 keyframes
- 9-12s scene → 4-6 keyframes
- 13-16s scene → 6-8 keyframes
- 17-22s scene → 7-10 keyframes

Cadence rules:
- Default cut interval: 1.6-2.6s
- Allow 1 hold beat per scene (2.8-4.0s) for discovery/aftermath/decision
- Avoid perfectly uniform intervals across all cuts in a scene

### Shot grammar contract (hard)
`shot` must be a single line with this structure:
`<ShotSize> + <Angle> + <Subject> + <Framing intent>`

Examples:
- `Medium close-up, low angle, Kiba face, decision locks in`
- `Wide, ground level, village street, shadow spawn crosses foreground`

Hard limits:
- 1 sentence only
- Max 22 words
- No chained action lists
- No lore exposition in `shot`

### Cut-purpose tagging (internal planning)
Each keyframe must have one cut purpose from this set:
- `orient`
- `intensify`
- `reveal`
- `reaction`
- `commit`
- `aftermath`

Scene-level progression requirement:
- Most scenes should follow: `orient -> intensify/reveal -> reaction/commit -> aftermath or handoff`
- Bridge scenes may use shorter variants

### Continuity guardrails
Across consecutive keyframes, maintain:
- Subject handoff clarity (who owns each frame)
- Screen direction consistency unless intentional break
- Eyeline continuity for dialogue/reaction exchanges
- Axis stability unless the axis break is the beat

Scene-boundary rule (hard):
- Do not re-stage prior-scene action inside the current scene unless explicitly requested.
- Treat previous-scene events as background aftermath/context only (e.g., smoke, debris), not new action beats.
- If user says "this is the scene after INTRO/Scene 1", start from post-event state.

### Audio field policy
- Do not invent audio details to pad cinematic realism.
- Include `audio` only when the user explicitly asks for audio/sound design or provides concrete audio cues.
- If audio is not requested, omit the `audio` key from keyframes rather than fabricating diegetic/score elements.

### Cinematic QA gate before final JSON
Run a self-check and repair once before returning output.

Reject and rewrite any keyframe that fails:
1. More than one beat in the same keyframe
2. `shot` longer than 22 words or more than one sentence
3. Missing explicit shot size or angle
4. Timing pattern too uniform for entire scene
5. Scene has no reaction cut when a character shift or reveal happens
6. `blocking` does not locate the principal visible subjects relative to the camera
7. `continuity` contradicts an adjacent shot's position, direction, physical state, or prop placement
8. `dramaticChange` only repeats the action already described in `motion`
9. Camera and blocking together do not provide enough information to draw or prompt the composition

Do not skip this QA gate on cheaper models.

### Keyframe density for horror scenes
- Standard: 3 keyframes per scene (A/B/C).
- Horror openers: increase to 6-7 keyframes at ~2s each. The extra cuts build the visceral sequence — each keyframe is one escalation step in the violation.
- Use 1-2 longer keyframes (3-4s) for the moments that need to breathe: the drain, the aftermath, the turn away.

## Camera and keyframe discipline (learned from HOST iteration)

### Every keyframe must have a clear shot type
- Every keyframe needs an explicit camera angle in the `shot` field: "Close-up", "Medium shot", "Medium close-up", "Wide", "Low angle", "Ground level", "Extreme close-up", "Two-shot", "Profile", etc.
- Every keyframe must name its SUBJECT: "Kiba's face", "the mother's face", "her torso", "the book page". Never ambiguous — the reader should never wonder what the camera is pointed at.
- If a keyframe's beat includes a reaction from a different character, that is a separate keyframe. Do not fold two subjects' reactions into one shot description.

### Behavior shift pattern (character body deciding before mind)
When a character makes a morally weighty decision, show the shift across multiple keyframes, not in one:
1. **Before** — body still in previous state (panicked, searching, coiled). Eyes darting. Weight shifting.
2. **Approaching** — eyes stop searching and lock. Posture lowers. Voice changes pitch.
3. **The shift** — close-up on their face. The change happens in stillness. Jaw sets. Something closes behind the eyes.
4. **The other sees** — cut to a close-up of the person watching them change. Their reaction (breathing stops, arms tighten, recognition) is its own beat, its own keyframe.
5. **Executing** — medium shot. Steps are now deliberate, measured, controlled. Body is already doing what words haven't said.
6. **Commitment** — profile or medium close-up of both. The act. Turn away. No look back.

The cut between the decision-maker's face (step 3) and the witness reading it (step 4) is critical. It is the moment the audience processes what happened through someone else's eyes.

### Frantic search / panic sequence pattern
For scenes where a character is tearing through a space looking for something:
- Change camera angles every keyframe: back shot → close-up hands → front close-up face → low angle → ground level
- Include object-level cuts: hands pulling things → item falling → cut to item landing on floor → back to character
- Use 5-7 keyframes for a 10-15s scene — the rapid cuts mirror the character's panic
- When they find what they need, HOLD the shot. The first stillness in the sequence lands hard because nothing has been still until then. Hold 2-3s on the discovery.

## Failure policy
- Fail hard if either stage cannot produce valid JSON after one repair pass.
- Never wrap result in markdown.
- Write output as `.json` next to the source blueprint unless user specifies otherwise.

## Operator corrections from production use (must-follow)

When the user asks to "use animestoryboard" or points to this skill path, treat it as strict contract mode.

1. **Do not dump full JSON in chat unless explicitly asked.**
   - Default behavior: write/update the JSON file directly and reply with path + what changed.

2. **Do not invent audio content to sound complete.**
   - If audio is unknown/unprovided, keep `audio` as empty string `""` for schema compatibility.
   - Do not fabricate SFX/music details.

3. **Adapt user scene intent into this schema; do not force a generic template beat.**
   - Preserve scene continuity constraints from prior scene context.
   - Keep action ownership exactly as described by user; avoid reintroducing previous-scene actions.

4. **Duration coverage is mandatory.**
   - Ensure `durationSec`, `estimatedRuntime`, keyframe count, and timing progression actually span the requested scene length.
   - For ~15s scenes, use the pacing map (typically 6-8 keyframes), not compressed 3-shot outputs.

5. **Language follows user directive.**
   - If the user requests English output, all JSON text fields must be English.
