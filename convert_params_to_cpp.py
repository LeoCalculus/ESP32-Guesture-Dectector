import re

def parse_parameters_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extract layers data (no more INPUT_MEAN/STD)
    layers_data = []
    layer_pattern = r'# Layer (\d+): (\d+) -> (\d+)\nLAYER_\d+_WEIGHTS:\n((?:[0-9\.\-,\s\n]+?))\nLAYER_\d+_BIASES:\n([0-9\.\-,\s]+)'
    
    matches = re.findall(layer_pattern, content, re.DOTALL)
    
    for match in matches:
        layer_num, input_size, output_size, weights_str, biases_str = match
        
        # Parse weights
        weights_lines = [line.strip() for line in weights_str.strip().split('\n') if line.strip()]
        weights = []
        for line in weights_lines:
            row = [float(x.strip()) for x in line.split(',') if x.strip()]
            if row:  # Only add non-empty rows
                weights.append(row)
        
        # Parse biases (handle both comma-separated and newline-separated)
        biases_str = biases_str.strip()
        if ',' in biases_str:
            # Comma-separated format
            biases = [float(x.strip()) for x in biases_str.split(',') if x.strip()]
        else:
            # Newline-separated format (from np.savetxt)
            biases = [float(x.strip()) for x in biases_str.split('\n') if x.strip()]
        
        layers_data.append({
            'layer_num': int(layer_num),
            'input_size': int(input_size),
            'output_size': int(output_size),
            'weights': weights,
            'biases': biases
        })
    
    return layers_data

def generate_cpp_arrays(layers_data):
    cpp_code = '#pragma once\n\n'
    cpp_code += '// Embedded neural network parameters\n\n'
    
    # Generate layer weights and biases
    for layer in sorted(layers_data, key=lambda x: x['layer_num']):
        layer_num = layer['layer_num']
        input_size = layer['input_size']
        output_size = layer['output_size']
        
        # Weights array
        cpp_code += f'const float LAYER_{layer_num}_WEIGHTS[{input_size}][{output_size}] = {{\n'
        for i, row in enumerate(layer['weights']):
            cpp_code += '    {'
            for j, val in enumerate(row):
                cpp_code += f'{val:.8f}f'
                if j < len(row) - 1:
                    cpp_code += ', '
            cpp_code += '}'
            if i < len(layer['weights']) - 1:
                cpp_code += ','
            cpp_code += '\n'
        cpp_code += '};\n\n'
        
        # Biases array
        cpp_code += f'const float LAYER_{layer_num}_BIASES[{output_size}] = {{\n'
        cpp_code += '    '
        for i, val in enumerate(layer['biases']):
            cpp_code += f'{val:.8f}f'
            if i < len(layer['biases']) - 1:
                cpp_code += ', '
        cpp_code += '\n};\n\n'
    
    return cpp_code

# Parse the parameters file
layers_data = parse_parameters_file('src/trained_model_parameters.txt')

# Generate C++ code
cpp_code = generate_cpp_arrays(layers_data)

# Write to header file
with open('src/model_parameters.h', 'w') as f:
    f.write(cpp_code)

print("Generated model_parameters.h with embedded parameters")
print(f"Number of layers: {len(layers_data)}")
for layer in layers_data:
    print(f"Layer {layer['layer_num']}: {layer['input_size']} -> {layer['output_size']}")