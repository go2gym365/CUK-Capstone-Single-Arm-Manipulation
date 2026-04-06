"""Smoke test for the ROBOTIS OMX reach environment."""
from __future__ import annotations

import argparse

from src.env import make_env


def main():
    parser = argparse.ArgumentParser(description="Run a quick smoke test on env.")
    parser.add_argument("--task", default="reach", choices=["reach"])
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--render", action="store_true", help="Render one rgb frame at startup.")
    args = parser.parse_args()

    render_mode = "rgb_array" if args.render else None
    env = make_env(task=args.task, robot="robotis_omx", render_mode=render_mode, seed=args.seed)

    obs, info = env.reset(seed=args.seed)
    print(f"[reset] obs_shape={obs.shape} dist={info['grasp_to_object_dist']:.4f}")

    if args.render:
        frame = env.render()
        print(f"[render] frame_shape={None if frame is None else frame.shape}")

    for t in range(args.steps):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        if t % 10 == 0 or terminated or truncated:
            print(
                f"[step {t:03d}] reward={reward:.4f} dist={info['grasp_to_object_dist']:.4f} "
                f"success={info['success']} term={terminated} trunc={truncated}"
            )
        if terminated or truncated:
            obs, info = env.reset()
            print(f"[reset] obs_shape={obs.shape} dist={info['grasp_to_object_dist']:.4f}")

    env.close()
    print("Smoke test completed.")


if __name__ == "__main__":
    main()
