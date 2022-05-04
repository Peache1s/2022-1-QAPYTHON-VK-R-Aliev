def req_by_types(path):
    list_of_requests = []
    counter_list = []
    with open(path, "r") as LogFile:
        while True:
            line = LogFile.readline()
            if len(line) > 0:
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
    return (list_of_requests, counter_list)