# AGENTS.md — Trae Agent Skills

This repo is a collection of [Trae IDE](https://www.trae.ai/) agent skills, stored under `.agents/skills/`. Currently contains one skill: `coros-activity-downloader` (v2.0.0).

## Repo structure

```
.agents/skills/<skill-name>/    # skill defs (installed into ~/.trae/skills/)
docs/                           # development guide + template
scripts/validate-skills.py      # validates all skills
```

Each skill **must** contain: `README.md`, `SKILL.md`, `scripts/` with at least one executable script.

## Validation

- Run `python scripts/validate-skills.py` to check all skills.
- Run `python scripts/validate-skills.py -s <skill-name>` for a single skill.
- Run `python scripts/validate-skills.py -v` for verbose output.
- Validates: required files, SKILL.md frontmatter (name + description fields), required sections (Purpose, Prerequisites, Usage, Architecture, Error Handling), scripts/ presence.

## SKILL.md requirements

Must start with:
```yaml
---
name: "skill-name"
description: "short desc (50 chars max)"
---
```
Then contain exactly these H2 sections: `## Purpose`, `## Prerequisites`, `## Usage`, `## Architecture`, `## Error Handling`.

## Style conventions

- Skill dirs: kebab-case (e.g., `coros-activity-downloader`)
- Script filenames: snake_case (e.g., `download_coros.py`)
- Python: PEP 8, snake_case functions, 4-space indent, Chinese comments for complex logic
- PR title format: `Add skill: skill-name vX.X.X`
- Commit format: `Add skill: skill-name v1.0.0`
- CLI scripts should support both human-readable and `--json-output` modes where applicable.

## Environment

- Python 3.6+ for Python skills (`.venv/` virtual env in root, gitignored)
- Chrome DevTools MCP configured in `.trae/mcp.json` (disabled by default)
- `.trae/cache/`, `.trae/logs/` are gitignored
- Sensitive files (`.env`, `*.pem`, `*.key`, `credentials.json`) are gitignored
- Downloaded data formats (`.fit`, `.gpx`, `.tcx`) and `download/`, `backup/` dirs are gitignored