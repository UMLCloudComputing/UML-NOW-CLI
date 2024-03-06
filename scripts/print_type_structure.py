import json
import os

def print_type_structure(data, indent=0, file=None):
    for key, value in data.items():
        if isinstance(value, dict):
            print(f'interface {key.capitalize()} {{', file=file)
            print_type_structure(value, indent + 1, file=file)
            print('}', file=file)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            print(f'interface {key.capitalize()}[] {{', file=file)
            print_type_structure(value[0], indent + 1, file=file)
            print('}', file=file)
        else:
            print(f'  {key}: {type(value).__name__};', file=file)

# Use os.path.join to construct the file paths
input_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'output.json'))
output_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'output.txt'))

with open(input_file_path, 'r', encoding='utf-16') as f:
    data = json.load(f)

with open(output_file_path, 'w') as f:
    print_type_structure(data, file=f)
