from __future__ import annotations

import io
import subprocess
import importlib.util
from pathlib import Path

import pytest

WRAPPER_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "d2-text-diagram-generator"
    / "scripts"
    / "d2_unicode_wrapper.py"
)
spec = importlib.util.spec_from_file_location("d2_unicode_wrapper", WRAPPER_PATH)
assert spec is not None
assert spec.loader is not None
wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrapper)


def fake_run_success(command: list[str], check: bool, capture_output: bool, text: bool):
    output_path = Path(command[-1])
    output_path.write_text("rendered unicode\n", encoding="utf-8")
    return subprocess.CompletedProcess(command, 0, stdout="", stderr="")


def test_read_source_from_file(tmp_path: Path):
    source = tmp_path / "diagram.d2"
    source.write_text("a -> b\n", encoding="utf-8")

    assert wrapper.read_source(source) == "a -> b\n"


def test_main_reads_source_from_stdin(monkeypatch: pytest.MonkeyPatch, capsys):
    monkeypatch.setattr("sys.stdin", type("Stdin", (), {"read": lambda self: "a -> b\n"})())
    monkeypatch.setattr(wrapper.subprocess, "run", fake_run_success)

    assert wrapper.main([]) == 0

    captured = capsys.readouterr()
    assert captured.out == "rendered unicode\n"


def test_render_invokes_d2_with_txt_output(monkeypatch: pytest.MonkeyPatch):
    calls: list[list[str]] = []

    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool):
        calls.append(command)
        Path(command[-1]).write_text("rendered unicode\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(wrapper.subprocess, "run", fake_run)

    assert wrapper.render_source("a -> b\n", keep=False, ascii_mode="unicode") == "rendered unicode\n"

    assert calls
    assert calls[0][0] == "d2"
    assert calls[0][-2].endswith(".d2")
    assert calls[0][-1].endswith(".txt")
    assert "--ascii-mode=standard" not in calls[0]


def test_render_cleans_temporary_files_by_default(monkeypatch: pytest.MonkeyPatch):
    paths: dict[str, Path] = {}

    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool):
        paths["input"] = Path(command[-2])
        paths["output"] = Path(command[-1])
        paths["output"].write_text("rendered unicode\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(wrapper.subprocess, "run", fake_run)

    wrapper.render_source("a -> b\n", keep=False, ascii_mode="unicode")

    assert not paths["input"].exists()
    assert not paths["output"].exists()


def test_render_keeps_generated_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(wrapper.subprocess, "run", fake_run_success)

    rendered = wrapper.render_source("a -> b\n", keep=True, ascii_mode="unicode")

    assert rendered == "rendered unicode\n"
    assert (tmp_path / wrapper.KEEP_INPUT).read_text(encoding="utf-8") == "a -> b\n"
    assert (tmp_path / wrapper.KEEP_OUTPUT).read_text(encoding="utf-8") == "rendered unicode\n"


def test_render_surfaces_d2_failure(monkeypatch: pytest.MonkeyPatch):
    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool):
        Path(command[-1]).write_text("partial\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="syntax error")

    monkeypatch.setattr(wrapper.subprocess, "run", fake_run)

    with pytest.raises(wrapper.RenderError, match="syntax error"):
        wrapper.render_source("bad\n", keep=False, ascii_mode="unicode")


def test_render_passes_standard_ascii_mode(monkeypatch: pytest.MonkeyPatch):
    calls: list[list[str]] = []

    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool):
        calls.append(command)
        Path(command[-1]).write_text("rendered ascii\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(wrapper.subprocess, "run", fake_run)

    wrapper.render_source("a -> b\n", keep=False, ascii_mode="standard")

    assert "--ascii-mode=standard" in calls[0]


def test_write_stdout_falls_back_to_utf8_buffer(monkeypatch: pytest.MonkeyPatch):
    class Cp1252Stdout:
        def __init__(self):
            self.buffer = io.BytesIO()

        def write(self, text: str):
            text.encode("cp1252")
            return len(text)

    stdout = Cp1252Stdout()
    monkeypatch.setattr("sys.stdout", stdout)

    wrapper.write_stdout("┌──┐")

    assert stdout.buffer.getvalue() == "┌──┐\n".encode("utf-8")
