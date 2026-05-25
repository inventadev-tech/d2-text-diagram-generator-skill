# Repository Guidelines

## Project Structure & Module Organization

This repository contains the publishable D2 Text Diagram Generator Skill for rendering D2 diagrams as Unicode text.

- `skills/d2-text-diagram-generator/SKILL.md` defines the skill metadata, behavior, workflows, and user-facing rules.
- `skills/d2-text-diagram-generator/scripts/d2_unicode_wrapper.py` is the Python wrapper that calls `d2` to render `.txt` output.
- `examples/` contains repository-only D2 examples for manual verification and should not be part of the installed skill.
- `tests/` contains repository-only tests and should not be part of the installed skill.
- `src/` and other new folders should get files only when the purpose is clear.
- `organizacion.md`, if present, contains early planning notes and should not be treated as end-user documentation.

## Build, Test, and Development Commands

There is no package manager or build step at the repository root.

- `python skills/d2-text-diagram-generator/scripts/d2_unicode_wrapper.py diagram.d2` renders a D2 file to Unicode text.
- `Get-Content diagram.d2 | python skills/d2-text-diagram-generator/scripts/d2_unicode_wrapper.py` renders from stdin on PowerShell.
- `python skills/d2-text-diagram-generator/scripts/d2_unicode_wrapper.py --ascii-mode standard diagram.d2` renders with standard ASCII characters.
- `python -m py_compile skills/d2-text-diagram-generator/scripts/d2_unicode_wrapper.py` checks the wrapper for Python syntax errors.
- `uv run pytest` installs dev dependencies as needed and runs the Python test suite.
- `d2 --version` verifies that the D2 CLI is available on `PATH`.

D2 is an external dependency. Do not add installer scripts or assume local dependency paths.

## Coding Style & Naming Conventions

Use Markdown for skill documentation and Python 3 for helper scripts. Keep Markdown headings descriptive and task oriented. Prefer fenced code blocks with language tags, for example `bash`, `powershell`, `python`, or `d2`.

Python code should use 4-space indentation, type hints where useful, `pathlib.Path` for filesystem paths, and small functions with clear command-line behavior. Use `snake_case` for files, functions, and variables.

## Testing Guidelines

Python tests use pytest through `uv` and live in `tests/`. Name files `test_<feature>.py` and keep one behavior per test. The wrapper tests mock D2 so unit tests do not require the CLI; still run one manual render with a minimal D2 diagram from `examples/` before changing release behavior.

## Commit & Pull Request Guidelines

Recent history uses short sentence-style commits, such as `Initial commit`, `Create LICENSE`, and `Some changes`. Keep commit subjects concise and imperative when possible, for example `Update D2 wrapper cleanup`.

Pull requests should describe the behavior changed, list manual verification commands, and include rendered output examples when the skill or wrapper output changes. Link related issues when available.

## Agent-Specific Instructions

Keep the skill self-contained under `skills/d2-text-diagram-generator/`. Do not vendor D2 or generated temporary files such as `d2_unicode_input.d2` and `d2_unicode_output.txt`. If adding new automation, document required external tools in `skills/d2-text-diagram-generator/SKILL.md`.
