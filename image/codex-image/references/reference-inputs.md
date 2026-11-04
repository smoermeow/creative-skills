# Reference inputs

## Choose one attachment mode

1. A user-specified list or corrected order: repeated `--ref 'image N: Role=/absolute/path.png'`, preserving exact order and labels.
2. A rerun with the same references: reuse the preceding receipt's ordered list and attachment mode unless the user changes it.
3. A prompt intentionally serving as its own attachment manifest: `--refs-from-prompt`.
4. An existing JSON manifest: `--refs-json <file>`, containing `[{"label": "image 1: Identity", "path": "/absolute/path.png"}]`.

Do not combine modes. The adapter merges their inputs and removes repeated paths, so using the same file in two intended slots will not preserve both slots. Surface this limitation instead of claiming exact attachment fidelity.

## Prompt-manifest syntax

The parser recognizes blocks shaped like:

```text
- image 1: Character identity
  Path: `/absolute/path/character.png`
```

It sorts these by image number. A line such as `Reference image 1: /path/image.png` is text only, not an attachment. Use explicit refs rather than rewriting an approved prompt merely to fit the parser.

For explicit refs, the authored creative prompt needs role descriptions, not filesystem `Path:` blocks. The current adapter itself adds attachment labels AND paths to the submitted text; do not claim filesystem paths are excluded from the entire request.

## Before and after the call

Verify each intended local file exists. A filename/hash resemblance does not establish identical bytes: do not silently replace a missing original with an optimized copy or recreate its cache path. Obtain the actual source or approval for substitution.

When removing references, inspect the prompt for stale image numbers and role descriptions as well as removing attachments. Apply only the authorized cleanup, preserving the original approved prompt as a separate version when edits are needed. Renumber surviving roles consistently with the actual attachment order.

After generation, read the receipt's `references` array and compare every label/path against the intended ordered list. Text in the prompt, filenames, and plausible output content do not prove attachment success.
