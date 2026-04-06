"""ROBOTIS OMX environment model package."""

from __future__ import annotations

from pathlib import Path

from ..model_paths import get_model_dir, list_model_scenes, resolve_model_xml

PACKAGE_ROOT = get_model_dir("env_ms")
SCENES = list_model_scenes("env_ms")
DEFAULT_XML = resolve_model_xml("env_ms")


def resolve_xml(scene: str | None = None) -> Path:
    """Resolve an env_ms scene alias to its XML path."""
    return resolve_model_xml("env_ms", scene=scene)


__all__ = ["DEFAULT_XML", "PACKAGE_ROOT", "SCENES", "resolve_xml"]
