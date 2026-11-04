# Midjourney Prompts V2

Version **0.1.0** · Copy-ready image prompt writing only; no image generation.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Midjourney Prompts V2 skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/midjourney-prompts-v2
```

### If you already use a protected orchestrator

```text
Install the complete Midjourney Prompts V2 skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/midjourney-prompts-v2

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Purpose

Write concise Midjourney prompts from an approved visual idea, reference, or baseline prompt. The method keeps visible content separate from explanatory prose, uses one coherent camera setup, preserves your exact style anchor, and limits revisions to the change you requested.

This package does not submit prompts to Midjourney, generate images, or create video prompts. A Midjourney account is not needed to draft text here; using the resulting prompt in a generation service is outside this skill's execution scope.

## Setup and prerequisites

Use an assistant that can read [SKILL.md](SKILL.md) and the [prompt template](templates/prompt-template.txt). No API key, MCP connection, CLI, or additional dependency is required for text drafting. An assistant needs image-reading support if you want it to interpret a supplied image.

Keep both files together so the template remains available at its relative path.

## Required files

| File | Role |
|---|---|
| [SKILL.md](SKILL.md) | Prompt construction, subject-specific rules, camera checks, and controlled revisions. |
| [templates/prompt-template.txt](templates/prompt-template.txt) | Required four-part prompt structure. |

## Inputs

Provide:

- An approved subject or scene: character, group, environment, object, or action scene.
- What must visibly appear, including only supported details.
- Shot size and camera angle, if you have preferences.
- The exact final style-anchor wording to preserve.
- For revisions, the complete approved baseline and the one change you want.
- Midjourney parameters only if you want them included; supply their exact values and order when they must be preserved.

Reference images establish identity or visual content. A reference pose or sheet layout is not automatically part of the requested scene.

## Copy-ready invocation example

Paste this into your assistant with the package accessible:

```text
Use midjourney-prompts-v2. Read SKILL.md and templates/prompt-template.txt from this package.

Write only a complete prompt, not an image or a generation request.
Subject: a red ceramic teapot centered on a pale oak table beside a rain-streaked window.
Camera: a close-up from an eye-level angle.
Details: a curved handle, short spout, steam rising from the lid, and soft overcast window light.
Exact style anchor: clean cel shading, muted warm colors, crisp contour lines

Use STYLE + CAMERA, SUBJECT, DETAILS, STYLE ANCHOR in that exact order, as four unlabeled paragraphs inside one code block. Preserve the style anchor verbatim as the final paragraph. Add no parameters, props, lore, negative constraints, or explanation. Do not generate an image.
```

## Expected output

An ordinary prompt has **exactly four parts in this order**:

1. **STYLE + CAMERA** — one short opening with one shot size and one physically coherent camera angle.
2. **SUBJECT** — the main visible composition.
3. **DETAILS** — useful visible appearance, materials, lighting, and state, without repeating the subject.
4. **STYLE ANCHOR** — your approved wording copied verbatim, once, at the end.

The delivered prompt uses four unlabeled paragraphs in **one code block**, not four separate blocks or fragments. For the invocation above, the expected form is:

```text
In anime-style, a close-up from an eye-level angle.

A red ceramic teapot sits centered on a pale oak table beside a rain-streaked window.

A curved handle, short spout, steam rising from the lid, and soft overcast window light.

clean cel shading, muted warm colors, crisp contour lines
```

For multiple requested prompts, each gets a short title and its own complete code block. A controlled revision returns the complete revised prompt, preserving other wording when practical.



## Chat setup — ChatGPT Project first, custom GPT or Gem equivalent

Follow the shared [chat setup guide](../../CHAT_SETUP.md). Prefer **one skill per ChatGPT Project or Gem** (and per custom GPT where its editor is available): different skills reuse `SKILL.md`, so mixing them creates ambiguous file names and methods.

### Original files to upload

Download these actual original files from this folder and upload their complete contents as Project files, custom GPT Knowledge, or Gem Knowledge. Do not replace them with this README, a summary or the short routing block.

- [SKILL.md](SKILL.md) — Required: complete prompting and controlled-revision method.
- [templates/prompt-template.txt](templates/prompt-template.txt) — Required: original four-part prompt template; uploaded filename may appear as prompt-template.txt.

Folder paths identify the originals; an upload UI may show only their basenames. Keep that mapping clear. **GitHub links alone are not uploaded context or live synchronization.** Refresh your uploaded copies yourself whenever the source changes; no automatic synchronization is provided.

### Copy-ready routing instructions

Paste only this short block into **ChatGPT Project instructions** (primary), **custom GPT Instructions** (secondary, if available), or **Gem instructions**. The original files above remain the method, not this routing text.

```text
Use the uploaded midjourney-prompts-v2 method for concise Midjourney image-prompt writing and scoped revisions.
Read SKILL.md and prompt-template.txt in full before drafting. Preserve the exact approved style anchor and the method's output contract. Do not route video prompting or image generation here.
If a required file is missing or cannot be read completely, stop and ask for
it; do not substitute a summary or invent the method. Preserve the originals
and the user's approved baseline. Do not rewrite or optimize the method, mix
in another skill, or run image/video generation jobs.
```

This setup is for text work, not rendering. If you supply image references, use a chat/model that can actually inspect them; a filename or GitHub link is not proof that it has seen the image. Exact character counts, when required by the method, need an actual counting tool; do not label an estimate as verified.

