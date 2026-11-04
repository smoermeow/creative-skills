# Creative Skills

Creative prompting, character design, storyboarding, image/video generation utilities and media preparation by **smoermeow / MORDERKAI**.

Browse by category, open a skill's README, and use the complete skill folder with a compatible agent. Each skill has its own instructions and supporting files; its README explains how to use it and what it produces. Prompt-writing skills produce prompts. Generation and media utilities have their own documented tool, account and runtime requirements.

## Copy this into your agent

Example: install Seedance Prompter V4. Every skill README has its own ready-to-copy message.

```text
Install the complete Seedance Prompter V4 skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/seedance/seedance-prompter-v4
```

## Choose your agent or chat setup

These skills can be used with **Claude, Codex, Hermes, or other agents that can read the complete files and follow the method**. The Creative Orchestrator is optional, not an installation prerequisite. Each skill README now has a copy-paste prompt to download/install that complete skill and a separate prompt to register it in an **existing** protected setup without replacing its methods or orchestration.

- **Text methods are portable:** Midjourney Prompts V2, Anime Character Design Lab, both Seedance prompters, and Storyboard can supply their original method/context to a suitable agent. For upload-based chat, start with [CHAT_SETUP.md](CHAT_SETUP.md): ChatGPT Projects first, with custom GPT and Gemini Gem equivalents. Each text skill lists and links the actual original files to upload, plus short routing instructions. Storyboard additionally needs Python validation and actual file output for a completed result; chat drafting alone is not completion.
- **Execution wrappers retain their documented integrations:** Krea generation uses the documented Hermes/Krea MCP connection; Dreamina uses its authenticated CLI; continuation-frame processing uses its local Python/FFmpeg environment. The Codex Image wrapper still requires a compatible **Hermes source checkout and Codex image plugin**, its Python dependencies and profile OAuth. Switching the host agent to Claude or Codex does not remove those dependencies. A text-only chat cannot execute these wrappers merely because their files were uploaded.

Use the agent's supported installation location; do not assume every agent uses the same paths or that every installer can download one GitHub folder. GitHub's **Code → Download ZIP** remains a whole-repository download. Copy a complete chosen skill folder from it, preserving supporting files and relative paths. There are no stored per-skill ZIP packages or synchronized chat copies here.


## Browse the skills

- **[Image](image/README.md)**: Midjourney prompting, anime character design, Krea image generation and Codex image execution.
- **[Video](video/README.md)**: Seedance Prompter V4, Seedance Narrative Prompter and Dreamina video execution.
- **[Media](media/README.md)**: continuation-tail and source-frame preparation.
- **[Scripting and storyboarding](scripting/README.md)**: storyboard JSON from ideas or scene blueprints.
- **[Editing](editing/README.md)**: reserved for future additions; no editing skill is included yet.
- **[Optional orchestration](orchestration/README.md)**: connect the library to the existing `hermes-immutable-techniques` architecture if you want that routing/protection setup.

## Get the files

Use GitHub's **Code → Download ZIP** to download this repository, or clone it. The repository download contains the collection; choose the skill folders you want to use. Keep each chosen folder's supporting files together.

There are no separately maintained per-skill ZIPs in this repository. Each skill's files are maintained in its category folder here.

## Use a skill

1. Open the selected skill's README for its purpose, required files, inputs, examples and expected outputs.
2. Give your agent access to the complete skill folder. Ask it to read `SKILL.md` and every supporting file that the skill requires, in full.
3. Supply your idea, script, references or source media, plus your creative direction and any constraints. Identify the role of each reference image.
4. Follow that skill's output and review workflow. Tool-execution skills require the user's own documented setup and approval for paid work.

The library does not require a project walkthrough or the Creative Orchestrator. Agents differ in file access, image analysis and execution capabilities; use each skill's documented requirements. An installation path is useful only when the agent can actually access it.

## Preserve the methods

Each skill's full method and knowledge files are included. Repository organization and installation-path examples do not shorten, blend or optimise those methods. A narrowly requested change should preserve everything outside its scope.

## Reuse and credit

**Skills and prompting methods:** Free to use and adapt. Please give credit where due.

**Renders and edited videos:** Please ask permission before re-uploading or republishing my media. Sharing links or using the platform’s repost function on my original posts is welcome.
