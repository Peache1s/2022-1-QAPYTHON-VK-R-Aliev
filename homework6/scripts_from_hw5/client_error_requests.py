path = 'short_access.log'

def client_error(path = path):
    with open(path, "r") as LogFile:
        list_size = []
        list_response = []
        list_ip = []
        list_url = []
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
        return data_list