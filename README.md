# Unicode Flow Skill

Skill to develop any type of software diagram in the agent coder like codex, claude and opencode.
Example, it can generate flow diagrams, C4 model diagrams, sequence diagrams when user ask to understand a new project.

The LLM generates a D2 diagram in the terminal.

## Structure

```text
skills/
  skill-flow-diagram/
    SKILL.md
    scripts/
      d2_unicode_wrapper.py
examples/
  nice-flow.d2
  bigger-flow.d2
tests/
```

## Installation

Add this skill to your workspace using:

```bash
npx skills add inventadev-tech/skills-flow-diagram/skills/skill-flow-diagram
```

The subpath keeps repository-only files, such as `examples/`, `tests/`, and project metadata, out of the installed skill.

## Usage

Render a D2 file to Unicode text:

```powershell
python skills\skill-flow-diagram\scripts\d2_unicode_wrapper.py examples\nice-flow.d2
```

Render from stdin on PowerShell:

```powershell
Get-Content examples\nice-flow.d2 | python skills\skill-flow-diagram\scripts\d2_unicode_wrapper.py
```

Render with standard ASCII instead of Unicode box drawing:

```powershell
python skills\skill-flow-diagram\scripts\d2_unicode_wrapper.py --ascii-mode standard examples\nice-flow.d2
```

## Development

Run the test suite and syntax check before changing release-facing behavior:

```powershell
uv run pytest
python -m py_compile skills\skill-flow-diagram\scripts\d2_unicode_wrapper.py
```

When D2 is installed, also run a manual render:

```powershell
python skills\skill-flow-diagram\scripts\d2_unicode_wrapper.py examples\nice-flow.d2
```

The wrapper calls the external D2 CLI:

```powershell
d2 input.d2 output.txt
```

D2 must be installed separately and available on `PATH`.
