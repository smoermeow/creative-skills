---
name: krea-image-generation
description: Use when a Hermes user wants to install Krea's official MCP, configure one of six curated Krea image models, work with moodboards/styles/references, or submit a validated Krea image request. Uses bundled capability references for normal work and live schema calls only for targeted repair or explicit refresh.
version: 0.3.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [Krea, MCP, Hermes, Images, Moodboards, LoRA]
    related_skills: []
---

# Krea Image Generation

## Overview

Use Krea's official remote MCP to prepare and run image requests through Hermes. Normal requests use the bundled, dated capability references and request templates; do not relist models or reload schemas on every call.

This skill is image-only. Do not route video, enhancement, 3D, node-app, or unrelated Krea-hosted model requests through it.

## When to Use

- Install or verify Krea MCP in Hermes.
- Show the curated Krea image menu or model-specific parameters.
- Draft a clean Krea 2, GPT Image 2, Nano Banana Pro, or Nano Banana 2 request.
- Browse or apply account-specific moodboards and Krea styles/LoRAs.
- Validate and submit an image request after explicit approval.
- Repair a cached model reference after Krea rejects a documented request.

## Hermes Setup

```bash
hermes --profile PROFILE mcp add krea \
  --url https://api.krea.ai/mcp \
  --auth oauth
hermes --profile PROFILE mcp login krea
hermes --profile PROFILE mcp test krea
hermes --profile PROFILE mcp list
```

Expected profile configuration:

```yaml
mcp_servers:
  krea:
    url: https://api.krea.ai/mcp
    auth: oauth
    enabled: true
```

Krea is an external MCP, not a native Hermes toolset. Its tools may appear as `generate_image` / `get_job` or host-qualified names such as `mcp__krea__generate_image`.

## Curated Models and References

| Label | MCP model ID | Capability reference | Request template |
|---|---|---|---|
| Krea 2 Large | `krea/krea-2/large` | [Krea 2](references/krea-2-models.md) | [Krea 2 YAML](templates/krea-2.yaml) |
| Krea 2 Medium | `krea/krea-2/medium` | [Krea 2](references/krea-2-models.md) | [Krea 2 YAML](templates/krea-2.yaml) |
| Krea 2 Medium Turbo | `krea/krea-2/medium-turbo` | [Krea 2](references/krea-2-models.md) | [Krea 2 YAML](templates/krea-2.yaml) |
| GPT Image 2 | `openai/gpt-image-2` | [GPT Image 2](references/gpt-image-2.md) | [GPT Image 2 YAML](templates/gpt-image-2.yaml) |
| Nano Banana Pro | `google/nano-banana-pro` | [Nano Banana Pro](references/nano-banana-pro.md) | [Nano Banana Pro YAML](templates/nano-banana-pro.yaml) |
| Nano Banana 2 | `google/nano-banana-2` | [Nano Banana 2](references/nano-banana-2.md) | [Nano Banana 2 YAML](templates/nano-banana-2.yaml) |

Use these compact IDs in the MCP `model` field. API endpoint paths are not MCP model IDs.

The references are the normal source of truth for parameters. The full MCP wrapper, upload, account-list, and job contracts are in [MCP call contracts](references/mcp-calls.md).

## Shared Preferred Krea Assets

All Hermes agents that use this skill share [preferred Krea assets](references/preferred-krea-assets.yaml). It is the user-curated shortlist of existing Krea moodboards, Krea Styles/LoRAs, and image-based style references.

The file stores only names, Krea IDs or asset URLs, default strengths, and model compatibility. The actual moodboards, styles, and media remain in Krea.

When the user asks for a moodboard, Krea Style/LoRA, or reusable style reference:

1. Read the preferred-assets list first.
2. Filter it by the selected model's `supported_models`.
3. Offer the matching preferred entries immediately.
4. Use the saved ID/URL and default strength when the user selects one.
5. Call Krea's full listing tools only if the preferred list is empty for that category, the user asks to browse all Krea items, or a saved item fails.

Users can edit the preferred-assets YAML directly. Do not overwrite it from a live listing without explicit approval.

## Normal Request Flow — No Discovery Calls

For ordinary model help, drafting, validation, and generation:

1. Resolve the user's label to one curated compact model ID.
2. Load only that model's bundled reference and template.
3. If a moodboard, Style/LoRA, or reusable style reference is requested, load the shared preferred-assets list and offer matching entries first.
4. Preserve the user's prompt exactly unless they ask for rewriting.
5. Fill only fields supported by the bundled reference.
6. Omit blank optional fields and empty arrays from the final `input` object.
7. Validate enums, required fields, ranges, and reference limits locally.
8. Ask for explicit approval before uploads or generation.
9. Call `generate_image` with the compact model ID and async mode by default.

Do **not** call `list_models` or `get_model_schema` during this normal flow. Do not call `list_moodboards` or `list_styles` when a suitable preferred entry already exists. The request is ready when it matches the bundled reference, template, and selected preferred asset.

## Full Krea Lists — Only When Needed

### Moodboards

Moodboards are available only for the Krea 2 models in this skill. Allow at most one; strength is `0..1`, default `0.23`.

Call `list_moodboards` only when the preferred list has no matching moodboard, the user asks to browse the full Krea collection, or a selected preferred moodboard fails. Show live names and kinds without dumping descriptions unless asked. Add or replace preferred entries only after explicit approval.

### Styles and LoRAs

Call `list_styles` only when the preferred list has no matching style, the user asks to browse all Krea styles, or a selected preferred style fails. Follow `next_cursor` only when pagination exists, filter entries by the selected model's `supported_models`, and use `{id, strength}` with strength `-2..2`.

`HOST ANIME` (`z7kkrlzk1`) was verified for Krea 2 Medium and Medium Turbo on 2026-07-17, but treat it as an example rather than a guaranteed asset for every account. Never show a style for an unsupported model.

## Reference Inputs

Keep these fields separate:

| Field | Meaning |
|---|---|
| `image_url` | Krea 2 source image |
| `strength` | Krea 2 denoising strength for the source image |
| `image_style_references` | Krea 2 style-image URLs and strengths |
| `styles` | Krea style/LoRA IDs and strengths |
| `moodboards` | One Krea moodboard UUID and optional strength |
| `image_urls` | GPT/Nano source or editing images |
| `style_images` | GPT/Nano style-image objects |

For public URLs, data URIs, or Krea asset URLs, use one array item per reference. Comma-separated URL strings are invalid.

For a local file or Hermes attachment, call `get_upload_url`, then upload multipart field `file`. Uploads write to the Krea account and require explicit approval. Reuse an existing Krea asset URL when possible.

For Nano Banana Pro and Nano Banana 2, populated `image_urls` causes `style_images` to be ignored.

## Generation and Jobs

The exact generic wrapper is:

```json
{
  "model": "<curated compact ID>",
  "input": {
    "<model-specific field>": "<value>"
  },
  "sync": false
}
```

`sync` defaults to false. `timeoutSeconds` is only relevant when `sync` is true and accepts 1–300 seconds.

Prefer async mode. When the host renders the Krea job widget, let it poll automatically. Call `get_job` only when the user requests a text status update or the host has no widget. Deliver completed media once.

No curated schema exposes output count, and Krea MCP exposes no cost estimator. Do not offer batch count or invent prices.

## Targeted Repair and Updates

Live model/schema discovery is a fallback, not routine work. Use [Updating cached Krea references](references/update-procedure.md) only when:

- Krea rejects a documented field or value;
- the compact model ID becomes unsupported;
- the response indicates schema drift;
- the user explicitly requests a capability refresh.

If one model fails, call `get_model_schema` for that model only. Use `list_models` only when a model ID is rejected or during an explicitly requested full curated audit.

For the current request, explain the live correction. Do not automatically retry paid generation. Before editing shared references/templates, report the drift and obtain explicit approval.

## Controlled Variants

When the user is exploring Krea 2 behavior, offer variants that change only one or two fields. Do not claim one is better without empirical evidence.

```yaml
variant_a:
  creativity: raw
  intensity: 0
  complexity: 0
  movement: 0
variant_b:
  creativity: medium
  intensity: 0
  complexity: 0
  movement: 0
variant_c:
  creativity: medium
  intensity: 0
  complexity: 40
  movement: 0
```

Variants are preparation, not authorization to generate.

## Safety Gates

- Model/reference help and local validation are read-only.
- `list_moodboards`, `list_styles`, `list_models`, `get_model_schema`, and `get_job` are read-only.
- Uploads and generation are external writes.
- A request for options, a draft, or “test it” does not authorize upload or generation.
- Submit one job only after explicit approval.
- Do not automatically resubmit after an error.
- Do not repost a completed result.

## Common Pitfalls

- Calling `list_models` and `get_model_schema` before every request instead of using the bundled references.
- Passing an API endpoint path instead of a compact MCP model ID.
- Promoting unrelated live models into the curated menu.
- Loading every model reference when only one is selected.
- Reusing Krea 2 fields on GPT or Nano schemas.
- Hardcoding account-specific moodboard or style IDs.
- Sending a style to a model absent from its `supported_models` list.
- Sending both Nano `image_urls` and `style_images` while expecting both to apply.
- Inventing limits where the schema declares none.
- Adding output count or invented pricing.
- Uploading or generating merely to verify the integration.

## Verification Checklist

- [ ] Krea MCP is connected in the selected Hermes profile.
- [ ] Exactly one curated compact model ID is selected.
- [ ] Only its bundled reference and template were loaded.
- [ ] No routine `list_models` or `get_model_schema` call was made.
- [ ] All request fields match the cached capability reference.
- [ ] Moodboard/style IDs, when used, came from the live account list.
- [ ] References occupy the correct model-specific fields.
- [ ] Upload and generation approval gates were respected.
- [ ] Completed media is delivered once.
