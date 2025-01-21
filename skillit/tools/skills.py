"""Tools for working with recorded skills."""

import json
from dataclasses import dataclass, field


@dataclass
class Frame:
    """Single frame of joint positions.

    Attributes:
        joint_positions: A dictionary mapping joint names to their positions.
    """

    joint_positions: dict[str, float] = field(default_factory=dict)

    def as_actuator_positions(self, joint_name_to_id: dict[str, int]) -> dict[int, float]:
        """Convert joint positions to actuator positions using joint name to ID mapping.

        Args:
            joint_name_to_id: Mapping from joint names to actuator IDs

        Returns:
            Dictionary mapping actuator IDs to their positions
        """
        return {
            joint_name_to_id[name]: position
            for name, position in self.joint_positions.items()
            if name in joint_name_to_id
        }


@dataclass
class SkillData:
    """Recorded skill data structure.

    Attributes:
        frequency: Sampling frequency of the skill recording.
        countdown: Countdown time before recording started.
        timestamp: Timestamp of when the skill was recorded.
        joint_name_to_id: Mapping from joint names to actuator IDs.
        frames: List of frames containing joint positions.
    """

    frequency: float
    countdown: int
    timestamp: str
    joint_name_to_id: dict[str, int]
    frames: list[Frame]

    def frames_as_actuator_positions(self) -> list[dict[int, float]]:
        """Get all frames with joint positions mapped to actuator IDs.

        Returns:
            List of dictionaries mapping actuator IDs to their positions
        """
        return [frame.as_actuator_positions(self.joint_name_to_id) for frame in self.frames]

    def save(self, filename: str) -> None:
        """Save the skill data to a JSON file.

        Args:
            filename: Path where to save the JSON file
        """
        data = {
            "frequency": self.frequency,
            "countdown": self.countdown,
            "timestamp": self.timestamp,
            "joint_name_to_id": self.joint_name_to_id,
            "frames": [frame.joint_positions for frame in self.frames],
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)


def load_skill(filename: str) -> SkillData:
    """Load a skill from a JSON file.

    Args:
        filename: Path to the recorded JSON file

    Returns:
        The loaded skill data with proper typing
    """
    with open(filename, "r") as f:
        data = json.load(f)

    frames = [Frame(joint_positions=frame) for frame in data["frames"]]

    skill_data = SkillData(
        frequency=float(data["frequency"]),
        countdown=int(data["countdown"]),
        timestamp=str(data["timestamp"]),
        joint_name_to_id=data["joint_name_to_id"],
        frames=frames,
    )

    return skill_data
