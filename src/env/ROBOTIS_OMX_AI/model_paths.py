"""Helpers for locating ROBOTIS OMX model assets."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

_MODEL_SCENES = {
    "env_ms": {
        "base": "scene.xml",
        "cube_bottle": "scene_cube_bottle.xml",
        "default": "scene_cube_bottle.xml",
    },
    "env_tm": {
        "base": "scene.xml",
        "env_tm": "env_tm.xml",
        "default": "env_tm.xml",
    },
}

MODEL_VARIANTS = tuple(_MODEL_SCENES)


def _normalize_model_name(model: str) -> str:
    if model not in _MODEL_SCENES:
        supported = ", ".join(MODEL_VARIANTS)
        raise ValueError(f"Unsupported model variant {model!r}. Supported variants: [{supported}]")
    return model


def get_model_dir(model: str) -> Path:
    """Return the package directory for a ROBOTIS OMX model variant."""
    return PACKAGE_ROOT / _normalize_model_name(model)


def list_model_scenes(model: str) -> tuple[str, ...]:
    """List the named scene aliases available for a model variant."""
    scenes = _MODEL_SCENES[_normalize_model_name(model)]
    return tuple(name for name in scenes if name != "default")


def resolve_model_xml(model: str = "env_ms", scene: str | None = None) -> Path:
    """Resolve a scene alias to an XML path inside a model variant package."""
    model_name = _normalize_model_name(model)
    scenes = _MODEL_SCENES[model_name]
    scene_name = "default" if scene is None else scene

    try:
        xml_name = scenes[scene_name]
    except KeyError as exc:
        supported = ", ".join(list_model_scenes(model_name))
        raise ValueError(
            f"Unsupported scene {scene_name!r} for model {model_name!r}. "
            f"Supported scenes: [{supported}]"
        ) from exc

    return get_model_dir(model_name) / xml_name

