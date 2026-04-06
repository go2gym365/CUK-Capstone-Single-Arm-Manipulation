"""Compatibility-aware MuJoCo GUI runner for ROBOTIS OMX models."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from ..model_paths import MODEL_VARIANTS, list_model_scenes, resolve_model_xml

_SCENE_CHOICES = tuple(
    dict.fromkeys(
        scene_name
        for model_name in MODEL_VARIANTS
        for scene_name in list_model_scenes(model_name)
    )
)


def _resolve_xml(scene: str | None = None, model: str = "env_ms") -> Path:
    return resolve_model_xml(model=model, scene=scene)


def main() -> None:
    try:
        import mujoco
        from mujoco import viewer
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "mujoco is required to run the ROBOTIS OMX viewer. "
            "Install it in the active environment and try again."
        ) from exc

    parser = argparse.ArgumentParser(description="View ROBOTIS OMX model assets in MuJoCo GUI.")
    parser.add_argument(
        "--model",
        choices=MODEL_VARIANTS,
        default="env_ms",
        help="Model asset package to load. Default keeps existing env_ms behavior.",
    )
    parser.add_argument(
        "--scene",
        choices=_SCENE_CHOICES,
        default=None,
        help="Named XML scene alias. Defaults to the selected model's default scene.",
    )
    parser.add_argument(
        "--show-site-group0",
        action="store_true",
        help="Show site group 0 markers at startup. Default is hidden.",
    )
    parser.add_argument(
        "--xml-path",
        default=None,
        help="Optional explicit XML path. If set, --model and --scene are ignored.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load model/data only and print summary without opening GUI.",
    )
    args = parser.parse_args()

    if args.xml_path:
        xml_path = Path(args.xml_path).resolve()
    else:
        xml_path = _resolve_xml(scene=args.scene, model=args.model)

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    print(f"[ok] loaded: {xml_path}")
    print(f"[model] variant={args.model} nq={model.nq}, nv={model.nv}, nu={model.nu}, nbody={model.nbody}")

    if args.dry_run:
        return

    print("Launching MuJoCo viewer. Close the GUI window to exit.")
    with viewer.launch_passive(model, data, show_left_ui=True, show_right_ui=True) as handle:
        with handle.lock():
            if not args.show_site_group0:
                handle.opt.sitegroup[0] = 0
        handle.sync()

        while handle.is_running():
            mujoco.mj_step(model, data)
            handle.sync()
            time.sleep(model.opt.timestep)


__all__ = ["_resolve_xml", "main"]


if __name__ == "__main__":
    main()
