import random
import json
import csv
import sys
import math


variance_in_percent = 2

def uniform_random(number_of_parameters, number_of_combinations):
    biased = True
    final_values = []
    k = 0
    loop_count = 0
    while (biased):
        distribution = []
        loop_count = loop_count + 1
        if loop_count % 100000 == 0:
            print(loop_count)
        final_values = [random.randint(0, number_of_parameters) for p in range(0, number_of_combinations)]
        for j in range(number_of_parameters + 1):
            count = 0
            for i in final_values:
                if i == j:
                    count = count + 1
            distribution.append(count)
        for k in range(len(distribution)):
            low = float(((100 - float(variance_in_percent))/100) * number_of_combinations/(number_of_parameters + 1))
            high = float((100 + float(variance_in_percent))/100 * number_of_combinations/(number_of_parameters + 1))
            if (low <= distribution[k]) and (distribution[k] <= high):
                continue
            else:
                k = k - 1
                break
        if k == number_of_parameters:
            biased = False
    print("Loop count:", loop_count)
    print("Distribution:", distribution)
    print("Final values:", final_values)
    return final_values


def mapper(input_filename):
    intermediate_json = {}
    with open(input_filename, "r") as fp:
        data = json.load(fp)
    number_of_rows = data["number_of_rows"]
    for key in data["parameters"].keys():
        temp_len = len(data["parameters"][key])
        intermediate_json[key] = {}
        for i in range(temp_len):
            intermediate_json[key][i] = data["parameters"][key][i]
    return number_of_rows, intermediate_json


def generate_list(intermediate_json, number_of_rows):
    complete_list = []
    for key in intermediate_json.keys():
        number_of_parameters = len(intermediate_json[key].keys())
        expected_average = float(number_of_rows/number_of_parameters)
        expected_average_floor = math.floor(expected_average)
        expected_average_ceil = math.ceil(expected_average)
        if (((100 - float(variance_in_percent))/100) * expected_average > expected_average_floor) or (((100 + float(variance_in_percent))/100) * expected_average < expected_average_ceil):
            print("Theoretically not possible to identify values in", variance_in_percent, "% variance  for", key, "parameter. Try increasing number_of_rows parameter or decreasing the number of options for the parameter.")
            sys.exit(1)
        number_of_parameters = number_of_parameters - 1
        temp_values = uniform_random(number_of_parameters, number_of_rows)
        for index, value in enumerate(temp_values):
            temp_values[index] = intermediate_json[key][value]
        temp_values = [key] + temp_values  # add parameter name to front of list
        complete_list.append(temp_values)
    print(complete_list)
    return list(map(list, zip(*complete_list))) #return transpose of list


def write_to_csv(data_list):
    with open("data.csv", "w", newline='') as fb:
        wr = csv.writer(fb)
        wr.writerows(data_list)


number_of_rows, intermediate_json = mapper(sys.argv[1])
print(intermediate_json)
data_list = generate_list(intermediate_json, number_of_rows)
write_to_csv(data_list)
