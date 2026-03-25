# Lessons

## Patterns To Remember

- Prefer small, targeted changes over broad refactors.
- Verify behavior with tests or direct evidence before marking work done.
- Capture repeated mistakes immediately so the same issue does not recur.
- If a fix feels fragile, stop and look for the simpler durable solution.

## Recent Corrections

- None yet.
- When testing helpers that validate config, patch the real source module (`src.config`) rather than only a re-exported constant in a downstream module.
- Clean up generated dependency trees after local installs before checking worktree status so untracked noise does not hide the real changes.
