import pykos
import csv
import time
# print('reached')
kos = pykos.KOS(ip='10.33.13.110')
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

parameters = {
    'l_shoulder' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'l_rotator' : {'kp': 90, 'kd': 40, 'torque_enabled': True},
    'l_elbow' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_shoulder' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_elbow' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_rotator' : {'kp': 90, 'kd': 40, 'torque_enabled': True},
    'l_ankle' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'l_knee' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'l_thigh' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'l_hamstring' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'l_hip' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_ankle' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_knee' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_thigh' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_hamstring' : {'kp': 50, 'kd': 40, 'torque_enabled': True},
    'r_hip' : {'kp': 50, 'kd': 40, 'torque_enabled': True}
}

def configure_motors(parameters, body):
    for part in body:
        kos.actuator.configure_actuator(actuator_id=body[part], **parameters[part])


 
actuator_id = body['r_elbow']
# kos.actuator.configure_actuator(actuator_id=actuator_id, kp=50, kd=20, torque_enabled=True)
# kos.actuator.configure_actuator(actuator_id=actuator_id, kp=50, kd=20, torque_enabled=True)
# [kos.actuator.configure_actuator(actuator_id=body[i],kp=50, kd=40, torque_enabled=True) for i in body]


# print(get_position('l_shoulder'))

def move_to_position(part, position, velocity: int = 2, threshold = 2, magnitude: bool = True):
    
    '''
    Moves the actuator to a specified position at a specified velocity till it hits a threshold. This is used to bypass the 
    undershoot and overshoot problems that exist in the 

    Args:
        part: The part of the body that is being moved
        position: The position that the actuator is being moved to (in degrees)
        velocity: The velocity at which the actuator is being moved (for convention, keep it a positive value. Direction will be controlled by the magnitude argument)
        threshold: The threshold at which the actuator stops moving. Set to two degrees of accuracy as a default
        magnitude: The direction in which the actuator is being moved. If True, the actuator moves in the positive direction, else it moves in the negative direction

    '''

    scaler = 1 if magnitude else -1

    actuator_id = body[part]
    cur_pos = kos.actuator.get_actuators_state([actuator_id])[0].position
    while abs(cur_pos - position) <= threshold:
        kos.actuator.command_actuators([{"actuator_id": actuator_id, "velocity": velocity * scaler}])
        # time.sleep(0.5)
        cur_pos = kos.actuator.get_actuators_state([actuator_id])[0].position
    kos.actuator.command_actuators([{"actuator_id": actuator_id, "position": position }])



def hold_position(part):
    id = body[part]
    cur_val = kos.actuator.get_actuators_state([id])[0].position
    kos.actuator.command_actuators([{"actuator_id": id, "position": cur_val}])

    


# print("Reached")

def prostate():
    # move_to_position('l_shoulder', 110)
    # move_to_position('l_rotator', 35)
    # move_to_position('l_elbow', -90)
    # time.sleep(0.5)
    # move_to_position('r_shoulder', -157, magnitude = False)
    # move_to_position('r_rotator', -70, magnitude = True)
    # move_to_position('r_elbow', -113, magnitude = False)
    # actuator_id = body['r_ankle']
    # kos.actuator.command_actuators([{"actuator_id": actuator_id, "position": 0}])
    # for part in body:
    #     kos.actuator.command_actuators([{"actuator_id": body[part], "position": 0}])
    # kos.actuator.command_actuators([{"actuator_id": body['l_shoulder'], "position": 110}, {"actuator_id": body['l_rotator'], "position": 35}, {"actuator_id": body['l_elbow'], "position": -90}])
    # time.sleep(4)
    # kos.actuator.command_actuators([{"actuator_id": body['r_shoulder'], "position": -157}, {"actuator_id": body['r_rotator'], "position": -70}])
    kos.actuator.command_actuators([{"actuator_id": body['l_ankle'], "position": 100}, {"actuator_id" : body['l_knee'], 'position' : 100}])
    kos.actuator.command_actuators([{"actuator_id": body['r_ankle'], "position": -100}, {'actuator_id': body['r_knee'], "position": -100}])
    time.sleep(4)
    # The two lines above deal with folding in the legs for the purpose of getting to the standing up state

    kos.actuator.command_actuators([{"actuator_id": body['l_rotator'], "position": -20}, {"actuator_id": body['r_rotator'], "position": 20}])
    kos.actuator.command_actuators([{"actuator_id": body['l_thigh'], "position": -62}, {"actuator_id": body['r_thigh'], "position": 59}])

    time.sleep(2)

    kos.actuator.command_actuators([{"actuator_id": body['l_rotator'], "position": -45}, {"actuator_id": body['r_rotator'], "position": 42}])

    time.sleep(2)

    kos.actuator.command_actuators([{"actuator_id": body['l_hamstring'], "position": 10}, {"actuator_id": body['r_hamstring'], "position": -26}])

    time.sleep(1)

    kos.actuator.command_actuators([{"actuator_id": body['l_hamstring'], "position": -40}, {"actuator_id": body['r_hamstring'], "position": 14}])

    # kos.actuator.command_actuators([{"actuator_id": body['l_shoulder'], "position": -45}, {"actuator_id": body['r_shoulder'], "position": 40}])

    # time.sleep(0.5)

    # kos.actuator.command_actuators([{"actuator_id": body['l_rotator'], "position": -86}, {"actuator_id": body['r_rotator'], "position": 80}])
    # kos.actuator.command_actuators([{"actuator_id": body['l_shoulder'], "position" : -20}], {"actuator_id": body['r_shoulder'], 'position': 39})

    # kos.actuator.command_actuators([{"actuator_id": body['l_hip'], "position": 50}, {"actuator_id": body['r_hip'], "position": -48}])

    # parameters['l_rotator']['kp'] = 140
    # parameters['r_rotator']['kp'] = 140

    # kos.actuator.command_actuators([{"actuator_id": body['l_rotator'], "position": -20}, {"actuator_id": body['r_rotator'], "position":20}])




configure_motors(parameters, body)
prostate()
