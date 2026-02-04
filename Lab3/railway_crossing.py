import random

gate ="MainGate"

#percept
track_values = [0, 1]
obstacle_values = [0,1] # "Detected =1", "Not Detected"= 0

# Actuators initialization raise, OFF, green
actuators = [[1,0,1]]

gate_arm = ["raise", "lowerd"]
alarm = ["ON", "OFF"]
signal = ["green", "red"]
percept = ["detected", "not detected"]

print("\n")
print(f"Crossing: {gate}")
print(f"Initial Actuators State:", gate_arm[actuators[0][0]], alarm[actuators[0][1]], signal[actuators[0][2]])
print("\n")

percepts = [[
    random.choice(track_values), # train coming to station 
    random.choice(track_values),  # train going away to station 
    random.choice(obstacle_values)
]]

print(f"Percepts at {gate}:")
print(f"Train coming: {'detected' if percepts[0][0]==1 else 'not detected'}")
print(f"Train going: {'detected' if percepts[0][1]==1 else 'not detected'}")
print(f"Obstacle: {'detected' if percepts[0][2]==1 else 'not detected'}\n")


if percepts[0][2] == 1:  # obstacle
    actuators[0] = [0, 1, 0]  # Lower, ON, RED

elif percepts[0][0] == 1 or percepts[0][1] == 1:  # no obstacle, train detected
    actuators[0] = [0, 1, 0]  # Lower, ON, RED

else:
    actuators[0] = [1,0,1] #inital 

print(f"Updated Actuators State at {gate}:")
print(f"Gate Arm: {gate_arm[actuators[0][0]]}")
print(f"Alarm: {alarm[actuators[0][1]]}")
print(f"Signal: {signal[actuators[0][2]]}\n")

