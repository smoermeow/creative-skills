# Dreamina Seedance Video

Version **1.1.0** · Video generation through an installed, authenticated `dreamina-canvas` CLI.

## Install this skill

Paste this installation request into your agent:

```text
Install the complete Dreamina Seedance Video skill from this GitHub folder into this agent’s supported skill directory, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/dreamina-seedance-video
```

### If you already use a protected orchestrator

```text
Install the complete Dreamina Seedance Video skill from this GitHub folder into my existing protected technique library, including all supporting files:
https://github.com/smoermeow/creative-skills/tree/main/video/dreamina-seedance-video

Register it with my existing orchestrator without changing the skill’s method, replacing the orchestrator or changing unrelated routes.
```

## Purpose

Generate Dreamina Seedance videos from an existing exact prompt, explicit settings, and optional ordered media references. The workflow prepares the request, obtains its exact credit quote, asks for **one paid-generation approval**, runs the approved node, and downloads and technically verifies the result.

This is an execution skill, not a prompt-development or creative-review method. It preserves your supplied prompt instead of rewriting or expanding it.

## Setup and prerequisites

- Use macOS or Linux with **`dreamina-canvas` already installed, available to the assistant, and authenticated to your own Dreamina account**. The package does not include the CLI, credentials, or an installer.
- Arrange installation and authentication through the CLI's own documentation before requesting a render. No installation command is supplied here because this package does not establish one.
- Have access and enough credits for the chosen model. The actual cost comes from quoting the prepared node, not an estimated price in this README.
- Supply accessible local media or existing Dreamina reference identities, a current project or project identity when none exists, and an agreed writable output path.
- The assistant must be able to run the CLI, download files, and check that video media is decodable and technically valid.

The model and limit information in [SKILL.md](SKILL.md) is a **bundled capability snapshot**, not a live API test. It documents `seedance_2.0` and `seedance_2.5`. Normal execution uses that snapshot; catalogue discovery is reserved for a CLI update or a rejected capability. Authentication status is checked after an authentication-related failure, not before every render.

## Required files

[SKILL.md](SKILL.md) is the required instruction file. It contains model limits, reference handling, the CLI procedure, approval rules, recovery, and verification. There are no required bundled templates or reference subdirectories.

Your input media and downloaded output are your own working files, not files shipped with this package.

## Inputs

Provide one complete render contract:

- Canonical model and **exact prompt text**, not merely a prompt-file path.
- Mode: `t2v`, `m2v`, or `first_last_frame`.
- Aspect ratio, resolution, duration in seconds, and output count.
- Every image, video, and audio reference in its intended order, with media type and role.
- Project identity if no current project exists, plus the destination for the downloaded result.

Reference roles determine mode:

| Input intent | Mode |
|---|---|
| No media references | `t2v` |
| General character, environment, style, composition, motion, or audio guidance | `m2v` |
| One image explicitly designated as the first frame | `first_last_frame` |
| Two images explicitly designated as first and last frames, in that order | `first_last_frame` |

Local media is uploaded during preparation. Existing Canvas nodes use `node:node_xxx`; uploaded resources use `res:resource-uuid`. Preserve the association between each original file, its media type, its position, and its returned identity. Ordinary guidance images must not silently become first/last frames.

## Copy-ready invocation example

Replace the example paths with accessible files and a writable destination. This is an **actual generation request**: it authorizes the non-paid preparation described below, including uploading the two supplied files.

```text
Use dreamina-seedance-video. Read this package's SKILL.md. Use the current Dreamina project; if none exists, ask me for its identity before preparing anything.

Model: seedance_2.5
Mode: m2v
Exact prompt: A lighthouse keeper raises a brass lantern as wind lifts the hem of her coat. The camera moves slowly toward her while rain crosses the harbor lights.
Ordered references:
1. image — assets/keeper.png — character and clothing guidance
2. video — assets/harbor-motion.mp4 — motion guidance
Settings: 16:9, 1080p, 10 seconds, 1 output
Download destination: renders/lighthouse.mp4

Preserve the exact prompt and reference order. This request authorizes reference uploads, creation of one unrun node, and its credit quote. Before spending credits, show the final exact prompt, ordered references and returned identities, model, mode, settings, and exact quoted total in one approval request. Do not run until I approve that payload and cost. After approval, confirm that exact credit ceiling, run the same node once, wait quietly, download, and technically verify the result. Do not automatically submit a replacement or paid retry.
```

## Expected output

1. **Before payment:** one compact approval showing the exact prompt, ordered reference mapping, model, mode, settings, and exact quoted credit total. At this point the references have been uploaded and the unrun node exists, but generation has not run.
2. **After approval:** confirmation of the approved credit ceiling, execution of that same node, and retention of its submit ID. There is no additional routine approval for upload, node creation, quoting, confirmation-token retrieval, waiting, downloading, or verification.
3. **On success:** a downloaded, non-empty, decodable video and a short report with actual model/mode/duration, ordered references, Node ID, submit ID, output path, dimensions, codec, and audio-stream presence when audio output was expected.

If you change the payload before running, the assistant updates the unrun node, obtains a new quote, and presents one replacement approval. The superseded payload must not run.

