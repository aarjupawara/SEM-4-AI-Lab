import random

environment = ["A", "B", "C"]

# State matrix: [[A, B, C]] where 0=Clean, 1=Dirty
state = [[random.choice([0, 1]), 
          random.choice([0, 1]), 
          random.choice([0, 1])]]

# Reward matrix: [cleaning, move, complete, timestep]
reward = [[10, -1, 20, -0.5]]

#initial location 
start = random.choice(environment)

final_reward = 0

def clean(state):
    for s in state[0]:
        if s != 0:
            return False
    return True

print("\n Initial State:", state)
print("Initial Location:", start)
print("Rewards:", reward)
print("(State: 0=Clean/1=Dirty | Rewards: [clean,move,complete,time])\n")

for step in range(10):
    loc_idx = {"A":0,"B":1,"C":2}[start]
    percept = (start, state[0][0], state[0][1], state[0][2])
    
    if state[0][loc_idx] == 1:
        action = "cleaning"
        state[0][loc_idx] = 0
        final_reward += reward[0][0]  # cleaning reward
    
    elif clean(state):
        action = "complete"
        final_reward += reward[0][2]  # complete
        print(f"Percept: {percept} | Action: {action} | Loc: {start}")
        break
    
    else:
        action = "move"
        final_reward += reward[0][1]  # move reward
        
        if start == "A": 
            start = "B" if state[0][1] ==1 else "C"
        elif start == "B": 
            start = "C" if state[0][2]==1 else "A"
        else: 
            start = "A" if state[0][0]==1 else "B"
    
    final_reward += reward[0][3]  # timestep every step
    print(f"Percept: {percept} | Action: {action} | Loc: {start}")

print("\n final Reward:", final_reward)

