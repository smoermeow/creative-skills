# Codex Image 1.1.0

A portable export of the Hermes `codex-image` execution skill. It submits a supplied prompt and optional ordered local image references through the Hermes Codex image plugin, then saves native image bytes and a JSON receipt. It is not a prompt-writing system, a standalone provider SDK, or a credential bundle.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Codex Image skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/codex-image
```

### If you already use a protected orchestrator

```text
Install the complete Codex Image skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/codex-image

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Dependencies and setup

- Use Python 3.10 or newer in an environment with `httpx` and the dependencies required by your Hermes checkout. This export does not install those dependencies or pin a Hermes revision.
- Supply a **Hermes source checkout** containing `plugins/image_gen/openai-codex/__init__.py` and the importable `agent.auxiliary_client` module. A skill folder alone is insufficient. Install that checkout's dependencies using its own documented setup; the script also imports the plugin's private constants and token reader, so compatibility with other Hermes revisions is not guaranteed.
- Set `HERMES_REPO` to the checkout root, not the plugin directory. Without this variable, the exported script uses `~/.hermes/hermes-agent`. The script expands `~` in this checkout setting.
- Configure **your own Codex OAuth** for the intended Hermes profile using current Hermes documentation and your installed CLI's supported authentication flow. Credentials are neither included nor copied by this package. Do not infer an authentication command from an old error message in the script. Check the intended `HERMES_HOME`/profile and its credential state without printing tokens.

Example local environment configuration (replace the checkout path):

```bash
export HERMES_REPO="$HOME/src/hermes-agent"
```

`--help` is a safe parser-only check. It exits before loading the Hermes plugin, reading OAuth, or importing `httpx`; success does **not** verify dependencies, authentication, access, or image generation:

```bash
python3 /path/to/codex-image/scripts/generate_codex_image.py --help
```

## Inputs

`--prompt` is required: provide a prompt text file path or inline prompt text. An existing path is read as UTF-8; a nonexistent path is treated as literal prompt text, so verify file existence first. Shell variables in these examples are expanded by the shell, not the script.

Use **one** optional reference mode:

- Repeated `--ref 'image N: Role=/absolute/path/image.png'`, preserving the intended attachment order.
- `--refs-json /absolute/path/references.json`, with an ordered JSON list such as `[{"label":"image 1: Identity","path":"/absolute/path/identity.png"}]`.
- `--refs-from-prompt`, recognizing blocks like the one below and sorting them by image number:

```text
- image 1: Character identity
  Path: `/absolute/path/identity.png`
```

Omit reference flags for text-only generation. Consult `references/reference-inputs.md` for deduplication, parser limitations, and attachment verification.

Other important options:

| Option | Meaning / default |
| --- | --- |
| `--model` | `gpt-image-2-medium`; also accepts the local `-low` and `-high` quality aliases |
| `--size` | Requested dimensions; default `1024x1024` |
| `--quality` | Fallback quality, default `medium`; the selected model suffix takes precedence |
| `--allow-low` | Required when the resolved quality is low; low also needs explicit user approval |
| `--out-dir` | Explicit output directory; otherwise `codex-image-output` under the invocation's current working directory |
| `--cache-dir` | Default empty string: no reference cache; set an explicit writable directory to enable it |
| `--name` | Filename base; otherwise prompt-file stem or `codex_image` |
| `--timeout` | HTTP read timeout, default 600 seconds; not a total execution-time guarantee |
| `--timestamp` / `--no-timestamp` | Timestamp enabled by default; disabling it can overwrite matching names |

## Invocation example — makes a real provider request

Run the following only after explicit approval for this specific generation and after replacing the paths with existing inputs and a writable output location. Packaging and `--help` do not authorize generation.

```bash
python3 /path/to/codex-image/scripts/generate_codex_image.py \
  --prompt "$PWD/prompt.txt" \
  --ref "image 1: Character identity=$PWD/identity.png" \
  --model gpt-image-2-medium \
  --size 1024x1024 \
  --out-dir "$PWD/codex-image-output" \
  --cache-dir '' \
  --name approved-example
```

For text-only generation, remove the `--ref` line without changing the approved prompt or other settings. Model/provider availability depends on the configured account and compatible Hermes plugin; it was not tested by this export.

## Expected outputs and verification

A successful call saves two files in the output directory:

- `<name>_<model>_<YYYYMMDD_HHMMSS>.png`: returned image bytes, with no local resizing.
- `<name>_<model>_<YYYYMMDD_HHMMSS>_meta.json`: provider, requested model and size, resolved quality, plugin API model, prompt origin, ordered reference labels/paths, and output path.

The timestamp component is omitted with `--no-timestamp`. The script prints stream events followed by `OUTPUT <path>` and `META <path>` when it returns successfully. The receipt is not a copy of the full submitted prompt and does not prove actual dimensions or stream completion.

Inspect each file's actual format/dimensions with an available metadata reader, and compare every receipt reference label/path and quality against the approved request. On macOS, `file <output.png>` and `sips -g pixelWidth -g pixelHeight <output.png>` are examples. Preserve native bytes; do not silently crop, resize, pad, or regenerate to match a requested size. Follow `references/output-and-stream-verification.md` for complete checks.

## Reference and output notes

- Mixing reference modes merges inputs; repeated paths are removed. One file cannot reliably occupy two separate intended attachment slots. Missing references raise an error.
- The adapter submits reference labels **and local paths** in request text and records paths in receipts. Reference caches contain base64 image content and source paths. Review privacy before submission or sharing outputs; keep credentials and personal data out of published bundles.
- Requested dimensions are not proof of actual native dimensions. The model suffix determines quality, so `--quality high` with the default `-medium` model still resolves to medium.
- A stream error after image data can save the latest, potentially partial image.
- Timestamps have second resolution. Different output names or directories prevent simultaneous requests from sharing a filename.

## Included files

`SKILL.md`, four reference documents in `references/`, and `scripts/generate_codex_image.py`.
