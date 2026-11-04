# Seedance Narrative Prompter

Write a timed, reference-aware Seedance video prompt as connected cinematic prose. Each passage can contain several cuts belonging to one dramatic beat, with camera, acting, dialogue, sound and visible changes tied to their place in the sequence.

This is a **prompt-writing skill**. It does not upload inputs or generate a video.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Seedance Narrative Prompter skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/seedance/seedance-narrative-prompter-v1
```

### If you already use a protected orchestrator

```text
Install the complete Seedance Narrative Prompter skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/seedance/seedance-narrative-prompter-v1

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Giving creative direction

When you supply reference images, the prompter analyses them and uses its knowledge base of cinematic and anime-related techniques and examples to develop a prompt from your direction. You can start with a loose idea and let it contribute action, acting and camera coverage. You do not need to plan every shot or write a technical specification.

If you have a particular vision, describe the qualities you are imagining: the mood, emotional contrasts, pace, humour, tension or visual energy. Words such as “awkward and teasing,” “fast and intense with a comical edge,” or “quiet at first, then suddenly explosive” give its creative work a direction. More of that context helps it align with your vision; an open brief is still a valid way to begin.

You can be precise about some aspects and leave others open. A detailed script might keep the story and dialogue fixed while inviting new camera coverage and acting. If you want the script reinterpreted more freely, say which parts may change and what you want that reinterpretation to achieve.

## Setup

Keep this complete folder together. Give an agent access to [SKILL.md](SKILL.md) and the required [knowledge file](references/knowledge.md), and explicitly ask it to read both in full. An agent with filesystem access can read the folder directly; otherwise supply both files through its supported document interface. A local path alone is insufficient if the agent cannot access that filesystem.

For a skill-aware agent, install the complete folder using that agent's supported skill installation procedure. No external creative router is required to read this standalone package.

No Python packages or provider credentials are needed for prompt writing. Image understanding is required when supplying image references. Actual video generation needs separate provider access and authorization.

## Required files

- `SKILL.md`: behavior, structure, reference handling and delivery contract.
- `references/knowledge.md`: full timing, cinematic and narrative guidance. Required before creating or revising a prompt.

## Inputs

Supply the intended action or script, exact clip duration, style and performance direction, and ordered references with their roles. Identify any exact dialogue, reveal timing, geography or character state that must remain unchanged. Say which aspects the agent may develop and what that development should accomplish.

Specify the target platform or an explicit character limit. The package contains platform-specific limits and uses a 4,500-character default including spaces; these are snapshot rules, not a guarantee about every provider's current interface.

If you do not want music, request **no music** explicitly while retaining the dialogue, ambience and sound effects you do want. Provide audio/video according to their intended role; content analysis of those media is a separate request in this skill.

## Two ways to start

These are reusable starting requests. Attach your images and, for the second example, your script sections and dialogue. Replace the character labels and material with your own. Use a duration supported by the service you will render with.

### References and a conversational idea

Use this approach when you have reference images, a loose event sequence and a clear mood or style you want the prompter to develop.

```text
Use Seedance Narrative Prompter from this package to create a prompt for a
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
Use Seedance Narrative Prompter from this package to create three prompts from
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

1. One `text` code block containing only the finished prompt.
2. A concise scene breakdown.
3. The exact character count, including spaces and excluding code fences, with the applicable limit.
4. Exactly four short creative suggestions, numbered 1–4.

The prompt starts with `[REFERENCES]`, establishes visual style, duration, characters and setting, then covers the full clip through chronological timed passages. It ends with `[FINAL VISUAL STYLE]` and `Avoid:`. `[AUDIO]` is included when relevant. Within the package's Seedance 2.5 syntax, `()` marks music/no-music, `<>` sound, `{}` spoken dialogue and `【】` subtitles; surrounding prose controls timing and delivery.

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

## Revisions

- Name the approved baseline and the exact passages to change. A revision request does not authorize a different story.


## Development and contributions

This skill is under ongoing development. I update it when I make a new version or find approaches that work better in practice. Suggestions, forks and ideas for improvements are welcome.



## Chat setup — ChatGPT Project first, custom GPT or Gem equivalent

Follow the shared [chat setup guide](../../../CHAT_SETUP.md). Prefer **one skill per ChatGPT Project or Gem** (and per custom GPT where its editor is available): different skills reuse `SKILL.md`, so mixing them creates ambiguous file names and methods.

### Original files to upload

Download these actual original files from this folder and upload their complete contents as Project files, custom GPT Knowledge, or Gem Knowledge. Do not replace them with this README, a summary or the short routing block.

- [SKILL.md](SKILL.md) — Required: full behavior, structure and delivery contract.
- [references/knowledge.md](references/knowledge.md) — Required: full cinematic, timing and narrative knowledge; uploaded filename may appear as knowledge.md.

Folder paths identify the originals; an upload UI may show only their basenames. Keep that mapping clear. **GitHub links alone are not uploaded context or live synchronization.** Refresh your uploaded copies yourself whenever the source changes; no automatic synchronization is provided.

### Copy-ready routing instructions

Paste only this short block into **ChatGPT Project instructions** (primary), **custom GPT Instructions** (secondary, if available), or **Gem instructions**. The original files above remain the method, not this routing text.

```text
Use the uploaded seedance-narrative-prompter-v1 method for timed narrative Seedance video-prompt writing, not video generation.
Read SKILL.md and knowledge.md in full before creating or revising a prompt. Keep the original connected-prose format, timing/reference discipline and delivery contract; do not blend it with V4.
If a required file is missing or cannot be read completely, stop and ask for
it; do not substitute a summary or invent the method. Preserve the originals
and the user's approved baseline. Do not rewrite or optimize the method, mix
in another skill, or run image/video generation jobs.
```

This setup is for text work, not rendering. If you supply image references, use a chat/model that can actually inspect them; a filename or GitHub link is not proof that it has seen the image. Exact character counts, when required by the method, need an actual counting tool; do not label an estimate as verified.

