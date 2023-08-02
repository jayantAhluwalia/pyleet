import sys
import os
import ast
def parse_input(input_str):
    input_lines = input_str.strip().split('\n')
    inputs = []
    current_input = []
    for line in input_lines:
        if line == '###':
            inputs.append(current_input)
            current_input = []
        else:
            try:
                input_data = [ast.literal_eval(item) for item in line.split()]
                current_input.append(input_data)
            except (ValueError, SyntaxError):
                print(f"Error parsing line: {line}. Skipping this input.")
                continue
    if current_input:
        inputs.append(current_input)
    return inputs

def run_script(script_number, inputs):
    script_filename = f"{script_number}.py"
    script_path = os.path.join("lib", script_filename)

    if not os.path.isfile(script_path):
        print(f"Script '{script_filename}' not found in the 'lib' folder.")
        return

    try:
        script_globals = {}
        exec(open(script_path).read(), script_globals)

        if 'solve' in script_globals:
            solve_function = script_globals['solve']
            for input_data in inputs:
                result = solve_function(*input_data)
                print(f"Input: {input_data}, Result: {result}")
        else:
            print(f"Script '{script_filename}' does not contain a 'solve' function.")
    except Exception as e:
        print(f"Error while executing '{script_filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run.py <script_number>")
    else:
        script_number = sys.argv[1]
        input_file_path = os.path.join("inputs", f"{script_number}_inp.txt")

        if not os.path.isfile(input_file_path):
            print(f"Input file '{input_file_path}' not found.")
        else:
            with open(input_file_path, 'r') as input_file:
                input_data_str = input_file.read()

            inputs = parse_input(input_data_str)
            run_script(script_number, inputs)


