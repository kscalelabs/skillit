"""Player for replaying recorded skills."""

import json
import time
from typing import Any

import pykos


class FramePlayer:
    def __init__(self, ip: str, joint_name_to_id: dict[str, int]) -> None:
        """Initialize the frame player.

        Args:
            ip: IP address or hostname of the robot
            joint_name_to_id: Dictionary mapping joint names to their IDs
        """
        self.kos = pykos.KOS(ip=ip)
        self.ac = self.kos.actuator
        self.joint_name_to_id = joint_name_to_id

    def load_skill(self, filename: str) -> dict[str, Any]:
        """Load a skill from a JSON file.

        Args:
            filename: Path to the recorded JSON file

        Returns:
            The loaded skill data
        """
        with open(filename, "r") as f:
            return json.load(f)

    def play(self, filename: str, joint_name_map: dict[str, str] | None = None) -> None:
        """Replay recorded frames.

        Args:
            filename: Path to the recorded JSON file
            joint_name_map: Optional mapping to rename joints (e.g., {"old_name": "new_name"})
        """
        data = self.load_skill(filename)

        frames = data["frames"]
        frequency = data.get("frequency", 20)
        frame_delay = 1.0 / frequency

        print(f"Playing {len(frames)} frames at {frequency}Hz...")
        time.sleep(1)

        for frame in frames:
            commands = []
            for joint_name, position in frame.items():
                # Map joint name if provided
                if joint_name_map and joint_name in joint_name_map:
                    joint_name = joint_name_map[joint_name]

                if joint_name in self.joint_name_to_id:
                    commands.append({"actuator_id": self.joint_name_to_id[joint_name], "position": position})
            self.ac.command_actuators(commands)
            time.sleep(frame_delay)
