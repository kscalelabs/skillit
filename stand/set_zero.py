import time

import pykos

kos = pykos.KOS(ip="192.168.42.1")

body = {
    "l_shoulder": 11,
    "l_rotator": 12,
    "l_elbow": 13,
    "r_shoulder": 21,
    "r_elbow": 23,
    "r_rotator": 22,
    "l_ankle": 35,
    "l_knee": 34,
    "l_thigh": 33,
    "l_hamstring": 32,
    "l_hip": 31,
    "r_ankle": 45,
    "r_knee": 44,
    "r_thigh": 43,
    "r_hamstring": 42,
    "r_hip": 41,
}

for i in range(10):
    [kos.actuator.configure_actuator(actuator_id=body[part], zero_position=True) for part in body]
    time.sleep(0.1)
