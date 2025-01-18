import time

import pykos
from walk import JOINT_NAME_TO_KOS_ID, demo, offsets_by_name, stable_stand

# Connect to robot
kos = pykos.KOS(ip=demo)
ac = kos.actuator

# Configure all joints
for id in JOINT_NAME_TO_KOS_ID.values():
    ac.configure_actuator(actuator_id=id, torque_enabled=True)


def wave_right_arm_up_commands() -> list[dict]:
    return [
        {
            "actuator_id": JOINT_NAME_TO_KOS_ID["right_shoulder_pitch"],
            "position": -180 - offsets_by_name["right_shoulder_pitch"],
        },
        {
            "actuator_id": JOINT_NAME_TO_KOS_ID["right_shoulder_roll"],
            "position": 10 - offsets_by_name["right_shoulder_roll"],
        },
        {"actuator_id": JOINT_NAME_TO_KOS_ID["right_elbow"], "position": -10 - offsets_by_name["right_elbow"]},
    ]


def wave_right_arm_down_commands() -> list[dict]:
    return [
        {
            "actuator_id": JOINT_NAME_TO_KOS_ID["right_shoulder_pitch"],
            "position": -180 - offsets_by_name["right_shoulder_pitch"],
        },
        {
            "actuator_id": JOINT_NAME_TO_KOS_ID["right_shoulder_roll"],
            "position": 0 - offsets_by_name["right_shoulder_roll"],
        },
        {"actuator_id": JOINT_NAME_TO_KOS_ID["right_elbow"], "position": 10 - offsets_by_name["right_elbow"]},
    ]


def wave_sequence():
    # Start from stable standing position
    stable_stand()
    time.sleep(1)  # Wait for robot to stabilize

    # Perform waving motion
    for _ in range(5):  # Wave 5 times
        ac.command_actuators(wave_right_arm_up_commands())
        time.sleep(0.5)
        ac.command_actuators(wave_right_arm_down_commands())
        time.sleep(0.5)

    # Return to stable standing position
    stable_stand()


if __name__ == "__main__":
    wave_sequence()
