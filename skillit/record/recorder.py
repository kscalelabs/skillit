"""Recorder for recording and replaying skills."""

import json
import signal
import sys
import time
from datetime import datetime
from types import FrameType
from typing import Any

import pykos


class SkillRecorder:
    def __init__(
        self,
        ip: str,
        joint_name_to_id: dict[str, int],
        frequency: int = 20,
        countdown: int = 3,
        skill_name: str | None = None,
    ) -> None:
        """Initialize the recorder.

        Args:
            ip: IP address or hostname of the robot
            joint_name_to_id: Dictionary mapping joint names to their IDs
            frequency: Recording frequency in Hz
            countdown: Countdown delay in seconds before recording starts
            skill_name: Optional name for the recorded skill
        """
        self.kos = pykos.KOS(ip=ip)
        self.ac = self.kos.actuator
        self.joint_name_to_id = joint_name_to_id
        self.frames: list[dict[str, float]] = []
        self.recording = False
        self.frequency = frequency
        self.frame_delay = 1.0 / frequency
        self.countdown = countdown
        self.skill_name = skill_name
        self.setup_signal_handler()

        # Store metadata
        self.metadata: dict[str, Any] = {
            "frequency": frequency,
            "countdown": countdown,
            "timestamp": None,
            "joint_name_to_id": joint_name_to_id,
            "frames": [],
        }

    def setup_signal_handler(self) -> None:
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, signum: int, frame: FrameType | None) -> None:
        if not self.recording:
            print("\nStarting countdown...")
            self._start_recording()
        else:
            print("\nStopping recording...")
            self.recording = False
            self.save_frames()
            sys.exit(0)

    def _start_recording(self) -> None:
        for i in range(self.countdown, 0, -1):
            print(f"Recording starts in {i}...")
            time.sleep(1)

        print("Recording started! Press Ctrl+C to stop.")
        self.recording = True
        self.frames = []
        self.metadata["timestamp"] = datetime.now().isoformat()

    def record_frame(self) -> dict[str, float]:
        joint_ids = list(self.joint_name_to_id.values())
        states_obj = self.ac.get_actuators_state(joint_ids)

        frame = {}
        for state in states_obj.states:
            joint_name = next(name for name, id in self.joint_name_to_id.items() if id == state.actuator_id)
            frame[joint_name] = state.position

        return frame

    def save_frames(self, output_dir: str = ".") -> str:
        if not self.frames:
            print("No frames recorded!")
            return ""

        # Update metadata
        self.metadata["frames"] = self.frames

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_part = f"_{self.skill_name}" if self.skill_name else ""
        filename = f"{output_dir}/skill{name_part}_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(self.metadata, f, indent=2)
        print(f"Saved {len(self.frames)} frames to {filename}")
        return filename

    def record(self) -> None:
        print("Disabling torque to allow manual positioning...")
        for joint_id in self.joint_name_to_id.values():
            self.ac.configure_actuator(actuator_id=joint_id, torque_enabled=False)

        print("Move the robot to desired positions.")
        print("Press Ctrl+C to start recording.")
        print(f"Recording will start after {self.countdown}s countdown.")
        print(f"Recording frequency: {self.frequency}Hz")

        try:
            while True:
                if self.recording:
                    frame = self.record_frame()
                    self.frames.append(frame)
                    time.sleep(self.frame_delay)
                else:
                    time.sleep(0.1)
        finally:
            print("\nRe-enabling torque...")
            for joint_id in self.joint_name_to_id.values():
                self.ac.configure_actuator(actuator_id=joint_id, torque_enabled=True)
