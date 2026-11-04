# Updating Cached Krea References

Use this procedure only when a bundled reference appears stale or the user explicitly requests a capability refresh.

## Refresh triggers

Refresh the affected model when:

- Krea rejects a documented field or enum value;
- `generate_image` reports that the compact model ID is unsupported;
- a required field, default, range, or reference limit appears to have changed;
- the user explicitly asks to refresh Krea capabilities;
- a scheduled/manual maintenance review is being performed.

Do not refresh merely because a normal request is being prepared.

## Targeted repair

When one model fails:

1. Preserve the failed request and exact Krea error.
2. Call `get_model_schema` for that compact model ID only.
3. Compare required fields, properties, enums, defaults, numeric ranges, array limits, descriptions, and `additionalProperties` against its reference.
4. Use the live schema to explain the correction for the current request.
5. Do not automatically resubmit a paid generation.
6. Ask for explicit approval before editing the shared reference or template.
7. Update only the affected model reference/template and its `Last verified` date.
8. Revalidate all examples that use the changed field.

## Full curated audit

Run only on explicit request:

1. Call `list_models` once.
2. Confirm all six curated compact IDs:
   - `krea/krea-2/large`
   - `krea/krea-2/medium`
   - `krea/krea-2/medium-turbo`
   - `openai/gpt-image-2`
   - `google/nano-banana-pro`
   - `google/nano-banana-2`
3. Call `get_model_schema` once per curated model.
4. Compare each live schema with its bundled reference and template.
5. Call `list_styles` and verify style model support/pagination.
6. Inspect the `list_moodboards` tool contract. Do not import the full account list into model references; preserve selected entries only in `preferred-krea-assets.yaml` after explicit user approval.
7. Report the exact drift before changing model references or templates.
8. Update only after explicit approval.

The full audit does not automatically change `preferred-krea-assets.yaml`. That file is a user-curated shortlist shared by all Hermes agents using this skill; change it only when the user explicitly selects additions, removals, or replacements.

Do not generate, upload, cancel jobs, or alter account data during an audit.

## Completion criteria

A reference update is complete when:

- every changed fact is backed by a live schema/tool result;
- unchanged models were not rewritten unnecessarily;
- templates contain only current schema fields;
- compact MCP model IDs are used everywhere;
- account-specific IDs are absent;
- no paid or write operation occurred;
- the user receives a concise change report.
