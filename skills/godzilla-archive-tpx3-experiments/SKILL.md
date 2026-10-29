---
name: godzilla-archive-tpx3-experiments
description: Audit and compress LumaCam/NCI TPX3 experiments in raw/experiment/run folders or the legacy tpx3Files layout on godzilla. Create verified .tar.gz archives, retain originals by default, and support explicitly authorized source removal after verification. Use for TPX3 compression, archiving, or freeing space, including exclusion of ongoing acquisitions.
---

# Archive TPX3 Experiment Folders

Use `scripts/archive_tpx3_experiments.sh` for deterministic audit and execution. Compression retains originals by default. Source deletion requires explicit authorization and `--delete-sources`; an instruction not to delete files overrides any space-saving workflow.

## Layout and selection

Inspect the current filesystem before describing or selecting targets; do not reuse an earlier conversation's layout without checking. The current proposal convention is:

```text
proposal/raw/                         # --root
├── experiment_name/                 # exact selected target
│   ├── run_00000/
│   │   ├── timestamp_000000.tpx3
│   │   └── timestamp_000001.tpx3
│   └── run_00001/
│       └── timestamp_000000.tpx3
├── .legacy_intermediates/            # excluded
└── .recycle/                         # excluded
```

Experiment and reference measurements can both be immediate experiment folders under `raw`; do not assume separate `experiment/` and `reference/` branches or a `tpx3Files` folder within each run. Run names may include the full experiment name, continuation names, or shorter names. Preserve actual names and paths.

The legacy `proposal/data/experiments/tpx3Files/<experiment>/...` layout remains supported by using that `tpx3Files` directory as `--root`. No folder renaming is needed. Each archive is created beside its source as `<root>/<experiment>.tar.gz` and contains `<experiment>/...`, so extraction into the root restores the hierarchy.

Hidden directories, including `.legacy_intermediates` and `.recycle`, are not experiment targets and are rejected by the script. If the user requests their archival, audit them separately and prepare an explicit plan for their distinct layout; do not silently include or discard them.

## Workflow

1. Resolve the absolute `raw` or legacy `tpx3Files` root. Enumerate immediate experiments, existing/partial archives, sizes, file counts, and newest writes.
2. Resolve an exact inclusion list. Never use globs or partial experiment names. Explicitly omit ongoing or user-excluded experiments and hidden directories.
3. Run the script without `--execute`. Use the same retention options intended for execution. Report empty/nearly empty folders, recent activity, source sizes, archive conflicts, and free space before changing data.
4. Stop for user direction when a folder is empty or scientifically suspicious. For removal of an empty experiment across the proposal layout, use `godzilla-remove-lumacam-experiment`; do not remove only its raw-data directory.
5. Keep each source grouping at or below 1,000,000,000,000 bytes. Split larger experiments at reviewed run-directory boundaries as described below.
6. Once compression is authorized, launch detached with reduced CPU and I/O priority. Preserve any existing no-deletion instruction. Use `--delete-sources` only when source removal is explicitly authorized for the selected targets.
7. Monitor until `ALL COMPLETE`. Report `ARCHIVE COMPLETE`, errors, retained or removed sources, partial/final archives, and archive sizes. Retaining originals consumes additional disk space; do not report it as released space.

## Audit and execution

Audit exact immediate experiment names:

```bash
<skill-dir>/scripts/archive_tpx3_experiments.sh \
  --root /absolute/proposal/raw \
  -- experiment_one experiment_two
```

Default mode is read-only. The script refuses symlinked roots/targets, hidden targets, paths outside the immediate root, empty sources, archive conflicts, recent writes, and oversized sources. Retention mode budgets free space for all selected archives using total uncompressed bytes plus overhead; removal mode budgets for the largest sequential archive. Do not enable deletion just to pass the free-space check. If space is insufficient, reduce the explicitly selected batch or arrange another destination through a reviewed wrapper.

Choose priorities according to acquisition state:

- No live acquisition on the filesystem: `ionice -c 2 -n 7 nice -n 10`, normally 16 `pigz` threads.
- Live acquisition on the same filesystem: exclude it by exact name and use `ionice -c 3 nice -n 15`, normally 8 threads. Warn that compression can still reduce acquisition headroom.

Example retaining all originals:

```bash
screen -dmS tpx3_archive_job bash -lc \
  'exec ionice -c 2 -n 7 nice -n 10 <skill-dir>/scripts/archive_tpx3_experiments.sh \
    --execute --threads 16 \
    --root /absolute/proposal/raw \
    --log /absolute/proposal/compression_tpx3_experiments.log \
    -- experiment_one experiment_two'
```

For explicitly authorized removal, add `--delete-sources` to both audit and execution commands. Each source is removed only after its archive is synced, fully read back with `tar -tzf`, and entry count and source metrics still match. This checks readability and counts/sizes; it is not a cryptographic comparison of every source file. Treat source removal as permanent.

Use `--replace-partials` only when removal of the stale partial is authorized and no archive process owns it. Never move a newly appearing final archive until its `ARCHIVE COMPLETE` line is present.

During `VERIFY START`, the `.tar.gz.partial` file stops growing while the entire archive is decompressed and listed. This is expected; do not interrupt merely because its size is stationary.

## Oversized experiments

Keep each source grouping at or below 1 TB for PSI/SciCat handling:

1. Require that an oversized experiment contains only immediate run directories and no loose files; otherwise review those files before defining parts.
2. Inspect the actual run names and acquisition order. Use fixed-width name sorting only when it matches chronology; continuation names can reset run counters.
3. Partition runs into contiguous groups whose uncompressed file totals are each at most 1,000,000,000,000 bytes. Stop for a separate plan if any single run exceeds the limit.
4. Name archives with explicit part and unambiguous run ranges, for example `exp004_part1_00000-00035.tar.gz`. Record full run names when counters repeat across continuations.
5. Store original experiment/run paths inside every archive so extracting all parts reconstructs the experiment directory.
6. Verify and sync each part, retaining all originals by default. Only with explicit source-removal authorization may the wrapper delete the verified part's selected run directories, then remove the experiment parent with `rmdir` after all parts pass and it is empty.

Use a reviewed proposal-specific wrapper for split execution; the bundled exact-folder script deliberately refuses oversized experiments rather than guessing scientific boundaries. Apply the same source-retention policy and free-space accounting to the wrapper.

## Safety invariants

- Preserve `.gitkeep`, proposal documentation, metadata, logs, software, processing parameters, and every non-target experiment.
- Archive all files inside each selected experiment directory, preserving run paths; never alter `.tpx3` contents or flatten runs.
- Do not infer that a folder is disposable from size alone.
- Keep source data whenever creation, sync, verification, or consistency checks fail.
- Never overwrite a final archive. Keep original sources unless their removal is explicitly authorized.
