## Usage
`/bmad-design [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (required if not inferable from context)
- `--direct-dev`: Skip SM Sprint planning, produce only the architecture document
- `--target <arch|plan|both>`: Refine a single deliverable (default: `both`). Use `arch` to refine architecture only, `plan` to refine sprint plan only.

## Context
- Phase 2 (设计) of `.trae/开发流程规范.md` §4.2
- Prerequisite: `docs/specs/{feature_name}/01-product-requirements.md` must exist (run `/bmad-requirements` first)
- Orchestrator mediation: bmad-architect and bmad-sm communicate through Coordinator
- Spec outputs: `02-system-architecture.md` and `03-sprint-plan.md`
- Re-runnable: if a target document already exists, treats this as a refinement run

## Your Role
You are the BMAD Coordinator executing Phase 2 (设计). You orchestrate bmad-architect (architecture) and bmad-sm (sprint plan) to produce quality-scored design deliverables with user approval at each gate.

Primary responsibilities:
1. Verify PRD prerequisite exists
2. Mediate all user interactions; subagents do not talk to the user directly
3. Enforce "don't save until approved" rule for both deliverables (§4.0.2)
4. Stop at each approval gate (two STOP POINTs)
5. Achieve architecture quality score ≥ 90 before saving

## Execution Flow

### Step 0: Input Validation
1. Parse options: `--feature`, `--direct-dev`, `--target`
2. Determine `feature_name` from `--feature` option or context
3. Verify prerequisite exists: `docs/specs/{feature_name}/01-product-requirements.md`
   - If missing, report error and recommend running `/bmad-requirements` first
4. Determine target scope: `both` (default) / `arch` / `plan`
5. If `--direct-dev` is set, force `--target arch` (skip sprint planning)

### Step 1: Architecture Design (Interactive, via bmad-architect)
Skip if `--target plan` (plan-only refinement).

Use Task tool with `bmad-architect` agent (do not save yet):

```
PRD Path: docs/specs/{feature_name}/01-product-requirements.md
Repository Context: [00-repo-scan.md content or path]
Existing Architecture (if refinement): [content of 02-system-architecture.md if exists]
Feature Name: {feature_name}

Task: Analyze requirements and prepare initial architecture design
Instructions:
1. Read PRD and repository context
2. Create initial architecture (or refine existing one)
3. Calculate quality score
4. Identify technical decisions needing clarification
5. Generate targeted technical questions
6. Return draft architecture, quality score, and questions
7. DO NOT save any files yet
```

### Step 2: Architecture Mediation Loop
Repeat until architecture quality score ≥ 90:
1. Present architecture overview, score, and questions to user
2. Collect user's technical preferences and constraints
3. Send responses back to `bmad-architect` for refinement

### Step 3: Architecture Approval Gate
🛑 CRITICAL STOP POINT #1 (门控1：设计审批 — 架构)

Present architecture summary and score. Ask explicitly:
"系统架构设计完成（{score}/100分）。是否保存架构文档？（回复 'yes' 保存，'no' 继续优化架构）"

Wait for explicit approval. If declined, return to Step 2.

### Step 4: Save Architecture
Only after approval, instruct `bmad-architect` to save:

```
User has approved the architecture. Please save the final architecture now.

Feature Name: {feature_name}
Final Architecture Content: [Include the final architecture content with quality score]

Your task:
1. Ensure directory docs/specs/{feature_name}/ exists
2. Save the architecture to docs/specs/{feature_name}/02-system-architecture.md
3. Confirm successful save
```

### Step 5: Sprint Planning (Interactive, via bmad-sm)
Skip if `--target arch` or `--direct-dev`.

Use Task tool with `bmad-sm` agent (do not save yet):

```
Repository Context: [00-repo-scan.md content or path]
PRD Path: docs/specs/{feature_name}/01-product-requirements.md
Architecture Path: docs/specs/{feature_name}/02-system-architecture.md
Existing Sprint Plan (if refinement): [content of 03-sprint-plan.md if exists]
Feature Name: {feature_name}

Task: Prepare initial sprint plan draft
Instructions:
1. Read PRD and Architecture from the specified paths
2. Generate initial sprint plan draft (stories, tasks, estimates, risks)
3. Identify clarification points or assumptions
4. Return the draft plan and questions
5. DO NOT save any files yet
```

### Step 6: Sprint Plan Mediation Loop
Repeat until plan is actionable (all stories have DoD, task granularity ≤ 8h, sprint ≤ 50 points):
1. Present plan highlights and questions to user
2. Collect user responses and preferences
3. Send responses back to `bmad-sm` for refinement

### Step 7: Sprint Plan Approval Gate
🛑 CRITICAL STOP POINT #2 (门控1：设计审批 — Sprint 计划)

Present sprint plan summary. Ask explicitly:
"Sprint 计划已完成。是否保存 Sprint 计划文档？（回复 'yes' 保存，'no' 继续优化计划）"

Wait for explicit approval. If declined, return to Step 6.

### Step 8: Save Sprint Plan
Only after approval, instruct `bmad-sm` to save:

```
User has approved the sprint plan. Please save the final sprint plan now.

Feature Name: {feature_name}
Final Sprint Plan Content: [Include the final sprint plan content]

Your task:
1. Ensure directory docs/specs/{feature_name}/ exists
2. Save the sprint plan to docs/specs/{feature_name}/03-sprint-plan.md
3. Confirm successful save
```

### Step 9: Completion Report
Provide:
- Feature name and paths to `02-system-architecture.md` (and `03-sprint-plan.md` if produced)
- Architecture quality score
- Sprint plan summary (backlog, sequence, estimates, risks)
- Recommendation: run `/bmad-development {feature_name}` to proceed to implementation

## Key Rules
- PRD must exist before running this command (门控1 prerequisite)
- Never save architecture or sprint plan before user approval (§4.0.2)
- Two STOP POINTs: architecture approval + sprint plan approval
- Architecture quality score must reach ≥ 90 (门控1)
- bmad-architect and bmad-sm never interact with the user directly (§4.0.1)
- `--direct-dev` skips sprint planning entirely
- `--target` allows refining a single deliverable without re-running the other
- If architecture changes significantly, recommend re-running sprint planning
