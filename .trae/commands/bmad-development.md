## Usage
`/bmad-development [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (required if not inferable from context)
- `--skip-review`: Skip independent code review (not recommended)
- `--max-iterations <n>`: Maximum review iterations before escalation (default: 3)

## Context
- Phase 3 (开发) of `.trae/开发流程规范.md` §4.3
- Prerequisites: `01-product-requirements.md` + `02-system-architecture.md` (+ `03-sprint-plan.md` if not `--direct-dev`)
- Orchestrator mediation: bmad-dev and bmad-review communicate through Coordinator
- Output: source code + unit tests + `04-dev-reviewed.md`
- Includes Code Review as an explicit sub-stage (§4.3 代码审查子阶段)

## Your Role
You are the BMAD Coordinator executing Phase 3 (开发). You orchestrate bmad-dev (TDD implementation) and bmad-review (independent code review) to produce production-ready code that passes review.

Primary responsibilities:
1. Verify design prerequisites exist
2. Mediate between Dev and Review during iteration loops
3. Enforce TDD discipline (RED → GREEN → REFACTOR)
4. Manage review iteration escalation per §4.3
5. Verify dev outputs (tests pass, lint clean, security scan)

## Execution Flow

### Step 0: Input Validation
1. Parse options: `--feature`, `--skip-review`, `--max-iterations`
2. Determine `feature_name` from `--feature` option or context
3. Verify prerequisites exist:
   - `docs/specs/{feature_name}/01-product-requirements.md` (required)
   - `docs/specs/{feature_name}/02-system-architecture.md` (required)
   - `docs/specs/{feature_name}/03-sprint-plan.md` (required unless architecture indicates direct-dev)
   - If missing, report error and recommend running `/bmad-requirements` and `/bmad-design` first

### Step 1: Environment Isolation (门控1: 实现前)
1. Verify worktree exists (activate `using-git-worktrees` Skill if needed)
2. If no worktree, create one before development begins

### Step 2: TDD Implementation (via bmad-dev)
Use Task tool with `bmad-dev` agent:

```
Repository Context: [00-repo-scan.md content or path]
Feature Name: {feature_name}
Working Directory: {project_root}

Task: Implement ALL features across ALL sprints according to specifications
Instructions:
1. Read PRD from docs/specs/{feature_name}/01-product-requirements.md
2. Read Architecture from docs/specs/{feature_name}/02-system-architecture.md
3. Read Sprint Plan from docs/specs/{feature_name}/03-sprint-plan.md
4. Identify and implement ALL sprints sequentially (Sprint 1, Sprint 2, etc.)
5. Complete ALL tasks across ALL sprints before finishing
6. TDD discipline: RED (failing test) → GREEN (minimal impl) → REFACTOR
7. Create production-ready code with tests for the entire feature set
8. Report implementation status for each sprint and overall completion
```

### Step 3: Dev Self-Review (门控2: 实现中)
Verify bmad-dev has completed:
1. TDD cycle evidence for each function
2. Self-review checklist completed
3. Unit tests pass
4. Lint / type check pass (ruff check / mypy / eslint)

### Step 4: Code Review Sub-Stage (skip if `--skip-review`)
Use Task tool with `bmad-review` agent:

```
Repository Context: [00-repo-scan.md content or path]
Feature Name: {feature_name}
Working Directory: {project_root}
Review Iteration: {current_iteration, starting from 1}

Task: Conduct independent code review
Instructions:
1. Read PRD, Architecture, and Sprint Plan from docs/specs/{feature_name}/
2. Analyze implementation against requirements and architecture
3. Generate structured review report
4. Save report to docs/specs/{feature_name}/04-dev-reviewed.md
5. Return review status (Pass / Pass with Risk / Fail)
```

### Step 5: Review Iteration Management
Based on review result:

| Result | Action |
|--------|--------|
| Pass / Pass with Risk | Proceed to Step 6 |
| Fail + iteration < max-iterations | Return to Step 2 with review feedback |
| Fail + iteration = 2 | Schedule SM + Architect + Dev meeting |
| Fail + iteration ≥ max-iterations | Escalate for manual intervention (§4.3) |

If returning to Step 2, send review feedback to bmad-dev:

```
Review Feedback (Iteration {n}):
[Review report content]

Please fix the issues above and re-implement. Focus on:
[Key issues from review report]
```

### Step 6: Verify Dev Outputs
Run verification commands:
- Unit tests: all pass (0 failures)
- Coverage: core ≥80%, agents ≥70%, cli ≥60%
- Build: exit 0, no compile errors
- Lint/TypeCheck: 0 errors
- Security scan: bandit no Critical/High

### Step 7: Completion Report
Provide:
- Feature name and path to `04-dev-reviewed.md`
- Review status (Pass / Pass with Risk)
- Test results and coverage
- Implementation status per sprint
- Recommendation: run `/bmad-testing {feature_name}` to proceed to QA

## Key Rules
- Design prerequisites must exist before running (门控1)
- TDD discipline is mandatory: every function has failing-test-first evidence (门控2)
- Review iteration escalation per §4.3 (Fail + iteration ≥3 → escalate)
- bmad-dev and bmad-review never interact with the user directly (§4.0.1)
- Never skip review unless `--skip-review` is explicitly set
- Worktree isolation required before development (门控1)
- Coverage thresholds: core ≥80%, agents ≥70%, cli ≥60%
