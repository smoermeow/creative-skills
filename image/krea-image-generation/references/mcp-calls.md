# Krea MCP Call Contracts

Last verified: 2026-07-17

## Normal rule

Use the bundled model references and templates for ordinary requests. Do not call `list_models` or `get_model_schema` before every generation.

## Install and verify in Hermes

```bash
hermes --profile PROFILE mcp add krea \
  --url https://api.krea.ai/mcp \
  --auth oauth
hermes --profile PROFILE mcp login krea
hermes --profile PROFILE mcp test krea
hermes --profile PROFILE mcp list
```

## Generate image

Krea exposes one generic wrapper:

```json
{
  "model": "<compact model ID>",
  "input": {
    "<model-specific field>": "<value>"
  },
  "sync": false
}
```

- `model` must be a compact ID from the curated menu.
- `input` must contain only fields from that model's bundled reference.
- `sync` defaults to false.
- `timeoutSeconds` applies only when `sync` is true and accepts 1–300 seconds.
- Prefer async mode so the MCP Apps UI can show progress.

## Job status

Async generation returns a job ID. When the host renders the Krea job widget, let it poll automatically. Call `get_job({"jobId":"..."})` only when the user requests a text status update or the host has no widget.

Terminal states:

```text
completed
failed
cancelled
```

Other observed states:

```text
backlogged
queued
scheduled
processing
sampling
intermediate-complete
```

Deliver a completed result once. Do not repost it after a status recheck.

## Models and schemas

Use these only for repair, refresh, or explicit discovery:

```text
list_models()
get_model_schema(model="<compact model ID>")
```

Do not pass route-style API endpoint paths to `get_model_schema`.

## Styles, moodboards, and preferred assets

Read [`preferred-krea-assets.yaml`](preferred-krea-assets.yaml) first. It is the shared shortlist for every Hermes agent that loads this skill.

Use `list_styles` or `list_moodboards` only when no matching preferred entry exists, the user asks to browse the full Krea collection, or a saved entry fails:

```text
list_styles(cursor?)
list_moodboards()
```

Follow style pagination until `next_cursor` is null. Do not overwrite the preferred list from live results without explicit approval.

## Uploads

`get_upload_url()` returns a three-hour presigned URL. Upload the file to that URL as multipart form field `file`; the response returns the Krea asset URL used by model inputs.

Uploads write to the Krea account and require explicit approval. Reuse an existing Krea asset URL when possible.

## Safety

- Listing models, reading schemas, listing styles, listing moodboards, and checking jobs are read-only.
- Uploading and generation are external writes.
- A request for options, a draft, or “test it” does not authorize upload or generation.
- Krea MCP exposes no cost-estimate tool; do not invent prices.
