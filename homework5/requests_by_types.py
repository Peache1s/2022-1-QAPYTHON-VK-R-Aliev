import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('LogFile', type=str, help='Нужен acces.log file первым аргументом')
parser.add_argument('ResultFile', type=str, help='Нужен Resulting file вторым аргументом')
parser.add_argument('--json', type=str)
list_of_requests = []
counter_list = []
args = parser.parse_args()
with open(args.LogFile, "r") as LogFile:
    while True:
        line = LogFile.readline()
        if len(line) >0:
            type_of_request = line.split('"')[1].split()[0]
            if type_of_request.isupper():
                if type_of_request not in list_of_requests:
                    list_of_requests.append(type_of_request)
                    counter_list.append(1)
                else:
                    index = list_of_requests.index(type_of_request)
                    counter_list[index] += 1
            else:
                continue
        else:
            break
with open(args.ResultFile, "w") as ResultFile:
    ResultFile.write("N:   TYPE: \n")
    for i in range(len(list_of_requests)):
        ResultFile.write(str(counter_list[i]))
        ResultFile.write(" ")
        ResultFile.write(str(list_of_requests[i]))
        ResultFile.write('\n')
if args.json:
    data = {}
    for i in range(len(list_of_requests)):
        data[list_of_requests[i]] = counter_list[i]
    with open(args.json, 'w') as JSON_FILE:
        json.dump(data, JSON_FILE)
        JSON_FILE.write('\n')