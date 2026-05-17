# Isolation Strategies

The eval runner offers two strategies. The intent is identical in both: every eval starts from a clean slate so the result reflects the skill itself, not the host's accumulated state.

## What we are isolating from

- The user's global `~/.llm/AGENTS.md` (private global instructions)
- Any ancestor `AGENTS.md` in the project tree above the skill
- Auto-memory at `~/.llm/projects/.../memory/MEMORY.md`
- Cached settings, MCP configurations, IDE integrations
- Prior conversation context bleeding via the shell

## Authentication

The isolated `llm -p` subprocess needs to authenticate, but cannot read the host's `~/.llm/` (HOME is overridden) or the macOS Keychain (Keychain ACLs are scoped to the process that wrote the entry). The runner solves this in the parent process:

1. On macOS, read the OAuth credential JSON from the Keychain entry `automation assistant-credentials` via `security find-generic-password -s "automation assistant-credentials" -w`. This succeeds because the parent runs as the same user that wrote the entry.
2. Stage that JSON as `<workspace>/.home/.llm/.credentials.json` (local mode) or copy it into `/home/evaluator/.llm/.credentials.json` inside the container (Docker mode).
3. The subprocess reads `.credentials.json` exactly the way automation assistant normally does, with no other host config bleed.

If the parent has `LLM_PROVIDER_API_KEY` set, that env var is also forwarded — and it takes precedence over the Keychain credential. On non-macOS hosts, the Keychain step is skipped and `LLM_PROVIDER_API_KEY` is the only auth path.

## Docker (preferred)

A single image, `bmad-eval-runner:latest`, is built once per machine. It contains Node 20, automation assistant (via `npm install -g @llm-provider-ai/llm-code`), Python 3, and standard tools. The image is intentionally minimal — every eval starts from this baseline.

### Image build

`scripts/docker_setup.py --build` builds the image from `assets/Dockerfile`. This runs once. Re-runs are a no-op unless `--rebuild` is passed.

### Per-eval container

Each eval gets a fresh container:

```
docker run --rm \
  -v "<project-root>:/project:ro" \
  -v "<output-dir>/<eval-id>:/output" \
  -v "<fixtures-dir>:/fixtures:ro" \
  -e LLM_PROVIDER_API_KEY \
  -e EVAL_PROMPT \
  -e EVAL_ID \
  -e SKILL_PATH \
  bmad-eval-runner:latest \
  /bin/bash -c "/scripts/run_one_eval.sh"
```

Inside the container:

1. The project is copied from `/project` (read-only) to `/workspace` (writable, container-local). Copy is fast because the underlying layer is shared.
2. Fixtures are copied into `/workspace/fixtures/`.
3. `HOME` is `/home/evaluator`, an empty directory created by the image — no global `AGENTS.md`, no memory.
4. `llm -p "$EVAL_PROMPT" --output-format stream-json --verbose` runs at `/workspace`.
5. The stream-json transcript is captured to `/output/transcript.jsonl`. Any files the skill writes under `/workspace` are rsynced to `/output/artifacts/` after the run completes.
6. The container exits and is removed automatically.

The host then has `<output-dir>/<eval-id>/transcript.jsonl`, `<output-dir>/<eval-id>/artifacts/`, and timing data. Nothing on the host is touched.

### Why Docker is preferred

- The image is reproducible — every run starts from byte-identical state.
- `HOME` is genuinely empty, not just overridden.
- Filesystem isolation is real, not just convention.
- Network can be locked down (`--network=none` for trigger evals; full network for artifact evals that may need it).

## Local fallback

When Docker is unavailable, the runner falls back to per-eval temp directories under `~/bmad-evals/<run-id>/<eval-id>/`. Layout:

```
~/bmad-evals/<run-id>/<eval-id>/
  workspace/         # the eval's working directory
    .home/           # HOME override — empty .llm/ inside
    project/         # rsync'd copy of <project-root>
    fixtures/        # staged fixture files
  transcript.jsonl   # llm -p stream output
  artifacts/         # files LLM wrote under workspace/
  metrics.json
```

Per-eval invocation roughly:

```
HOME="$WORKSPACE/.home" \
AGENTS_CONFIG_DIR="$WORKSPACE/.home/.llm" \
LLM_PROVIDER_API_KEY="$LLM_PROVIDER_API_KEY" \
  llm -p "$EVAL_PROMPT" \
    --output-format stream-json --verbose \
    > transcript.jsonl
```

### Limitations of local mode

- `HOME` override prevents global `AGENTS.md` and memory loading, but ancestor discovery still happens from the workspace's cwd. If the workspace is created inside a directory tree that contains a `.llm/skills/` further up, the subprocess may discover those skills regardless of `HOME`. This matters most for trigger evals, where stray host skills can fire instead of the synthetic skill we're testing — **prefer Docker for trigger evals**, where filesystem isolation is real.
- Filesystem isolation is by convention only — the skill could write outside its workspace if it tries. We don't sandbox syscalls.
- Network is unrestricted.

Tell the user clearly when local mode is in use and that it is best-effort.

## Why a real skill, not a slash command, for trigger evals

The trigger runner stages a synthetic skill at `<workspace>/.llm/skills/<unique-name>/SKILL.md` — not at `.llm/commands/<name>.md`. Slash commands are user-invoked (`/<name>`); they do not surface as `Skill` tool calls and so a description placed there can never be observed firing the way a real skill would. LLM provider's reference `run_eval.py` uses the commands path and is known to report 0% trigger rates as a result. Placing the synthetic at `.llm/skills/` matches how real skills load and lets the detector observe genuine `Skill` (or `Read` of the synthetic SKILL.md) tool calls.

## Why not `--add-dir` only?

`llm -p --add-dir <skill>` would let LLM see the skill but would still inherit the user's `AGENTS.md` and memory from the cwd's ancestors. The whole point of this runner is to test the skill, not the host's accumulated state. So we always either Docker-isolate or temp-dir-isolate.

## Artifact retention

Run folders are never deleted by this skill. Disk management is the user's responsibility. The runner emits the run folder path on completion; users who want to clean up old runs can delete `~/bmad-evals/<run-id>/` directly.
