#!/usr/bin/python3
"""Prepare and extract a continuation frame from a video's ending."""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FFMPEG = os.environ.get("FFMPEG", shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = os.environ.get("FFPROBE", shutil.which("ffprobe") or "ffprobe")


def fail(message):
    raise SystemExit(message)


def run(command, capture=False):
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if result.returncode:
        detail = result.stderr.strip() if capture else ""
        fail(f"Command failed ({result.returncode}): {' '.join(command)}\n{detail}")
    return result.stdout if capture else ""


def require_tools():
    for path in (FFMPEG, FFPROBE):
        if not os.path.isfile(path) or not os.access(path, os.X_OK):
            fail(f"Required executable is missing or not executable: {path}")


def probe(path):
    raw = run([
        FFPROBE, "-v", "error", "-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,width,height,"
        "avg_frame_rate,r_frame_rate,nb_frames,duration,start_time,pix_fmt,"
        "color_range,color_space,color_transfer,color_primaries,chroma_location,time_base,duration_ts",
        "-of", "json", path,
    ], capture=True)
    data = json.loads(raw)
    videos = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
    if not videos:
        fail(f"No video stream found: {path}")
    video = videos[0]
    duration = (float(int(video["duration_ts"]) * Fraction(video["time_base"]))
                if video.get("duration_ts") is not None and video.get("time_base")
                else float(video.get("duration") or data["format"]["duration"]))
    return data, video, duration


def frame_pts(path):
    raw = run([
        FFPROBE, "-v", "error", "-select_streams", "v:0",
        "-show_entries", "frame=best_effort_timestamp_time",
        "-of", "json", path,
    ], capture=True)
    rows = json.loads(raw).get("frames", [])
    pts = []
    for row in rows:
        value = row.get("best_effort_timestamp_time")
        if value is not None:
            pts.append(float(value))
    if not pts:
        fail(f"Could not read frame timestamps: {path}")
    base = pts[0]
    return [value - base for value in pts], pts


def decoded_frame_hashes(path):
    raw = run([
        FFMPEG, "-hide_banner", "-loglevel", "error",
        "-i", path, "-map", "0:v:0", "-f", "framemd5", "-",
    ], capture=True)
    return [
        row.split(",")[-1].strip()
        for row in raw.splitlines()
        if row and not row.startswith("#")
    ]


def read_frames(path, indices):
    wanted = sorted(set(indices))
    if not wanted:
        return {}
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        fail(f"OpenCV could not open: {path}")
    output = {}
    wanted_set = set(wanted)
    final_index = wanted[-1]
    index = 0
    while index <= final_index:
        ok, bgr = cap.read()
        if not ok:
            cap.release()
            fail(f"Could not decode frame {index} from {path}")
        if index in wanted_set:
            output[index] = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        index += 1
    cap.release()
    return output


def nearest_index(values, target):
    return min(range(len(values)), key=lambda index: abs(values[index] - target))


def font(size=18):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def make_grid(items, output, cols=5, cell_width=240, image_height=426):
    label_height = 50
    cell_height = image_height + label_height
    rows = math.ceil(len(items) / cols)
    grid = Image.new("RGB", (cols * cell_width, rows * cell_height), (18, 18, 18))
    draw = ImageDraw.Draw(grid)
    label_font = font(18)

    for position, item in enumerate(items):
        image = item["image"].copy()
        image.thumbnail((cell_width, image_height), Image.Resampling.LANCZOS)
        x = (position % cols) * cell_width
        y = (position // cols) * cell_height
        grid.paste(image, (x + (cell_width - image.width) // 2, y))
        color = (70, 220, 120) if item.get("eligible", True) else (185, 185, 185)
        draw.rectangle(
            (x, y, x + cell_width - 1, y + cell_height - 1),
            outline=color,
            width=3 if item.get("eligible", True) else 1,
        )
        draw.text((x + 7, y + image_height + 3), item["label1"], fill=color, font=label_font)
        draw.text((x + 7, y + image_height + 25), item["label2"], fill=(220, 220, 220), font=label_font)

    grid.save(output)


def trim_video(source, output, start, duration):
    # Preserve native timestamps; a frame may straddle the requested start.
    _, video, _ = probe(source)
    if video.get("pix_fmt") != "yuv420p":
        fail("V3 requires 8-bit yuv420p; refusing automatic pixel-format conversion")
    if abs(float(video.get("start_time", 0))) > 0.00001:
        fail("V3 currently requires a zero-based source video timeline")
    pts, _ = frame_pts(source)
    time_base = Fraction(video["time_base"])
    start_tick = round(Fraction(str(start)) / time_base)
    end_tick = round(Fraction(str(start + duration)) / time_base)
    if end_tick <= start_tick:
        fail("Requested range contains no source timeline ticks")
    start = float(start_tick * time_base)
    end = float(end_tick * time_base)
    duration = end - start
    source_ticks = [round(Fraction(str(value)) / time_base) for value in pts]
    first = max((i for i, tick in enumerate(source_ticks) if tick <= start_tick),
                default=0)
    source_indices = [i for i in range(first, len(pts))
                      if source_ticks[i] < end_tick]
    if not source_indices:
        fail("Requested range contains no source pictures")
    color_args = []
    for field, option in (("color_range", "-color_range"),
                          ("color_space", "-colorspace"),
                          ("color_transfer", "-color_trc"),
                          ("color_primaries", "-color_primaries"),
                          ("chroma_location", "-chroma_sample_location")):
        value = video.get(field)
        if value and value not in ("unknown", "unspecified", "reserved"):
            color_args += [option, value]
    output_path = Path(output)
    encoded_path = output_path.with_name(output_path.stem + ".encoded.mp4")
    if output_path.exists() or encoded_path.exists():
        fail("Refusing to overwrite an existing tail or intermediate export")
    # Keep the picture already on screen at the cut and its remaining interval.
    vf = (f"trim=start_frame={first}:end_frame={source_indices[-1] + 1},"
          f"setpts=max(PTS-{start_tick}\\,0)")
    af = f"atrim=start={start:.12f}:end={end:.12f},asetpts=PTS-STARTPTS"
    run([
        FFMPEG, "-hide_banner", "-loglevel", "error", "-n",
        "-noautorotate", "-i", source,
        "-map", "0:v:0", "-map", "0:a:0?", "-vf", vf, "-af", af,
        "-t", f"{duration:.12f}",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
        "-crf", "10", "-pix_fmt", "yuv420p", "-bf", "0",
        "-fps_mode", "passthrough", "-enc_time_base:v", str(time_base),
        "-video_track_timescale", str(time_base.denominator), *color_args,
        "-c:a", "aac", "-b:a", "192k",
        "-avoid_negative_ts", "disabled", "-movflags", "+faststart",
        str(encoded_path),
    ])
    # Bound the final packet's display duration; no second picture encoding.
    # This is not a stream-copy cut of the original non-keyframe source.
    duration_filter = f"setts=duration='min(DURATION,{duration:.12f}/TB-PTS)'"
    run([
        FFMPEG, "-hide_banner", "-loglevel", "error", "-n",
        "-i", str(encoded_path), "-map", "0", "-c", "copy",
        "-bsf:v", duration_filter,
        "-video_track_timescale", str(time_base.denominator),
        "-avoid_negative_ts", "disabled", "-movflags", "+faststart", output,
    ])
    _, result_video, result_duration = probe(output)
    result_pts, absolute_pts = frame_pts(output)
    expected_pts = [max(0.0, pts[i] - start) for i in source_indices]
    tolerance = max(float(time_base), 0.00001)
    if (len(result_pts) != len(expected_pts) or
            any(abs(a - b) > tolerance for a, b in zip(expected_pts, result_pts)) or
            abs(result_duration - duration) > tolerance or
            abs(absolute_pts[0]) > tolerance):
        fail("Tail pictures or timestamps differ from the requested source interval")
    if (result_video["width"], result_video["height"]) != (video["width"], video["height"]):
        fail("Tail dimensions differ from the source")
    packet_data = json.loads(run([
        FFPROBE, "-v", "error", "-select_streams", "v:0",
        "-show_packets", "-show_entries", "packet=pts_time,dts_time,flags",
        "-of", "json", output,
    ], capture=True))["packets"]
    if not packet_data or "K" not in packet_data[0].get("flags", ""):
        fail("Tail does not start with a keyframe")
    if any("D" in p.get("flags", "") or
           float(p.get("pts_time", -1)) < 0 or
           float(p.get("dts_time", -1)) < 0 for p in packet_data):
        fail("Tail contains discarded or negative-timestamp video packets")
    encoded_path.unlink()
    return start, end


def prepare(args):
    require_tools()
    source = str(Path(args.input).expanduser().resolve())
    if not os.path.isfile(source):
        fail(f"Input does not exist: {source}")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source_probe, source_video, source_duration = probe(source)

    explicit = args.cut_start is not None or args.cut_end is not None
    if explicit and (args.cut_start is None or args.cut_end is None):
        fail("--cut-start and --cut-end must be supplied together")

    if explicit:
        start = float(args.cut_start)
        end = float(args.cut_end)
        if start < 0 or end <= start or end > source_duration + 0.001:
            fail(f"Invalid cut range {start}–{end} for {source_duration:.3f}s video stream")
        analysis_clip = str(output_dir / "requested_cut.mp4")
        start, end = trim_video(source, analysis_clip, start, end - start)
        trimmed = True
        mode = "explicit-range"
    elif source_duration > 7.0:
        start = max(0.0, source_duration - 5.0)
        end = source_duration
        analysis_clip = str(output_dir / "tail_5s.mp4")
        start, end = trim_video(source, analysis_clip, start, 5.0)
        trimmed = True
        mode = "retain-ending"
    else:
        start = 0.0
        end = source_duration
        analysis_clip = source
        trimmed = False
        mode = "whole-source"

    analysis_probe, analysis_video, analysis_duration = probe(analysis_clip)
    relative_pts, absolute_analysis_pts = frame_pts(analysis_clip)
    source_relative_pts, source_absolute_pts = frame_pts(source)
    # Re-encoded video is not hash-identical. Preserve one-to-one source
    # frame identity through exact range membership and timestamp checks.
    first_source_frame = max(
        (index for index, value in enumerate(source_relative_pts)
         if value <= start + 0.000001), default=0)
    source_frame_numbers = [
        index for index in range(first_source_frame, len(source_relative_pts))
        if source_relative_pts[index] < end - 0.000001
    ]
    if len(source_frame_numbers) != len(relative_pts):
        fail("Tail frame count does not match the exact source range")
    timing_tolerance = max(float(Fraction(source_video["time_base"])), 0.00001)
    if any(abs(max(0.0, source_relative_pts[source_index] - start) - tail_pts) > timing_tolerance
           for source_index, tail_pts in zip(source_frame_numbers, relative_pts)):
        fail("Tail timing does not match source frames; refusing approximate mapping")
    source_eligible_start = max(start, end - 3.0)
    source_eligible_end = max(source_eligible_start, end - 0.5)
    analysis_source_frames = []
    for analysis_index, analysis_timestamp in enumerate(relative_pts):
        source_index = source_frame_numbers[analysis_index]
        source_timestamp = source_relative_pts[source_index]
        analysis_source_frames.append({
            "analysis_frame_number": analysis_index,
            "analysis_timestamp_seconds": analysis_timestamp,
            "source_frame_number": source_index,
            "source_timestamp_seconds": source_timestamp,
            "eligible": source_eligible_start <= source_timestamp < source_eligible_end,
        })
    eligible_rows = [row for row in analysis_source_frames if row["eligible"]]
    if not eligible_rows:
        fail("No source frames remain inside the eligible continuation window")
    eligible_start = eligible_rows[0]["analysis_timestamp_seconds"]
    first_excluded = next(
        (row for row in analysis_source_frames
         if row["source_timestamp_seconds"] >= source_eligible_end),
        None,
    )
    eligible_end = (
        first_excluded["analysis_timestamp_seconds"]
        if first_excluded else analysis_duration
    )

    targets = []
    cursor = 0.0
    while cursor < analysis_duration:
        targets.append(cursor)
        cursor += 0.25
    indices = [nearest_index(relative_pts, target) for target in targets]
    original_frames = read_frames(source, [source_frame_numbers[i] for i in indices])
    decoded = {i: original_frames[source_frame_numbers[i]] for i in indices}

    frames_dir = output_dir / "overview_frames"
    frames_dir.mkdir(exist_ok=True)
    grid_items = []
    samples = []
    for number, (target, index) in enumerate(zip(targets, indices), start=1):
        timestamp = relative_pts[index]
        frame_path = frames_dir / f"{number:02d}_t{timestamp:06.3f}_f{index:05d}.png"
        decoded[index].save(frame_path)
        mapping = analysis_source_frames[index]
        eligible = mapping["eligible"]
        grid_items.append({
            "image": decoded[index], "eligible": eligible,
            "label1": f"#{number:02d}  t={timestamp:.2f}s",
            "label2": f"frame {index}",
        })
        samples.append({
            "index": number, "target_seconds": target,
            "analysis_timestamp_seconds": timestamp,
            "analysis_frame_number": index,
            "source_frame_number": mapping["source_frame_number"],
            "source_timestamp_seconds": mapping["source_timestamp_seconds"],
            "eligible": eligible, "path": str(frame_path),
        })

    overview_grid = output_dir / "overview_grid.png"
    make_grid(grid_items, overview_grid)
    manifest = {
        "skill_version": "3.0.0",
        "appearance_acceptance": "not reviewed",
        "dreamina_acceptance": "not tested",
        "source_video": source,
        "source_video_stream_duration_seconds": source_duration,
        "source_video_stream": source_video,
        "analysis_clip": analysis_clip,
        "analysis_video_stream_duration_seconds": analysis_duration,
        "analysis_video": analysis_video,
        "normalization": {
            "mode": mode, "trimmed": trimmed,
            "source_start_seconds": start, "source_end_seconds": end,
        },
        "eligible_window": {
            "start_seconds": eligible_start,
            "end_exclusive_seconds": eligible_end,
            "excluded_final_seconds": 0.5,
            "source_start_seconds": source_eligible_start,
            "source_end_exclusive_seconds": source_eligible_end,
        },
        "analysis_source_frames": analysis_source_frames,
        "overview_grid": str(overview_grid),
        "overview_samples": samples,
    }
    manifest_path = output_dir / "analysis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "manifest": str(manifest_path), "analysis_clip": analysis_clip,
        "overview_grid": str(overview_grid), "mode": mode,
        "source_duration": source_duration, "analysis_duration": analysis_duration,
        "eligible_window": manifest["eligible_window"],
    }, indent=2))


def candidates(args):
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text())
    output_dir = manifest_path.parent
    analysis_clip = manifest["analysis_clip"]
    relative_pts, _ = frame_pts(analysis_clip)
    eligible = manifest["eligible_window"]
    low = max(eligible["start_seconds"], args.center - args.radius)
    high = min(eligible["end_exclusive_seconds"], args.center + args.radius)
    mappings = manifest["analysis_source_frames"]
    indices = [
        index for index, value in enumerate(relative_pts)
        if low <= value < high and mappings[index]["eligible"]
    ]
    if not indices:
        fail(f"No eligible frames around {args.center:.3f}s")
    original_frames = read_frames(manifest["source_video"],
                                  [mappings[i]["source_frame_number"] for i in indices])
    decoded = {i: original_frames[mappings[i]["source_frame_number"]] for i in indices}
    frames_dir = output_dir / "candidate_frames"
    frames_dir.mkdir(exist_ok=True)
    items = []
    rows = []
    for index in indices:
        timestamp = relative_pts[index]
        mapping = mappings[index]
        path = frames_dir / f"frame_{index:05d}_t{timestamp:.3f}.png"
        decoded[index].save(path)
        items.append({
            "image": decoded[index], "eligible": True,
            "label1": f"frame {index}", "label2": f"t={timestamp:.3f}s",
        })
        rows.append({
            "analysis_frame_number": index,
            "analysis_timestamp_seconds": timestamp,
            "source_frame_number": mapping["source_frame_number"],
            "source_timestamp_seconds": mapping["source_timestamp_seconds"],
            "path": str(path),
        })
    grid = output_dir / "candidate_grid.png"
    make_grid(items, grid, cols=min(6, len(items)), cell_width=220, image_height=391)
    candidate_manifest = {
        "analysis_manifest": str(manifest_path), "center_seconds": args.center,
        "radius_seconds": args.radius, "actual_start_seconds": low,
        "actual_end_exclusive_seconds": high, "candidate_grid": str(grid),
        "frames": rows,
    }
    candidate_path = output_dir / "candidate_manifest.json"
    candidate_path.write_text(json.dumps(candidate_manifest, indent=2) + "\n")
    print(json.dumps({
        "candidate_manifest": str(candidate_path), "candidate_grid": str(grid),
        "frame_count": len(rows), "first_frame": rows[0], "last_frame": rows[-1],
    }, indent=2))


def select(args):
    require_tools()
    manifest_path = Path(args.manifest).expanduser().resolve()
    candidate_path = Path(args.candidate_manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text())
    candidate_manifest = json.loads(candidate_path.read_text())
    matches = [row for row in candidate_manifest["frames"]
               if row["analysis_frame_number"] == args.frame]
    if not matches:
        fail(f"Frame {args.frame} is not present in the candidate manifest")
    candidate = matches[0]
    analysis_timestamp = float(candidate["analysis_timestamp_seconds"])
    eligible = manifest["eligible_window"]
    if not eligible["start_seconds"] <= analysis_timestamp < eligible["end_exclusive_seconds"]:
        fail(f"Frame {args.frame} lies outside the eligible window")
    source_index = int(candidate["source_frame_number"])
    exact_source_timestamp = float(candidate["source_timestamp_seconds"])
    source_cutoff = float(eligible["source_end_exclusive_seconds"])
    if exact_source_timestamp >= source_cutoff:
        fail("Selected source frame lies inside the excluded final 0.5 seconds")
    analysis_remaining = manifest["analysis_video_stream_duration_seconds"] - analysis_timestamp
    output_dir = manifest_path.parent
    output_frame = output_dir / "continuation_frame.png"
    run([
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
        "-i", manifest["source_video"],
        "-vf", f"select=eq(n\\,{source_index})",
        "-frames:v", "1", "-fps_mode", "passthrough", "-update", "1",
        str(output_frame),
    ])

    exported = cv2.imread(str(output_frame))
    candidate_image = cv2.imread(candidate["path"])
    if exported is None:
        fail("Exported continuation frame could not be decoded")
    height, width = exported.shape[:2]
    source_video = manifest["source_video"]
    expected_width = int(manifest["source_video"].get("width", width)) if isinstance(manifest["source_video"], dict) else width
    expected_height = int(manifest["source_video"].get("height", height)) if isinstance(manifest["source_video"], dict) else height
    # Dimensions are also available in the stored source_video stream object.
    source_stream = manifest.get("source_video_stream") or manifest.get("source_video")
    if isinstance(source_stream, dict):
        expected_width = int(source_stream.get("width", width))
        expected_height = int(source_stream.get("height", height))
    if (width, height) != (expected_width, expected_height):
        fail(f"Native dimension mismatch: got {width}x{height}, expected {expected_width}x{expected_height}")

    if candidate_image is None:
        fail("Selected candidate image could not be decoded")
    if candidate_image.shape != exported.shape:
        fail("Exported continuation frame does not exactly match candidate dimensions")
    mean_abs_diff = float(np.mean(np.abs(
        candidate_image.astype(np.int16) - exported.astype(np.int16)
    )))
    if not np.array_equal(candidate_image, exported):
        fail(
            "Exported continuation frame does not exactly match the selected "
            f"candidate pixels (mean absolute difference {mean_abs_diff:.9f})"
        )
    source_duration = manifest["source_video_stream_duration_seconds"]
    selection = {
        "source_video": manifest["source_video"],
        "analysis_clip": manifest["analysis_clip"],
        "eligible_window": eligible,
        "selection": {
            "analysis_frame_number": args.frame,
            "analysis_timestamp_seconds": analysis_timestamp,
            "analysis_seconds_remaining": analysis_remaining,
            "source_frame_number": source_index,
            "exact_source_timestamp_seconds": exact_source_timestamp,
            "source_video_seconds_remaining": source_duration - exact_source_timestamp,
            "output_frame": str(output_frame),
            "native_dimensions": {"width": width, "height": height},
            "candidate_export_mean_abs_pixel_difference": mean_abs_diff,
            "reason": args.reason,
        },
        "overview_grid": manifest["overview_grid"],
        "candidate_grid": candidate_manifest["candidate_grid"],
    }
    selection_path = output_dir / "selection.json"
    selection_path.write_text(json.dumps(selection, indent=2) + "\n")
    print(json.dumps({
        "selection": str(selection_path), "continuation_frame": str(output_frame),
        "analysis_timestamp": analysis_timestamp,
        "exact_source_timestamp": exact_source_timestamp,
        "analysis_seconds_remaining": analysis_remaining,
        "native_dimensions": selection["selection"]["native_dimensions"],
        "candidate_export_mean_abs_pixel_difference": mean_abs_diff,
    }, indent=2))


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    prep = commands.add_parser("prepare")
    prep.add_argument("--input", required=True)
    prep.add_argument("--output-dir", required=True)
    prep.add_argument("--cut-start", type=float)
    prep.add_argument("--cut-end", type=float)
    prep.set_defaults(function=prepare)

    cand = commands.add_parser("candidates")
    cand.add_argument("--manifest", required=True)
    cand.add_argument("--center", required=True, type=float)
    cand.add_argument("--radius", type=float, default=0.4)
    cand.set_defaults(function=candidates)

    choose = commands.add_parser("select")
    choose.add_argument("--manifest", required=True)
    choose.add_argument("--candidate-manifest", required=True)
    choose.add_argument("--frame", required=True, type=int)
    choose.add_argument("--reason", default="Selected after visual comparison of neighboring frames.")
    choose.set_defaults(function=select)
    return root


if __name__ == "__main__":
    args = parser().parse_args()
    args.function(args)
