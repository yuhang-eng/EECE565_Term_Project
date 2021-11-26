from gurobipy import *


class UE:

    def __init__(self, transmit_data_size, position, compute_task_size, max_transmit_power, min_transmit_power, cpu_power, gurobi_model, index):
        self.data_size = transmit_data_size
        self.position = position
        self.task_size = compute_task_size
        self.max_power = max_transmit_power
        self.min_power = min_transmit_power
        self.cpu_power = cpu_power

        self.overall_time_sum = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t" + index)
        self.local_compute_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_l" + index)
        self.mec_compute_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_ec" + index)
        self.local_to_mec_time = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="t_et" + index)

        self.transmit_rate = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="r" + index)
        self.mec_cpu_power = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="f" + index)
        self.max_transmit_rate = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="mr" + index)
        self.signal_power_plus = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="mir" + index)
        self.interference = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="ir" + index)
        self.transmit_power = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="p" + index)
        self.signal_power = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="SINR" + index)

        self.total_energy = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="e" + index)
        self.local_energy_consumption = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="el" + index)
        self.mec_energy_consumption = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="ee" + index)

        self.x = gurobi_model.addVar(vtype=GRB.BINARY, name="x")
        # self.x = gurobi_model.addVar(vtype=GRB.CONTINUOUS, name="x")
        self.index = index

    def distance(self, x, y):
        return math.sqrt((self.position[0] - x) ** 2 + (self.position[1] - y) ** 2)

    def get_result(self):
        result = [self.index, self.x.x, self.overall_time_sum.x, self.total_energy.x, self.mec_cpu_power.x, self.transmit_rate.x,
                  self.transmit_power.x, self.mec_compute_time.x, self.local_compute_time.x, self.local_to_mec_time.x,
                  self.signal_power.x, self.data_size, self.task_size, self.max_transmit_rate.x, self.distance(0,0), self.interference.x]
        return result