from collections import defaultdict, deque

class HangingSpot:
    def __init__(self, id):
        self.id = id
        self.parents = set()
        self.children = set()

class BananaTree:
    def __init__(self):
        self.spots = {}

    def add_relation(self, parent, child):
        if parent not in self.spots:
            self.spots[parent] = HangingSpot(parent)
        if child not in self.spots:
            self.spots[child] = HangingSpot(child)
        self.spots[parent].children.add(child)
        self.spots[child].parents.add(parent)

class Grove:
    def __init__(self):
        self.spot_map = {}

    def add_tree(self, tree):
        for spot_id, spot in tree.spots.items():
            if spot_id not in self.spot_map:
                self.spot_map[spot_id] = HangingSpot(spot_id)
            self.spot_map[spot_id].parents.update(spot.parents)
            self.spot_map[spot_id].children.update(spot.children)

    def min_energy(self, start, end):
        queue = deque()
        queue.append((start, 0))
        visited = set()

        while queue:
            current, energy = queue.popleft()
            if current == end:
                return energy
            if (current, energy) in visited:
                continue
            visited.add((current, energy))
            
            spot = self.spot_map[current]
            # Climb down (free): go to children
            for child in spot.children:
                if (child, energy) not in visited:
                    queue.appendleft((child, energy))  # zero cost path

            # Climb up or tree switch (cost 1): parents and possible switch spots
            for next_spot in spot.parents | {s for s in self.spot_map if current in self.spot_map[s].children and s != current}:
                if (next_spot, energy + 1) not in visited:
                    queue.append((next_spot, energy + 1))
        return -1  # unreachable
