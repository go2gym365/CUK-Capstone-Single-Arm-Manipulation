"""Compatibility wrapper for the ROBOTIS OMX smoke test runner."""

from ..env_ms.runners.smoke_test import main

__all__ = ["main"]


if __name__ == "__main__":
    main()
