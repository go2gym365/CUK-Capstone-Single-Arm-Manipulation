"""Launch MuJoCo GUI viewer for ROBOTIS OMX models."""
from __future__ import annotations

import argparse
from pathlib import Path

import mujoco
from mujoco import viewer


def _resolve_xml(scene: str) -> Path:
    base_dir = Path(__file__).resolve().parents[1]
    if scene == "base":
        return base_dir / "scene.xml"
    if scene == "reach":
        return base_dir / "scene_reach.xml"
    raise ValueError(f"Unsupported scene: {scene}")


def main() -> None:
    parser = argparse.ArgumentParser(description="View ROBOTIS OMX model in MuJoCo GUI.")
    parser.add_argument("--scene", choices=["base", "reach"], default="base")
    parser.add_argument(
        "--xml-path",
        default=None,
        help="Optional explicit XML path. If set, --scene is ignored.",
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
        xml_path = _resolve_xml(args.scene)

    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    print(f"[ok] loaded: {xml_path}")
    print(f"[model] nq={model.nq}, nv={model.nv}, nu={model.nu}, nbody={model.nbody}")

    if args.dry_run:
        return

    print("Launching MuJoCo viewer. Close the GUI window to exit.")
    viewer.launch(model, data)


if __name__ == "__main__":
    main()
