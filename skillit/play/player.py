"""Player for replaying recorded skills."""

import time

import pykos

from skillit.tools.skills import load_skill


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

    def play(self, filename: str, joint_name_map: dict[str, str] | None = None) -> None:
        """Replay recorded frames.

        Args:
            filename: Path to the recorded JSON file
            joint_name_map: Optional mapping to rename joints (e.g., {"old_name": "new_name"})
        """
        skill_data = load_skill(filename)
        frame_delay = 1.0 / skill_data.frequency

        print(f"Playing {len(skill_data.frames)} frames at {skill_data.frequency}Hz...")
        time.sleep(1)

        for frame in skill_data.frames:
            process_start = time.time()
            commands: list[pykos.services.actuator.ActuatorCommand] = []
            for joint_name, position in frame.joint_positions.items():
                # Map joint name if provided
                if joint_name_map and joint_name in joint_name_map:
                    joint_name = joint_name_map[joint_name]

                if joint_name in self.joint_name_to_id:
                    commands.append({"actuator_id": self.joint_name_to_id[joint_name], "position": position})
            self.ac.command_actuators(commands)
            time.sleep(max(0, frame_delay - (time.time() - process_start)))
