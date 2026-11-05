# Seedance Prompter V4

## Purpose

Write structured cinematic Seedance 2.0 prompts from a scene brief. The package gives an assistant a bracketed prompt format, character and setting modeling, timestamped choreography, reference-image discipline, camera rules, lighting guidance, and production notes. It produces text; it does not render video, upload references, or submit generation jobs.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Seedance Prompter V4 skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/seedance/seedance-prompter-v4
```

### If you already use a protected orchestrator

```text
Install the complete Seedance Prompter V4 skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/seedance/seedance-prompter-v4

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Giving creative direction

When you supply reference images, the prompter analyses them and uses its knowledge base of cinematic and anime-related techniques and examples to develop a prompt from your direction. You can start with a loose idea and let it contribute action, acting and camera coverage. You do not need to plan every shot or write a technical specification.

If you have a particular vision, describe the qualities you are imagining: the mood, emotional contrasts, pace, humour, tension or visual energy. Words such as “awkward and teasing,” “fast and intense with a comical edge,” or “quiet at first, then suddenly explosive” give its creative work a direction. More of that context helps it align with your vision; an open brief is still a valid way to begin.

You can be precise about some aspects and leave others open. A detailed script might keep the story and dialogue fixed while inviting new camera coverage and acting. If you want the script reinterpreted more freely, say which parts may change and what you want that reinterpretation to achieve.

## Prerequisites and setup

Download or copy the **complete `seedance-prompter-v4` folder**, including `references/`. An AI assistant with local-file reading is sufficient: tell it which files to read and give it your brief. If you provide reference images, it must also be able to inspect them. There is no package-specific installer, CLI, Python dependency, or API-key requirement for prompt writing.

Start with `SKILL.md`, then read `instructions.md` and `seedance-prompter-v4-master-knowledge.md` **in full**. Read `references/platform-character-limits.md` when selecting a platform-specific limit. The `SKILL.md` file is only the publication wrapper; the instructions and master knowledge contain the actual prompting method. This README explains usage without replacing those files.

This package's default target is **under 5,000 characters, including spaces**.

## Required files

| File | Role |
| --- | --- |
| `SKILL.md` | Agent entry-point wrapper and loading instructions. |
| `instructions.md` | Behavior, delivery format, reference rules, and prompt skeleton. |
| `seedance-prompter-v4-master-knowledge.md` | Field guidance, camera and action discipline, pacing, examples, and continuity rules. |
| `references/platform-character-limits.md` | Bundled defaults and platform-specific prompt-length limits. |

Keep the complete folder and relative paths intact.

## Inputs

- **A scene brief:** subjects, environment, concrete actions, emotional intent, and ending state.
- **Duration in seconds:** required. If absent, the assistant asks, “How long is this clip?” before drafting.
- **Style and constraints:** genre, animation language, materials, mood, camera limits, and anything that must or must not happen.
- **Optional image references in order:** provide accessible images and identify their roles. Tags are `@image1`, `@image2`, etc., without spaces. For direct video continuation, provide the actual video reference (`@video1`) and the scene state to preserve.
- **Optional dialogue and audio direction:** supply exact lines, speaker attribution, language, sound cues, or silence/no-music requirements.
- **Optional platform or explicit character limit:** an explicit user limit overrides the bundled platform value. The reference counts the complete prompt, including spaces but excluding code fences. An unlisted platform falls back to the 5,000-character default, not a claimed verified platform maximum.

The limit table is part of this snapshot, not a live service-capability check. In particular, its Dreamina and Dreamina CLI entries are separate; name the intended target precisely.

## Two ways to start

These are reusable starting requests. Attach your images and, for the second example, your script sections and dialogue. Replace the character labels and material with your own. Use a duration supported by the service you will render with.

### References and a conversational idea

Use this approach when you have reference images, a loose event sequence and a clear mood or style you want the prompter to develop.

```text
Use Seedance Prompter V4 from this package to create a prompt for a
25-second retro-anime video.

Image 1 is Character B.
Image 2 is Character C.
Image 3 is the environment.

Character B walks through the location. Character C enters, and the sequence
ends with both of them exploding.

Use multiple cuts, fast pacing, diverse camera angles, insert shots and
foreshortened perspectives. Make it intense with a comical edge.
Develop the physical action, coverage and comic timing around this idea.
Write the prompt only; do not generate a video.
```

The direction gives the prompter something to develop without specifying every shot. You can also begin more loosely and explore what it proposes.

### References and a developed script

This example starts with a script divided into sections, four reference images and dialogue that must remain unchanged.

```text
Use Seedance Prompter V4 from this package to create three prompts from
the supplied script sections, using the durations and Japanese dialogue
provided with them.

Image 1 is Malfoid.
Image 2 is Male 1 / Harry.
Image 3 is Foideldore.
Image 4 is the office.

Create a retro-anime drama sequence focused on Japanese anime acting,
emotional arcs and character personality.

You may optimise camera language, continuity and pacing. Preserve the
narrative and use the supplied Japanese dialogue exactly. Raise important
narrative changes before making them.

Shot 16 is locked: the slow zoom and turn are essential. Do not reveal
that Foideldore is a woman before the turn.

Preserve the contrast between irritation, attraction, embarrassment and
anger. Do not make the whole sequence understated; restraint can serve a
particular beat, such as Foideldore's stillness before the outburst.
Write the prompts only; do not generate videos.
```

Here the script supplies more detail, and the request identifies the creative work still wanted. If you instead want the prompter to rethink the coverage or the scene itself, change those permissions explicitly rather than expecting it to infer them from a detailed script.

## Expected output

The assistant returns, in order:

1. A **single `text` code block** with only the copyable final prompt.
2. A **plain-language scene breakdown** showing how the clip plays out.
3. **Exactly four short creative suggestions**, numbered 1–4.

The prompt uses `[TITLE]`, `[REFERENCES]`, `[STYLE]`, `[VISUAL FEEL]`, `[DURATION]`, `[CHARACTERS]`, optional `[SETTING]`, `[SHOT SEQUENCE]`, and `[PRODUCTION NOTES]`. `[REFERENCES]` immediately follows `[TITLE]`. Only for a supplied continuation video, prepend `[PROMPT START]` containing `Continue from @video1.` before the title.

Characters and active props are described before the timeline. Timestamp ranges cover the full requested duration without gaps, each with `Camera:`, `Action:`, and `Lighting:`. Production notes include `Avoid:`. The normal deliverable is prompt text, not JSON, an automatically saved file, or rendered media.


## Reviewing the result

The scene breakdown is the readable summary of what the clip will show. Both prompters are designed to provide this summary and four creative suggestions alongside the long prompt. Ideally, you review the summary and suggestions to judge the direction without having to read the full generation prompt line by line.

That is the intended workflow, not a promise that every result is correct. If the summary or generated result misses something, ask for that point to be checked in the prompt. The suggestions are options for you to choose, not changes you have to accept.

## Common user pitfalls

- **Leaving reference roles ambiguous.** File names and your description may let the assistant infer what each image shows, but an explicit mapping is clearer: “Image 1 is Character B; Image 2 is Character C; Image 3 is the environment.” State any additional role that matters to your request.
- **Providing a detailed script while expecting an unstated reinterpretation.** Tell the prompter what it may develop or rethink and what must stay. Otherwise, it may follow the supplied direction more closely than you intended.
- **Keeping a specific vision to yourself.** A vague brief can produce an interesting result, but the prompter has more to decide. If you already imagine a particular mood, energy or performance, describe it in ordinary language.
- **Requesting a revision without identifying the approved version.** Supply the prompt you want revised, name the change and say what you want to keep. This helps distinguish a focused adjustment from a request for a new interpretation.
- **Expecting prompt writing to resolve a generation-service refusal.** The video service applies its own restrictions and may refuse character references that another service generated. Creating your own interpretations can be a more workable starting point than copying canon designs directly.
- **Leaving the intended sound unclear.** If you want dialogue, ambience and sound effects but no music, say so. “No music” and “silent video” describe different results.


## Development and contributions

This skill is under ongoing development. I update it when I make a new version or find approaches that work better in practice. Suggestions, forks and ideas for improvements are welcome.



## Chat setup — ChatGPT Project first, custom GPT or Gem equivalent

Follow the shared [chat setup guide](../../../CHAT_SETUP.md). Prefer **one skill per ChatGPT Project or Gem** (and per custom GPT where its editor is available): different skills reuse `SKILL.md`, so mixing them creates ambiguous file names and methods.

### Original files to upload

Download these actual original files from this folder and upload their complete contents as Project files, custom GPT Knowledge, or Gem Knowledge. Do not replace them with this README, a summary or the short routing block.

- [SKILL.md](SKILL.md) — Required: entry-point loader, not the full method.
- [instructions.md](instructions.md) — Required: complete behavior, structure and delivery contract.
- [seedance-prompter-v4-master-knowledge.md](seedance-prompter-v4-master-knowledge.md) — Required: full master knowledge, including its original examples.
- [references/platform-character-limits.md](references/platform-character-limits.md) — Upload as well for platform-specific limits; uploaded filename may appear as platform-character-limits.md. Its bundled values are a snapshot, not live service verification.

Folder paths identify the originals; an upload UI may show only their basenames. Keep that mapping clear. **GitHub links alone are not uploaded context or live synchronization.** Refresh your uploaded copies yourself whenever the source changes; no automatic synchronization is provided.

### Copy-ready routing instructions

[Project instruction file](../../../chatgpt-projects/seedance-prompter-v4.txt) · [Files to upload and setup](../../../chatgpt-projects/README.md#seedance-prompter-v4)

Paste only this short block into **ChatGPT Project instructions** (primary), **custom GPT Instructions** (secondary, if available), or **Gem instructions**. The original files above remain the method, not this routing text.

```text
Use the uploaded Seedance Prompter V4 method.

Before answering each request, read these uploaded files in full:
- SKILL.md
- instructions.md
- seedance-prompter-v4-master-knowledge.md
- platform-character-limits.md

Follow their method and output requirements. Do not rewrite the method or combine it with another prompting system.

If a required file is missing or cannot be read fully, ask for it before proceeding.
```

This setup is for text work, not rendering. If you supply image references, use a chat/model that can actually inspect them; a filename or GitHub link is not proof that it has seen the image. Exact character counts, when required by the method, need an actual counting tool; do not label an estimate as verified.

