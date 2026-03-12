
def change_keys_dict_list(list_dicts, directions):
    
    new_list = []

    for key, value in directions.items():
        current_item = list(filter(lambda item: item.get(key), list_dicts))[0]
        new_list.append({value: current_item[key]})

    return new_list


def parse_list_to_dict(list_dicts):
    new_dict = {}

    for item in list_dicts:
        new_dict[list(item.keys())[0]] = list(item.values())[0]

    return new_dict

def order_tuple_list(unordered_list, instructions):
    return list(unordered_list.items())