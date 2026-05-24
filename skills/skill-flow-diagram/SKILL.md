---
name: skill-flow-diagram
description: Use this skill to create flowcharts, flow diagrams, and activity-style diagrams with D2. Use it when the user is lost in code flow or wants a visual explanation of code paths, workflows, orchestration, state transitions, retries, validation branches, or error handling. Prefer this skill when a rendered text diagram would clarify multi-step behavior, even if the user does not explicitly say "D2".
---

# Skill flow diagram

Use this skill to turn technical behavior into a rendered Unicode text diagram. The final answer should contain the rendered diagram, not just D2 source, unless the user asks for source or troubleshooting details.

## Trigger Judgment

Create a diagram when the user explicitly requests one, or when a recent change affects control flow, request handling, job orchestration, state transitions, retries, validation branches, or multi-step error handling.

Skip the diagram for small copy edits, isolated type fixes, cosmetic UI changes, or explanations where prose is clearer than a visual.

## Output Contract

- Use D2 syntax.
- Render with the D2 CLI to a `.txt` output file and return the generated Unicode text.
- Put the rendered output in a fenced `text` block.
- Keep diagrams compact enough to read in chat; split only when one diagram becomes crowded.
- Include important branches, loops, terminal states, side effects, and error paths.
- Label nodes with user-meaningful behavior, not implementation trivia.
- Do not default to SVG, PNG, or PDF for chat responses. Use those formats only when the user asks for graphical output.
- Do not fabricate rendered output. If rendering cannot run, explain the dependency or command failure.

## Dependency Policy

The D2 CLI is an external system dependency. Check it before rendering:

```bash
d2 --version
```

If `d2` is missing, explain that the D2 CLI must be installed. Ask for explicit permission before installing D2, package managers, or any system dependency.

## Render Workflow

1. Understand the process or code path and decide whether a diagram is warranted.
2. Draft a small D2 diagram using nodes and labeled arrows.
3. Prefer the bundled wrapper script when it is available. Run it from the installed skill directory or pass its full path:

   ```bash
   python scripts/d2_unicode_wrapper.py diagram.d2
   ```

   Or pipe source through stdin:

   ```bash
   cat diagram.d2 | python scripts/d2_unicode_wrapper.py
   ```

   PowerShell equivalent:

   ```powershell
   Get-Content diagram.d2 | python scripts/d2_unicode_wrapper.py
   ```

4. Read stdout from the wrapper and paste the rendered Unicode diagram into the final answer.
5. Let the wrapper delete temporary `.d2` and `.txt` files by default. If the user asks to keep temporary files, pass `--keep` and report their locations from stderr.

## D2 Shape

Use this baseline:

```d2
request: Receive request
valid: Valid?
process: Process request
error: Return error
done: Done

request -> valid
valid -> process: yes
valid -> error: no
process -> done
error -> done
```

Mapping guidance:

- Sequential work: `step1 -> step2`
- Branches: one decision node with labeled outgoing arrows
- Loops: an arrow back to the repeated decision or action with a clear label
- Early exits: explicit terminal node such as `error`, `rejected`, or `done`
- Errors: separate paths with clear failure labels

## Error Recovery

If rendering fails because the D2 source is invalid, read the error, fix the diagram, and rerun. Treat the D2 exit status as authoritative; D2 can leave partial output behind during failures. If dependencies are missing, stop at a clear installation/permission prompt instead of substituting unrendered D2 source.

## Acceptance Checklist

Before finalizing, verify:

- The answer includes rendered Unicode text, not only D2 source.
- The diagram has a clear entry and terminal path.
- Branch labels are clear, usually `yes`/`no` or domain-specific outcomes.
- Error paths and early exits are represented when relevant.
- Temporary files are cleaned unless the user asked to keep them.
