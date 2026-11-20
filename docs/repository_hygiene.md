# Repository hygiene: slim clones, LFS media, release assets

Every human install and every bot run clones this repository. The default
`git clone` transfers the full pack history, so anything that ever landed in
git as a plain blob keeps punishing every clone forever. This runbook keeps
the clone lean without touching `sessions/` state or engagement history.

## What historically inflated the pack

`git rev-list --objects --all` shows one dominant offender: a
`lazysentinel.db` blob of ~98 MB (plus two older ~74 MB and ~55 MB
generations) and several ~45-52 MB generations of
`readmenator-graphrag/index.json` predating the LFS filter. Demo media
(`assets/demo/*.gif`, `readmenator.mp4`) is small per file but belongs in
LFS or release assets by policy, not as plain blobs.

## Policy (already enforced in `.gitattributes`)

1. Heavy binaries never re-enter history as plain objects: `*.mp4`, `*.gif`,
   `*.webm`, `*.mp3`, `*.db`, `*.sqlite*` and `readmenator-graphrag/**` are
   LFS-filtered.
2. Language statistics stay Python: `external/**`, `static/**`,
   `readmenator-agent/**`, `readmenator-wiki/**`, `readmenator-maps/**`,
   `readmenator-rules/**` and `parquets/**` are marked for linguist, so the
   GitHub bar reflects the source tree, not vendored JS or generated docs.
3. One-off demo media ships as a **release asset**, not a tracked file: the
   mp4 demo (gitignored at the root) is published on the release page and
   linked from the README media section instead of living in the tree.

## Safe, non-destructive reclaim

The loose-object area grows after heavy work sessions. Plain `git gc` keeps
the reflog (safe recovery points):

```bash
git gc
git count-objects -vH
```

To reclaim unreachable loose objects immediately (drops recovery points for
unreachable work — run it only with a clean worktree):

```bash
git reflog expire --expire-unreachable=now --all
git gc --prune=now
```

## One-time history rewrite (operator, destructive)

Removing the historic `lazysentinel.db` and pre-LFS `index.json` blobs
requires rewriting history. Coordinate with collaborators first:

```bash
git lfs migrate import --everything \
  --include="*.mp4,*.gif,*.db,*.sqlite*,readmenator-graphrag/index.json"
git push --force-with-lease origin dev
```

This moves every matching blob (all generations) into LFS, shrinking the
pack by the size of the offender list above. Old clones keep working
against the LFS backend; new clones stop downloading those bytes.

## Keeping it slim

- Never `git add` a database, capture or recording: campaign state lives in
  `sessions/` (gitignored) and evidence exports in `sessions/lazy/`.
- Screenshots and demos for the README: prefer the release page over the
  tree; only small, stable images (`<200 KB`) belong in `assets/`.
- Regenerate heavy generated artefacts (`readmenator-graphrag/`) locally
  with `readmenator . --rebuild` rather than committing new generations.
