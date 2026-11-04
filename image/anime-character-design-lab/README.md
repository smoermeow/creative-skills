# Anime Character Design Lab

Version **0.1.0** · Character design and prompt writing, not image generation.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Anime Character Design Lab skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/anime-character-design-lab
```

### If you already use a protected orchestrator

```text
Install the complete Anime Character Design Lab skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/anime-character-design-lab

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Purpose

Develop anime- and manga-inspired characters through concrete visual decisions: silhouette, body and facial geometry, garment construction, materials, emotional posture, and one memorable design hook. Style is treated as visual grammar, not an artist name pasted onto a generic character.

Use the skill at the stage your design actually needs. It does not automatically turn a loose idea into a finished character sheet or render an image.

## Setup and prerequisites

- Use an assistant that can read the packaged Markdown files and follow their instructions. Image-reference analysis also requires image-reading support.
- Keep the package files together. Have the assistant read [SKILL.md](SKILL.md) and the [required design logic sheet](ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md) before designing; consult the relevant full style profile rather than only the short roster.
- No image-service account, rendering API, or generation CLI is needed for text-only design work.

## Required files

| File | Role |
|---|---|
| [SKILL.md](SKILL.md) | Modes, output contracts, consistency fields, and prompting rules. |
| [ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md](ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md) | Required design method, style profiles, specificity, divergence, and refinement logic. |
| [modern-anime-styles.md](modern-anime-styles.md) | Supplementary working material for newer production-style anchors; not a replacement for the required logic sheet. |

There is no required project tracker or starter character image. A text brief is enough to begin.

## Inputs

Provide a concept, the design stage, and any constraints. Useful details include role, world, age, species, emotional pressure, materials, a signature feature, and traits that must remain unchanged. You can supply an existing design or one or more images instead of starting from text.

Choose a mode explicitly, or let the assistant infer it:

| Mode | Use it for | Expected response |
|---|---|---|
| `ideate` | A loose role, concept, or emotional direction. | 3–4 distinct directions, each with a concept label, role, premise, silhouette, emotional read, hook, materials, and social signal. |
| `expand` | One promising direction. | Deeper body/face logic, garment architecture, materials, social read, and signature element. |
| `differentiate` | Options that feel too similar or generic. | Diagnosis and materially different silhouette, history, costume, emotion, or motif choices. |
| `refine` | Improving a selected design. | Focused changes to weak layers while preserving the successful core. |
| `analyze` | An existing character, image, or written reference. | Reusable silhouette, geometry, garment, material, motif, and relevant effect logic. |
| `translate` | A resolved design ready for documentation. | Prompt-ready descriptions, visual cue strings, sheet prompts, outfit breakdowns, or structured JSON as requested. |

Name one style anchor if you want one. If none is specified, the assistant chooses suitable visual logic and explains the construction. Hybrid styles require an explicit request.

## Copy-ready invocation example

Paste this into your assistant with the package accessible:

```text
Read SKILL.md and ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md from the anime-character-design-lab package. Use ideate mode.

Design an original 46-year-old human woman who repairs flood-warning bells in a coastal town. She is practical, impatient with ceremony, and visibly protective of her apprentices. Her clothing must show salt exposure and repeated repairs. Give her one dominant occupational design hook.

Use the Hayao Miyazaki / Studio Ghibli profile's visual grammar from the logic sheet, without borrowing a canon character. Return 3 distinct directions with concept label, role, design premise, silhouette, emotional read, hook, material language, and social signal. Do not produce a full consistency schema, sheet prompt, or image yet.
```

## Expected output

Early requests produce design choices rather than full schemas. Refinement preserves your chosen identity. Translation produces the requested reusable text; prompts, visual cue strings, sheet-ready text, and JSON appear in code blocks for copying.

For a resolved consistency description, [SKILL.md](SKILL.md) requires identity/world/background; role and personality; baseline and current emotion; age and apparent age; gender and presentation; race/species/ancestry and skin tone; body and face geometry; eye color and shape; hair color and style; main outfit, layering, legwear and footwear; accessories; `visualAura`; and a compact Visual Cue String. Relevant aura descriptions specify color, behavior, body placement, and environmental interaction.

A character-sheet **prompt** is text, not a rendered sheet. The optional dashboard-facing folder convention in SKILL.md describes a complete saved character state; this text-only skill does not itself create the required `sheet.png`.



## Chat setup — ChatGPT Project first, custom GPT or Gem equivalent

Follow the shared [chat setup guide](../../CHAT_SETUP.md). Prefer **one skill per ChatGPT Project or Gem** (and per custom GPT where its editor is available): different skills reuse `SKILL.md`, so mixing them creates ambiguous file names and methods.

### Original files to upload

Download these actual original files from this folder and upload their complete contents as Project files, custom GPT Knowledge, or Gem Knowledge. Do not replace them with this README, a summary or the short routing block.

- [SKILL.md](SKILL.md) — Required: modes, behavior and delivery contracts.
- [ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md](ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md) — Required: complete design logic and full style profiles.
- [modern-anime-styles.md](modern-anime-styles.md) — Supplementary: upload too if using the newer production-style working material; it does not replace the required logic sheet.

Folder paths identify the originals; an upload UI may show only their basenames. Keep that mapping clear. **GitHub links alone are not uploaded context or live synchronization.** Refresh your uploaded copies yourself whenever the source changes; no automatic synchronization is provided.

### Copy-ready routing instructions

Paste only this short block into **ChatGPT Project instructions** (primary), **custom GPT Instructions** (secondary, if available), or **Gem instructions**. The original files above remain the method, not this routing text.

```text
Use the uploaded anime-character-design-lab method for anime character ideation, analysis, refinement and prompt-ready translation.
Read SKILL.md and ANIME_CHARACTER_DESIGN_LOGIC_SHEET.md in full, then use the relevant complete style profile. Consult modern-anime-styles.md when the request calls for its supplementary material. Preserve design-stage routing and locked style grammar; do not turn every request into a finished sheet.
If a required file is missing or cannot be read completely, stop and ask for
it; do not substitute a summary or invent the method. Preserve the originals
and the user's approved baseline. Do not rewrite or optimize the method, mix
in another skill, or run image/video generation jobs.
```

This setup is for text work, not rendering. If you supply image references, use a chat/model that can actually inspect them; a filename or GitHub link is not proof that it has seen the image. Exact character counts, when required by the method, need an actual counting tool; do not label an estimate as verified.

