import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('LogFile', type=str, help='Нужен acces.log file первым аргументом')
parser.add_argument('ResultFile', type=str, help='Нужен Resulting file вторым аргументом')
parser.add_argument('--json', type=str)
args = parser.parse_args()
list_of_requests = []
counter_list = []
with open(args.LogFile, "r") as LogFile:
    while True:
        line = LogFile.readline()
        if len(line) > 0:
            url = line.split()[6]
            if url not in list_of_requests:
                list_of_requests.append(url)
                counter_list.append(1)
            else:
                index = list_of_requests.index(url)
                counter_list[index] += 1
        else:
            break
    data = {}
    for i in range(len(list_of_requests)):
        data[list_of_requests[i]] = counter_list[i]
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    sorted_list = list(sorted_data)
    new_data = sorted_list[:9]
    data = dict(new_data)
with open(args.ResultFile, "w") as ResultFile:
    ResultFile.write("URL                      N\n" )
    for x in data:
        ResultFile.write(str(x))
        ResultFile.write(" ")
        ResultFile.write(str(data[x]))
        ResultFile.write('\n')
if args.json:
    with open(args.json, 'w') as JSON_FILE:
        json.dump(data, JSON_FILE)