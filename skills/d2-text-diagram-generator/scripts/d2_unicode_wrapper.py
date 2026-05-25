from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


KEEP_INPUT = "d2_unicode_input.d2"
KEEP_OUTPUT = "d2_unicode_output.txt"


class RenderError(RuntimeError):
    pass


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render D2 source to Unicode text using the D2 CLI."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="Path to a .d2 file. Reads from stdin when omitted.",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep generated d2_unicode_input.d2 and d2_unicode_output.txt files.",
    )
    parser.add_argument(
        "--ascii-mode",
        choices=("unicode", "standard"),
        default="unicode",
        help="Character set for D2 text output. Defaults to unicode.",
    )
    return parser.parse_args(argv)


def read_source(source: Path | None) -> str:
    if source is None:
        return sys.stdin.read()
    return source.read_text(encoding="utf-8")


def build_command(input_path: Path, output_path: Path, ascii_mode: str) -> list[str]:
    command = ["d2"]
    if ascii_mode == "standard":
        command.append("--ascii-mode=standard")
    command.extend([str(input_path), str(output_path)])
    return command


def run_d2(input_path: Path, output_path: Path, ascii_mode: str) -> None:
    command = build_command(input_path, output_path, ascii_mode)
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RenderError("D2 CLI not found. Install `d2` and ensure it is on PATH.") from exc

    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip()
        if details:
            raise RenderError(f"D2 render failed:\n{details}")
        raise RenderError(f"D2 render failed with exit code {completed.returncode}.")


def render_source(source_text: str, keep: bool, ascii_mode: str) -> str:
    if keep:
        input_path = Path.cwd() / KEEP_INPUT
        output_path = Path.cwd() / KEEP_OUTPUT
        input_path.write_text(source_text, encoding="utf-8")
        run_d2(input_path, output_path, ascii_mode)
        if not output_path.exists():
            raise RenderError(f"D2 completed but did not create {output_path}.")
        print(f"Kept D2 source: {input_path}", file=sys.stderr)
        print(f"Kept rendered text: {output_path}", file=sys.stderr)
        return output_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="d2-unicode-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / "input.d2"
        output_path = tmp_path / "output.txt"
        input_path.write_text(source_text, encoding="utf-8")
        run_d2(input_path, output_path, ascii_mode)
        if not output_path.exists():
            raise RenderError("D2 completed but did not create the text output file.")
        return output_path.read_text(encoding="utf-8")


def write_stdout(text: str) -> None:
    output = text if text.endswith("\n") else f"{text}\n"
    try:
        sys.stdout.write(output)
    except UnicodeEncodeError:
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is None:
            raise
        buffer.write(output.encode("utf-8"))
        buffer.flush()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        source_text = read_source(args.source)
        rendered = render_source(source_text, args.keep, args.ascii_mode)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except RenderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    write_stdout(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
