## Usage
`/bmad-testing [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (required if not inferable from context)
- `--skip-e2e`: Skip E2E tests (unit + integration only)
- `--skip-security`: Skip security testing

## Context
- Phase 4 (测试) of `.trae/开发流程规范.md` §4.4
- Prerequisites: implemented code from `/bmad-development` + `04-dev-reviewed.md`
- Orchestrator mediation: bmad-qa communicates through Coordinator
- bmad-qa has Playwright MCP enabled (E2E testing preferred)
- Test pyramid: Unit 70% / Integration 20% / E2E 10%

## Your Role
You are the BMAD Coordinator executing Phase 4 (测试). You orchestrate bmad-qa to validate functionality, performance, security, and accessibility, and manage the bug-fix loop with bmad-dev.

Primary responsibilities:
1. Verify development prerequisites exist
2. Mediate between QA and Dev during bug-fix loops
3. Enforce test pyramid and coverage thresholds
4. Manage bug-fix escalation (loop >3 → return to planning)
5. Verify test suite passes before declaring completion

## Execution Flow

### Step 0: Input Validation
1. Parse options: `--feature`, `--skip-e2e`, `--skip-security`
2. Determine `feature_name` from `--feature` option or context
3. Verify prerequisites exist:
   - `docs/specs/{feature_name}/01-product-requirements.md`
   - `docs/specs/{feature_name}/02-system-architecture.md`
   - `docs/specs/{feature_name}/04-dev-reviewed.md` (review report)
   - Implemented source code
   - If missing, report error and recommend running `/bmad-development` first

### Step 1: QA Test Strategy & Execution (via bmad-qa)
Use Task tool with `bmad-qa` agent:

```
Repository Context: [test patterns from 00-repo-scan.md]
Feature Name: {feature_name}
Working Directory: {project_root}
Skip E2E: {true/false based on --skip-e2e}
Skip Security: {true/false based on --skip-security}

Task: Create and execute comprehensive test suite
Instructions:
1. Read PRD, Architecture, Sprint Plan, and Review Report from docs/specs/{feature_name}/
2. Review implemented code from development phase
3. Create comprehensive test suite validating all acceptance criteria:
   - Functional tests: core business logic + boundary values + error scenarios
   - Integration tests: component interactions + API endpoints
   - Performance tests: response time + concurrent load
   - Security tests: SQL injection / XSS / auth bypass (unless --skip-security)
   - Accessibility tests: ARIA labels + keyboard navigation
   - E2E tests via Playwright (unless --skip-e2e)
4. Focus on risk areas flagged in the review report
5. Execute tests and report results
6. Ensure quality standards are met (coverage thresholds)
```

### Step 2: Bug-Fix Loop
If QA discovers bugs:

1. Present bug list to user (summary)
2. Dispatch each bug to bmad-dev for TDD fix:

```
Bug Report from QA:
[Bug description and reproduction steps]

Task: Fix the bug using TDD
Instructions:
1. Write a failing test that reproduces the bug
2. Implement the minimal fix to make the test pass
3. Refactor if needed while keeping tests green
4. Run existing tests to ensure no regressions
5. Report fix summary
```

3. Re-run QA regression on fixed areas
4. Loop until all bugs resolved

### Step 3: Bug-Fix Escalation
If bug-fix loop > 3 iterations on the same bug:
- Escalate: question the architecture
- Recommend returning to `/bmad-design` for re-planning (§4.4)

### Step 4: Verification Gate (门控3: 验证前)
Confirm all checks pass:

| Check | Threshold |
|-------|-----------|
| Test suite | All pass (0 failures) |
| Coverage | core ≥80%, agents ≥70%, cli ≥60% |
| Build | exit 0, no compile errors |
| Lint/TypeCheck | 0 errors |
| Verification evidence | Run within last 5 minutes |

If any check fails, return to Step 2 for fixes.

### Step 5: Test Report
bmad-qa generates a test report including:
- Coverage report (unit / integration / E2E)
- Test results (pass / fail / skipped)
- Defect list (resolved + known issues)
- Risk areas assessment

Save report to `docs/specs/{feature_name}/05-test-report.md`

### Step 6: Completion Report
Provide:
- Feature name and path to `05-test-report.md`
- Test results summary (pass rate, coverage)
- Bug-fix iteration count
- Known issues and risks
- Recommendation: run `/bmad-deployment {feature_name}` to proceed to release

## Key Rules
- Development prerequisites must exist before running (门控3)
- Test pyramid: Unit 70% / Integration 20% / E2E 10%
- Playwright preferred for E2E (bmad-qa has mcp_Playwright enabled)
- Bug-fix loop > 3 → return to planning (§4.4 escalation)
- Coverage thresholds: core ≥80%, agents ≥70%, cli ≥60% (门控3)
- Verification evidence must be fresh (< 5 minutes) (门控3)
- bmad-qa never interacts with the user directly (§4.0.1)
