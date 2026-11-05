# Storyboard

## Purpose

Convert raw story ideas or a written scene blueprint into a production-oriented storyboard JSON file. Version `1.1.0` extracts dramatic tensions, decomposes scenes into atomic beats, expands them into timed cinematic keyframes, and applies continuity and shot-quality checks.

The deliverable is **validated JSON written to disk**, not a rendered storyboard image, video, or a standalone list of tensions. Confrontation extraction is an internal stage, not the final result.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Storyboard skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/scripting/storyboard
```

### If you already use a protected orchestrator

```text
Install the complete Storyboard skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/scripting/storyboard

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Prerequisites and setup

Download or copy the **complete `storyboard` folder**. Give an AI assistant access to the folder, your source blueprint, and the directory where the JSON should be written. Directly asking it to read `SKILL.md` is enough; no skill installer, special CLI, provider account, or generation API key is required.

The assistant needs file-reading and file-writing tools and a Python environment that can run the standard-library `json.load()` validation required by the skill. There are no bundled runtime scripts, third-party Python requirements, or image-generation dependencies.

Read `SKILL.md` in full, including its mandatory reliability layer and final operator corrections—not just the initial A/B/C example. This README describes use; it does not replace the skill's method.

## Required files

| File/input | Role |
| --- | --- |
| `SKILL.md` | Complete two-stage method, intermediate beat-planning rules, output contract, pacing, QA, validation, and file-delivery policy. |
| Your blueprint or idea text | The story material to adapt. A source file gives the default output location. |

Keep the full downloaded folder together.

## Inputs

- **Source idea or blueprint:** story premise, characters, dramatic conflict, scene order, concrete actions, and intended ending. Supply a readable file path or the text itself.
- **Format and timing:** intended video format, scene durations, and total runtime when known. State timing constraints explicitly so keyframes cover the actual requested length.
- **Continuity constraints:** starting positions, geography, axis of action, screen direction, prior-event aftermath, props, costume state, wounds, and action ownership that must be preserved.
- **Language and tone:** specify the output language and desired dramatic treatment.
- **Audio, only if supplied or requested:** provide concrete cues or explicitly say no invented audio.
- **Output path:** optional when the source is a file; by default the result is a `.json` file next to the source blueprint. For pasted text, provide a destination because there is no source-file directory to inherit.

## Copy-ready invocation example

Replace the skill and output paths with accessible local locations, then paste this request into your assistant:

```text
Read /absolute/path/to/storyboard/SKILL.md in full and follow its complete
method, including beat decomposition, duration-based pacing, continuity QA,
operator corrections, and JSON validation. Do not modify the skill files.

Create an English storyboard JSON file at /absolute/path/to/storyboard.json
from this blueprint. Title: The Last Light. Format: landscape short film.
Two scenes, each exactly 12 seconds, total runtime 24 seconds.

Scene 1: An adult lighthouse keeper enters the lamp room from the frame-left
stair door. The lamp has stopped. The sea window is frame-right; the manual
crank is fixed in the center foreground. She sets a copper mug on the small
frame-left shelf, studies the motionless gears, and grips the crank with both
hands. End before she turns it.

Scene 2: Begin from that held grip; do not replay her entrance or discovery.
She strains against the crank, finds a steady rhythm, then stops as the lamp
restarts. Warm light sweeps across her face. She looks toward the sea window
in quiet relief. The mug stays on the shelf; geography and screen direction
remain consistent.

Use restrained physical acting. Do not invent audio cues; keep unknown audio
as an empty string for schema compatibility. Plan atomic beats before
keyframes and use the skill's duration-based keyframe counts, not a compressed
three-shot summary. Cover both full scene durations.
Validate JSON with json.load() and check required fields before writing the
final file. Reply with the saved absolute path and a short validation summary,
not the full JSON in chat. Do not generate images or video.
```

## Expected output

A parseable `.json` file with two top-level objects:

- **`confrontation_blueprint`:** `projectTitle`, `premise`, `tensions`, `escalationPath`, and `thematicCore`. Tensions carry an ID, label, type, description, dramatic weight, and the scene numbers where they apply. Thematic core contains 3–5 statements; the skill typically expects 5–8 tensions.
- **`storyboard`:** `videoTitle`, `format`, `estimatedRuntime`, `tone`, and `scenes`. Each scene contains `sceneNumber`, `title`, `durationSec`, `confrontations`, `purpose`, and `keyframes`.

Keyframes carry `kf`, `timing`, `shot`, `blocking`, `visual`, `motion`, `continuity`, and `dramaticChange`, with audio handled according to the request and skill corrections. Timing is cumulative **from each scene's start**. `blocking` locates subjects relative to the camera; `continuity` explains the adjacent-shot handoff; `dramaticChange` describes what changes in situation, understanding, power, or expressed emotion rather than merely repeating motion.

The initial A/B/C convention means establish, develop, and land. It is not a universal three-keyframe cap: the mandatory pacing map calls for 4–6 keyframes at 9–12 seconds and 6–8 at 13–16 seconds. The agent plans beats and cut purposes internally before writing keyframes, then performs the cinematic QA gate and one repair pass where needed.

Validation must include `json.load()` parsing, a string `storyboard.videoTitle`, at least one scene, and at least one keyframe per scene. Also check the full requested duration, scene/keyframe fields, tension references, shot grammar, geography, and continuity. The normal response is the **saved file path plus a short change/validation summary**. Full JSON in chat is only returned when explicitly requested; the JSON file itself must not contain Markdown fences.



## Chat setup — ChatGPT Project first, custom GPT or Gem equivalent

Follow the shared [chat setup guide](../../CHAT_SETUP.md). Prefer **one skill per ChatGPT Project or Gem** (and per custom GPT where its editor is available): different skills reuse `SKILL.md`, so mixing them creates ambiguous file names and methods.

### Original files to upload

Download these actual original files from this folder and upload their complete contents as Project files, custom GPT Knowledge, or Gem Knowledge. Do not replace them with this README, a summary or the short routing block.

- [SKILL.md](SKILL.md) — Required: complete method, reliability layer, final operator corrections, Python validation and file-output contract.

Folder paths identify the originals; an upload UI may show only their basenames. Keep that mapping clear. **GitHub links alone are not uploaded context or live synchronization.** Refresh your uploaded copies yourself whenever the source changes; no automatic synchronization is provided.

### Copy-ready routing instructions

[Project instruction file](../../chatgpt-projects/storyboard.txt) · [Files to upload and setup](../../chatgpt-projects/README.md#storyboard)

Paste only this short block into **ChatGPT Project instructions** (primary), **custom GPT Instructions** (secondary, if available), or **Gem instructions**. The original files above remain the method, not this routing text.

```text
Use the uploaded Storyboard method.

Before answering each request, read these uploaded files in full:
- SKILL.md

Follow their method and output requirements. Do not rewrite the method or combine it with another prompting system.

If a required file is missing or cannot be read fully, ask for it before proceeding.

Do not claim validation or file delivery unless the required Python checks and file output were actually completed.
```

**Drafting is not completed execution.** Plain chat can help develop a storyboard draft only with your agreement. The complete skill requires actual Python `json.load()` validation, required-field checks and a real saved `.json` file. Use an environment with those tools, or hand the draft to a file-capable agent; without execution evidence, validation and file delivery remain uncompleted.

