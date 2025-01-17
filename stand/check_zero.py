import pykos
import csv
import time
# print('reached')
kos = pykos.KOS(ip='192.168.42.1')
# print("reached2")


body = {
    'l_shoulder' : 11,
    'l_rotator' : 12,
    'l_elbow' : 13,
    'r_shoulder' : 21,
    'r_elbow' : 23,
    'r_rotator' : 22,
    'l_ankle' : 35,
    'l_knee' : 34,
    'l_thigh' : 33,
    'l_hamstring' : 32,
    'l_hip' : 31,
    'r_ankle' : 45,
    'r_knee' : 44,
    'r_thigh' : 43,
    'r_hamstring' :42,
    'r_hip' : 41
}

for i in range(1):
    [kos.actuator.configure_actuator(actuator_id=body[i],kp=50, kd=40, torque_enabled=True) for i in body]
for i in range(1):
    # [kos.actuator.command_actuators([{"actuator_id": body[part], "position": 0} for part in body])]
    [kos.actuator.command_actuators([{"actuator_id": body['l_ankle'], 'position': 0}])]
    [kos.actuator.command_actuators([{"actuator_id": body['l_knee'], 'position': 0}])]