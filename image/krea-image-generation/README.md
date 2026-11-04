# Krea Image Generation

Version **0.3.0** · Prepare image requests and, after approval, generate through Krea's official MCP.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Krea Image Generation skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/krea-image-generation
```

### If you already use a protected orchestrator

```text
Install the complete Krea Image Generation skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/image/krea-image-generation

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Purpose

Turn an image brief into a model-specific, locally validated request; optionally apply your own reference images, moodboards, or styles; and submit an approved image job. This package supports image work only—not video, enhancement, 3D, or node-app execution.

Drafting is not generation. Asking for options, a draft, or an integration test does not authorize an upload or a paid request.

## Setup and prerequisites

- For execution, use Hermes with **Krea's official remote MCP connected and OAuth-authenticated in the selected profile**, plus your own Krea account with access and sufficient generation capacity. Krea is an external MCP, not a built-in Hermes image toolset.
- Follow the setup section of [SKILL.md](SKILL.md) and the [MCP call contracts](references/mcp-calls.md). This README does not duplicate installation commands whose host support may change. The bundled setup instructions are documentation, not proof that your local connection works.
- Read the selected model's capability reference and template before preparing a request. Offline drafting can use those files without calling Krea; execution requires the connection above.
- Supply assets you own or are authorized to use. The package contains no images, credentials, or usable account presets. Its [preferred-assets shortlist](references/preferred-krea-assets.yaml) is intentionally empty.

**Capability snapshot:** the bundled model references say they were last verified on **July 17, 2026**. They are not a live catalogue or a claim that today's APIs were tested. Normal requests use this snapshot; follow the [targeted repair procedure](references/update-procedure.md) if Krea rejects a documented model or field, or if you explicitly request a refresh.

## Required files

Keep [SKILL.md](SKILL.md), [MCP call contracts](references/mcp-calls.md), [preferred assets](references/preferred-krea-assets.yaml), and the selected model's reference/template together:

| Model in this package's snapshot | Compact MCP ID | Reference | Template |
|---|---|---|---|
| Krea 2 Large | `krea/krea-2/large` | [Krea 2](references/krea-2-models.md) | [YAML](templates/krea-2.yaml) |
| Krea 2 Medium | `krea/krea-2/medium` | [Krea 2](references/krea-2-models.md) | [YAML](templates/krea-2.yaml) |
| Krea 2 Medium Turbo | `krea/krea-2/medium-turbo` | [Krea 2](references/krea-2-models.md) | [YAML](templates/krea-2.yaml) |
| GPT Image 2 | `openai/gpt-image-2` | [GPT Image 2](references/gpt-image-2.md) | [YAML](templates/gpt-image-2.yaml) |
| Nano Banana Pro | `google/nano-banana-pro` | [Nano Banana Pro](references/nano-banana-pro.md) | [YAML](templates/nano-banana-pro.yaml) |
| Nano Banana 2 | `google/nano-banana-2` | [Nano Banana 2](references/nano-banana-2.md) | [YAML](templates/nano-banana-2.yaml) |

Only the selected model's reference and template need loading for an ordinary request. Keep [update-procedure.md](references/update-procedure.md) for repair and maintenance.

## Inputs

Supply the model, exact prompt, aspect ratio, resolution, and any model-supported controls. Specify whether you want a draft or actual generation. Prompts are preserved unless you request rewriting.

For references, identify their role and supply a public URL, data URI, existing Krea asset URL, or local file. Local files and attachments require an approved upload first. Use one array entry per reference, not a comma-separated string.

If you want a moodboard or style, select assets from **your own account** and respect model compatibility. The preferred-assets file is a shortlist, not the media itself. Historical account IDs in the knowledge files are examples, not portable presets; do not copy them into a request. Do not modify the shortlist without approval.

## Copy-ready invocation example

This starts a **draft-only** request with no references or account assets:

```text
Use krea-image-generation. Read SKILL.md, references/krea-2-models.md, and templates/krea-2.yaml from this package.

Draft and locally validate one request for krea/krea-2/medium-turbo.
Exact prompt: A red ceramic teapot on a pale oak table beside a rain-streaked window.
Settings: aspect_ratio 16:9, resolution 1K, creativity raw, intensity 0, complexity 0, movement 0, sync false.
No source images, style images, moodboards, or Krea styles/LoRAs.

Return the complete model/input/sync payload and validation notes. Do not rewrite the prompt, upload anything, or generate. Ask for explicit generation approval before submitting one job. If I later supply a local reference, request upload approval before uploading it, then show the revised payload for generation approval. Do not retry a paid request automatically.
```

The corresponding draft payload is:

```json
{
  "model": "krea/krea-2/medium-turbo",
  "input": {
    "prompt": "A red ceramic teapot on a pale oak table beside a rain-streaked window.",
    "aspect_ratio": "16:9",
    "resolution": "1K",
    "creativity": "raw",
    "intensity": 0,
    "complexity": 0,
    "movement": 0
  },
  "sync": false
}
```

## Expected output

A draft returns a clean request using only supported fields, with blank optional fields and empty arrays omitted. No remote job exists at this stage.

After explicit approval, the assistant submits one async `generate_image` request and retains the job ID. The host's job widget normally handles polling; text status checks use `get_job` when requested or when no widget exists. Completed media is delivered once. Failure is reported, not silently resubmitted.

