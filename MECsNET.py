import random
from typing import List
from gurobipy import *
from Model.userEquipments import UE


class MECsNET:
    nodes = List[UE]

    def __init__(self, model):
        self.max_cpu = 10 ** 10  # 10GHz
        self.bandwidth = 2 * (10 ** 7)  # 20 MHz
        self.mec_max_thread = 100
        self.background_noise = 10 ** -9  # -100db
        self.model = model
        self.nodes = []
        self.k = 5 * (10 ** -27)
        self.SINR_threshold = 10 ** -26
        self.busy_thread = model.addVar(vtype=GRB.CONTINUOUS, name="busy_thread")

    def add_new_random_node(self, transmit_data_size, compute_task_size, X_coordinate, Y_coordinate):
        max_transmit_power = 100
        min_transmit_power = 0
        local_cpu_power = 10 ** 9  # 1GHz
        self.nodes.append(
            UE(int(transmit_data_size), [int(X_coordinate), int(Y_coordinate)], int(compute_task_size),
                 max_transmit_power, min_transmit_power, local_cpu_power, self.model, str(self.get_size() + 1)))

    def get_size(self):
        return len(self.nodes)
