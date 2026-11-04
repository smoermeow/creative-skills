---
name: seedance-narrative-prompter-v1
description: Write timed narrative prompts for Seedance video.
version: 1.0.0
author: User, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [seedance, video-prompts, narrative, timing]
    related_skills: []
---

# Seedance Narrative Prompter

## Required Knowledge

CRITICAL: Read `references/knowledge.md` in full before creating or revising any Seedance prompt.

Analyze all supplied images before constructing the prompt. Use supplied video and audio according to the role given by the user. Analyze video or audio content only when the user specifically asks for that analysis.

## Core Behavior

1. **Output format:** Always deliver the final Seedance prompt inside a single `text` code block so the user can copy and paste it directly. Only the prompt goes inside the code block.

2. **After the code block:** Provide exactly three things in this order:
   - **Scene breakdown:** A concise plain-language description of exactly how the clip should play out if the model follows the prompt correctly — what the viewer sees through the sequence, written as a visualization guide rather than a repeat of the prompt.
   - **Character count:** Report the exact character count of the final Seedance prompt, including spaces and excluding the code fences, followed by the applicable limit. Example: `Character count: 4,312 / 4,500`.
   - **Four creative suggestions:** Exactly four short ideas for where to take the scene next or modifications to try. Keep them specific, one to two sentences each, numbered 1–4.

3. **Duration handling:**
   - Use the clip length supplied by the user.
   - If the user does not specify a duration, ask: `How long is this clip?`
   - Cover the full duration with no gaps.
   - Stagger timestamps according to scene rhythm. Do not default to evenly divided intervals.
   - Use the timing and pacing guidance in the knowledge base before writing the detailed sequence.
   - Give the cuts, shots, beats, scenes and sequences enough time to breathe and resolve. 
   - Do not rush the action or dialogue. Avoid cutting off a beat before it has fully played out.

4. **Reference handling:**
   - Label images sequentially in the order received: `@image1`, `@image2`, `@image3`, etc.
   - Label videos sequentially in the order received: `@video1`, `@video2`, etc.
   - Label audio sequentially in the order received: `@audio1`, `@audio2`, etc.
   - Use no space between `@` and the reference number.
   - List every supplied image and video separately inside `[REFERENCES]`.
   - List image references first, followed by video references. When `@video1` is the direct continuity reference, list it first.
   - State the role of each reference: character identity, wardrobe, prop design, environment, composition, palette, lighting, style, spatial layout, continuity state, or other relevant visual information.
   - By default, do not reproduce a reference's exact original composition or framing unless the user explicitly wants it preserved.
   - Use `[AUDIO]` directly below `[REFERENCES]` when supplied audio or video controls dialogue, vocal performance, timing, music, or specific sound behavior.

5. **Character limits:**
   - **Dreamina:** 5,500 characters
   - **Dreamina CLI** 15000 characters
   - **Flova:** 4,500 characters
   - **Artcraft:** 10,000 characters
   - **OpenArt:** 8,000 characters
   - **Default:** 4,500 characters
   - Count characters including spaces.
   - If the user specifies a platform, use that platform's limit.
   - If the user gives an explicit character limit, it overrides the platform limit.
   - If neither platform nor limit is given, use 4,500 characters.
   - Write for maximum useful specificity within the available budget. Trim repeated setup, duplicated information, and unnecessary wording before cutting details that control identity, performance, timing, geography, focus, transitions, continuity, or reference use.

6. **Multi-part prompt rule — Seedance memory rule:**
   - Every separate generation fully re-establishes the character, environment, wardrobe, materials, physical state, and important spatial relationships needed for that clip.
   - Carry visible physical damage and changed scene state forward explicitly.
   - Direct continuation through `@video1` carries the generation boundary mechanically; important current state is still established in the prompt.

## Creative Logic (read before writing)

**The first prompt must land hot.** Every paid render should already contain a deliberate creative interpretation, not a safe first pass.

- **Reject the generic default.** When the brief leaves room, choose the least-obvious viable reading instead of the safest AI-standard staging.
- **Every beat must earn its seconds.** It should change power, emotion, information, rhythm, position, attention, or visual state.
- **Write what can be seen or heard.** Turn abstract ideas into physical action, performance, focus, light, sound, or visible change.
- **Cut redundancy, never specificity.** Remove repeated setup, duplicated instructions, and unnecessary wording before removing the details that make the scene distinctive.
- **Use the right logic beat by beat.** A sequence can move from restrained drama into violent action and back again.
- **Intensity is not the same as noise.** Movement, impact, silence, stillness, hesitation, compression, and release can all create pressure.

### Action / high-intensity scenes

1. **Start with a strong visual decision.** Enter from an angle, depth plane, motion state, or composition that gives the action an immediate identity.

2. **Push the framing as the action changes.** Change angle, distance, height, depth, or orientation when the physical situation changes. Framing follows the escalation.

3. **Keep the camera readable.** Camera movement gets one clear job at a time: track, orbit, push, pull, rise, drop, follow, or reveal. When subject action becomes complex, keep the camera controlled enough for the action to read.

4. **Choreography, not summary.** Write the step, swing, block, collision, recoil, stumble, recovery, and counter. Every important verb should be visible frame by frame.

5. **Escalate through change.** Raise or turn the action through force, distance, footing, rhythm, threat, environmental damage, reversal, or control of the space.

6. **Grade the impacts.** Ordinary strikes read cleanly. Major collisions earn stronger shake, hit-stop, flash, debris, distortion, lighting response, or sound weight. Save the strongest treatment for the beats that matter most.

7. **Make the environment react.** Cloth snaps, dust lifts, furniture shifts, water ripples, loose objects jump, light flickers, surfaces crack. Physical consequence sells force.

8. **Stack the senses around the impact.** Camera, body motion, expression, material response, light, sound, and VFX can reinforce the same beat.

9. **Keep dense FX readable.** Preserve the important face, body silhouette, weapon or attack path, target, and direction of force.

10. **Let the impact remain visible.** Bloom, debris, smoke, blood, particles, flashes, and distortion support the contact rather than swallowing it.

11. **Use stillness as contrast.** A hold, eye-lock, recoil, or silence before or after a major movement can make the next beat hit harder.

12. **End on a deliberate image.** Unresolved movement, a stunned hold, an interrupted strike, settling debris, recovery, or a hard visual beat can all carry the ending.

### Dramatic / slower scenes

1. **Make the acting specific.** Replace broad emotion labels with behavior: the delayed answer, broken eye contact, tightening jaw, held breath, forced smile, restless fingers, swallowed word, stiffened posture, or voice that changes halfway through the line.

2. **Dialogue is a physical event.** Direct pace, hesitation, interruption, breath, restraint, emphasis, volume, and gaze when they matter to the performance.

3. **Let subtext leak through behavior.** Posture, hands, eyelines, distance, silence, and timing can contradict or complicate the spoken words.

4. **Use stillness deliberately.** A held close-up, locked composition, or motionless character can create pressure when the moment deserves to be held.

5. **Move the camera when the scene changes.** Push closer as pressure or intimacy increases. Pull away when connection breaks. Reframe when power shifts. Cut when attention changes.

6. **Use depth to control attention.** Foreground, midground, background, partial occlusion, shallow focus, and rack focus can reveal information and redirect attention.

7. **Treat eye lines as beats.** Who looks, who avoids looking, who notices first, and when contact breaks can carry the scene.

8. **Use silence as part of the dialogue.** Pauses, unfinished sentences, breath, room tone, footsteps, distant noise, and the absence of music can hold tension.

9. **Let tension tighten before it breaks.** Reduce movement, shorten replies, narrow space, delay an answer, hold focus, introduce a background sound, or let one character notice something first.

10. **Keep quiet scenes progressing.** Trust, suspicion, distance, attention, confidence, control, understanding, or emotional exposure should continue changing.

11. **Use affect locks when the distinction matters.** Example: `calm and threatening — NOT angry`, `embarrassed and pleading — NOT terrified`.

12. **Let lighting support the emotional turn.** Use shadow, backlight, practical light, reflection, exposure, or color changes when they strengthen the beat.

13. **Let transitions grow out of the scene.** Sound, movement, light, smoke, reflections, foreground wipes, focus shifts, or matching shapes can build, take over, and resolve into the next image.

14. **Follow supplied performance references.** When `@audio1`, `@audio2`, or another reference defines delivery, preserve its wording, timing, pauses, breath, tone, and emotional shape. Build the visible acting around that performance.

15. **End on what lingers.** A look that is not returned, a hand stopping, an unfinished sentence, a focus shift, someone leaving frame, or held silence can carry the ending.

## Prompt Structure

Every prompt follows this structure:

```text
[REFERENCES]
@image1 — ...
@image2 — ...
@video1 — ...
@video2 — ...

[AUDIO]
@audio1 — ...
@audio2 — ...

[VISUAL STYLE]
...

[DURATION]
...

[CHARACTERS]
CHARACTER NAME:
Base: ...
Features: ...
Physics / personality / detail: ...
Motion anchor: ...
Emotional state: ...
State in this scene: ...
Power: ...
Power this scene: ...

[SETTING]
SETTING NAME:
Base: ...
Features: ...
Lighting: ...

00–XX seconds:
...

XX–YY seconds:
...

[FINAL VISUAL STYLE]
...

Avoid: ...
```

Include `[AUDIO]` when relevant. Inside `[CHARACTERS]` and `[SETTING]`, internal labels are optional; use them only when they improve clarity and serve a narrative function for the overall sequence. `[REFERENCES]`, `[VISUAL STYLE]`, `[DURATION]`, `[FINAL VISUAL STYLE]`, and `Avoid:` are part of every prompt.

## Non-Negotiable Rules

### Reference Discipline

- **`[REFERENCES]` comes first.** Reference-use instructions are established before style, character descriptions, setting, and the timed sequence.

- **Reference composition is not preserved by default.** Preserve exact composition or framing only when the user explicitly assigns it as part of the reference's role.

- **Use spatially incompatible framing when reference drift is a risk.** Extreme macro close-ups, overhead top-downs, 90-degree side profiles, direct rear over-the-shoulder shots, inverted close-ups, first-person POV, and extreme low-angle worm's-eye views can break a strong unwanted reference-pose prior when they also fit the scene.

- **Use `Motion anchor:` inside the character block.** Character-specific movement rules stay beside the character description.

- **Carry visible physical damage forward between clips.** Wounds, missing parts, broken features, damaged clothing, and other persistent changes become part of the current character description.

- **Reinforce high-risk reference rules where they matter.** A movement restriction belongs in `Motion anchor:`; an environment rule belongs in `[SETTING]`; a shot-specific composition rule belongs in the relevant timed beat.

### Core Prompt Discipline

- **References before generation instructions.** Establish every supplied reference and its role before style, characters, setting, or action.
- **Visual style before action.** Define the visual language in `[VISUAL STYLE]` before the timed sequence begins.
- **Character modeling before the timeline.** Define every character, active object, creature, or entity that needs identity consistency before the timed sequence.
- **Setting before the timeline.** Define environments that need continuity before the timed sequence.
- **Timestamped sequence.** Every second of the clip is accounted for in explicit timestamp ranges.
- **A timestamp range can contain multiple cuts.** Group cuts inside one range when they belong to one continuous dramatic or visual beat.
- **Dialogue attribution stays clear.** Name the speaker and write the exact line and delivery when dialogue matters. Spoken dialogue uses `{}`.
- **Seedance 2.5 inline audio and text syntax.** Use `()` for music or no-music instructions, `<>` for SFX, ambience, room tone, and nonverbal vocal sounds, `{}` for spoken dialogue, and `【】` for subtitles. These markers classify only the enclosed content; the surrounding narrative controls timing, delivery, progression, mixing, and interaction. Silence remains narrative direction rather than audible content. Group related sounds inside one `<>` when they share timing and treatment.
- **Stagger timestamps based on scene rhythm.** Short beats suit impacts and realizations; longer beats suit sustained action, dialogue, ritual, transformation, atmosphere, and performance.
- **Camera direction stays explicit.** Every distinct shot or cut states camera position and movement naturally inside the narrative.
- **Action is choreography, not summary.** Describe specific physical movements the model can render.
- **Sensory stacking stays inside the beat.** Camera, action, expression, texture, lighting, sound, focus, and VFX can reinforce the same moment.
- **VFX and physics appear where they occur.** Particle effects, transformations, material behavior, and physical reactions stay attached to the beat that causes them.
- **Stable information stays anchored.** Character identity, environment, and stable lighting are established once and carried through until they change.
- **Final visual state.** `[FINAL VISUAL STYLE]` defines the desired finished visual output of the whole clip. Use it to lock any sequence-wide style, depth/focus behavior, lighting consistency, motion behavior, spatial or character-state continuity, and transition behavior that must remain true in the finished result.

### Camera and Motion Rules

- **One primary camera instruction per distinct shot.** Optionally add one secondary movement using `then`.
- **Keep each camera instruction concise.** Position + movement + qualifier is usually enough; aim for under 20 words for the camera portion of a shot description.
- **Rhythm over specs.** Use `slow`, `smooth`, `gentle`, `controlled`, `steady`, and similar motion language. Technical photography specifications can appear as visual style anchors but do not drive camera behavior.
- **Speed asymmetry rule.** Fast camera movement, fast subject action, and a complex scene do not peak simultaneously. Keep at least one axis controlled enough for the action to read.
- **Separate camera from subject movement.** Write them as distinct actions even when they appear in the same paragraph.
- **Lighting state remains clear for every shot.** Stable lighting can be inherited from `[SETTING]`; lighting changes are written at the moment they occur.
- **Stability constraints close every prompt.** `Avoid:` begins with `Jitter, bent or distorted limbs.` and adds relevant scene-specific failure modes.
- **Use specific visual language.** Replace vague words such as `epic`, `amazing`, `beautiful`, `cool`, `lots of movement`, and unqualified `fast` with renderable direction.
- **`[VISUAL STYLE]` uses sensory and rhythm language.** Rendering intentions such as grain, haze, volumetric fog, subsurface scattering, brushstroke boil, bloom, or bokeh describe visible texture and are appropriate here.

## Writing Style

- Use brackets only for major fields.
- Character and setting names are unbracketed subsections. Internal labels are optional; use them only when they improve clarity and serve a narrative function for the overall sequence.
- Timed ranges are written as chronological cinematic prose.
- Be specific about materials, colors, textures, physics, movement, and performance.
- Make emotional and tonal direction explicit when it materially affects the scene.
- State flat, embedded, surface-level, or other physical animation constraints clearly when they matter.
- Match vocabulary and energy to the genre.
- Keep camera direction concise.
- Keep action choreographic.
- Keep lighting brief and specific when it changes or requires emphasis.
- Give `[REFERENCES]` enough space for exact role definition and anti-drift instructions.
