import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('LogFile', type=str, help='Нужен acces.log file первым аргументом')
parser.add_argument('ResultFile', type=str, help='Нужен Resulting file вторым аргументом')
parser.add_argument('--json', type=str)
url_counter = 0
args = parser.parse_args()
with open(args.LogFile, "r") as LogFile:
        while True:
            list_of_fields = LogFile.readline().split()
            if len(list_of_fields) > 1:
                if list_of_fields[6].startswith('/') or list_of_fields[6].startswith('http'):
                    url_counter += 1
            else: break
with open(args.ResultFile, "w") as ResultFile:
        ResultFile.write("Число запросов: \n")
        ResultFile.write(str(url_counter))
if args.json:
    data = {"N": url_counter}
    with open(args.json, 'w') as JSON_FILE:
        json.dump(data, JSON_FILE)