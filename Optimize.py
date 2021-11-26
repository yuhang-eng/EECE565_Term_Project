from gurobipy import *
from tabulate import tabulate

from Model.MECsNET import MECsNET


def run():
    try:
        file = open("./UserData.dat", "r")
        model = Model("Mobile Edge Computing Optimization")
        network = MECsNET(model)

        N = int(file.readline())

        for i in range(N):
            l = file.readline()
            node_data = l.split(",")
            network.add_new_random_node(node_data[0], node_data[1], node_data[2], node_data[3])

        set_objective_function(network)
        set_equality_constrain(network)
        set_inequality_constrain(network)

        model.setParam("NonConvex", 2)
        # model.setParam("MIPGap", 0.25)
        model.Params.TimeLimit = 600

        model.write("log.lp")
        model.optimize()

        print_result(network, N)

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError as e:
        print('Encountered an attribute error')


def set_objective_function(network: MECsNET):
    network.model.setObjectiveN(quicksum(network.nodes[i].overall_time_sum for i in range(network.get_size())), 1)
    network.model.setObjectiveN(quicksum(network.nodes[i].total_energy for i in range(network.get_size())),
                                2)


def set_equality_constrain(network: MECsNET):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.local_compute_time == ((1 - node.x) * node.task_size) / node.cpu_power)
        model.addConstr(node.local_to_mec_time * node.transmit_rate == node.x * node.data_size)
        model.addConstr(node.mec_compute_time * node.mec_cpu_power == node.x * node.task_size)

        model.addConstr(node.interference == quicksum(network.nodes[j].x * network.nodes[j].transmit_power
                                                      * (node.distance(0, 0) ** -2) for j in range(network.get_size())
                                                      if j != i)
                        + network.background_noise)
        model.addConstr(node.signal_power == node.x * node.transmit_power * (node.distance(0, 0) ** 2))

        model.addConstr(node.signal_power_plus == node.signal_power + 1)
        model.addGenConstrLogA(node.signal_power_plus, node.max_transmit_rate, 2)

        model.addConstr(
            node.local_energy_consumption == node.task_size * node.cpu_power * node.cpu_power * network.k * (1 - node.x))
        model.addConstr(node.mec_energy_consumption == node.transmit_power * node.local_to_mec_time)
        model.addConstr(node.total_energy == node.x * node.mec_energy_consumption + (1 - node.x) * node.local_energy_consumption)
        model.addConstr(quicksum(network.nodes[i].x for i in range(network.get_size())) == network.busy_thread)


def set_inequality_constrain(network: MECsNET):
    model = network.model
    for i in range(network.get_size()):
        node = network.nodes[i]
        model.addConstr(node.overall_time_sum >= node.mec_compute_time + node.local_to_mec_time)
        model.addConstr(node.overall_time_sum >= node.local_compute_time)
        model.addConstr(node.signal_power >= node.interference * network.SINR_threshold)
        model.addConstr(node.transmit_rate * network.busy_thread <= node.max_transmit_rate * 2 * network.bandwidth)
        model.addConstr(node.transmit_power >= node.min_power)
        model.addConstr(node.transmit_power <= node.max_power)
        model.addConstr(network.busy_thread <= network.mec_max_thread)
        model.addConstr(quicksum(network.nodes[i].mec_cpu_power * network.nodes[i].x
                                 for i in range(network.get_size())) <= network.max_cpu)

        # model.addConstr(node.x <= 1)
        # model.addConstr(node.x >= 0)


def print_result(network: MECsNET, N):
    result = []
    for i in range(network.get_size()):
        result.append(network.nodes[i].get_result())

    m = network.model
    nSolutions = m.SolCount
    nObjectives = m.NumObj
    print('Problem has', nObjectives, 'objectives')
    print('Gurobi found', nSolutions, 'solutions')
    print(tabulate(result, headers=['index', 'x', 'time', 'energy', 'cpu', 'rate', 'power',
                                    'edge time', 'local time', 'transmit time', 'edge time',
                                    'Signal Power', 'data size', 'task size', 'maximum rate', 'distance',
                                    'interference']))
    m.params.SolutionNumber = 0
    m.params.ObjNumber = 1
    print(' ', m.ObjNVal / N, end='')
    m.params.ObjNumber = 2
    print(' ', m.ObjNVal / N, end='')


run()
