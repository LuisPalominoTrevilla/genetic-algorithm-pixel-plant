import math

class RulesManager:
    def __init__(self, execution_mode):
        self.execution_mode = execution_mode

        if self.execution_mode == 1 or execution_mode == 2:
            self.max_num_leaves = 8
            self.min_num_branches = 0
            self.max_num_branches = math.inf

        if self.execution_mode == 3:
            self.max_num_leaves = 15
            self.min_num_branches = 1
            self.max_num_branches = 5

    def calc_score(self, energyProduced, energyConsumed, nutrientsStored, nutrientsConsumed):
        if self.execution_mode == 1:
            return (energyProduced - energyConsumed) ** 2 + (nutrientsStored - nutrientsConsumed) ** 2
        else:
            return (energyProduced ** 3) - energyConsumed  + (nutrientsStored ** 2) - nutrientsConsumed
