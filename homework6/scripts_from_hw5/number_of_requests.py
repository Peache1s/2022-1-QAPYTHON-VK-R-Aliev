path = 'short_access.log'


def numb_of_req(path = path):
    url_counter = 0
    with open(path, "r") as LogFile:
            while True:
                list_of_fields = LogFile.readline().split()
                if len(list_of_fields) > 1:
                    if list_of_fields[6].startswith('/') or list_of_fields[6].startswith('http'):
                        url_counter += 1
                else: break
    return url_counter

print(numb_of_req())