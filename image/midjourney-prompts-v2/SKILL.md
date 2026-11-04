---
name: midjourney-prompts-v2
description: Use when writing concise Midjourney image prompts.
version: 0.1.0
author: User, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [midjourney, image-prompts, camera, controlled-revision]
    related_skills: []
---

# Midjourney Prompts V2

Create direct, copy-ready Midjourney prompts from approved visual ideas. This skill prioritizes visible content, one coherent camera setup, exact style anchors, and minimal revisions. It does not impose JSON, storyboard schemas, artist variations, or fixed rendering tails.

## When to Use

Use this skill when:

- the user asks for a Midjourney image prompt;
- the user wants character, object, environment, or scene design;
- the user supplies a style anchor that must remain exact;
- the user is iterating on an existing prompt and wants one scoped change;
- a previous prompt became bloated with explanations, blockers, or invented geometry.

Do not use this skill for:

- video prompts;
- provider execution or image generation;
- storyboard parsing or grid assembly unless the user explicitly requests a grid;
- artist-style variations unless the user explicitly asks for them.

## Canonical Prompt Structure

Every ordinary prompt uses four parts in this order:

1. **STYLE + CAMERA**
2. **SUBJECT**
3. **DETAILS**
4. **STYLE ANCHOR**

Use the template in `templates/prompt-template.txt`.

The delivered prompt contains no section labels unless the user asks for them. The default visible form is:

```text
In anime-style, a [SHOT SIZE] from a [CAMERA ANGLE].

[SUBJECT]

[DETAILS]

[STYLE ANCHOR]
```

## Procedure

### 1. Establish authority

Identify the user-approved concept, source image, baseline prompt, and style anchor. Treat supplied wording as authoritative. Completion criterion: every detail in the prompt is supported by the user, source, or an unavoidable literal completion.

### 2. Classify the subject

Choose one subject class:

- character;
- group;
- environment;
- object;
- action scene.

Do not force character-shot logic onto environments or environment logic onto characters. Completion criterion: framing language fits the actual subject.

### 3. Write STYLE + CAMERA

Use one short opening sentence:

```text
In anime-style, a [shot size] from a [camera angle].
```

State only the shot size and one physically coherent camera angle. Add lens language only when the user requests it or it materially changes composition.

Examples of valid environment framing:

- `a wide interior view from a high side angle`;
- `a medium-wide eye-level view from the doorway`;
- `a top-down overhead wide shot`.

Completion criterion: the camera occupies one possible position and faces one direction.

### 4. Write SUBJECT

Describe the primary visible composition in one sentence or compact paragraph. State what is in frame and where the principal elements sit.

Rules:

- Use ordinary nouns for ordinary places.
- Do not explain what the image is for.
- Do not diagnose prior failures inside the prompt.
- Do not write `reads as`, `should feel like`, `designed to`, `meant to`, `allows`, `helps`, or workflow rationale.
- Do not restate the style anchor here.

Completion criterion: a reader can sketch the main composition from the subject paragraph alone.

### 5. Write DETAILS

Add only visible appearance, materials, clothing, objects, surfaces, lighting, and state. Keep the detail level proportional to the request.

Rules:

- Describe what is present, not everything that must be absent.
- Omit unwanted elements instead of naming them as negative constraints.
- Do not repeat the subject paragraph in expanded wording.
- Do not turn a normal place into a themed, futuristic, symbolic, or geometrically unusual design unless requested.
- Do not add lore, relationships, actions, props, doors, counters, passages, or adjoining rooms without support.
- Put stored objects on shelves, active work on work surfaces, and architecture in physically plausible positions.

Completion criterion: every detail is visible, useful, non-duplicative, and requested or naturally necessary.

### 6. Append STYLE ANCHOR

Copy the user or project style anchor verbatim as the final paragraph. Never paraphrase, expand, merge, or replace an approved anchor.

Do not append a default phrase such as `cinematic lightning`, model parameters, artist attribution, or quality claims unless the user supplied it.

Completion criterion: the final paragraph byte-matches the approved style anchor when practical.

### 7. Deliver only the usable artifact

Return the complete prompt in one code block unless the user requests another format. Do not precede it with design rationale when the user asks for `only the prompt`.

For several prompts, give each a short human-readable title and one complete code block. Do not make the user assemble fragments.

Completion criterion: each prompt is directly copyable and self-contained.

## Environment Discipline

### Normal environments

When the user asks for a normal restaurant, kitchen, bedroom, office, or similar place:

- use ordinary real-world fixtures;
- choose only enough objects to establish function;
- let the style anchor carry the broader world treatment;
- avoid gimmick architecture and unrequested technology;
- do not convert `normal` into empty or generic.

### Geometry

Never invent room shape. Words such as `rectangular`, `square`, `L-shaped`, `irregular`, `long`, `narrow`, or `wide` alter geometry and require user support.

Do not prove the complete floor plan inside one image. Describe only surfaces and openings visible from the chosen camera. Opposing doors or walls cannot all appear front-on from one viewpoint.

If one space continues out of sight, use the smallest supported phrase. Example:

```text
At the back corner, a passage turns out of sight.
```

Do not name the hidden destination unless the user asks for it to be visible or identified.

### Functional objects

Distinguish these explicitly:

- a preparation table is a freestanding work surface;
- a wall-mounted shelf stores objects and is not another table;
- a cooking line contains burners, ovens, and ventilation;
- a passage is not automatically an exterior exit;
- PVC strip curtains cover an opening without defining its width or destination.

Completion criterion: no object changes category because of loose wording.

## Character Discipline

Describe identity, face, hair, anatomy, clothing, accessories, pose, and expression only to the level supported by the request or references.

When a character reference exists:

- treat it as identity authority;
- do not convert the character into a written lookalike;
- do not copy the reference pose or sheet layout into a scene prompt unless requested;
- distinguish character identity from story canon when the user only selected an asset.

## Controlled Revisions

When the user asks to add, remove, or change one thing:

1. Freeze the approved baseline.
2. Locate the smallest phrase that controls the requested result.
3. Replace that phrase once.
4. Preserve every other word when practical.
5. Return the complete revised prompt.

Do not use the correction as permission to redesign, normalize wording, add constraints, or explain the change inside the prompt.

Example:

- Request: add PVC strip curtains over the passage.
- Correct edit: add `PVC strip curtains covering the passage`.
- Incorrect edit: redefine the passage width, transparency, destination, turn, architecture, and visibility.

Completion criterion: a semantic diff shows only the requested change.

## Negative Constraints

Default to positive prompting. Negative constraints are permitted only when:

- the user explicitly supplies them;
- the target model has a verified recurring artifact that cannot be controlled positively;
- the user asks for a negative-prompt block.

Never place conversational diagnoses into a generation prompt. Phrases such as `not an empty room with tables`, `must read as functional`, or `do not make the same mistake` describe the prompting process rather than visible content.

## Grid Prompts

Use a grid only when requested. Preserve the requested template exactly and replace only its variable content.

For angle studies:

- let the reference image define subject content;
- write only the requested camera positions, angles, and framing sizes;
- do not add story action, movement paths, or repeated environment descriptions;
- correct contradictory counts such as `2x2` with `9 panels` before delivery;
- ensure the number of listed views equals the grid cell count.

## Midjourney Parameters

Append Midjourney parameters only when the user supplies or requests them. Preserve exact values and order when revising an approved prompt.

Do not invent `--ar`, `--stylize`, `--chaos`, `--seed`, model version, quality, or image weights.

## Pitfalls

- Solving an unasked architecture problem.
- Repeating the same composition with different adjectives.
- Treating every room as a geometric box.
- Naming a hidden room and causing the model to reveal it.
- Turning a shelf into a counter or second table.
- Describing a doorway as an exterior exit.
- Showing mutually opposing surfaces from one camera.
- Copying an example taxonomy instead of adapting its structure.
- Replacing a complete prompt with fragments during revision.
- Using another model's schema because its advice seems convenient.

## Verification

Before delivery, verify:

- [ ] Four-part order is STYLE + CAMERA → SUBJECT → DETAILS → STYLE ANCHOR.
- [ ] Opening has one shot size and one camera angle.
- [ ] Subject type and framing language match.
- [ ] Camera geometry is physically possible.
- [ ] Subject and details contain visible content only.
- [ ] No unrequested geometry, connections, props, or lore were introduced.
- [ ] Negative constraints are authorized and necessary.
- [ ] Approved style anchor is verbatim and appears once at the end.
- [ ] Controlled revisions change only the requested semantic field.
- [ ] Final output is complete, concise, and directly copyable.
