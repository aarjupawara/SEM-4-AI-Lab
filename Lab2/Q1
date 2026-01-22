start = (7,2,4,
         5,0,6,
         8,3,1)

goal  = (0,1,2,
         3,4,5,
         6,7,8)

class Queue:
    def __init__(self):
        self.items = [] #Stores queue elements in a list.

    def enqueue(self, item):
        self.items.append(item)  # add to end

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # remove from front
        return None

    def is_empty(self):
        return len(self.items) == 0  #check if empty

def bfs(start, goal):
    queue = Queue()
    queue.enqueue((start, 0, [start]))  # store state, moves, path
    visited = {start}
    count = 0

    while not queue.is_empty():
        state, moves, path = queue.dequeue()
        count += 1

        if state == goal:
            print(f"Number of moves to reach goal: {moves}")
            print(f"Number of states explored: {count}")
            print("Path from start to goal:")
            for s in path:
                # print as 3x3 puzzle for clarity
                print(f"{s[0]} {s[1]} {s[2]}")
                print(f"{s[3]} {s[4]} {s[5]}")
                print(f"{s[6]} {s[7]} {s[8]}")
                print("---")
            return count

        i = state.index(0) #find the blank tiles.
        for j in [(i-3),(i+3),(i-1),(i+1)]:
            # check boundaries and prevent left/right wrap
            if 0 <= j < 9 and not (i%3==0 and j==i-1) and not (i%3==2 and j==i+1):
                new = list(state)
                new[i], new[j] = new[j], new[i]
                new = tuple(new)

                if new not in visited:
                    visited.add(new)
                    queue.enqueue((new, moves + 1, path + [new]))

print("BFS states explored:", bfs(start, goal))
