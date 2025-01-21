"""Example script showing how to downsample a recorded skill."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from skillit.tools.resample import downsample_skill
from skillit.tools.skills import SkillData, load_skill


def plot_comparison(original_data: SkillData, resampled_data: SkillData, joint_name: str) -> None:
    """Plot original vs resampled trajectories for a given joint.

    Args:
        original_data: Original skill data
        resampled_data: Resampled skill data
        joint_name: Name of joint to plot
    """
    # Extract trajectories
    original_trajectory = [frame.joint_positions[joint_name] for frame in original_data.frames]
    original_times = np.arange(len(original_trajectory)) / original_data.frequency

    resampled_trajectory = [frame.joint_positions[joint_name] for frame in resampled_data.frames]
    resampled_times = np.arange(len(resampled_trajectory)) / resampled_data.frequency

    # Create comparison plot
    plt.figure(figsize=(12, 6))

    # Original trajectory
    plt.subplot(1, 2, 1)
    plt.plot(original_times, original_trajectory, "b-", label="Original")
    plt.title(f"Original ({len(original_data.frames)} frames)")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{joint_name} Angle")
    plt.legend()

    # Resampled trajectory
    plt.subplot(1, 2, 2)
    plt.plot(resampled_times, resampled_trajectory, "r-", label="Resampled")
    plt.title(f"Resampled ({len(resampled_data.frames)} frames)")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{joint_name} Angle")
    plt.legend()

    plt.tight_layout()
    plt.show()


def main() -> None:
    """Downsample a recorded skill and visualize the results."""
    parser = argparse.ArgumentParser(description="Downsample a recorded skill")
    parser.add_argument("filename", type=Path, help="Path to the skill JSON file")
    parser.add_argument("--speed-factor", type=float, help="Speed factor (e.g., 1.42 for 42%% faster)")
    parser.add_argument("--target-frames", type=int, help="Target number of frames")
    parser.add_argument("--joint", help="Specific joint to plot (defaults to first joint in recording)")
    args = parser.parse_args()

    # Load the skill
    skill_data = load_skill(args.filename)
    print(f"\nLoaded skill with {len(skill_data.frames)} frames at {skill_data.frequency}Hz")

    # Determine joint to plot
    if args.joint:
        joint_name = args.joint
        if joint_name not in skill_data.frames[0].joint_positions:
            available_joints = list(skill_data.frames[0].joint_positions.keys())
            raise ValueError(f"Joint '{joint_name}' not found in recording. Available joints: {available_joints}")
    else:
        # Use first joint in the data
        joint_name = next(iter(skill_data.frames[0].joint_positions.keys()))
        print(f"No joint specified, using: {joint_name}")

    # Resample the skill
    if args.speed_factor:
        print(f"Resampling with speed factor: {args.speed_factor}")
        new_data = downsample_skill(skill_data, speed_factor=args.speed_factor)
    elif args.target_frames:
        print(f"Resampling to {args.target_frames} frames")
        new_data = downsample_skill(skill_data, target_frame_count=args.target_frames)
    else:
        print("Using default speed factor of 1.42 (42% faster)")
        new_data = downsample_skill(skill_data, speed_factor=1.42)

    print(f"Resampled to {len(new_data.frames)} frames")

    # Plot the comparison
    plot_comparison(skill_data, new_data, joint_name)


if __name__ == "__main__":
    main()
