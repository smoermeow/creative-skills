#!/usr/bin/env python3
"""Generate images with OpenAI Codex OAuth + gpt-image-2.

Skill-local canonical script for Hermes `codex-image`.

Supports:
- prompt text or prompt .txt path
- ordered local reference images via --ref, --refs-json, or --refs-from-prompt
- Codex OAuth token from Hermes
- gpt-image-2 low/medium/high tiers, default medium
- metadata JSON next to output
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import mimetypes
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

HERMES_REPO = Path(os.environ.get('HERMES_REPO', str(Path.home()/'.hermes/hermes-agent'))).expanduser()
DEFAULT_OUT_DIR = Path.cwd()/'codex-image-output'
DEFAULT_MODEL = "gpt-image-2-medium"
DEFAULT_SIZE = "1024x1024"


def load_openai_codex_plugin():
    sys.path.insert(0, str(HERMES_REPO))
    plugin_path = HERMES_REPO / "plugins/image_gen/openai-codex/__init__.py"
    spec = importlib.util.spec_from_file_location("openai_codex_image", plugin_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load openai-codex image plugin from {plugin_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_ref_arg(value: str) -> tuple[str, Path]:
    if "=" in value:
        label, path = value.split("=", 1)
    elif ":" in value:
        label, path = value.split(":", 1)
    else:
        raise ValueError(f"Reference must be LABEL=PATH, got: {value}")
    return label.strip(), Path(path.strip())


def extract_refs_from_prompt(prompt: str) -> list[tuple[str, Path]]:
    """Extract ordered refs from prompt blocks containing `- image N:` and `Path: `...``."""
    refs: list[tuple[int, str, Path]] = []
    pattern = re.compile(
        r"-\s*image\s+(\d+)\s*:\s*([^\n]+)\n(?:.*?\n)*?\s*Path:\s*`([^`]+)`",
        re.IGNORECASE,
    )
    for m in pattern.finditer(prompt):
        n = int(m.group(1))
        label = f"image {n}: {m.group(2).strip()}"
        path = Path(m.group(3).strip())
        refs.append((n, label, path))
    refs.sort(key=lambda item: item[0])
    return [(label, path) for _n, label, path in refs]


def load_refs(args: argparse.Namespace, prompt: str) -> list[tuple[str, Path]]:
    refs: list[tuple[str, Path]] = []

    if args.refs_from_prompt:
        refs.extend(extract_refs_from_prompt(prompt))

    for item in args.ref or []:
        refs.append(parse_ref_arg(item))

    if args.refs_json:
        data = json.loads(Path(args.refs_json).read_text(encoding="utf-8"))
        for entry in data:
            refs.append((str(entry["label"]), Path(entry["path"])))

    seen: set[Path] = set()
    deduped: list[tuple[str, Path]] = []
    for label, path in refs:
        resolved = path.expanduser()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not resolved.exists():
            raise FileNotFoundError(f"Reference missing: {label} -> {resolved}")
        deduped.append((label, resolved))
    return deduped


def data_url_for(path: Path, cache_dir: Path | None = None) -> str:
    """Return a data URL for a local image, optionally using a file cache.

    Cache key includes path, size, and mtime. This avoids repeated base64 encoding
    for repeated runs while preserving correctness if files change.
    """
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    stat = path.stat()
    key_raw = f"{path.resolve()}|{stat.st_size}|{stat.st_mtime_ns}"
    key = hashlib.sha256(key_raw.encode("utf-8")).hexdigest()

    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{key}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            if cached.get("path") == str(path.resolve()) and cached.get("data_url"):
                return str(cached["data_url"])

    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    data_url = f"data:{mime};base64,{b64}"

    if cache_dir:
        cache_path.write_text(json.dumps({"path": str(path.resolve()), "data_url": data_url}), encoding="utf-8")

    return data_url


def build_content(prompt: str, refs: list[tuple[str, Path]], cache_dir: Path | None) -> list[dict[str, Any]]:
    if refs:
        reference_order = "\n".join(f"- {label}: {path}" for label, path in refs)
        text = (
            "Use the attached reference images in exactly this order. "
            "The textual image numbering in the prompt corresponds to this attachment order:\n"
            f"{reference_order}\n\n"
            "Now generate the image from this prompt:\n\n"
            f"{prompt}"
        )
    else:
        text = prompt

    content: list[dict[str, Any]] = [{"type": "input_text", "text": text}]
    for _label, path in refs:
        content.append({"type": "input_image", "image_url": data_url_for(path, cache_dir), "detail": "high"})
    return content


def _iter_sse_json(response: Any):
    event_name = None
    data_lines: list[str] = []

    def flush():
        nonlocal event_name, data_lines
        if not data_lines:
            event_name = None
            return None
        raw = "\n".join(data_lines).strip()
        event = event_name
        event_name = None
        data_lines = []
        if not raw or raw == "[DONE]":
            return None
        payload = json.loads(raw)
        if isinstance(payload, dict) and event and "type" not in payload:
            payload["type"] = event
        return payload

    for line in response.iter_lines():
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="replace")
        line = str(line)
        if line == "":
            payload = flush()
            if payload is not None:
                yield payload
            continue
        if line.startswith(":"):
            continue
        if line.startswith("event:"):
            event_name = line[len("event:"):].strip()
        elif line.startswith("data:"):
            data_lines.append(line[len("data:"):].lstrip())
    payload = flush()
    if payload is not None:
        yield payload


def _extract_image_b64(value: Any) -> str | None:
    found = None
    if isinstance(value, dict):
        if value.get("type") == "image_generation_call":
            result = value.get("result")
            if isinstance(result, str) and result:
                found = result
        partial = value.get("partial_image_b64")
        if isinstance(partial, str) and partial:
            found = partial
        for child in value.values():
            nested = _extract_image_b64(child)
            if nested:
                found = nested
    elif isinstance(value, list):
        for child in value:
            nested = _extract_image_b64(child)
            if nested:
                found = nested
    return found


def quality_from_model(model: str, fallback: str) -> str:
    if model.endswith("-low"):
        return "low"
    if model.endswith("-medium"):
        return "medium"
    if model.endswith("-high"):
        return "high"
    return fallback


def generate(args: argparse.Namespace) -> tuple[Path, Path]:
    mod = load_openai_codex_plugin()
    token = mod._read_codex_access_token()
    if not token:
        raise RuntimeError("Could not initialize Codex token. Run: hermes auth codex")

    import httpx
    from agent.auxiliary_client import _codex_cloudflare_headers

    prompt_path = Path(args.prompt)
    prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else args.prompt
    refs = load_refs(args, prompt)
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    content = build_content(prompt, refs, cache_dir)

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    stem_base = args.name or (prompt_path.stem if prompt_path.exists() else "codex_image")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{stem_base}_{args.model}_{stamp}" if args.timestamp else f"{stem_base}_{args.model}"
    out_path = out_dir / f"{stem}.png"
    meta_path = out_dir / f"{stem}_meta.json"

    quality = quality_from_model(args.model, args.quality)
    if quality == "low" and not args.allow_low:
        raise RuntimeError("Low quality requested but --allow-low was not passed. Default/approved quality is medium.")

    payload = {
        "model": mod._CODEX_CHAT_MODEL,
        "store": False,
        "instructions": mod._CODEX_INSTRUCTIONS,
        "input": [{"type": "message", "role": "user", "content": content}],
        "tools": [{
            "type": "image_generation",
            "model": mod.API_MODEL,
            "size": args.size,
            "quality": quality,
            "output_format": "png",
            "background": "opaque",
            "partial_images": 1,
        }],
        "tool_choice": {
            "type": "allowed_tools",
            "mode": "required",
            "tools": [{"type": "image_generation"}],
        },
        "stream": True,
    }

    headers = _codex_cloudflare_headers(token)
    headers.update({
        "Accept": "text/event-stream",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })

    image_b64 = None
    timeout = httpx.Timeout(args.timeout, connect=30.0, read=args.timeout, write=60.0, pool=30.0)
    try:
        with httpx.Client(timeout=timeout, headers=headers) as http:
            with http.stream("POST", f"{mod._CODEX_BASE_URL}/responses", json=payload) as response:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    exc.response.read()
                    body = exc.response.text[:1000]
                    raise RuntimeError(f"Codex Responses API returned HTTP {exc.response.status_code}: {body}") from exc

                for event in _iter_sse_json(response):
                    etype = event.get("type", "unknown") if isinstance(event, dict) else "unknown"
                    if etype not in {"response.output_text.delta"}:
                        summary = ""
                        if isinstance(event, dict):
                            if event.get("error"):
                                summary = f" error={event.get('error')}"
                            elif event.get("status"):
                                summary = f" status={event.get('status')}"
                        print(f"event: {etype}{summary}", flush=True)
                    found = _extract_image_b64(event)
                    if found:
                        image_b64 = found
                        print(f"image event received: {etype}", flush=True)
    except Exception as exc:
        if image_b64:
            print(f"stream ended with {type(exc).__name__} after image data; saving latest image", flush=True)
        else:
            raise

    if not image_b64:
        raise RuntimeError("No image result returned")

    out_path.write_bytes(base64.b64decode(image_b64))
    meta = {
        "provider": "openai-codex",
        "model": args.model,
        "api_model": mod.API_MODEL,
        "size": args.size,
        "quality": quality,
        "prompt": str(prompt_path) if prompt_path.exists() else "inline",
        "references": [{"label": label, "path": str(path)} for label, path in refs],
        "output": str(out_path),
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out_path, meta_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image with Codex OAuth + gpt-image-2 and optional local references.")
    parser.add_argument("--prompt", required=True, help="Prompt text or path to a prompt .txt file.")
    parser.add_argument("--refs-from-prompt", action="store_true", help="Extract ordered references from `- image N:` / `Path: `...`` blocks in the prompt.")
    parser.add_argument("--ref", action="append", help="Reference image as LABEL=PATH. Repeat for multiple refs.")
    parser.add_argument("--refs-json", help="JSON list of {label, path} reference images.")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=["gpt-image-2-low", "gpt-image-2-medium", "gpt-image-2-high"])
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--allow-low", action="store_true", help="Required if --model gpt-image-2-low or --quality low is used.")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Use 1024x1024 for 1:1 1K.")
    parser.add_argument("--out-dir", help="Output directory.")
    parser.add_argument("--name", help="Output filename stem.")
    parser.add_argument("--cache-dir", default='', help="Cache data URLs by path/mtime/size. Pass empty string to disable.")
    parser.add_argument("--timeout", type=float, default=600.0, help="HTTP read timeout seconds.")
    parser.add_argument("--timestamp", action=argparse.BooleanOptionalAction, default=True, help="Append timestamp to output filename.")
    args = parser.parse_args()

    if args.cache_dir == "":
        args.cache_dir = None

    out, meta = generate(args)
    print(f"OUTPUT {out}")
    print(f"META {meta}")


if __name__ == "__main__":
    main()
