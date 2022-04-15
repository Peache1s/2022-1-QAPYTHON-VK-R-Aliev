import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('LogFile', type=str, help='Нужен acces.log file первым аргументом')
parser.add_argument('ResultFile', type=str, help='Нужен Resulting file вторым аргументом')
parser.add_argument('--json', type=str)
args = parser.parse_args()
list_size = []
list_response = []
list_ip = []
list_url = []
with open(args.LogFile, "r") as LogFile:
    while True:
        line = LogFile.readline()
        if len(line) > 0:
            response = line.split()[8]
            if response.startswith("4"):
                list_size.append(int(line.split()[9]))
                list_ip.append(line.split()[0])
                list_url.append(line.split()[6])
                list_response.append(response)
        else:
            break
    data_list = []
    for x in range(len(list_size)):
        data_list.append((list_size[x], (list_ip[x], list_response[x], list_url[x])))
    sorted_list = sorted(data_list, key = lambda x: x[0], reverse=True)
    data_list = sorted_list[0:5]
with open(args.ResultFile, "w") as ResultFile:
    ResultFile.write("SIZE:IP:        RESPONSE:URL:\n" )
    for x in data_list:
        ResultFile.write(str(x[0]))
        ResultFile.write(" ")
        ResultFile.write(str(x[1][0]))
        ResultFile.write(" ")
        ResultFile.write(str(x[1][1]))
        ResultFile.write(" ")
        ResultFile.write(str(x[1][2]))
        ResultFile.write('\n')
if args.json:
    data = {}
    for x in range(0,5):
        temp_dict = {"size": data_list[x][0], "ip": data_list[x][1][0], "response": data_list[x][1][1], "url": data_list[x][1][2]}
        data[x] = temp_dict
    print(data)
    with open(args.json, 'w') as JSON_FILE:
        json.dump(data, JSON_FILE)