from random import randint, choices, random, choice
from copy import deepcopy


class PixelPlant:
    def __init__(self):
        self.TRUNK = '#663d14'
        self.BRANCH = '#855723'
        self.LEAF = '#4e691a'
        self.NULL = '#ffffff'
        self.w = 16
        self.h = 32
        self.trunk_limit = self.h - 8
        self.im = self._createEmptyCanvas()

    def _createEmptyCanvas(self):
        return [[self.NULL for j in range(self.w)] for i in range(self.h)]

    def _getPossibleLocations(self, i, j):
        successors = []
        forbidden = set([self.BRANCH, self.TRUNK])
        if j > 0 and self.im[i][j-1] not in forbidden:
            successors.append((i, j-1))
        if j < self.w-1 and self.im[i][j+1] not in forbidden:
            successors.append((i, j+1))
        if i > 0 and self.im[i-1][j] not in forbidden:
            successors.append((i-1, j))
        if i < self.trunk_limit-1 and self.im[i+1][j] not in forbidden:
            successors.append((i+1, j))
        return successors

    def _getNeighbors(self, i, j):
        neighbors = []
        if j > 0:
            neighbors.append((i, j-1))
        if j < self.w-1:
            neighbors.append((i, j+1))
        if i > 0:
            neighbors.append((i-1, j))
        if i < self.trunk_limit-1:
            neighbors.append((i+1, j))
        return neighbors

    def genRandom(self):
        num = randint(4, 10)
        for i in range(self.h-1, 2, -1):
            if i >= self.trunk_limit:
                trunk_girth = 3
            elif i % 2 != self.trunk_limit % 2:
                num = randint(prev[0]-1, prev[1]-2)
                if num < prev[0]:
                    trunk_girth = choices(
                        population=[2, 3, 4],
                        weights=[.1, .5, .4],
                        k=1)[0]
                elif num == prev[1]-1:
                    trunk_girth = choices(
                        population=[1, 2],
                        weights=[.2, .8],
                        k=1)[0]
                else:
                    trunk_girth = choices(
                        population=[1, 2, 3],
                        weights=[.1, .3, .6],
                        k=1)[0]
            prev = (num, num+trunk_girth)
            # Paint tree trunk
            for j in range(num, num+trunk_girth):
                if j < 0 or j >= self.w:
                    continue
                self.im[i][j] = self.TRUNK
            # Paint tree branch
            if (trunk_girth > 1 and i < self.trunk_limit and random() < .34 and i % 2 != self.trunk_limit % 2):
                left_growth = randint(0, 1) == 0
                branch_start = prev[0] if left_growth else prev[1] - 1
                pixel_pos_i = i
                pixel_pos_j = branch_start
                while pixel_pos_j > 0 and pixel_pos_j < self.w-1 and pixel_pos_i > 0 and pixel_pos_i < self.trunk_limit:
                    pixel_pos_j += -1 if left_growth else 1
                    if self.im[pixel_pos_i][pixel_pos_j] != self.NULL:
                        break
                    self.im[pixel_pos_i][pixel_pos_j] = self.BRANCH
                    pixel_pos_i += choices(
                        population=[1, 0, -1],
                        weights=[.05, .25, .7],
                        k=1
                    )[0]
                    self.im[pixel_pos_i][pixel_pos_j] = self.BRANCH
                # Paint tree leaf
                num_leafs = randint(3, 8)
                leaf_positions = self._getPossibleLocations(
                    pixel_pos_i, pixel_pos_j)
                while num_leafs > 0 and len(leaf_positions) > 0:
                    i, j = leaf_positions.pop()
                    self.im[i][j] = self.LEAF
                    if (len(leaf_positions) == 0):
                        leaf_positions = self._getPossibleLocations(i, j)
                    num_leafs -= 1
            if (prev[0] < 0 and prev[1] <= 0) or (prev[0] >= self.w and prev[1] > self.w):
                break
        return self.im

    def getScore(self):
        nutrientsStored, nutrientsConsumed = 0, 0
        energyProduced, energyConsumed = 0, 0
        im = deepcopy(self.im)
        # Calculate leaf score and validate rules
        for i in range(self.h):
            for j in range(self.w):
                if im[i][j] != self.LEAF:
                    continue
                visited = set()
                frontier = [(i, j)]
                connected = False
                num_leafs = 0
                while len(frontier) > 0:
                    leaf_i, leaf_j = frontier.pop()
                    num_leafs += 1
                    energyProduced += 2
                    nutrientsConsumed += .25
                    im[leaf_i][leaf_j] = self.NULL
                    neighbors = self._getNeighbors(leaf_i, leaf_j)
                    for n_i, n_j in neighbors:
                        if im[n_i][n_j] == self.LEAF and (n_i, n_j) not in visited:
                            visited.add((n_i, n_j))
                            frontier.append((n_i, n_j))
                        elif im[n_i][n_j] == self.BRANCH:
                            connected = True
                if not connected or num_leafs > 8:
                    return 0
        # Calculate branch score and validate rules
        for i in range(self.h):
            for j in range(self.w):
                if im[i][j] != self.BRANCH:
                    continue
                energyConsumed += .25
                nutrientsConsumed += .5
                im[i][j] = self.NULL
        # Calculate trunk score and validate rules
        for i in range(self.h):
            for j in range(self.w):
                if im[i][j] != self.TRUNK:
                    continue
                energyConsumed += .1
                nutrientsStored += 1.5
                im[i][j] = self.NULL
        return (energyProduced - energyConsumed) ** 2 + (nutrientsStored - nutrientsConsumed) ** 2
