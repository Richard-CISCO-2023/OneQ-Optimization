def replace_sx_with_rx(file_path):
    # Construct the new file name
    new_file_name = file_path.replace('.qasm', '_modified.qasm')

    # Open the original file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Open the new file for writing
    with open(new_file_name, 'w') as new_file:
        for line in lines:
            # Replace 'sx' with 'rx(pi/2)'
            if line.strip().startswith('sx'):
                line = line.replace('sx', 'rx(pi/2)', 1)
            new_file.write(line)

    print(f"Modified file saved as: {new_file_name}")

# Example usage
file_path = 'qasm_files/qf21_n15_transpiled_ori.qasm'  # Replace with your QASM file path
replace_sx_with_rx(file_path)