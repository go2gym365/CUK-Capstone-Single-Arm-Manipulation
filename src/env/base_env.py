"""Base environment definitions for single-arm manipulation tasks."""
from __future__ import annotations

from typing import Callable, Dict, Optional, Tuple, Any

import gymnasium as gym
import mujoco
import numpy as np
from gymnasium import spaces


class BaseEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}

    def __init__(
        self,
        xml_path: str,
        reward_fn: Optional[Callable] = None,
        frame_skip: int = 10,
        max_steps: int = 500,  # 물체가 두 개이므로 최대 스텝 수를 늘렸습니다.
        render_mode: Optional[str] = None,
        seed: Optional[int] = None,
    ):
        super().__init__()

        self.xml_path = xml_path
        self.reward_fn = reward_fn
        self.frame_skip = frame_skip
        self.max_steps = max_steps
        self.render_mode = render_mode

        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

        self.np_random = np.random.default_rng(seed)
        self.step_count = 0

        self.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5"]
        self.actuator_names = ["a_joint1", "a_joint2", "a_joint3", "a_joint4", "a_joint5", "a_gripper"]

        self._init_ids()
        self._init_ctrl_range()
        self._init_task_state()

        obs = self._get_obs()
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=obs.shape, dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(6,), dtype=np.float32
        )

        self.renderer = None
        if self.render_mode == "rgb_array":
            self.renderer = mujoco.Renderer(self.model)

    # -----------------------------
    # init helpers
    # -----------------------------
    def _name2id(self, obj_type, name: str) -> int:
        idx = mujoco.mj_name2id(self.model, obj_type, name)
        if idx == -1:
            raise ValueError(f"MuJoCo object not found: {name}")
        return idx

    def _init_ids(self):
        self.ee_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "ee_site")
        self.grasp_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "grasp_site")
        
        # 큐브 및 물병 ID
        self.object_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "object_main_site")
        self.bottle_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "object_bottle_site")
        
        self.target_blue_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "target_blue_site")
        self.target_purple_site_id = self._name2id(mujoco.mjtObj.mjOBJ_SITE, "target_purple_site")

        self.object_geom_id = self._name2id(mujoco.mjtObj.mjOBJ_GEOM, "object_main_geom")
        self.bottle_geom_id = self._name2id(mujoco.mjtObj.mjOBJ_GEOM, "object_bottle_geom")
        
        self.object_joint_id = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, "object_main_free")
        self.bottle_joint_id = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, "object_bottle_free")
        
        self.left_finger_joint_id = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, "left_finger_joint")

        self.object_qpos_adr = self.model.jnt_qposadr[self.object_joint_id]
        self.object_qvel_adr = self.model.jnt_dofadr[self.object_joint_id]
        
        self.bottle_qpos_adr = self.model.jnt_qposadr[self.bottle_joint_id]
        self.bottle_qvel_adr = self.model.jnt_dofadr[self.bottle_joint_id]

        self.gripper_qpos_adr = self.model.jnt_qposadr[self.left_finger_joint_id]
        self.gripper_qvel_adr = self.model.jnt_dofadr[self.left_finger_joint_id]

        self.joint_qpos_adr = []
        self.joint_qvel_adr = []
        for joint_name in self.joint_names:
            jid = self._name2id(mujoco.mjtObj.mjOBJ_JOINT, joint_name)
            self.joint_qpos_adr.append(self.model.jnt_qposadr[jid])
            self.joint_qvel_adr.append(self.model.jnt_dofadr[jid])

    def _init_ctrl_range(self):
        self.ctrl_min = np.zeros(6, dtype=np.float32)
        self.ctrl_max = np.zeros(6, dtype=np.float32)

        for i, actuator_name in enumerate(self.actuator_names):
            aid = self._name2id(mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)
            self.ctrl_min[i] = self.model.actuator_ctrlrange[aid, 0]
            self.ctrl_max[i] = self.model.actuator_ctrlrange[aid, 1]

    def _init_task_state(self):
        self.cube_color_id = 0
        self.bottle_color_id = 0
        self.last_action = np.zeros(6, dtype=np.float32)

    # -----------------------------
    # task helpers
    # -----------------------------
    def _sample_task(self):
        # 0: 파랑, 1: 보라
        self.cube_color_id = int(self.np_random.integers(0, 2))
        self.bottle_color_id = int(self.np_random.integers(0, 2))

    def _apply_object_color(self):
        colors = {
            0: np.array([0.2, 0.45, 1.0, 1.0], dtype=np.float32),
            1: np.array([0.65, 0.35, 0.85, 1.0], dtype=np.float32)
        }
        
        self.model.geom_rgba[self.object_geom_id] = colors[self.cube_color_id]
        self.model.geom_rgba[self.bottle_geom_id] = colors[self.bottle_color_id]

    def _sample_object_xy(self) -> Tuple[np.ndarray, np.ndarray]:
        while True:
            cube_x = self.np_random.uniform(0.05, 0.18)   
            cube_y = self.np_random.uniform(0.05, 0.20)
            
            bottle_x = self.np_random.uniform(0.05, 0.18)  
            bottle_y = self.np_random.uniform(0.05, 0.20)
            
            dist = float(np.linalg.norm([cube_x - bottle_x, cube_y - bottle_y]))
            if dist > 0.05:
                break
                
        return np.array([cube_x, cube_y], dtype=np.float64), np.array([bottle_x, bottle_y], dtype=np.float64)

    def _set_object_pose(self, cube_pos: np.ndarray, bottle_pos: np.ndarray):
        cqadr = self.object_qpos_adr
        self.data.qpos[cqadr:cqadr + 3] = cube_pos
        self.data.qpos[cqadr + 3:cqadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        self.data.qvel[self.object_qvel_adr:self.object_qvel_adr + 6] = 0.0

        bqadr = self.bottle_qpos_adr
        self.data.qpos[bqadr:bqadr + 3] = bottle_pos
        self.data.qpos[bqadr + 3:bqadr + 7] = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        self.data.qvel[self.bottle_qvel_adr:self.bottle_qvel_adr + 6] = 0.0

    def _get_target_pos(self, color_id: int) -> np.ndarray:
        if color_id == 0:
            return self.data.site_xpos[self.target_blue_site_id].copy()
        return self.data.site_xpos[self.target_purple_site_id].copy()

    def _scale_action(self, action: np.ndarray) -> np.ndarray:
        action = np.clip(action, -1.0, 1.0)
        ctrl = self.ctrl_min + 0.5 * (action + 1.0) * (self.ctrl_max - self.ctrl_min)
        return ctrl.astype(np.float64)

    # -----------------------------
    # observation / info
    # -----------------------------
    def _get_obs(self) -> np.ndarray:
        qpos = np.array([self.data.qpos[a] for a in self.joint_qpos_adr], dtype=np.float32)
        qvel = np.array([self.data.qvel[a] for a in self.joint_qvel_adr], dtype=np.float32)

        gripper_joint_pos = np.array([self.data.qpos[self.gripper_qpos_adr]], dtype=np.float32)
        gripper_joint_vel = np.array([self.data.qvel[self.gripper_qvel_adr]], dtype=np.float32)

        ee_pos = self.data.site_xpos[self.ee_site_id].astype(np.float32).copy()
        grasp_pos = self.data.site_xpos[self.grasp_site_id].astype(np.float32).copy()
        
        cube_pos = self.data.site_xpos[self.object_site_id].astype(np.float32).copy()
        cube_vel = self.data.qvel[self.object_qvel_adr:self.object_qvel_adr + 3].astype(np.float32).copy()
        
        bottle_pos = self.data.site_xpos[self.bottle_site_id].astype(np.float32).copy()
        bottle_vel = self.data.qvel[self.bottle_qvel_adr:self.bottle_qvel_adr + 3].astype(np.float32).copy()

        target_blue_pos = self.data.site_xpos[self.target_blue_site_id].astype(np.float32).copy()
        target_purple_pos = self.data.site_xpos[self.target_purple_site_id].astype(np.float32).copy()

        cube_color_onehot = np.array([1.0, 0.0] if self.cube_color_id == 0 else [0.0, 1.0], dtype=np.float32)
        bottle_color_onehot = np.array([1.0, 0.0] if self.bottle_color_id == 0 else [0.0, 1.0], dtype=np.float32)

        obs = np.concatenate([
            qpos,
            qvel,
            gripper_joint_pos,
            gripper_joint_vel,
            ee_pos,
            grasp_pos,
            cube_pos,
            cube_vel,
            bottle_pos,
            bottle_vel,
            target_blue_pos,
            target_purple_pos,
            cube_color_onehot,
            bottle_color_onehot,
        ]).astype(np.float32)

        return obs

    def _get_info(self) -> Dict[str, Any]:
        grasp_pos = self.data.site_xpos[self.grasp_site_id].copy()
        
        cube_pos = self.data.site_xpos[self.object_site_id].copy()
        bottle_pos = self.data.site_xpos[self.bottle_site_id].copy()
        
        # 큐브는 같은 색상 목표로, 물병은 다른 색상 목표로
        cube_target_pos = self._get_target_pos(self.cube_color_id)
        bottle_target_pos = self._get_target_pos(1 - self.bottle_color_id)

        grasp_to_cube = float(np.linalg.norm(grasp_pos - cube_pos))
        grasp_to_bottle = float(np.linalg.norm(grasp_pos - bottle_pos))
        
        cube_to_target = float(np.linalg.norm(cube_pos - cube_target_pos))
        bottle_to_target = float(np.linalg.norm(bottle_pos - bottle_target_pos))

        gripper_joint_pos = float(self.data.qpos[self.gripper_qpos_adr])
        gripper_closed = gripper_joint_pos > 0.020

        cube_lifted = cube_pos[2] > 0.155
        bottle_lifted = bottle_pos[2] > 0.165 # 물병이 더 높으므로 기준 상향

        cube_grasped = (grasp_to_cube < 0.03) and gripper_closed and cube_lifted
        bottle_grasped = (grasp_to_bottle < 0.03) and gripper_closed and bottle_lifted
        
        cube_on_target = cube_to_target < 0.04
        bottle_on_target = bottle_to_target < 0.04

        success = bool(cube_on_target and bottle_on_target)

        return {
            "grasp_to_cube_dist": grasp_to_cube,
            "grasp_to_bottle_dist": grasp_to_bottle,
            "cube_to_target_dist": cube_to_target,
            "bottle_to_target_dist": bottle_to_target,
            "cube_lifted": bool(cube_lifted),
            "bottle_lifted": bool(bottle_lifted),
            "cube_grasped": bool(cube_grasped),
            "bottle_grasped": bool(bottle_grasped),
            "cube_on_target": bool(cube_on_target),
            "bottle_on_target": bool(bottle_on_target),
            "success": bool(success),
            "step_count": int(self.step_count),
        }

    # -----------------------------
    # reward / terminate
    # -----------------------------
    def _default_reward(self, info: Dict[str, Any], action: np.ndarray) -> float:
        reward = 0.0
        
        # 단계별 보상: 큐브를 먼저 제자리에 둔 후, 물병을 옮기도록 유도
        if not info["cube_on_target"]:
            reward -= 1.0 * info["grasp_to_cube_dist"]
            reward -= 1.2 * info["cube_to_target_dist"]
            reward += 2.0 * float(info["cube_grasped"])
            reward += 2.5 * float(info["cube_lifted"])
        else:
            reward += 5.0  # 큐브 성공 유지 보상
            reward -= 1.0 * info["grasp_to_bottle_dist"]
            reward -= 1.2 * info["bottle_to_target_dist"]
            reward += 2.0 * float(info["bottle_grasped"])
            reward += 2.5 * float(info["bottle_lifted"])

        reward += 20.0 * float(info["success"])
        reward -= 0.01 * float(np.linalg.norm(action))
        reward -= 0.005
        return float(reward)

    def _object_fell(self) -> bool:
        cube_pos = self.data.site_xpos[self.object_site_id]
        bottle_pos = self.data.site_xpos[self.bottle_site_id]
        return bool(cube_pos[2] < 0.05 or bottle_pos[2] < 0.05)

    # -----------------------------
    # gym api
    # -----------------------------
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

        self._sample_task()
        self._apply_object_color()

        cube_xy, bottle_xy = self._sample_object_xy()
        cube_pos = np.array([cube_xy[0], cube_xy[1], 0.136], dtype=np.float64)
        bottle_pos = np.array([bottle_xy[0], bottle_xy[1], 0.150], dtype=np.float64) # 물병은 높이가 약간 더 큽니다
        self._set_object_pose(cube_pos, bottle_pos)

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
        self.data.ctrl[:] = ctrl

        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)

        self.step_count += 1

        obs = self._get_obs()
        info = self._get_info()

        if self.reward_fn is None:
            reward = self._default_reward(info, action)
        else:
            reward = float(self.reward_fn(info, action))

        terminated = bool(info["success"] or self._object_fell())
        truncated = bool(self.step_count >= self.max_steps)

        info["terminated_by_fall"] = self._object_fell()

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