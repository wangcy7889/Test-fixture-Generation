import argparse
import os
import re
import shutil
from pathlib import Path
from openai import OpenAI

def parse_args():
    parser = argparse.ArgumentParser(description='Generate tests.')
    parser.add_argument('--api_key', required=True, help='API key')
    parser.add_argument('--base_url', required=True, help='API base URL')
    parser.add_argument('--model', required=True, help='Model name to use for generation')
    return parser.parse_args()

def copy_non_test_files(source_dirs, dest_dir):
    if not isinstance(source_dirs, list):
        source_dirs = [source_dirs]

    for source_dir in source_dirs:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    source_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_dir, os.path.relpath(source_file_path, source_dir))
                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                    shutil.copy2(source_file_path, dest_file_path)
                    print(f"Copied {source_file_path} to {dest_file_path}")


def generate_test_suite(function_file_path, generated_calls_dir, filename, model_name):
    with open(function_file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()

    base_name, ext = os.path.splitext(filename)

    invo_example_path = os.path.join(generated_calls_dir, f"{base_name}.py")
    has_invo_example = os.path.exists(invo_example_path)

    if has_invo_example:
        with open(invo_example_path, 'r', encoding='utf-8') as f:
            invo_example = f.read()

        test_cases = generate_test_cases(model_name, base_name, original_code, invo_example)
    else:
        test_cases = generate_test_cases(model_name, base_name, original_code)

    return test_cases


def generate_test_cases(model_name, base_name, original_code, invo_example=None):
    prompt = f"""
           Based on the following code, please use `unittest` to generate a Python test suite that includes 5 test cases.
           Import each function from the specified file using the syntax: `from {base_name} import <func1>, <func2>, ...`.
           Function code:
           ```python
           {original_code}
           ```\n
           """
    if invo_example:
        prompt += f"""
           Here is its invocation example: 
           ```python
           {invo_example}
           ```\n
           This can help you generate the test fixture section.
           """
    else:
        prompt += f"**Ensure the presence of the test fixture in the test suite.**"
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        pattern = r"```(?:python|py)?\n(.*?)\n```"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0].strip()
        return content.strip()

    except Exception as e:
        print(f"Error calling the LLM: {e}")
        return None


def process_directory(function_dir, generated_calls_dir, output_dir, model_name):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(function_dir):
        if filename.endswith('.py'):
            function_path = os.path.join(function_dir, filename)
            output_path1 = os.path.join(output_dir, f"test_{filename}")
            if os.path.exists(output_path1):
                print(f"The file {filename} already has a successfully generated test, skip it")
                continue

            test_suite = generate_test_suite(function_path, generated_calls_dir, filename, model_name)

            if test_suite:
                output_path = os.path.join(output_dir, f"test_{filename}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(test_suite)
                print(f"Generated test suite for {filename}")
            else:
                print(f"Failed to generate test suite for {filename}")


if __name__ == "__main__":
    args = parse_args()

    client = OpenAI(api_key=args.api_key, base_url=args.base_url)

    function_yes_dir = "classified_results/yes"
    generated_calls_dir = "generated_calls"
    output_dir = "generated_tests"
    copy_non_test_files(function_yes_dir, output_dir)

    process_directory(function_yes_dir, generated_calls_dir, output_dir, args.model)
