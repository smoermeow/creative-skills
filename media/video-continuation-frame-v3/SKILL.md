---
name: video-continuation-frame-v3
description: Prepare five-second tails and source continuation frames.
version: 3.0.0
author: smoermeow, Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [video, continuation, frame-extraction, ffmpeg]
---

# Video Continuation Frame V3

Separate V3 copy. The original `video-continuation-frame` skill remains untouched. V3 changes timestamp handling to accept nonuniform frame timing; frame extraction, grids, selection window and tail-range rules are retained.

## Requirement

**Neither the tail nor the extracted frame may change the source in any visible way.** This includes brightness, shadows, color, contrast, detail and framing. Compression-level differences are acceptable only if invisible. Mathematical pixel identity is not the tail requirement.

The automatic tail must retain the source ending and be exactly five seconds. Never substitute a longer keyframe-aligned tail. Dreamina must accept it during generation, not merely upload.

## When to use

Use when preparing a clean short continuation video and one source frame for downstream generation. Like V2, this version avoids v1's non-keyframe packet-copy trimming and its hidden discarded pre-roll.

Creating or editing this skill does not authorize running it, generating test media, uploading references, or spending generation credits. Run only the stages the user requests. No subagents are necessary.

## Dependencies

The bundled script uses this workstation's existing tools:

- FFmpeg and FFprobe. Set `FFMPEG` and `FFPROBE` to their executable paths when the inherited workstation defaults are unavailable. These overrides do not change extraction settings.
- `/usr/bin/python3` with OpenCV, Pillow and NumPy

Script: `scripts/video_continuation.py`, relative to this skill directory.

## Tail implementation

- Sources longer than seven seconds: export the exact final five seconds.
- Sources at most seven seconds: retain the original whole-source behavior.
- Explicit `--cut-start` and `--cut-end`: export that exact range.
- Decode and re-encode using standard H.264 High, CRF 10, slow preset, native `yuv420p`, no B-frames. This gives a new starting keyframe without pre-cut dependencies or negative video decode timestamps.
- Keep original resolution and frame timing. No scaling, grading, tone mapping, RGB round-trip or automatic rotation.
- Preserve known color range, matrix, transfer, primaries and chroma-location metadata. Do not invent tags when the source is untagged.
- Encode audio as AAC at 192 kbps, preserving its relationship to the cut. Normal AAC encoder-priming metadata is separate from the defective video pre-roll. Do not shift video later to hide audio priming.
- Use a new output directory. Tail export refuses to overwrite an existing file.

V3 accepts zero-based, 8-bit `yuv420p` sources with constant or nonuniform frame timing. Cuts use actual source timestamps, quantized only to the native time-base tick, not an FPS grid. A boundary inside a displayed frame retains that picture for its remaining display interval. No frame-rate conversion, interpolation or uniform-FPS frame-count calculation is used. The inherited pixel-format and zero-based-timeline restrictions remain unchanged.

## Source-frame preservation

Re-encoded tail pictures are no longer hash-identical to the source. V3 maps the actual retained source pictures and timestamps, including the picture already displayed at a non-frame-aligned cut. It does not derive a frame count from average FPS. A packet-duration-only remux bounds the final displayed picture at the requested cut end; it does not re-encode or change image pixels.

Overview and candidate images are decoded from the mapped **original source frames**, not from the re-encoded tail. The final PNG is still extracted directly from the exact original frame number using v1's existing FFmpeg extraction. Its native dimensions and exact match against the chosen candidate remain checked. Do not introduce new color conversion or image-processing behavior into frame extraction.

## How to run

Use `terminal` for the requested stage. Replace placeholders with actual absolute paths; `<skill-dir>` is this v2 directory. Do not automatically execute the examples when asked only to build the skill.

### Prepare

```bash
/usr/bin/python3 '<skill-dir>/scripts/video_continuation.py' prepare \
  --input '/absolute/source.mp4' \
  --output-dir '/absolute/new-v3-output'
```

Optional explicit range: append `--cut-start 23 --cut-end 28`.

Outputs: `tail_5s.mp4` for automatic trimming, or `requested_cut.mp4` for an explicit range, plus `overview_grid.png`, source overview PNGs and `analysis_manifest.json`.

### Candidates

After reviewing the overview when frame selection is requested:

```bash
/usr/bin/python3 '<skill-dir>/scripts/video_continuation.py' candidates \
  --manifest '/absolute/new-v3-output/analysis_manifest.json' \
  --center 4.0 --radius 0.4
```

Outputs: `candidate_grid.png`, source candidate PNGs and `candidate_manifest.json`.

### Select

```bash
/usr/bin/python3 '<skill-dir>/scripts/video_continuation.py' select \
  --manifest '/absolute/new-v3-output/analysis_manifest.json' \
  --candidate-manifest '/absolute/new-v3-output/candidate_manifest.json' \
  --frame 97 --reason 'Reason for choosing this original source frame'
```

Outputs: `continuation_frame.png` and `selection.json`.

## Selection rules retained from v1

- Eligible window: the final three seconds of the analysis interval, excluding its final half-second.
- Review chronologically, then compare adjacent candidate frames.
- Prefer clear, stable anatomy, readable geography and useful continuation poses.
- Avoid cuts, fades, blinks, occlusion, exposure flashes and anomalous frames.
- Export the selected original frame at native dimensions, without cropping or resizing.

## Runtime checks and acceptance

When the user runs preparation, the script checks tail duration, zero-based video start, retained source pictures and decoded output pictures, initial keyframe, absence of discarded or negative-timestamp video packets, and exact source-frame timing correspondence. These are structural checks, not proof of visual equivalence or Dreamina compatibility.

The manifest explicitly records appearance as `not reviewed` and Dreamina as `not tested`. Do not claim either passed because encoding completed.

Only when testing is requested:

1. Compare the tail against the matching source interval for any visible change. A visible shift is a failure regardless of CRF or numerical similarity scores.
2. Confirm the chosen PNG matches the source's appearance.
3. With upload/generation authorization, test Dreamina generation using the tail. Upload acceptance alone is not acceptance.

No automatic provider calls, uploads, generation jobs or visual-analysis calls are part of this script.

## Pitfalls

- Do not restore `-c copy` for arbitrary non-keyframe starts.
- Do not extend a five-second request to reach a keyframe.
- Do not use unusual lossless H.264 profiles as a compatibility shortcut.
- Do not extract the final PNG from the re-encoded tail.
- Do not mistake successful decoding, preserved tags or high-quality encoding for a completed visual/provider acceptance test.
- Use a new output directory for v3; do not reuse V1/V2 manifests or overwrite existing project artifacts.
