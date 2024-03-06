import json
import os

def print_type_structure(data, indent=0, is_last=True, file=None):
    for i, (key, value) in enumerate(data.items()):
        is_last = i == len(data) - 1
        if isinstance(value, dict):
            print('  ' * indent + (f'|-- {key}: object' if is_last else f'|-- {key}: object'), file=file)
            print_type_structure(value, indent + 1, is_last, file=file)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            print('  ' * indent + (f'|-- {key}: array' if is_last else f'|-- {key}: array'), file=file)
            print_type_structure(value[0], indent + 1, is_last, file=file)
        else:
            print('  ' * indent + (f'|-- {key}: {type(value).__name__}' if is_last else f'|-- {key}: {type(value).__name__}'), file=file)

# Use os.path.join to construct the file paths
input_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'output.json'))
output_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'output.txt'))

with open(input_file_path, 'r', encoding='utf-16') as f:
    data = json.load(f)

with open(output_file_path, 'w') as f:
    print_type_structure(data, file=f)
