import json
import signal
import sys
import time

import pykos
from walk import JOINT_NAME_TO_KOS_ID, demo, stable_stand


class FrameRecorder:
    def __init__(self):
        self.kos = pykos.KOS(ip=demo)
        self.ac = self.kos.actuator
        self.frames = []
        self.recording = False
        self.setup_signal_handler()

    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, signum, frame):
        if not self.recording:
            print("\nStarting recording... Press Ctrl+C again to stop.")
            self.recording = True
            self.frames = []
        else:
            print("\nStopping recording...")
            self.recording = False
            self.save_frames()
            sys.exit(0)

    def record_frame(self):
        # Get all joint IDs
        joint_ids = list(JOINT_NAME_TO_KOS_ID.values())

        # Batch get all actuator states
        states_obj = self.ac.get_actuators_state(joint_ids)

        # Create frame dictionary mapping joint names to positions
        frame = {}
        for state in states_obj.states:
            # Find joint name by ID
            joint_name = next(name for name, id in JOINT_NAME_TO_KOS_ID.items() if id == state.actuator_id)
            frame[joint_name] = state.position

        return frame

    def save_frames(self):
        if not self.frames:
            print("No frames recorded!")
            return

        filename = f"recorded_motion_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(self.frames, f, indent=2)
        print(f"Saved {len(self.frames)} frames to {filename}")

    def replay_frames(self, filename):
        with open(filename, "r") as f:
            frames = json.load(f)

        print(f"Replaying {len(frames)} frames...")
        stable_stand()  # Start from stable position
        time.sleep(1)

        for frame in frames:
            commands = []
            for joint_name, position in frame.items():
                commands.append({"actuator_id": JOINT_NAME_TO_KOS_ID[joint_name], "position": position})
            self.ac.command_actuators(commands)
            time.sleep(0.05)  # 50ms between frames

        stable_stand()  # Return to stable position

    def record(self):
        print("Disabling torque to allow manual positioning...")
        # Disable torque on all joints
        for joint_id in JOINT_NAME_TO_KOS_ID.values():
            self.ac.configure_actuator(actuator_id=joint_id, torque_enabled=False)

        print("Move the robot to desired positions.")
        print("Press Ctrl+C to start recording.")
        print("Press Ctrl+C again to stop recording and save frames.")

        try:
            while True:
                if self.recording:
                    frame = self.record_frame()
                    self.frames.append(frame)
                    time.sleep(0.05)  # Record at 20Hz
                else:
                    time.sleep(0.1)
        finally:
            # Re-enable torque when done or if interrupted
            print("\nRe-enabling torque...")
            for joint_id in JOINT_NAME_TO_KOS_ID.values():
                self.ac.configure_actuator(actuator_id=joint_id, torque_enabled=True)


def main():
    recorder = FrameRecorder()
    if len(sys.argv) > 1 and sys.argv[1] == "--replay":
        if len(sys.argv) != 3:
            print("Usage for replay: python record_frames.py --replay <filename>")
            sys.exit(1)
        recorder.replay_frames(sys.argv[2])
    else:
        recorder.record()


if __name__ == "__main__":
    main()
