"""Example of recording and playing back a skill."""

import argparse

from skillit.play import FramePlayer
from skillit.record import SkillRecorder

# Example joint name to ID mapping for the robot (needed to record and play skills)
joint_name_to_id = {
    "right_ankle_pitch": 1,
    "right_knee_pitch": 2,
    "right_hip_pitch": 3,
    "right_hip_roll": 4,
    "right_hip_yaw": 5,
    "left_ankle_pitch": 6,
    "left_knee_pitch": 7,
    "left_hip_pitch": 8,
    "left_hip_roll": 9,
    "left_hip_yaw": 10,
    "right_elbow": 11,
    "right_shoulder_pitch": 12,
    "right_shoulder_roll": 13,
    "left_elbow": 16,
    "left_shoulder_pitch": 15,
    "left_shoulder_roll": 14,
}


def record_skill(ip: str, skill_name: str) -> None:
    """Record a new skill.

    Args:
        ip: IP address of the robot
        skill_name: Name of the skill to record
    """
    # Initialize the recorder with robot IP and joint mapping
    recorder = SkillRecorder(
        ip=ip,
        joint_name_to_id=joint_name_to_id,
        frequency=20,  # Record at 20Hz
        countdown=3,  # 3 second countdown before recording
        skill_name=skill_name,  # Optional name for the skill
    )

    print("Starting recording session...")
    print("1. Robot joints will be set to passive mode")
    print("2. Move the robot to desired positions")
    print("3. Press Ctrl+C to start recording")
    print("4. Press Ctrl+C again to stop recording")

    # Start recording - this will block until Ctrl+C is pressed twice
    recorder.record()


def play_skill(ip: str, filename: str) -> None:
    """Play back a recorded skill.

    Args:
        ip: IP address of the robot
        filename: Path to the recorded skill JSON file
    """
    # Initialize the player with robot IP and joint mapping
    player = FramePlayer(ip=ip, joint_name_to_id=joint_name_to_id)

    # Play back the recorded movements
    print(f"Playing back skill from {filename}")
    player.play(filename)


def main() -> None:
    parser = argparse.ArgumentParser(description="Record or play robot movements")
    parser.add_argument("action", choices=["record", "play"], help="Action to perform")
    parser.add_argument("--ip", default="localhost", help="IP address of the robot")
    parser.add_argument("--file", help="Skill file to play (required for play action)")
    parser.add_argument("--skill-name", default="wave", help="Name of the skill to record")
    args = parser.parse_args()

    if args.action == "record":
        record_skill(ip=args.ip, skill_name=args.skill_name)
    else:
        if not args.file:
            parser.error("--file is required for play action")
        play_skill(ip=args.ip, filename=args.file)


if __name__ == "__main__":
    # python -m examples.play_record_example
    main()
