---
name: dreamina-seedance-video
description: Generate Dreamina Seedance videos with one approval.
version: 1.1.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [dreamina, seedance, video, references, cli]
---

# Dreamina Seedance Video

Generate Seedance 2.0 or 2.5 videos through the installed `dreamina-canvas` CLI with minimal interaction. A normal request has one user approval: the final paid-generation approval after references are uploaded, the node exists, and its credit cost is known.

Do not add a separate upload approval, routine authentication check, routine model-catalogue lookup, repeated progress messages, or approval between mechanical CLI steps.

## When to Use

Use when the user asks to generate a Dreamina Seedance 2.0 or 2.5 video from text, local media, or existing Dreamina `node:` or `res:` references.

Do not use for prompt development alone or creative review of a finished video.

## Interaction Contract

A generation request authorizes these non-paid preparation steps without another question:

1. Resolve the supplied prompt, settings, and references.
2. Upload supplied local references.
3. Create the unrun video node.
4. Retrieve its credit quote.

Then show one compact approval containing the final payload and exact credit cost. After approval, confirm the quoted ceiling, run the same node, wait quietly, download, and technically verify it without further approval.

Ask before preparation only when required information is absent or genuinely ambiguous. Never ask the user to reconfirm values already supplied in the current session.

## Known Capabilities

Use these capabilities directly during a normal render. Do not query the catalogue first.

### Seedance 2.5

- Model: `seedance_2.5`
- Modes: `t2v`, `first_last_frame`, `m2v`
- Prompt: up to 15,000 characters
- Duration: 4–30 seconds in one-second steps
- Resolution: `480p`, `720p`, `1080p`
- Ratio: `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`
- Count: 1–4
- `m2v`: 1–50 references; up to 30 images, 10 videos, and 10 audio files

### Seedance 2.0

- Model: `seedance_2.0`
- Modes: `t2v`, `first_last_frame`, `m2v`
- Prompt: up to 4,000 characters
- Duration: 4–15 seconds in one-second steps
- Resolution: `720p`, `1080p`, `4K`
- Ratio: `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`
- Count: 1–4
- `m2v`: 1–12 references; up to 9 images, 3 videos, and 3 audio files
- Audio-only input is invalid; include at least one image or video

Query `dreamina-canvas --format json model list --type video` only when the CLI was updated or Dreamina rejects a model, mode, setting, or reference capability.

Run `dreamina-canvas --format json auth status` only after an authentication-related command failure. Neither check belongs in every generation.

## Resolve the Render Contract

Use the latest session values for:

- canonical model;
- exact prompt;
- ordered image, video, and audio references;
- mode;
- ratio, resolution, duration, and output count;
- project identity when no current project exists.

Preserve the exact prompt. Do not expand it, impose a template, or replace it with a prompt-file path.

### Mode and reference roles

- No media: `t2v`.
- General image, video, or audio guidance: `m2v`.
- One image explicitly designated as the first frame: `first_last_frame`.
- Two images explicitly designated as first and last frames: `first_last_frame`, in that order.

Treat ordinary character, environment, style, and composition images as `m2v` references. Do not reinterpret them as first or last frames.

When references are supplied and their roles are clear, proceed without asking. Ask one focused question only if:

- first/last-frame intent or order is ambiguous;
- intended inclusion or ordering cannot be determined;
- a required setting is absent and no established session default applies;
- a rejected model or capability does not resolve uniquely.

Do not analyze reference content unless requested. Never add, replace, omit, or reorder references silently.

## Reference Identities

Use existing Canvas sources as `--ref node:node_xxx` and uploaded resources as `--ref res:resource-uuid`.

Upload local files directly and retain every returned `data.resourceId`:

```bash
dreamina-canvas --format json --non-interactive resource upload --file "/path/reference.png" --type image
dreamina-canvas --format json --non-interactive resource upload --file "/path/reference.mp4" --type video
dreamina-canvas --format json --non-interactive resource upload --file "/path/reference.wav" --type audio
```

Uploading is preparation, not a separate approval gate. Preserve the association between path, media type, position, and resource ID. If an upload fails, retain successful IDs and retry only the failed upload.

Repeated `--ref` flags normally suffice. Use `{{res:resource-uuid}}` or `{{node:node_xxx}}` in the prompt only when a reference must bind to a precise subject, action, or relationship; the same identity must still appear through `--ref`.

## Procedure

### 1. Minimal preflight

Validate only this request's prompt length, required settings, mode/reference compatibility, and known count limits. Do not run broad discovery.

Completion criterion: one unambiguous render contract exists.

### 2. Upload references

Upload every authorized local reference in order. Existing `node:` and `res:` references need no upload.

Completion criterion: every ordered reference has one usable identity.

### 3. Create one unrun node

```bash
dreamina-canvas --format json --non-interactive node create video \
  --mode MODE \
  --model MODEL \
  --prompt "EXACT PROMPT" \
  --ref REF_1 \
  --ref REF_2 \
  --ratio RATIO \
  --resolution RESOLUTION \
  --duration SECONDS \
  --count COUNT
```

Omit `--ref` for `t2v`. Replace every placeholder with the resolved contract. Retain the returned Node ID and Project ID.

Completion criterion: the exact unrun node exists once and no credits were spent.

### 4. Quote that node

```bash
dreamina-canvas --format json --non-interactive node quote \
  --node-id NODE_ID \
  --project-id PROJECT_ID
```

Completion criterion: the exact credit total is known.

### 5. Request the single approval

Show one compact approval:

```text
Model: seedance_2.5
Mode: m2v
References:
1. image — /path/character.png → res:...
2. video — /path/motion.mp4 → res:...
Prompt: <exact prompt>
Settings: 16:9 · 1080p · 10 seconds · 1 output
Credit cost: <exact quoted total>
Run this generation?
```

This is the only normal approval gate. It covers the final payload and paid execution together. Do not ask separately about uploads, node creation, quoting, confirmation-token retrieval, waiting, downloading, or verification.

If the user changes the payload, update the unrun node, quote the corrected payload, and present one replacement approval. Never run the superseded payload.

### 6. Confirm and run

After approval, confirm the exact ceiling:

```bash
dreamina-canvas --format json --non-interactive node confirm \
  --node-id NODE_ID \
  --project-id PROJECT_ID \
  --credit-ceiling APPROVED_TOTAL
```

Capture the returned `creditConfirmationToken`, then run the same Node ID:

```bash
dreamina-canvas --format json --non-interactive node run \
  --node-id NODE_ID \
  --project-id PROJECT_ID \
  --credit-token CREDIT_CONFIRMATION_TOKEN
```

Retain the submit ID. Never use `--yes` for an unknown amount and never create a replacement because waiting timed out.

Completion criterion: one paid submission exists with a retained submit ID.

### 7. Wait sparsely and quietly

Seedance commonly takes 5–10 minutes under normal traffic. Do not begin rapid status polling.

- Wait five minutes after submission before the first status check.
- If still queued or processing, wait about two minutes before each later check.
- Use one quiet background process when possible.
- Do not narrate checks or send progress messages unless the user asks.
- Stop immediately on terminal success or failure.
- Bound the automatic wait. If the job remains active after roughly 15 minutes, report that once with the retained submit ID and wait for the user to request resumption.

Do not use `operation wait` with its five-second default interval. Sparse checks may use:

```bash
dreamina-canvas --format json --non-interactive operation status SUBMIT_ID \
  --project-id PROJECT_ID
```

A successful status request only proves the lookup worked. Inspect the returned generation state.

Completion criterion: terminal state is known, or the still-active job is handed back once without duplicate submission.

### 8. Download and verify

On terminal success, download the returned resource:

```bash
dreamina-canvas --format json --non-interactive resource download RESOURCE_ID \
  --project-id PROJECT_ID \
  --output "/agreed/output/path"
```

Verify that the file is non-empty and decodable. Report duration, dimensions, codec, and audio-stream presence when audio output was expected. Do not perform creative analysis unless requested.

Completion criterion: the resource is downloaded and technically valid.

## Recovery

- Authentication failure: run `auth status`, repair only authentication, and resume the same step.
- Capability rejection: query the live catalogue once; ask only if resolving it changes the render contract.
- Upload failure: preserve successful IDs and retry only the failed upload.
- Active after the bounded wait: preserve the original submit ID; do not continue polling or create a replacement until asked.
- Credit increase: present one updated final approval with the new exact total.
- Terminal failure: report it immediately with the Node ID and submit ID.

## Final Report

Keep delivery short:

- actual model, mode, and duration;
- ordered references;
- Node ID and submit ID;
- output path;
- technical status.

## Hard Rules

- One normal approval: final payload plus exact credit cost.
- No upload approval.
- No routine auth or catalogue check.
- No repeated confirmation of session-supplied values.
- No rapid or narrated polling.
- No prompt rewriting or silent reference changes.
- No duplicate paid retry.
