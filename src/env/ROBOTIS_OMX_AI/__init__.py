"""ROBOTIS OMX package exports."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .model_paths import MODEL_VARIANTS, get_model_dir, list_model_scenes, resolve_model_xml

if TYPE_CHECKING:
    from .env_ms.robotis_env import OMXReachEnv


def make_env(*args: Any, **kwargs: Any):
    """Lazily import the environment factory to avoid optional deps at package import time."""
    from .env_ms.runners.factory import make_env as _make_env

    return _make_env(*args, **kwargs)


def __getattr__(name: str):
    if name == "OMXReachEnv":
        from .env_ms.robotis_env import OMXReachEnv as _OMXReachEnv

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
