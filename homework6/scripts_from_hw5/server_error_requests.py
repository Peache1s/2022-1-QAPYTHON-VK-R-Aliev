path = 'short_access.log'

def server_error(path = path):
    with open(path, "r") as LogFile:
        list_of_requests = []
        counter_list = []
        while True:
            line = LogFile.readline()
            if len(line)>0:
                response = line.split()[8]
                if response.startswith("5"):
                    ip = line.split()[0]
                    if ip not in list_of_requests:
                        list_of_requests.append(ip)
                        counter_list.append(1)
                    else:
                        index = list_of_requests.index(ip)
                        counter_list[index] += 1
            else:
                break
        data = {}
        for i in range(len(list_of_requests)):
            data[list_of_requests[i]] = counter_list[i]
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        sorted_list = list(sorted_data)
        new_data = sorted_list[:5]
        data = dict(new_data)
        return data
