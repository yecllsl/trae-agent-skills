## Usage
`/bmad-deployment [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (required if not inferable from context)
- `--version <x.y.z>`: Specify version number (e.g., `1.2.0`). If omitted, prompt user.
- `--skip-ci`: Skip CI/CD wait (not recommended; assumes CI already green)

## Context
- Phase 5 (部署) of `.trae/开发流程规范.md` §4.5
- Prerequisites: tested code from `/bmad-testing` + `05-test-report.md`
- Orchestrator (Coordinator) directly executes git/CI operations
- Version consistency required across pyproject.toml / README.md / CHANGELOG.md

## Your Role
You are the BMAD Coordinator executing Phase 5 (部署). You perform version consistency checks, update CHANGELOG, execute git operations, wait for CI, and create tags.

Primary responsibilities:
1. Verify testing prerequisites exist
2. Enforce version number consistency across three files
3. Update CHANGELOG.md (mandatory)
4. Execute git operations safely (no force-push main, no skip CI for tags)
5. Wait for CI to pass before tagging
6. Enforce merge gate (门控4: 合并前)

## Execution Flow

### Step 0: Input Validation
1. Parse options: `--feature`, `--version`, `--skip-ci`
2. Determine `feature_name` from `--feature` option or context
3. Verify prerequisites exist:
   - `docs/specs/{feature_name}/05-test-report.md` (test report)
   - If missing, report error and recommend running `/bmad-testing` first
4. Determine version number from `--version` or prompt user

### Step 1: Version Consistency Check
Verify version number is identical across:
- `pyproject.toml` (or `package.json` / `Cargo.toml` as applicable)
- `README.md` (version badge or section)
- `CHANGELOG.md` (new version entry)

If inconsistent, update all three to the target version before proceeding.

### Step 2: Update CHANGELOG.md (Mandatory)
Add a new version entry to CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [{version}] - {YYYY-MM-DD}

### 新增
- [Feature summary from PRD]

### 变更
- [Change summary from development]

### 修复
- [Bug fixes from QA phase]
```

Pull change details from:
- `01-product-requirements.md` (new features)
- `04-dev-reviewed.md` (implementation changes)
- `05-test-report.md` (bug fixes)

### Step 3: Verification Gate (门控4: 合并前)
Confirm all checks pass:

| Check | Requirement |
|-------|-------------|
| Verification evidence fresh | Tests run within last 5 minutes |
| All reviews passed | `04-dev-reviewed.md` returns Pass |
| Security scan | bandit no Critical/High |
| Version number consistent | Three files match |
| CHANGELOG updated | Contains this version's changes |

If any check fails, block deployment and recommend returning to the relevant phase.

### Step 4: Git Operations
Execute git operations safely:

```powershell
# Stage specific files (NEVER use git add -A)
git add {specific files}

# Commit with version tag
git commit -m "feat: {feature description} (v{version})"

# Push to remote
git push origin main
```

Branch strategy (single-person mode):
| Scenario | Strategy |
|----------|---------|
| Small change | Direct on main |
| Large feature | feature branch → `git merge --squash` |
| Forbidden | force-push main, skip CI for tags |

### Step 5: CI/CD Wait (skip if `--skip-ci`)
1. Monitor CI pipeline status
2. Wait for all checks to pass (green)
3. If CI fails:
   - Analyze failure cause
   - Fix and re-push
   - Re-wait for CI

Use `gh run watch` or equivalent to monitor CI status.

### Step 6: Tag and Release
Only after CI passes:

```powershell
# Create annotated tag
git tag -a v{version} -m "Release v{version}: {feature summary}"

# Push tag
git push origin v{version}
```

If applicable, create a GitHub Release via `gh release create`.

### Step 7: Rollback Plan (if needed)
If release fails post-tag:
1. Use Git revert to roll back
2. Re-publish with patch version
3. Document rollback in release report

### Step 8: Release Report (large versions only)
For major versions, save release report to `docs/devops/发布报告_{version}.md`:
- Version summary
- Change list
- Test results
- Known issues
- Rollback procedure

### Step 9: Completion Report
Provide:
- Feature name and version number
- Tag created: `v{version}`
- CI status: green
- CHANGELOG updated: yes
- Release report path (if large version)
- Recommendation: feature complete. For future bugs, run `/bmad-maintenance`.

## Key Rules
- Testing prerequisites must exist before running (门控4)
- Version number must be consistent across three files (门控4)
- CHANGELOG.md update is mandatory (门控4)
- Verification evidence must be fresh (< 5 minutes) (门控4)
- Never force-push main, never skip CI for tags
- Stage specific files, never `git add -A` (security)
- Wait for CI green before tagging
- All reviews must pass before deployment (门控4)
