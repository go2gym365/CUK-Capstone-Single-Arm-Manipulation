"""Environment package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ROBOTIS_OMX_AI.robotis_env import OMXReachEnv


def make_env(*args: Any, **kwargs: Any):
    """Lazily import the environment factory to avoid optional deps at package import time."""
    from .ROBOTIS_OMX_AI.runners.factory import make_env as _make_env

    return _make_env(*args, **kwargs)


def __getattr__(name: str):
    if name == "OMXReachEnv":
        from .ROBOTIS_OMX_AI.robotis_env import OMXReachEnv as _OMXReachEnv

        return _OMXReachEnv
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["OMXReachEnv", "make_env"]
