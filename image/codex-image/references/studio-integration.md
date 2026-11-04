# Conditional Studio integration

Read this only when the user selects a Studio project output location. Do not search unrelated projects merely because an image prompt is provided.

Read that project's actual layout contract and applicable Studio generation-lifecycle skill before choosing paths or constructing manifests. This file does not replace their schema.

For a project requiring `_staging/`:
- Give each independently approvable output its own stage, even for identical prompts or paired quality tiers.
- Include the native image, exact prompt copy, and metadata receipt as persistent manifest items. A transformed derivative must never be the only retained/manifested image.
- Use unique final destination names. Verify every manifest source exists and that the prompt copy matches the exact submitted source.
- Check native dimensions and complete ordered receipt references for each variant independently.

Approval can move manifest items to their declared destinations; rejection can archive a stage. Before reporting a path in a later turn, resolve its current existing location through the manifest/ledger and filesystem. Do not recreate a stale staging path merely to make a previous answer true.

For a requested rerun of an approved prompt, read its current approved destination and adjacent receipt. Preserve prompt text and ordered references except for explicit changes. Create a new stage with unique destinations rather than overwriting an approved generation. Return the actual current prompt path when asked for it.
