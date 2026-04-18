---
name: "skill-name"
description: "Brief description of what this skill does (50 chars max)"
---

# Skill Name

## Purpose

Describe what this skill does and why it's useful.

Example:
This skill enables automated downloading of running activity records from the COROS Training Hub platform. It extracts activity data in .fit format for further analysis, backup, or import into other fitness platforms.

## Architecture Overview

```
[Insert architecture diagram or flow chart]

Example:
┌─────────────────────────────────────┐
│           Input Source              │
│  (Browser, File, API, etc.)         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         Processing Layer            │
│  (Python script, logic, etc.)       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│           Output                    │
│  (Files, Data, Reports, etc.)       │
└─────────────────────────────────────┘
```

## Prerequisites and Dependencies

### System Requirements
- **Operating System**: Windows 10/11 / macOS / Linux
- **Runtime**: Python 3.6+ / Node.js 14+ / etc.
- **Other**: Browser, API keys, etc.

### Authentication Requirements
- Required accounts or credentials
- How to obtain them
- Security considerations

### Required Tools
- List of required tools and versions
- Installation instructions if needed

### Script Location
```
skills/skill-name/scripts/main.py
```

## Quick Start (Recommended Workflow)

### Step 1: Setup/Preparation

```
Commands or instructions for initial setup
```

### Step 2: Execute Main Task

```
Commands or instructions for main execution
```

### Step 3: Verify Results

```
Commands or instructions for verification
```

## Script Reference

### Location
```
skills/skill-name/scripts/main.py
```

### CLI Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--arg1` | string | None | Description of arg1 |
| `--arg2` | int | 10 | Description of arg2 |
| `--flag` | flag | false | Description of flag |

### Key Features

Describe the main features and how they work:

1. **Feature 1**: Description
2. **Feature 2**: Description
3. **Feature 3**: Description

## Input/Output Specifications

### Input Format

```json
{
  "field1": "type - description",
  "field2": "type - description"
}
```

### Output Format (JSON mode)

```json
{
  "success": true,
  "data": {
    "field1": "value",
    "field2": "value"
  },
  "timestamp": "2026-04-17T14:30:00Z"
}
```

## Error Handling

### Common Issues

#### 1. Error Name
```
Error message or symptom
```
**Cause**: Description of what causes this error

**Resolution**:
```
Steps to resolve
```

#### 2. Another Error
...

## Usage Examples

### Example 1: Basic Usage

```bash
python scripts/main.py --arg1 value
```

Expected output:
```
Success message or output
```

### Example 2: Advanced Usage

```bash
python scripts/main.py --arg1 value --arg2 value2 --flag
```

### Example 3: JSON Output

```bash
python scripts/main.py --arg1 value --json-output
```

## Limitations and Edge Cases

### Known Limitations

1. **Limitation 1**: Description and workaround
2. **Limitation 2**: Description and workaround

### Edge Cases

#### Case 1: Description
How the skill handles this case.

#### Case 2: Description
How the skill handles this case.

### Performance Considerations

- Expected execution time
- Memory usage
- Rate limits or quotas

### Security Considerations

- How credentials are handled
- Data privacy concerns
- Best practices

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
| 1.0.1 | YYYY-MM-DD | Bug fixes |
| 1.1.0 | YYYY-MM-DD | New features |

## Support and Troubleshooting

For issues or questions:
1. Check error messages in output
2. Review this documentation
3. Check system requirements
4. Open an issue on GitHub

## License and Usage Terms

This skill is for personal use only. Users must:
- Comply with relevant terms of service
- Not use for unauthorized access
- Follow applicable laws and regulations
