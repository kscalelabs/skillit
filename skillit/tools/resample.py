"""Tools for resampling recorded skills to adjust playback speed."""

import numpy as np

from skillit.tools.skills import Frame, SkillData, load_skill


def downsample_skill(
    data: SkillData,
    speed_factor: float | None = None,
    target_frame_count: int | None = None,
) -> SkillData:
    """Downsample a recorded skill to increase playback speed.

    Args:
        data: The loaded skill data containing frames and frequency
        speed_factor: How much faster to play (e.g., 1.42 for 42% faster)
        target_frame_count: Alternative to speed_factor - specify exact number of frames

    Returns:
        New skill data with resampled frames and adjusted frequency

    Raises:
        ValueError: If neither speed_factor nor target_frame_count is provided
    """
    if speed_factor is None and target_frame_count is None:
        raise ValueError("Must provide either speed_factor or target_frame_count")

    frames = data.frames
    old_frequency = data.frequency

    # Calculate timing parameters
    n_frames = len(frames)
    total_duration = (n_frames - 1) / old_frequency  # Total duration

    # Calculate new frame count
    if speed_factor is not None:
        new_frame_count = int(n_frames / speed_factor)
    elif target_frame_count is not None:
        new_frame_count = target_frame_count
    else:
        raise ValueError("Must provide either speed_factor or target_frame_count")

    # Calculate new duration based on frame ratio
    ratio = new_frame_count / float(n_frames)
    total_duration_new = total_duration * ratio

    # Create time arrays
    old_times = np.linspace(0, total_duration, n_frames)
    new_times = np.linspace(0, total_duration_new, new_frame_count)

    def interpolate_frame(query_time: float) -> Frame:
        """Interpolate joint angles at a given time point."""
        # Find surrounding frames
        i = np.searchsorted(old_times, query_time) - 1

        # Edge cases
        if i < 0:
            return frames[0]
        if i >= n_frames - 1:
            return frames[-1]

        # Interpolation factor
        t_i = old_times[i]
        t_next = old_times[i + 1]
        alpha = (query_time - t_i) / (t_next - t_i)

        # Get frames to interpolate between
        frame_i = frames[i].joint_positions
        frame_next = frames[i + 1].joint_positions

        # Interpolate each joint angle
        new_joint_positions = {}
        all_joints = set(frame_i.keys()) | set(frame_next.keys())

        for joint in all_joints:
            v_i = frame_i.get(joint, None)
            v_next = frame_next.get(joint, v_i)
            if v_i is None:
                v_i = v_next
            new_joint_positions[joint] = (1 - alpha) * v_i + alpha * v_next

        return Frame(joint_positions=new_joint_positions)

    # Generate new frames through interpolation
    new_frames = [interpolate_frame(t) for t in new_times]

    # Create new skill data
    new_data = SkillData(
        frequency=data.frequency,
        countdown=data.countdown,
        timestamp=data.timestamp,
        joint_name_to_id=data.joint_name_to_id,
        frames=new_frames,
    )

    return new_data


def main() -> None:
    """Example usage of the resampling functionality."""
    import argparse

    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description="Resample a recorded skill")
    parser.add_argument("filename", help="Path to the skill JSON file")
    parser.add_argument("--speed-factor", type=float, help="Speed factor (e.g., 1.42 for 42%% faster)")
    parser.add_argument("--target-frames", type=int, help="Target number of frames")
    args = parser.parse_args()

    # Load the skill
    skill_data = load_skill(args.filename)
    original_frames = skill_data.frames

    # Example joint to plot (using first joint in the data)
    joint_name = next(iter(original_frames[0].joint_positions.keys()))

    # Extract original trajectory for the selected joint
    original_trajectory = [frame.joint_positions[joint_name] for frame in original_frames]
    original_times = np.arange(len(original_trajectory)) / skill_data.frequency

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

    breakpoint()

    # Extract resampled trajectory
    resampled_frames = new_data.frames
    resampled_trajectory = [frame.joint_positions[joint_name] for frame in resampled_frames]
    resampled_times = np.arange(len(resampled_trajectory)) / new_data.frequency

    # Plot original vs resampled trajectories
    plt.figure(figsize=(12, 6))

    # Original trajectory
    plt.subplot(1, 2, 1)
    plt.plot(original_times, original_trajectory, "b-", label="Original")
    plt.title("Original Frames")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{joint_name} Angle")
    plt.legend()

    # Resampled trajectory
    plt.subplot(1, 2, 2)
    plt.plot(resampled_times, resampled_trajectory, "r-", label="Resampled")
    plt.title("Resampled Frames")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{joint_name} Angle")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
