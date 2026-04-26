# MB-Protocol Integration Guide

## Platform-Specific Setup

### Claude Code

**File**: `.claude/skills/{skill-name}/SKILL.md`

1. Create skill directory:
```bash
mkdir -p .claude/skills/my-agent
```

2. Add Iron Rules at top of SKILL.md
3. Mark critical steps with `MANDATORY STEP N — ... (BLOCKING, 不可跳过)`
4. Include CHECKPOINT verification

**Example**: See [`examples/claude-code/evaluator-skill.md`](../examples/claude-code/evaluator-skill.md)

### Cursor IDE

**File**: `.cursorrules` (project root)

1. Create `.cursorrules` file
2. Add blocking rules section
3. Cursor will apply these constraints to all AI-generated code

**Example**: See [`examples/cursor/.cursorrules`](../examples/cursor/.cursorrules)

### AutoGPT

**File**: `autogpt/plugins/mb_protocol_plugin.py`

1. Copy plugin to AutoGPT plugins directory
2. Enable in `.env`:
```env
USE_MB_PROTOCOL=true
```

**Example**: See [`examples/autogpt/mb_protocol_plugin.py`](../examples/autogpt/mb_protocol_plugin.py)

### Generic System Prompt

Add to any system prompt:
```
You MUST adhere to the MB-Protocol for all mandatory execution steps.
Key rules:
1. Steps marked (BLOCKING, 不可跳过) cannot be skipped
2. Every BLOCKING step must have a CHECKPOINT verification
3. No task is complete without feedback
4. Check Iron Rules before declaring completion
```

## Integration Checklist

- [ ] Iron Rules defined at top of prompt/skill
- [ ] All external state mutations have BLOCKING steps
- [ ] CHECKPOINT uses tool-based verification (not inference)
- [ ] Self-Healing Loop defined (Retry-Wait-Fallback)
- [ ] Final callback writes feedback to observable location
- [ ] Test with 3+ tasks to verify compliance
