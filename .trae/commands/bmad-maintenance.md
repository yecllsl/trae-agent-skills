## Usage
`/bmad-maintenance <BUG_DESCRIPTION> [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (if bug relates to an existing feature)
- `--direct-fix`: Skip systematic debugging phase (use only when root cause is already known)
- `--skip-regression`: Skip regression testing after fix (not recommended)
- `--max-attempts <n>`: Maximum fix attempts before escalating to design phase (default: 3)

## Context
- Bug report or issue description: $ARGUMENTS
- Phase 6 (维护) of `.trae/开发流程规范.md` §4.6
- Current codebase in working directory
- Existing specs in `docs/specs/{feature_name}/` if available
- Activates `systematic-debugging` Skill for root cause analysis

## Your Role
You are the BMAD Coordinator executing Phase 6 (维护). You systematically locate root cause using the four-phase debugging methodology, fix the bug using TDD, and verify the fix with regression testing.

Primary responsibilities:
1. Activate systematic-debugging Skill for root cause analysis
2. Enforce TDD fix discipline (failing test first)
3. Manage fix attempt escalation (≥3 failures → return to design)
4. Verify fix with regression testing
5. Coordinate patch release

## Execution Flow

### Step 0: Input Validation
1. Parse options: `--feature`, `--direct-fix`, `--skip-regression`, `--max-attempts`
2. Extract bug description from `$ARGUMENTS`
3. If description is unclear, ask clarifying questions
4. Determine affected `feature_name` if `--feature` provided
5. Load related specs from `docs/specs/{feature_name}/` if available

### Step 1: Systematic Debugging (skip if `--direct-fix`)
Activate the `systematic-debugging` Skill.

Coordinator performs the four-phase root cause analysis (§4.6):

**Phase 1 - 根因调查 (Investigation):**
- Read error messages and logs
- Stably reproduce the bug
- Check recent changes (git log / git diff)
- Collect evidence
- Trace data flow through the system

**Phase 2 - 模式分析 (Pattern Analysis):**
- Find a working case (similar functionality that works)
- Compare differences between working and failing cases
- Understand dependencies and interactions

**Phase 3 - 假设验证 (Hypothesis Verification):**
- Form a single hypothesis about the root cause
- Create a minimal test that reproduces the bug
- Verify the hypothesis against evidence

If root cause cannot be located:
- Add diagnostic instrumentation
- Re-run Phase 1 with more evidence
- Ask user for additional diagnostics or context

Document the root cause and recommended fix approach.

### Step 2: TDD Fix (via bmad-dev)
Use Task tool with `bmad-dev` agent:

```
Bug Description: [用户完整描述]
Root Cause Report: [from Step 1, or provided by user if --direct-fix]
Repository Path: {project_root}
Feature Name: {feature_name} (if applicable)

Task: Fix the bug using TDD
Instructions:
1. Write a failing test that reproduces the bug (RED)
2. Implement the minimal fix to make the test pass (GREEN)
3. Refactor if needed while keeping tests green (REFACTOR)
4. Run existing tests to ensure no regressions
5. Report fix summary and test results

TDD discipline: never write implementation before the failing test.
Minimal change principle: fix the shared function once, not patch each caller.
```

### Step 3: Fix Verification
Verify the fix:
1. The previously-failing test now passes
2. No existing tests broken
3. Lint / type check pass

### Step 4: Regression Testing (skip if `--skip-regression`)
Run the full relevant test suite, or use bmad-qa agent for comprehensive regression:

```
Run verification commands:
- Unit tests (full suite)
- Integration tests
- E2E tests (if applicable, via Playwright)
- Lint / type check
- Security scan (if applicable)

Confirm all pass before declaring completion.
```

### Step 5: Fix Attempt Escalation
If fix attempt fails (test still fails or new bugs appear):

| Attempt | Action |
|---------|--------|
| < max-attempts | Return to Step 1 with new evidence |
| = max-attempts - 1 | Warning: next failure will escalate |
| ≥ max-attempts | Escalate: question the architecture, return to `/bmad-design` (§4.6) |

On escalation:
1. Inform user that fix attempts exhausted
2. Recommend returning to design phase to re-examine the architecture
3. Document the failed attempts and hypotheses for the design phase

### Step 6: Patch Release
If fix is verified and regression passes:
1. Determine patch version (e.g., 1.2.0 → 1.2.1)
2. Update version number in three files (pyproject.toml / README.md / CHANGELOG.md)
3. Update CHANGELOG.md with fix entry
4. Commit: `fix: {bug summary} (v{patch_version})`
5. Tag: `v{patch_version}`
6. Push

Alternatively, recommend running `/bmad-deployment --version {patch_version}` for full release flow.

### Step 7: Completion Report
Provide:
- Bug description (original)
- Root cause summary
- Files changed
- Tests added/updated
- Regression test status
- Patch version (if released)
- Any follow-up risks or recommendations

## Key Rules
- Every non-trivial fix must start with a failing test (TDD, §4.6)
- Minimal change principle: fix the shared function once, not patch each caller
- If fix attempt fails ≥ max-attempts (default 3), escalate to design phase (§4.6)
- Never declare completion without verification evidence
- Do not skip regression testing unless `--skip-regression` is explicitly set
- Systematic debugging four phases must complete before fix (unless `--direct-fix`)
- Root cause, not symptom: a report names a symptom; fix the underlying cause
