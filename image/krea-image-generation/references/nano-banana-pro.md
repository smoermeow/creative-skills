# Nano Banana Pro on Krea MCP

Last verified against Krea MCP: 2026-07-17

## Model

```text
Label: Nano Banana Pro
MCP model ID: google/nano-banana-pro
Category: image
```

## Verified input schema

```text
prompt: required string, minimum 3 characters
aspect_ratio: 21:9 | 1:1 | 4:3 | 3:2 | 2:3 | 5:4 | 4:5 | 3:4 | 16:9 | 9:16
resolution: 1K | 2K | 4K; default 1K
width: optional number
height: optional number
image_urls: optional URL array; schema declares no maximum
style_images: optional object array; schema declares no maximum
```

The schema sets `additionalProperties: false`. It exposes no quality field, Krea 2 sliders, moodboards, or Krea style/LoRA IDs.

## Image references

```json
{
  "image_urls": [
    "<asset URL>"
  ]
}
```

The provider limit is unknown because the schema declares no maximum. Do not invent one.

## Style-image references

```json
{
  "style_images": [
    {
      "url": "<asset URL>",
      "strength": 1.0
    }
  ]
}
```

Strength accepts `-2..2`. The live schema requires `strength` but does not mark `url` as required; supply the URL when using an image reference. The provider count limit is unknown.

## Interaction rule

When `image_urls` is populated, Krea documents that `style_images` is ignored. Do not send both while expecting both to influence the result.

## Output and price

- No output-count field is exposed.
- Do not offer batch count or imply multi-output support.
- Krea MCP exposes no cost estimator or schema price.

## Template

Use [`../templates/nano-banana-pro.yaml`](../templates/nano-banana-pro.yaml). Omit empty arrays from the final `input` object.
