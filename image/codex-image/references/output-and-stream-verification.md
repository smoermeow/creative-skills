# Native output and stream verification

## Sizes and quality

The adapter passes `--size` to the image tool and saves returned bytes without a local resize. Receipts record REQUESTED size. The backend has returned different dimensions across runs, including parallel calls with identical settings; historical successes or limits are not current guarantees.

Inspect every saved file independently, for example using `terminal` on macOS:

```bash
file <OUTPUT.png>
sips -g pixelWidth -g pixelHeight <OUTPUT.png>
```

Elsewhere use an available image metadata reader. Report requested versus actual dimensions when they differ. Quality and dimensions are separate: `gpt-image-2-high` is a local quality alias, while the receipt's `api_model` can remain `gpt-image-2`. Matching dimensions do not prove matching quality.

Preserve and deliver the complete native image. Never crop, pad, resize, or silently substitute a lower-resolution generation to satisfy a requested size. Explain a mismatch and obtain permission for a specific transformation or additional call. Retain the original if a derivative is authorized.

## Streaming failures

- An HTTP/backend error before image data: report the exact available error/request ID and stop; no automatic retry or prompt rewrite.
- `response.image_generation_call.generating` means the remote call has started. Do not interrupt it or launch a competing call without authorization.
- If image data arrives before a stream error, the adapter saves the latest received image. Verify the file, disclose the interruption, and do not describe a recovered partial as a confirmed complete result.
- `No image result returned` is a failure, not a successful image and not permission to rewrite the prompt. Preserve logs and ask before another call.

## Multiple outputs

Use separate names/directories for independently requested outputs. Preserve locked prompts and all unchanged settings/reference slots. Check every file's dimensions, receipt quality/model, and complete ordered reference list. Deliver successful artifacts and report failed calls separately; never infer success from a sibling call.

Verification here is file/receipt verification, not unsolicited visual critique. Only analyze image content when explicitly requested.
