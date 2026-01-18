"""
AB Runner Module
Handles execution of ApacheBench commands using subprocess.
Provides both synchronous and asynchronous (QThread) execution.
"""

import subprocess
import signal
from typing import Optional, Callable
from dataclasses import dataclass
from PySide6.QtCore import QThread, Signal, QObject

from ab_resolver import get_ab_path, ABResolverError


@dataclass
class ABTestConfig:
    """Configuration for an ApacheBench test."""
    url: str
    requests: int = 1000
    concurrency: int = 10
    keep_alive: bool = True

    def validate(self) -> tuple[bool, str]:
        """
        Validate the test configuration.

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        # Validate URL
        if not self.url:
            return False, "URL is required"

        if not self.url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"

        # Validate requests
        if self.requests <= 0:
            return False, "Number of requests must be greater than 0"

        # Validate concurrency
        if self.concurrency <= 0:
            return False, "Concurrency must be greater than 0"

        if self.concurrency > self.requests:
            return False, "Concurrency cannot be greater than total requests"

        return True, ""


@dataclass
class ABTestResult:
    """Result of an ApacheBench test."""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    error_message: str = ""


class ABRunnerWorker(QThread):
    """
    Worker thread for running ApacheBench tests without blocking the UI.
    """

    # Signals
    started_signal = Signal()
    output_signal = Signal(str)  # Emits output lines as they come
    completed_signal = Signal(ABTestResult)
    error_signal = Signal(str)

    def __init__(self, config: ABTestConfig, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.config = config
        self._process: Optional[subprocess.Popen] = None
        self._cancelled = False

    def build_command(self, ab_path: str) -> list[str]:
        """Build the ab command with all arguments."""
        cmd = [
            str(ab_path),
            "-n", str(self.config.requests),
            "-c", str(self.config.concurrency),
        ]

        if self.config.keep_alive:
            cmd.append("-k")

        cmd.append(self.config.url)

        return cmd

    def run(self):
        """Execute the ApacheBench test."""
        self.started_signal.emit()
        self._cancelled = False

        try:
            # Get ab binary path (uses abs.exe for HTTPS URLs)
            ab_path = get_ab_path(self.config.url)

            # Build command
            cmd = self.build_command(ab_path)

            # Log the command being run
            cmd_str = ' '.join(cmd)
            self.output_signal.emit(f"Running: {cmd_str}\n")
            self.output_signal.emit("-" * 60 + "\n")

            # Start the process
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(
                    subprocess, 'CREATE_NO_WINDOW') else 0
            )

            # Read stdout in real-time
            stdout_lines = []
            if self._process.stdout:
                for line in iter(self._process.stdout.readline, ''):
                    if self._cancelled:
                        break
                    stdout_lines.append(line)
                    self.output_signal.emit(line)

            # Wait for process to complete
            self._process.wait()

            # Get any remaining stderr
            stderr = self._process.stderr.read() if self._process.stderr else ""

            stdout = ''.join(stdout_lines)

            if self._cancelled:
                result = ABTestResult(
                    success=False,
                    return_code=-1,
                    stdout=stdout,
                    stderr=stderr,
                    error_message="Test cancelled by user"
                )
            else:
                result = ABTestResult(
                    success=self._process.returncode == 0,
                    return_code=self._process.returncode,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=stderr if self._process.returncode != 0 else ""
                )

            self.completed_signal.emit(result)

        except ABResolverError as e:
            self.error_signal.emit(str(e))
            self.completed_signal.emit(ABTestResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr=str(e),
                error_message=str(e)
            ))
        except Exception as e:
            error_msg = f"Error running test: {str(e)}"
            self.error_signal.emit(error_msg)
            self.completed_signal.emit(ABTestResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr=error_msg,
                error_message=error_msg
            ))
        finally:
            self._process = None

    def cancel(self):
        """Cancel the running test."""
        self._cancelled = True
        if self._process:
            try:
                self._process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    self._process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self._process.kill()
            except Exception:
                pass


def run_ab_sync(config: ABTestConfig) -> ABTestResult:
    """
    Run ApacheBench synchronously (blocking).
    Use for testing or when not in a GUI context.

    Args:
        config: Test configuration

    Returns:
        ABTestResult: The test result
    """
    try:
        # Validate config
        is_valid, error = config.validate()
        if not is_valid:
            return ABTestResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr=error,
                error_message=error
            )

        # Get ab path
        ab_path = get_ab_path()

        # Build command
        cmd = [
            str(ab_path),
            "-n", str(config.requests),
            "-c", str(config.concurrency),
        ]
        if config.keep_alive:
            cmd.append("-k")
        cmd.append(config.url)

        # Run the process
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(
                subprocess, 'CREATE_NO_WINDOW') else 0
        )

        return ABTestResult(
            success=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            error_message=result.stderr if result.returncode != 0 else ""
        )

    except ABResolverError as e:
        return ABTestResult(
            success=False,
            return_code=-1,
            stdout="",
            stderr=str(e),
            error_message=str(e)
        )
    except Exception as e:
        return ABTestResult(
            success=False,
            return_code=-1,
            stdout="",
            stderr=str(e),
            error_message=str(e)
        )
