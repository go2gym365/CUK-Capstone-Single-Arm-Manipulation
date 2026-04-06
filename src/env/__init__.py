"""Environment package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .ROBOTIS_OMX_AI import MODEL_VARIANTS, get_model_dir, list_model_scenes, resolve_model_xml

if TYPE_CHECKING:
    from .ROBOTIS_OMX_AI import OMXReachEnv


def make_env(*args: Any, **kwargs: Any):
    """Lazily import the environment factory to avoid optional deps at package import time."""
    from .ROBOTIS_OMX_AI import make_env as _make_env

    return _make_env(*args, **kwargs)


def __getattr__(name: str):
    if name == "OMXReachEnv":
        from .ROBOTIS_OMX_AI import OMXReachEnv as _OMXReachEnv

        return _OMXReachEnv
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "MODEL_VARIANTS",
    "OMXReachEnv",
    "get_model_dir",
    "list_model_scenes",
    "make_env",
    "resolve_model_xml",
]
