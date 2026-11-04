---
name: codex-image
description: Call Codex image generation with ordered local references.
version: 1.1.0
metadata:
  hermes:
    tags: [codex, image-generation, reference-images]
---

# Codex Image

Run `scripts/generate_codex_image.py` for Codex OAuth image generation. This skill handles execution, attachments, receipts, and native output verification. It does not write creative prompts or prescribe poster, character-sheet, anime, or storyboard designs.

## When to use

Use when the user explicitly requests a Codex / GPT Image generation or rerun. Prompt review, attachments, critique, and loading this skill are not generation approval. Use the requested provider; never silently substitute Codex for Krea or Vidu.

For prompt authorship, use the creative orchestrator's `gpt-image-sheets` route or the user's explicitly named prompt method. A supplied approved prompt needs no prompting skill merely to execute it.

## Prerequisites

- Resolve this installed skill's directory from `skill_view`; use its bundled script, not a historical path or one-off replacement.
- Use a Python environment with the script's Hermes imports and `httpx` available, plus working Codex OAuth for the intended profile.
- The existing adapter depends on a Hermes source/plugin installation configured by its `HERMES_REPO` constant. Check this when installing elsewhere; copying the skill does not install Hermes or copy credentials. See `references/profile-troubleshooting.md`.

## Run

Use `terminal` with the resolved absolute script path:

```bash
python3 <SKILL_DIR>/scripts/generate_codex_image.py \
  --prompt <PROMPT_FILE> \
  --ref 'image 1: Character identity=/absolute/path/character.png' \
  --ref 'image 2: Environment=/absolute/path/environment.png' \
  --model gpt-image-2-medium \
  --size <REQUESTED_WIDTH>x<REQUESTED_HEIGHT> \
  --out-dir <OUTPUT_DIR> \
  --cache-dir '' \
  --name <UNIQUE_NAME>
```

Omit `--ref` for text-only runs. Use one attachment mode per call: explicit `--ref`, `--refs-json`, or `--refs-from-prompt`. Read `references/reference-inputs.md` for syntax and precedence. The example disables the adapter's installation-specific default reference cache; set an explicit writable cache directory if wanted.

## Execution rules

1. Read the exact requested prompt. Preserve its content, model, size, and ordered references except for changes the user requested. Default quality is medium; low requires explicit permission and `--allow-low`.
2. Verify all inputs exist and choose a writable output directory. Inspect project contracts only when writing into that project. Use `references/studio-integration.md` only for a Studio project.
3. Execute once. Independent multiple outputs may run concurrently when requested, with distinct names/directories. A retry, prompt variant, additional output, or backend change needs authorization; never rewrite a rejected prompt automatically.
4. Verify every returned native file and receipt using `references/output-and-stream-verification.md`. Metadata `size` is the requested size, not proof of actual dimensions.
5. Deliver each image once with its existing path, actual dimensions, and `MEDIA:<absolute-path>`. Report failures honestly. Do not automatically analyze image content or crop, pad, resize, or transform outputs.

## Reference index

- `references/reference-inputs.md`: attachment syntax, exact order, parser limitations, missing files, and reference removal.
- `references/output-and-stream-verification.md`: native dimensions, quality aliases, stream failures, partial results, and parallel outputs.
- `references/profile-troubleshooting.md`: installation portability, profile/auth attribution, cached skill paths, and conservative diagnosis.
- `references/studio-integration.md`: project-only staging, separate variants, native-source retention, and moved prompt paths.

Only open the references needed for the current execution. Do not append project prompt formats or session histories to this skill.
