"""ROBOTIS OMX reach environment."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import gymnasium as gym
import mujoco
import numpy as np
from gymnasium import spaces


class OMXReachEnv(gym.Env):
    """MuJoCo reach task environment based on ROBOTIS OMX."""

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}

    def __init__(
        self,
        xml_path: Optional[str] = None,
        frame_skip: int = 5,
        max_steps: int = 200,
        success_threshold: float = 0.03,
        render_mode: Optional[str] = None,
        seed: Optional[int] = None,
    ):
        super().__init__()

        if xml_path is None:
            xml_path = str(Path(__file__).resolve().parent / "scene_cube_bottle.xml")

        self.xml_path = xml_path
        self.frame_skip = frame_skip
        self.max_steps = max_steps
        self.success_threshold = float(success_threshold)
        self.render_mode = render_mode

        self.model = mujoco.MjModel.from_xml_path(self.xml_path)
        self.data = mujoco.MjData(self.model)

        self.np_random = np.random.default_rng(seed)
        self.step_count = 0
        self.last_action = np.zeros(6, dtype=np.float32)

        self.arm_joint_names = ["Joint1", "Joint2", "Joint3", "Joint4", "Joint5"]
        self.arm_actuator_names = ["Joint1", "Joint2", "Joint3", "Joint4", "Joint5"]
        self.gripper_joint_name = "Gripper"
        self.gripper_actuator_name = "Gripper"
        self.object_joint_name = "object_main_free"

        self.home_joint_qpos = np.array([0.0, -0.35, 0.75, -0.45, 0.0], dtype=np.float64)
        self.table_top_z = 0.12
        self.object_half_extent = 0.012

        self._init_ids()
        self._init_ctrl_range()

        obs = self._get_obs()
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=obs.shape, dtype=np.float32
        )
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(6,), dtype=np.float32)

        self.renderer = None
        if self.render_mode == "rgb_array":
            self.renderer = mujoco.Renderer(self.model)

    def _name2id(self, obj_type, name: str) -> int:
        idx = mujoco.mj_name2id(self.model, obj_type, name)
        if idx == -1:
            raise ValueError(f"MuJoCo object not found: {name}")
        return idx

    def _init_ids(self) -> None:
        self.ee_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "ee_site")
        self.grasp_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "grasp_site")
        self.object_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "object_main_site")

        self.object_geom_id = self._name2id(mujoco.mjtObj.mjOBJ_GEOM, "object_main_geom")
        self.object_joint_id = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, self.object_joint_name)
        self.object_qpos_adr = self.model.jnt_qposadr[self.object_joint_id]
        self.object_qvel_adr = self.model.jnt_dofadr[self.object_joint_id]

        self.arm_joint_qpos_adr = []
        self.arm_joint_qvel_adr = []
        for joint_name in self.arm_joint_names:
            jid = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, joint_name)
            self.arm_joint_qpos_adr.append(self.model.jnt_qposadr[jid])
            self.arm_joint_qvel_adr.append(self.model.jnt_dofadr[jid])

        self.gripper_joint_id = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, self.gripper_joint_name)
        self.gripper_qpos_adr = self.model.jnt_qposadr[self.gripper_joint_id]
        self.gripper_qvel_adr = self.model.jnt_dofadr[self.gripper_joint_id]

        gripper_mimic_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "Gripper_mimic")
        self.has_gripper_mimic = gripper_mimic_id != -1
        if self.has_gripper_mimic:
            self.gripper_mimic_qpos_adr = self.model.jnt_qposadr[gripper_mimic_id]
            self.gripper_mimic_qvel_adr = self.model.jnt_dofadr[gripper_mimic_id]
        else:
            self.gripper_mimic_qpos_adr = None
            self.gripper_mimic_qvel_adr = None

    def _init_ctrl_range(self) -> None:
        self.ctrl_min = np.zeros(6, dtype=np.float64)
        self.ctrl_max = np.zeros(6, dtype=np.float64)
        self.arm_actuator_ids = []

        for i, actuator_name in enumerate(self.arm_actuator_names):
            aid = self._name2id(mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)
            self.arm_actuator_ids.append(aid)
            self.ctrl_min[i] = float(self.model.actuator_ctrlrange[aid, 0])
            self.ctrl_max[i] = float(self.model.actuator_ctrlrange[aid, 1])

        self.gripper_actuator_id = self._name2id(
            mujoco.mjtObj.mjOBJ_ACTUATOR, self.gripper_actuator_name
        )
        self.ctrl_min[5] = float(self.model.actuator_ctrlrange[self.gripper_actuator_id, 0])
        self.ctrl_max[5] = float(self.model.actuator_ctrlrange[self.gripper_actuator_id, 1])

        self.gripper_open_qpos = float(self.ctrl_max[5] * 0.8)

    def _scale_action(self, action: np.ndarray) -> np.ndarray:
        action = np.clip(action, -1.0, 1.0)
        ctrl = self.ctrl_min + 0.5 * (action + 1.0) * (self.ctrl_max - self.ctrl_min)
        return ctrl.astype(np.float64)

    def _sample_object_xy(self) -> np.ndarray:
        x = float(self.np_random.uniform(0.18, 0.30))
        y = float(self.np_random.uniform(-0.10, 0.10))
        return np.array([x, y], dtype=np.float64)

    def _set_robot_home(self) -> None:
        for qpos_adr, qvel_adr, qpos in zip(
            self.arm_joint_qpos_adr, self.arm_joint_qvel_adr, self.home_joint_qpos
        ):
            self.data.qpos[qpos_adr] = qpos
            self.data.qvel[qvel_adr] = 0.0

        self.data.qpos[self.gripper_qpos_adr] = self.gripper_open_qpos
        self.data.qvel[self.gripper_qvel_adr] = 0.0

        if self.has_gripper_mimic:
            self.data.qpos[self.gripper_mimic_qpos_adr] = -self.gripper_open_qpos
            self.data.qvel[self.gripper_mimic_qvel_adr] = 0.0

    def _set_object_pose(self, object_xy: np.ndarray) -> None:
        qadr = self.object_qpos_adr
        object_z = self.table_top_z + self.object_half_extent
        self.data.qpos[qadr : qadr + 3] = np.array([object_xy[0], object_xy[1], object_z], dtype=np.float64)
        self.data.qpos[qadr + 3 : qadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        self.data.qvel[self.object_qvel_adr : self.object_qvel_adr + 6] = 0.0

    def _get_obs(self) -> np.ndarray:
        qpos = np.array([self.data.qpos[a] for a in self.arm_joint_qpos_adr], dtype=np.float32)
        qvel = np.array([self.data.qvel[a] for a in self.arm_joint_qvel_adr], dtype=np.float32)
        gripper_qpos = np.array([self.data.qpos[self.gripper_qpos_adr]], dtype=np.float32)
        gripper_qvel = np.array([self.data.qvel[self.gripper_qvel_adr]], dtype=np.float32)

        ee_pos = self.data.site_xpos[self.ee_site_id].astype(np.float32).copy()
        grasp_pos = self.data.site_xpos[self.grasp_site_id].astype(np.float32).copy()
        object_pos = self.data.site_xpos[self.object_site_id].astype(np.float32).copy()
        rel_grasp_to_object = (object_pos - grasp_pos).astype(np.float32)

        return np.concatenate(
            [qpos, qvel, gripper_qpos, gripper_qvel, ee_pos, grasp_pos, object_pos, rel_grasp_to_object]
        ).astype(np.float32)

    def _get_info(self) -> Dict[str, Any]:
        grasp_pos = self.data.site_xpos[self.grasp_site_id].copy()
        object_pos = self.data.site_xpos[self.object_site_id].copy()

        grasp_to_object_dist = float(np.linalg.norm(grasp_pos - object_pos))
        success = grasp_to_object_dist < self.success_threshold
        object_fell = bool(object_pos[2] < 0.02)

        return {
            "grasp_to_object_dist": grasp_to_object_dist,
            "success": bool(success),
            "object_fell": object_fell,
            "step_count": int(self.step_count),
        }

    def _default_reward(self, info: Dict[str, Any], action: np.ndarray) -> float:
        reward = -1.0 * info["grasp_to_object_dist"]
        reward -= 0.01 * float(np.linalg.norm(action))
        reward += 2.0 * float(info["success"])
        reward -= 2.0 * float(info["object_fell"])
        return float(reward)

    def reset(self, *, seed=None, options=None) -> Tuple[np.ndarray, Dict[str, Any]]:
        super().reset(seed=seed)

        if seed is not None:
            self.np_random = np.random.default_rng(seed)

        self.step_count = 0
        self.last_action[:] = 0.0

        mujoco.mj_resetData(self.model, self.data)

        if self.model.nkey > 0:
            try:
                mujoco.mj_resetDataKeyframe(self.model, self.data, 0)
            except Exception:
                pass

        self._set_robot_home()
        self._set_object_pose(self._sample_object_xy())

        self.data.ctrl[:] = 0.0
        for i, actuator_id in enumerate(self.arm_actuator_ids):
            self.data.ctrl[actuator_id] = self.home_joint_qpos[i]
        self.data.ctrl[self.gripper_actuator_id] = self.gripper_open_qpos

        mujoco.mj_forward(self.model, self.data)
        for _ in range(40):
            mujoco.mj_step(self.model, self.data)
        mujoco.mj_forward(self.model, self.data)

        obs = self._get_obs()
        info = self._get_info()
        return obs, info

    def step(self, action: np.ndarray):
        action = np.asarray(action, dtype=np.float32).reshape(-1)
        if action.shape != (6,):
            raise ValueError(f"Action shape must be (6,), got {action.shape}")

        self.last_action = action.copy()
        ctrl = self._scale_action(action)

        self.data.ctrl[:] = 0.0
        for i, actuator_id in enumerate(self.arm_actuator_ids):
            self.data.ctrl[actuator_id] = ctrl[i]
        self.data.ctrl[self.gripper_actuator_id] = ctrl[5]

        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)
        mujoco.mj_forward(self.model, self.data)

        self.step_count += 1

        obs = self._get_obs()
        info = self._get_info()
        reward = self._default_reward(info, action)

        terminated = bool(info["success"] or info["object_fell"])
        truncated = bool(self.step_count >= self.max_steps)
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "rgb_array":
            self.renderer.update_scene(self.data)
            return self.renderer.render()
        return None

    def close(self):
        if self.renderer is not None:
            self.renderer.close()
            self.renderer = None
