# Video Continuation Frame V3

## Purpose

Prepare a source video's ending for continuation: a short analysis clip, overview and candidate contact sheets, and one selected original-source PNG at native dimensions. Version `3.0.0` maps actual source timestamps, including nonuniform frame timing, instead of calculating source-frame identity from average FPS.

The visual requirement is that neither the tail nor the final frame visibly changes the source's brightness, shadows, color, detail, or framing. The tail is re-encoded, so mathematical pixel identity is not its requirement. The selected PNG is extracted from the original source, not the re-encoded tail, and is checked against the reviewed candidate pixels.

This is a local media-preparation tool, not a generator or upload client. Reading or installing it does not authorize processing media. Run only the stages explicitly requested by the user.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Video Continuation Frame V3 skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/media/video-continuation-frame-v3
```

### If you already use a protected orchestrator

```text
Install the complete Video Continuation Frame V3 skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/media/video-continuation-frame-v3

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Prerequisites and setup

Keep the **complete `video-continuation-frame-v3` folder**, including `scripts/` and `requirements.txt`. An assistant can read `SKILL.md` directly; no skill-registration command or special installer is needed. Actual media stages require:

- Python 3 with a working `venv` and `pip`.
- OpenCV, Pillow, and NumPy, using the pinned dependencies in `requirements.txt`.
- FFmpeg and FFprobe executables. The script uses `libx264`, AAC, timestamp-preserving options, and the `setts` bitstream filter; the FFmpeg build must support them.
- Read access to the original video, a fresh writable output directory, and a way to inspect generated contact sheets before selection.

The skill declares macOS as its platform; this README does not establish support on other operating systems.

### Python environment

Replace `SKILL_DIR` with the absolute path to your downloaded folder. These setup commands install Python dependencies, not media or generation services:

```bash
SKILL_DIR="/absolute/path/to/video-continuation-frame-v3"
VENV_DIR="$HOME/.venvs/video-continuation-frame-v3"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install -r "$SKILL_DIR/requirements.txt"
PYTHON="$VENV_DIR/bin/python"
```

Use that interpreter for every stage; the script's shebang and the workstation interpreter shown in `SKILL.md` do not install dependencies into your chosen Python. The requirements file pins versions for the publication's safe CLI-help check, not a newly verified extraction or generation run. If installation fails, resolve the Python/package compatibility issue before processing media rather than silently changing the pins.

### FFmpeg and FFprobe

Install these tools through your operating system's normal package-management or distribution method if they are absent. By default, the script finds `ffmpeg` and `ffprobe` on `PATH`. Alternatively, set both executable paths explicitly:

```bash
export FFMPEG="/absolute/path/to/ffmpeg"
export FFPROBE="/absolute/path/to/ffprobe"
```

Use real executable files, not directories or shell aliases. These environment variables override `PATH` discovery and do not change the extraction settings.

### Safe CLI discovery

After Python setup, help can be inspected without opening a video or creating media:

```bash
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" --help
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" prepare --help
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" candidates --help
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" select --help
```

Help checks do not exercise FFmpeg encoding, visual preservation, or provider acceptance.

## Required files

| File | Role |
| --- | --- |
| `SKILL.md` | Operating rules, preservation contract, selection policy, and acceptance limits. |
| `scripts/video_continuation.py` | The `prepare`, `candidates`, and `select` command implementation. |
| `requirements.txt` | Pinned OpenCV, Pillow, and NumPy dependencies. |

Preserve the folder layout. Keep the original source and the generated manifests available through all requested stages: manifests reference the source, analysis clip, and candidate image paths.

## Inputs

- **Original video:** an absolute local file path. The V3 trim implementation accepts a zero-based video timeline and 8-bit `yuv420p`; it refuses automatic pixel-format conversion. Constant and nonuniform frame timing are handled through actual timestamps.
- **Fresh output directory:** do not reuse an earlier run or V1/V2 manifests.
- **Optional explicit range:** `--cut-start` and `--cut-end`, in source seconds, must be supplied together and lie within the source video duration.
- **Candidate center and radius:** seconds relative to the analysis clip, not the full source timeline. Default radius is `0.4` seconds.
- **Selection:** a reviewed `analysis_frame_number` from `candidate_manifest.json`, plus a reason. This is not the original-source frame number or the overview thumbnail ordinal.

Automatic behavior depends on source video-stream duration:

| Source/range | Analysis clip |
| --- | --- |
| Source longer than 7 seconds, no explicit range | Exact final 5 seconds, exported as `tail_5s.mp4`. |
| Source at most 7 seconds, no explicit range | Original whole source; no new tail MP4 is exported. |
| Explicit start/end range | Requested interval exported as `requested_cut.mp4`. |

The eligible selection window is the final three seconds of the analysis interval, excluding its final half-second. The manifest records the exact eligible bounds and source mapping.

## Copy-ready invocation example

For agent-driven use, replace paths and paste:

```text
Read /absolute/path/to/video-continuation-frame-v3/SKILL.md and inspect
its scripts/video_continuation.py. Use the Python environment installed from
its requirements.txt, with FFmpeg and FFprobe available.

Run only the prepare stage for /absolute/path/to/source.mp4, writing to the
fresh directory /absolute/path/to/new-continuation-output. Use the default
ending policy. Return the analysis clip, overview grid, manifest paths, and
eligible window. Stop for review; do not run candidates or select yet.
Do not upload anything or submit a generation job.
```

### Actual staged CLI usage

The following commands create media when run. Execute each stage only when authorized; do not run them as a setup test. Keep the shell variables from setup, and replace the input/output paths:

**1. Prepare**

```bash
INPUT="/absolute/path/to/source.mp4"
OUTPUT_DIR="/absolute/path/to/new-continuation-output"
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" prepare \
  --input "$INPUT" \
  --output-dir "$OUTPUT_DIR"
```

For an explicitly requested source range, append `--cut-start 23 --cut-end 28` to that command **instead of running the automatic cut first**. Those example times require a source at least 28 seconds long. Review `overview_grid.png` and the manifest's eligible window before choosing a candidate center.

**2. Inspect neighboring candidates**

```bash
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" candidates \
  --manifest "$OUTPUT_DIR/analysis_manifest.json" \
  --center 4.0 --radius 0.4
```

`4.0` is an example center in analysis-clip seconds, suitable only if it falls within this run's eligible window. Replace it after overview review. The script intersects the requested neighborhood with eligible timestamps; a neighborhood containing no eligible frames fails. Compare candidates chronologically and against adjacent frames.

**3. Export a reviewed selection**

```bash
FRAME=97  # Replace with an actual reviewed analysis_frame_number from this run.
"$PYTHON" "$SKILL_DIR/scripts/video_continuation.py" select \
  --manifest "$OUTPUT_DIR/analysis_manifest.json" \
  --candidate-manifest "$OUTPUT_DIR/candidate_manifest.json" \
  --frame "$FRAME" \
  --reason "Stable anatomy, readable geography, and a clear continuation pose."
```

Do not select the example frame number blindly. It must exist in this candidate manifest, be eligible, and match the frame you reviewed.

## Expected output

All generated files below live under the output directory, except the original source reused by whole-source mode:

| Stage | Files and reported result |
| --- | --- |
| `prepare` | `analysis_manifest.json`, `overview_grid.png`, and source-decoded PNGs under `overview_frames/`; `tail_5s.mp4` or `requested_cut.mp4` when trimming applies. Prints JSON with paths, mode, durations, and eligible window. |
| `candidates` | `candidate_manifest.json`, `candidate_grid.png`, and source candidate PNGs under `candidate_frames/`. Prints JSON with paths, count, and first/last candidate details. |
| `select` | `continuation_frame.png` and `selection.json`, recording source/analysis frame identity, timestamps, native dimensions, comparison result, and selection reason. Prints a JSON summary. |

Preparation checks timing correspondence, frame mapping, duration, dimensions, starting keyframe, and video-packet structure for the exported tail. Selection checks native dimensions and exact equality with the selected candidate. These are structural and pixel-comparison checks, **not** a completed visual or provider-compatibility test.

`analysis_manifest.json` records `appearance_acceptance: "not reviewed"` and `dreamina_acceptance: "not tested"`. Visual comparison needs separate review. Provider compatibility requires an explicitly authorized generation test; successful upload alone is insufficient. The script makes no automatic provider calls.

