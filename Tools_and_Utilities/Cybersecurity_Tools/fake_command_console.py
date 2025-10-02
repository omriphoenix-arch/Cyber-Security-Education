"""Educational fake command console with wow-factor background actions."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import tkinter as tk
from tkinter import scrolledtext, ttk


MAX_OUTPUT_CHARS = 6000


@dataclass
class FakeCommand:
    """Map a friendly command keyword to the real action that will run."""

    keyword: str
    description: str
    windows_command: Optional[str] = None
    posix_command: Optional[str] = None
    runner: Optional[Callable[[Path], str]] = None
    display_hint: Optional[str] = None
    output_limit: int = MAX_OUTPUT_CHARS

    def execute(self, *, is_windows: bool, cwd: Path) -> tuple[str, str]:
        """Execute the backing action and return (actual_command, output)."""

        if self.runner is not None:
            actual = self.display_hint or "Python routine"
            output = self.runner(cwd)
            truncated = truncate_output(output, self.output_limit)
            return actual, truncated

        command = self.windows_command if is_windows else self.posix_command
        if not command:
            raise ValueError(
                f"No backing command defined for platform {'Windows' if is_windows else 'POSIX'}"
            )

        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(cwd),
        )
        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        if stdout and stderr:
            combined = f"{stdout}\n[stderr]\n{stderr}"
        elif stderr:
            combined = f"[stderr]\n{stderr}"
        else:
            combined = stdout or "[No output returned]"

        truncated = truncate_output(combined, self.output_limit)
        return command, truncated


def truncate_output(output: str, limit: int) -> str:
    """Truncate long output for readability."""

    if len(output) <= limit:
        return output
    head = output[: limit - 200]
    tail = output[-200:]
    return f"{head}\n…\n[Output truncated — showing last 200 characters]\n{tail}"


def python_env_dump(cwd: Path) -> str:
    """Return environment variables as key=value pairs sorted alphabetically."""

    rows = [f"{key}={value}" for key, value in sorted(os.environ.items())]
    return "Environment Snapshot\n" + "\n".join(rows)


def python_tree_scan(cwd: Path, depth: int = 2, limit: int = 150) -> str:
    """Walk the directory tree to a limited depth for demonstration."""

    root = Path(cwd)
    lines: list[str] = [f"Scanning: {root.resolve()}"]
    count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        current_path = Path(dirpath)
        relative = current_path.relative_to(root)
        depth_level = len(relative.parts)
        if depth_level > depth:
            dirnames[:] = []
            continue

        indent = "  " * depth_level
        lines.append(f"{indent}[DIR] {relative if relative.parts else '.'}")

        for file_name in filenames:
            lines.append(f"{indent}  - {file_name}")
            count += 1
            if count >= limit:
                lines.append("…")
                lines.append("[File listing truncated for brevity]")
                return "\n".join(lines)

    lines.append(f"Total files listed: {count}")
    return "\n".join(lines)


def python_inventory_summary(cwd: Path) -> str:
    """Summarize file counts and total size within the current directory."""

    total_size = 0
    file_count = 0
    directory_count = 0

    for dirpath, dirnames, filenames in os.walk(cwd):
        directory_count += len(dirnames)
        file_count += len(filenames)
        for filename in filenames:
            try:
                total_size += (Path(dirpath) / filename).stat().st_size
            except OSError:
                continue

    return (
        "Inventory Summary\n"
        f"• Folders discovered: {directory_count}\n"
        f"• Files discovered:   {file_count}\n"
        f"• Total size:         {total_size / 1_048_576:.2f} MB"
    )


def python_recent_files(cwd: Path, limit: int = 20) -> str:
    """Show the most recently modified files within the current directory."""

    entries = []
    for path in Path(cwd).glob("**/*"):
        if path.is_file():
            try:
                entries.append((path.stat().st_mtime, path))
            except OSError:
                continue

    if not entries:
        return "No files accessible for timestamp analysis."

    entries.sort(reverse=True)
    lines = ["Most Recent Files"]
    for timestamp, path in entries[:limit]:
        try:
            relative = path.relative_to(cwd)
        except ValueError:
            relative = path
        stamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"• {relative} — {stamp}")

    return "\n".join(lines)


def python_disk_usage(cwd: Path) -> str:
    """Estimate disk usage for the current drive/root using Python."""

    target = Path(cwd).resolve()
    anchor = target.anchor or str(target)

    try:
        usage = shutil.disk_usage(anchor)
    except OSError:
        usage = shutil.disk_usage(str(target))

    total = usage.total
    free = usage.free
    used = usage.used

    return (
        "Disk Usage Estimate\n"
        f"• Total: {total / 1_073_741_824:.2f} GB\n"
        f"• Used:  {used / 1_073_741_824:.2f} GB\n"
        f"• Free:  {free / 1_073_741_824:.2f} GB"
    )


class FakeCommandConsole(tk.Tk):
    """Tkinter application implementing the educational fake console."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Educational Fake Command Console")
        self.geometry("940x620")
        self.minsize(720, 480)

        self.is_windows = platform.system().lower().startswith("win")
        self.cwd = Path.cwd()
        self.command_history: list[str] = []
        self.history_index = 0

        self.commands = self._build_command_map()

        self._create_widgets()
        self._print_banner()

    def _create_widgets(self) -> None:
        self.style = ttk.Style(self)
        self.style.configure("Console.TFrame", background="#111")
        self.style.configure("Console.TLabel", background="#111", foreground="#0f0", font=("Consolas", 10))
        self.style.configure("Console.TButton", font=("Consolas", 9))

        frame = ttk.Frame(self, style="Console.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            background="#000",
            foreground="#0f0",
            insertbackground="#0f0",
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.output.config(state=tk.DISABLED)

        entry_frame = ttk.Frame(frame, style="Console.TFrame")
        entry_frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        self.prompt_var = tk.StringVar(value=f"{self.cwd}> ")
        self.prompt_label = ttk.Label(entry_frame, textvariable=self.prompt_var, style="Console.TLabel")
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = ttk.Entry(entry_frame, font=("Consolas", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.focus_set()

        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Up>", self._history_back)
        self.entry.bind("<Down>", self._history_forward)

    def _print_banner(self) -> None:
        banner = (
            "Educational Fake Command Console\n"
            "Type 'help' to see available friendly commands.\n"
            "Type 'real <command>' to learn which underlying action runs.\n"
            "Type 'clear' to reset the screen, 'exit' to quit.\n"
        )
        self._write_output(banner)

    def _build_command_map(self) -> dict[str, FakeCommand]:
        return {
            "peek": FakeCommand(
                "peek",
                "Quick glance at the current directory contents",
                windows_command="dir",
                posix_command="ls -l",
            ),
            "deeppeek": FakeCommand(
                "deeppeek",
                "Show a limited tree view using Python's os.walk",
                runner=lambda cwd: python_tree_scan(cwd, depth=2, limit=120),
                display_hint="Python os.walk depth=2",
            ),
            "processes": FakeCommand(
                "processes",
                "List running processes",
                windows_command="tasklist",
                posix_command="ps aux",
            ),
            "ports": FakeCommand(
                "ports",
                "Display active network ports",
                windows_command="netstat -an",
                posix_command="netstat -an",
                output_limit=4000,
            ),
            "sysinfo": FakeCommand(
                "sysinfo",
                "Retrieve detailed system information",
                windows_command="systeminfo",
                posix_command="uname -a",
            ),
            "inventory": FakeCommand(
                "inventory",
                "Count files, folders, and total disk usage using Python",
                runner=python_inventory_summary,
                display_hint="Python os.walk summary",
            ),
            "envdump": FakeCommand(
                "envdump",
                "Dump environment variables",
                runner=python_env_dump,
                display_hint="Python os.environ dump",
                output_limit=4000,
            ),
            "recent": FakeCommand(
                "recent",
                "Highlight recently modified files",
                runner=lambda cwd: python_recent_files(cwd, limit=25),
                display_hint="Python sorted file timestamps",
            ),
            "disk": FakeCommand(
                "disk",
                "Estimate disk usage",
                runner=python_disk_usage,
                display_hint="Python disk_usage",
            ),
        }

    def _on_enter(self, event: tk.Event) -> None:
        raw = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not raw:
            return

        self.command_history.append(raw)
        self.history_index = len(self.command_history)

        self._write_output(f"\n{self.prompt_var.get()}{raw}\n")

        if raw.lower() in {"exit", "quit"}:
            self._write_output("Closing console...")
            self.after(350, self.destroy)
            return

        if raw.lower() == "clear":
            self._clear_output()
            return

        if raw.lower() == "help":
            self._show_help()
            return

        if raw.lower().startswith("real "):
            self._show_real_command(raw.split(maxsplit=1)[1])
            return

        if raw.lower() == "history":
            self._show_history()
            return

        if raw.lower() in {"pwd", "where"}:
            self._write_output(str(self.cwd.resolve()))
            return

        if raw.lower().startswith("cd "):
            self._change_directory(raw[3:].strip())
            return

        command = self.commands.get(raw.lower())
        if not command:
            self._write_output("Unknown command. Type 'help' to see what's available.")
            return

        threading.Thread(
            target=self._execute_command_thread,
            args=(raw.lower(), command),
            daemon=True,
        ).start()

    def _execute_command_thread(self, keyword: str, command: FakeCommand) -> None:
        try:
            actual, output = command.execute(is_windows=self.is_windows, cwd=self.cwd)
        except Exception as exc:  # noqa: BLE001
            output = f"[Execution failed] {exc}"
            actual = command.display_hint or "<none>"

        self.after(0, lambda: self._display_command_result(keyword, actual, output))

    def _display_command_result(self, keyword: str, actual: str, output: str) -> None:
        self._write_output(f"[alias '{keyword}' executed -> {actual}]\n{output}\n")

    def _clear_output(self) -> None:
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)

    def _write_output(self, text: str) -> None:
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def _show_help(self) -> None:
        lines = ["Available fake commands:"]
        for keyword, command in sorted(self.commands.items()):
            lines.append(f"• {keyword:<10} {command.description}")
        lines.append("\nSpecial commands: help, real <command>, cd <path>, pwd, history, clear, exit")
        self._write_output("\n".join(lines))

    def _show_real_command(self, keyword: str) -> None:
        command = self.commands.get(keyword.lower())
        if not command:
            self._write_output(f"No command named '{keyword}'.")
            return

        if command.runner is not None:
            actual = command.display_hint or "<Python routine>"
        else:
            actual = command.windows_command if self.is_windows else command.posix_command
            if not actual:
                actual = "<Python routine>"
        self._write_output(f"Alias '{keyword}' triggers: {actual}")

    def _show_history(self) -> None:
        if not self.command_history:
            self._write_output("No history yet.")
            return
        lines = ["Command history:"]
        for index, command in enumerate(self.command_history, start=1):
            lines.append(f"{index:>2}: {command}")
        self._write_output("\n".join(lines))

    def _change_directory(self, path_text: str) -> None:
        target = (self.cwd / path_text).resolve() if not Path(path_text).is_absolute() else Path(path_text)
        if not target.exists() or not target.is_dir():
            self._write_output(f"Cannot change directory: '{path_text}' is not a valid folder.")
            return

        self.cwd = target
        self.prompt_var.set(f"{self.cwd}> ")
        self._write_output(f"Changed directory to {self.cwd}\n")

    def _history_back(self, event: tk.Event) -> str:
        if not self.command_history:
            return "break"
        if self.history_index > 0:
            self.history_index -= 1
        else:
            self.history_index = 0
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.command_history[self.history_index])
        return "break"

    def _history_forward(self, event: tk.Event) -> str:
        if not self.command_history:
            return "break"
        if self.history_index < len(self.command_history):
            self.history_index += 1
        if self.history_index >= len(self.command_history):
            self.entry.delete(0, tk.END)
            self.history_index = len(self.command_history)
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])
        return "break"


if __name__ == "__main__":
    app = FakeCommandConsole()
    app.mainloop()
