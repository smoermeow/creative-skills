# Krea 2 Image Models

Last verified against Krea MCP: 2026-07-17

## Model IDs

| Label | MCP model ID |
|---|---|
| Krea 2 Large | `krea/krea-2/large` |
| Krea 2 Medium | `krea/krea-2/medium` |
| Krea 2 Medium Turbo | `krea/krea-2/medium-turbo` |

Use these compact IDs in `get_model_schema` and `generate_image`. Do not use API endpoint paths as MCP model IDs.

## Verified input schema

Required:

```text
prompt: string
aspect_ratio: 1:1 | 4:3 | 3:2 | 16:9 | 2.35:1 | 4:5 | 2:3 | 9:16
resolution: 1K
```

Optional:

```text
seed: number or null
creativity: raw | low | medium | high; default low
intensity: integer -100..100; default 0
complexity: integer -100..100; default 0
movement: integer -100..100; default 0
image_url: URL or null
strength: number 0..1; default 0.99; meaningful only with image_url
image_style_references: max 10 objects
styles: array of Krea style/LoRA objects
moodboards: max 1 object
```

Every Krea 2 schema sets `additionalProperties: false`. Submit only documented fields.

## Source image

```json
{
  "image_url": "<asset URL>",
  "strength": 0.99
}
```

`strength` is denoising strength: `0` preserves the source; `1` fully replaces it. It has no effect without `image_url`.

## Style-image references

Up to ten:

```json
{
  "image_style_references": [
    {
      "url": "<asset URL>",
      "strength": 0.5
    }
  ]
}
```

Strength defaults to `0.5` and accepts `0..1`.

## Krea styles and LoRAs

Read [`preferred-krea-assets.yaml`](preferred-krea-assets.yaml) first and offer compatible preferred styles/LoRAs. Call `list_styles` only when no matching preferred style exists, the user asks to browse the full Krea list, or a selected saved style fails. Filter every live result by `supported_models` before showing it.

Request shape:

```json
{
  "styles": [
    {
      "id": "<live style ID>",
      "strength": 1.0
    }
  ]
}
```

Strength accepts `-2..2`. The schema declares no maximum style count.

Verified account example on 2026-07-17:

```text
HOST ANIME
id: z7kkrlzk1
supported_models:
  - krea/krea-2/medium
  - krea/krea-2/medium-turbo
next_cursor: null
```

This is an example, not a globally guaranteed account asset. Do not show it for Krea 2 Large or for models absent from its live `supported_models` list.

## Moodboards

Read [`preferred-krea-assets.yaml`](preferred-krea-assets.yaml) first and offer compatible preferred moodboards. Call `list_moodboards` only when no matching preferred moodboard exists, the user asks to browse the full Krea collection, or a selected saved moodboard fails.

The preferred-assets list is intentionally part of this shared skill so every Hermes agent using the skill sees the same curated Krea shortlist.

At most one moodboard:

```json
{
  "moodboards": [
    {
      "id": "<live moodboard UUID>",
      "strength": 0.23
    }
  ]
}
```

Strength defaults to `0.23` and accepts `0..1`. Show live moodboard name and kind; omit long descriptions unless asked.

## K2 controls

```text
creativity: raw disables prompt expansion; low/medium/high control expansion strength
intensity: -100..100
complexity: -100..100
movement: -100..100
```

The slider default is `0`, meaning neutral/no slider LoRA. If the user says `speed`, map it to `movement` and mention the mapping briefly. Do not invent undocumented descriptions of slider behavior.

## Output and price

- No output-count field is exposed.
- Do not offer batch count or imply multi-output support.
- Krea MCP exposes no cost estimator or schema price. Do not invent one.

## Template

Use [`../templates/krea-2.yaml`](../templates/krea-2.yaml). Omit blank optional fields from the final `input` object.
