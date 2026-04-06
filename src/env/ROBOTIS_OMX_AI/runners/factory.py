"""Environment factory helpers."""
from __future__ import annotations

from typing import Any

from ..robotis_env import OMXReachEnv


def make_env(task: str = "reach", robot: str = "robotis_omx", **kwargs: Any):
    """Create an environment instance from task/robot identifiers."""
    if robot != "robotis_omx":
        raise ValueError(
            f"Unsupported robot '{robot}'. Currently supported robots: ['robotis_omx']"
        )

    if task == "reach":
        return OMXReachEnv(**kwargs)

    raise ValueError(
        f"Unsupported task '{task}'. Currently supported tasks for robotis_omx: ['reach']"
    )
