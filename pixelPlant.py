from random import randint, choices, random, choice
import imageManipulation as img
from copy import deepcopy
import sys

class PixelPlant:
    def __init__(self, rulesManager):
        self.TRUNK = '#663d14'
        self.BRANCH = '#855723'
        self.LEAF = '#4e691a'
        self.NULL = '#ffffff'
        self.w = 16
        self.h = 32
        self.trunk_limit = self.h - 8
        self.im = self._createEmptyCanvas()
        self.rulesManager = rulesManager

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

    def _getNeighbors(self, i, j, i_limit=None):
        if i_limit is None:
            i_limit = self.h-1
        neighbors = []
        if j > 0:
            neighbors.append((i, j-1))
        if j < self.w-1:
            neighbors.append((i, j+1))
        if i > 0:
            neighbors.append((i-1, j))
        if i < i_limit:
            neighbors.append((i+1, j))
        return neighbors

    def genRandom(self):
        MAX_NUM_LEAVES = self.rulesManager.max_num_leaves

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
                painted_branch = False
                while pixel_pos_j > 0 and pixel_pos_j < self.w-1 and pixel_pos_i > 0 and pixel_pos_i < self.trunk_limit:
                    pixel_pos_j += -1 if left_growth else 1
                    if self.im[pixel_pos_i][pixel_pos_j] != self.NULL:
                        break
                    self.im[pixel_pos_i][pixel_pos_j] = self.BRANCH
                    painted_branch = True
                    pixel_pos_i += choices(
                        population=[1, 0, -1],
                        weights=[.05, .25, .7],
                        k=1
                    )[0]
                    if pixel_pos_i >= self.trunk_limit or self.im[pixel_pos_i][pixel_pos_j] != self.NULL:
                        break
                    self.im[pixel_pos_i][pixel_pos_j] = self.BRANCH
                if not painted_branch or pixel_pos_j < 0 or pixel_pos_j >= self.w or pixel_pos_i < 0 or pixel_pos_i >= self.trunk_limit:
                    continue
                # Paint tree leaf
                num_leafs = randint(3, MAX_NUM_LEAVES)
                leaf_positions = self._getPossibleLocations(
                    pixel_pos_i, pixel_pos_j)
                while num_leafs > 0 and len(leaf_positions) > 0:
                    leaf_i, leaf_j = leaf_positions.pop()
                    self.im[leaf_i][leaf_j] = self.LEAF
                    if (len(leaf_positions) == 0):
                        leaf_positions = self._getPossibleLocations(
                            leaf_i, leaf_j)
                    num_leafs -= 1
            if (prev[0] < 0 and prev[1] <= 0) or (prev[0] >= self.w and prev[1] > self.w):
                break

    def crossover(self, plant):
        crossover_i, crossover_j = self.h/2, self.w/2
        offspring = PixelPlant(plant.rulesManager)
        parent_1 = True
        for i in range(offspring.h):
            for j in range(offspring.w):
                if i == crossover_i and j == crossover_j:
                    parent_1 = False
                offspring.im[i][j] = self.im[i][j] if parent_1 else plant.im[i][j]
        return offspring

    def getScore(self):
        MAX_NUM_LEAVES = self.rulesManager.max_num_leaves
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
                forbidden_position = False
                while len(frontier) > 0:
                    leaf_i, leaf_j = frontier.pop()
                    num_leafs += 1
                    if leaf_i >= self.trunk_limit or num_leafs > MAX_NUM_LEAVES:
                        forbidden_position = True
                        break
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
                if not connected or num_leafs > MAX_NUM_LEAVES or forbidden_position:
                    return 0
        # Calculate branch score and validate rules
        for i in range(self.h):
            for j in range(self.w):
                if im[i][j] != self.BRANCH:
                    continue
                num_branches = 0
                visited = set()
                frontier = [(i, j)]
                connected = False
                forbidden_position = False
                while len(frontier) > 0:
                    branch_i, branch_j = frontier.pop()
                    num_branches += 1
                    if branch_i >= self.trunk_limit:
                        print("Forbidden position branch")
                        forbidden_position = True
                        break
                    energyConsumed += .25
                    nutrientsConsumed += .5
                    im[branch_i][branch_j] = self.NULL
                    neighbors = self._getNeighbors(branch_i, branch_j)
                    for n_i, n_j in neighbors:
                        if im[n_i][n_j] == self.BRANCH and (n_i, n_j) not in visited:
                            visited.add((n_i, n_j))
                            frontier.append((n_i, n_j))
                        elif im[n_i][n_j] == self.TRUNK:
                            connected = True
                if not connected or forbidden_position or num_branches < self.rulesManager.min_num_branches or num_branches > self.rulesManager.max_num_branches:
                    return 0
        # Calculate trunk score and validate rules
        foundTrunk = False
        for i in range(self.h):
            for j in range(self.w):
                if im[i][j] != self.TRUNK:
                    continue
                if foundTrunk:
                    return 0
                visited = set()
                frontier = [(i, j)]
                rooted = False
                foundTrunk = True
                while len(frontier) > 0:
                    trunk_i, trunk_j = frontier.pop()
                    if trunk_i == self.h-1:
                        rooted = True
                    energyConsumed += .1
                    nutrientsStored += 1.5
                    im[trunk_i][trunk_j] = self.NULL
                    neighbors = self._getNeighbors(trunk_i, trunk_j)
                    for n_i, n_j in neighbors:
                        if im[n_i][n_j] == self.TRUNK and (n_i, n_j) not in visited:
                            visited.add((n_i, n_j))
                            frontier.append((n_i, n_j))
                if not rooted:
                    return 0

        return self.rulesManager.calc_score(energyProduced, energyConsumed, nutrientsStored, nutrientsConsumed)


    def toImage(self):
        return img.toRGBImage(self.im)
