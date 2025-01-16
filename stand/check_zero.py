import pykos
import csv
import time
# print('reached')
kos = pykos.KOS(ip='192.168.42.1')
# print("reached2")


body = {
    'l_shoulder' : 14,
    'l_rotator' : 15,
    'l_elbow' : 16,
    'r_shoulder' : 13,
    'r_elbow' : 11,
    'r_rotator' : 12,
    'l_ankle' : 6,
    'l_knee' : 7,
    'l_thigh' : 8,
    'l_hamstring' : 9,
    'l_hip' : 10,
    'r_ankle' : 1,
    'r_knee' : 2,
    'r_thigh' : 3,
    'r_hamstring' : 4,
    'r_hip' : 5
}

[kos.actuator.configure_actuator(actuator_id=body[i],kp=50, kd=40, torque_enabled=True) for i in body]
[kos.actuator.command_actuators([{"actuator_id": body[part], "position": 0} for part in body])]