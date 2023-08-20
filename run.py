import os
import ast
import argparse
import logging


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


def parse_test(test_str):
    expected_results = test_str.strip().split("\n")
    return expected_results


def read_content(file_path):
    if not os.path.isfile(file_path):
        raise ValueError(f"Input file '{file_path}' not found.")
    else:
        with open(file_path, 'r') as file:
            data_str = file.read()
    return data_str


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_script(script_number, inputs, tests):
    script_filename = f"{script_number}.py"
    script_path = os.path.join("lib", script_filename)

    if not os.path.isfile(script_path):
        logger.error(
            f"Script '{script_filename}' not found in the 'lib' folder.")
        return
    try:
        script_globals = {}
        exec(open(script_path).read(), script_globals)

        if 'solve' in script_globals:
            solve_function = script_globals['solve']
            results = [solve_function(*input_data) for input_data in inputs]
        else:
            logger.error(
                f"Script '{script_filename}' does not contain a 'solve' function.")
            return

        run_tests(results, tests)
    except Exception as e:
        logger.error(f"Error while executing '{script_filename}': {e}")


def run_tests(results, tests):
    for i, (result, expected) in enumerate(zip(results, tests), start=1):
        if result == expected:
            logger.info(f"Test {i} passed")
        else:
            logger.info(
                f"Test {i} failed. Expected: {expected}, Got: {result}")


def main():
    parser = argparse.ArgumentParser(
        description="Automated testing and execution of Python scripts.")
    parser.add_argument("script_number", type=str,
                        help="Number of the script to run")
    args = parser.parse_args()

    script_number = args.script_number
    input_file_path = os.path.join("inputs", f"{script_number}_inp.txt")
    tests_file_path = os.path.join("tests", f"{script_number}.txt")

    try:
        input_data_str = read_content(input_file_path)
        tests_data_str = read_content(tests_file_path)

        tests = parse_test(tests_data_str)
        inputs = parse_input(input_data_str)
        run_script(script_number, inputs, tests)
    except ValueError as ve:
        logger.error(ve)


if __name__ == "__main__":
    main()
