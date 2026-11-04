# Installation and profile troubleshooting

## Installation checks

The bundled adapter currently expects a Hermes source tree and its `plugins/image_gen/openai-codex/__init__.py` through the script's `HERMES_REPO` constant, and imports `agent.auxiliary_client`. This is an installation dependency, not a self-contained HTTP client. Confirm that configured source path exists and the selected interpreter has the required imports and `httpx` before a generation call. Do not confuse a missing plugin path with a prompt or OAuth failure.

Pass an explicit `--out-dir` and either a writable `--cache-dir` or `--cache-dir ''`; the adapter's built-in output/cache paths are installation-specific. Do not silently create old machine mounts. Do not create an alternative generation script to work around an unconfigured installation.

## Attribute the failure first

Distinguish:
- the intended Hermes profile and actual `HERMES_HOME`;
- the running gateway process and bot identity, if relevant;
- main chat-provider authentication versus Codex image authentication;
- the skill/script loaded by this session versus a recently installed copy.

Use current Hermes documentation and installed CLI help for diagnostic/auth commands rather than assuming historical command syntax. Inspect logs and safe credential metadata only; never print tokens or copy an entire auth store.

Expired credentials/401, quota exhaustion/429, missing source paths, and cached skill resolution are different failures. Skill copying does not copy OAuth state. Shared or copied credentials can become stale after refresh rotation; establish the actual store and any shadowing from current evidence before starting a login flow.

A running session can retain an older skill catalog. Verify the exact loaded path and use the supported reload/fresh-session mechanism before blaming newly installed files.

Do not restart gateways, edit auth, synchronize secrets, or start login flows without approval. If two gateways share a bot identity, correlate logs/timestamps and attribute artifacts before stopping either one. After an approved repair, verify the exact affected profile; a billable/provider request still needs authorization.
