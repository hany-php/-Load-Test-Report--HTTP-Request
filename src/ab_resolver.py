"""
AB Binary Resolver Module
Detects the operating system and returns the appropriate ab binary path.
Supports both HTTP (ab.exe) and HTTPS (abs.exe) URLs.
"""

import os
import sys
import platform
from pathlib import Path


class ABResolverError(Exception):
    """Raised when ab binary cannot be found or is not executable."""
    pass


def get_base_path() -> Path:
    """
    Get the base path for the application.
    Handles both normal execution and PyInstaller frozen state.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable (PyInstaller)
        return Path(sys._MEIPASS)
    else:
        # Running as script
        return Path(__file__).parent.parent


def get_os_name() -> str:
    """
    Detect the current operating system.
    Returns: 'windows', 'linux', or 'macos'
    """
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'macos'
    else:
        raise ABResolverError(f"Unsupported operating system: {system}")


def get_ab_binary_name(use_ssl: bool = False) -> str:
    """
    Get the ab binary filename based on OS and SSL requirement.

    Args:
        use_ssl: If True, return SSL-enabled binary (abs.exe for Windows)
    """
    os_name = get_os_name()
    if os_name == 'windows':
        return 'abs.exe' if use_ssl else 'ab.exe'
    # For Linux/macOS, ab typically supports SSL natively
    return 'ab'


def get_ab_path(url: str = None) -> Path:
    """
    Get the absolute path to the ab binary for the current OS.
    Automatically selects abs.exe for HTTPS URLs on Windows.

    Args:
        url: Optional URL to determine if SSL binary is needed

    Returns:
        Path: Absolute path to the ab binary

    Raises:
        ABResolverError: If binary not found or not executable
    """
    base_path = get_base_path()
    os_name = get_os_name()

    # Determine if SSL is needed based on URL
    use_ssl = False
    if url and url.lower().startswith('https://'):
        use_ssl = True

    binary_name = get_ab_binary_name(use_ssl)

    # Construct the path to the ab binary
    ab_path = base_path / 'vendor' / 'ab' / os_name / binary_name

    if not ab_path.exists():
        # Try fallback to non-SSL version if SSL version not found
        if use_ssl:
            fallback_name = get_ab_binary_name(use_ssl=False)
            fallback_path = base_path / 'vendor' / 'ab' / os_name / fallback_name
            if fallback_path.exists():
                return fallback_path

        raise ABResolverError(
            f"ApacheBench binary not found at: {ab_path}\n\n"
            f"Please ensure the ab binary is placed in:\n"
            f"  {ab_path}\n\n"
            f"See vendor/ab/README.md for instructions on obtaining the binary."
        )

    # Check if executable (on Unix-like systems)
    if os_name != 'windows' and not os.access(ab_path, os.X_OK):
        raise ABResolverError(
            f"ApacheBench binary is not executable: {ab_path}\n\n"
            f"Run: chmod +x {ab_path}"
        )

    return ab_path


def verify_ab_installation() -> tuple[bool, str]:
    """
    Verify that ab is properly installed and accessible.

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        ab_path = get_ab_path()
        abs_path = get_ab_path("https://example.com")
        messages = [f"ApacheBench (HTTP) found at: {ab_path}"]
        if ab_path != abs_path:
            messages.append(f"ApacheBench (HTTPS/SSL) found at: {abs_path}")
        return True, "\n".join(messages)
    except ABResolverError as e:
        return False, str(e)


if __name__ == "__main__":
    # Test the resolver
    success, message = verify_ab_installation()
    print(f"Success: {success}")
    print(f"Message: {message}")
