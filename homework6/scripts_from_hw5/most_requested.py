def most_req(path):
    with open(path, "r") as LogFile:
        list_of_requests = []
        counter_list = []
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
        new_data = sorted_list[:10]
        data = dict(new_data)
        return data