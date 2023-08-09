import json


def deserializer(folder_directory):

    with open(folder_directory, 'r') as file:
        serialized_text_file = file.read()
        serialized_data = json.loads(serialized_text_file)
        file.close()

    return serialized_data
