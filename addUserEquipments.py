import random

file = open("UserData.dat", "w")
N = 30

file.write(str(N) + "\n")
for i in range(N):
    transmit_data_size = str(random.randint(10 ** 7, 5 * 10 ** 8))
    compute_task_size = str(random.randint(10 ** 9, 10 ** 12))
    X_coordinate = str(random.randint(10, 20))
    Y_coordinate = str(random.randint(10, 20))
    file.write("%s,%s,%s,%s\n" % (transmit_data_size, compute_task_size, X_coordinate, Y_coordinate))