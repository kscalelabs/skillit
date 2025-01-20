"""Freezes actuators in place."""

import pykos
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("freeze", choices=["on", "off"], help="Freeze or unfreeze actuators")
    parser.add_argument("--ip", type=str, default="192.168.42.1")
    args = parser.parse_args()

    kos = pykos.KOS(args.ip)
    for joint_id in list(range(41, 46)) + list(range(31, 36)):
        kos.actuator.configure_actuator(actuator_id=joint_id, torque_enabled=args.freeze == "on")


if __name__ == "__main__":
    # python -m examples.freeze
    main()
