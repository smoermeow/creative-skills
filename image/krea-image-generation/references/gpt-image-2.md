# GPT Image 2 on Krea MCP

Last verified against Krea MCP: 2026-07-17

## Model

```text
Label: GPT Image 2
MCP model ID: openai/gpt-image-2
Category: image
```

Use the compact ID in `get_model_schema` and `generate_image`.

## Verified input schema

```text
prompt: required non-empty string
quality: low | medium | high | auto; default high
aspect_ratio: 16:9 | 2:1 | 3:2 | 4:3 | 1:1 | 3:4 | 2:3 | 1:2 | 9:16
resolution: 1K | 2K | 4K
width: optional number
height: optional number
image_urls: optional string array, max 10
style_images: optional object array, max 10
```

The schema sets `additionalProperties: false` and exposes no Krea 2 sliders, moodboards, or Krea style/LoRA IDs.

## Image references

```json
{
  "image_urls": [
    "<asset URL>"
  ]
}
```

Maximum: ten.

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

Maximum: ten. Strength accepts `-2..2`. The live schema requires `strength` but does not mark `url` as required; when the object represents an image reference, supply its URL.

## Output and price

- No output-count field is exposed.
- Do not offer batch count or imply multi-output support.
- Krea MCP exposes no cost estimator or schema price. Do not invent one.

## Template

Use [`../templates/gpt-image-2.yaml`](../templates/gpt-image-2.yaml). Omit empty reference arrays from the final `input` object.
