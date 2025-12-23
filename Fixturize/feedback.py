import argparse
import json
import multiprocessing
import os
import re
import shutil
import pytest
from io import StringIO
import contextlib
import time
from pathlib import Path

from openai import OpenAI

CONFIG_FILE = "clear_env_config.json"

def parse_args():
    parser = argparse.ArgumentParser(description='Iteration.')
    parser.add_argument('--api_key', required=True, help='OpenAI API key')
    parser.add_argument('--base_url', required=True, help='OpenAI API base URL')
    parser.add_argument('--model', required=True, help='Model name to use for generation')
    return parser.parse_args()


def initialize_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    all_items = os.listdir(script_dir)
    dirs = {item for item in all_items if os.path.isdir(os.path.join(script_dir, item))}
    files = {item for item in all_items if os.path.isfile(os.path.join(script_dir, item))}

    files.discard(os.path.basename(__file__))
    files.discard(CONFIG_FILE)

    config = {
        "keep_dirs": list(dirs),
        "keep_files": list(files)
    }

    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        json.dump(config, f, indent=4)

    return dirs, files


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            config = json.load(f)
        return set(config["keep_dirs"]), set(config["keep_files"])
    except FileNotFoundError:
        return initialize_config()


def clear_env():
    keep_dirs, keep_files = load_config()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)

        if item == CONFIG_FILE or item == os.path.basename(__file__):
            continue

        if os.path.isdir(item_path):
            if item not in keep_dirs:
                try:
                    shutil.rmtree(item_path)
                    print(f"folder deleted: {item}")
                except Exception as e:
                    print(f"Error deleting folder {item}: {e}")

        # 处理文件
        elif os.path.isfile(item_path):
            if item not in keep_files:
                try:
                    os.remove(item_path)
                    print(f"folder deleted: {item}")
                except Exception as e:
                    print(f"Error deleting folder {item}: {e}")


def generate_test_input(model, function_code, original_code, error_message=None):
    prompt = f"""
    The following Python test code failed to run. Please analyze the error and regenerate the correct test code:

    Original function code:
    ```python
    {function_code}
    ```
    
    Original test code:
    ```python
    {original_code}
    ```

    error_message:
    {error_message}

    Please return the revised complete Python test code directly, only the code itself, without any explanation or 
    comments. Ensure that the code format is correct and can be run directly."""

    try:
        response = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        pattern = r"```python\n(.*?)\n```"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0].strip()
        return content.strip()

    except Exception as e:
        print(f"Error calling the API: {e}")
        return None


def run_test_with_timeout(model, file_path, fp2, timeout=30):
    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(
        target=run_test_and_capture_output,
        args=(file_path, child_conn)
    )
    p.start()

    output_parts = []
    start_time = time.time()

    while True:
        if parent_conn.poll(0.1):
            try:
                output = parent_conn.recv()
                output_parts.append(output)
            except (EOFError, ConnectionResetError):
                break

        if time.time() - start_time > timeout:
            p.terminate()
            p.join()

            while parent_conn.poll(0.1):
                try:
                    output_parts.append(parent_conn.recv())
                except:
                    break

            full_output = "".join(output_parts)
            result = {
                'status': 'TIMEOUT',
                'time_lines': extract_time_lines(full_output),
                'output': full_output
            }
            break

        if not p.is_alive():
            break

    p.join()
    full_output = "".join(output_parts)

    if 'result' not in locals():
        result = {
            'status': 'COMPLETED',
            'time_lines': extract_time_lines(full_output),
            'output': full_output
        }

    time_line = result['time_lines'][0] if result['time_lines'] else ""
    passed_match = re.search(r'(\d+) passed', time_line)
    failed_match = re.search(r'(\d+) failed', time_line)
    warning_match = re.search(r'(\d+) warning', time_line)
    error_match = re.search(r'(\d+) error', time_line.lower())

    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    errors = int(error_match.group(1)) if error_match else 0

    if result['status'] == 'TIMEOUT':
        if not result['time_lines']:
            is_pass = False
        else:
            is_pass = (failed == 0 and errors == 0)
    else:
        is_pass = (failed == 0 and errors == 0)

    if not is_pass:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        with open(fp2, 'r', encoding='utf-8') as f1:
            function_code = f1.read()

        new_code = generate_test_input(
            model=model,
            function_code=function_code,
            original_code=original_code,
            error_message=full_output
        )

        if new_code:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            print(f"Test failed. New code generated and overwritten: {os.path.basename(file_path)}")
        else:
            print(f"Test failed, and no new code was generated: {os.path.basename(file_path)}")


def run_test_and_capture_output(file_path, conn):
    output_buffer = StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer), \
                contextlib.redirect_stderr(output_buffer):
            pytest.main([file_path, "-v"])
    finally:
        conn.send(output_buffer.getvalue())
        conn.close()
    print(output_buffer.getvalue())
    clear_env()


def extract_time_lines(output):
    return [
        line.strip() for line in output.split('\n')
        if re.search(r'in\s+\d+\.?\d*\s*s', line)
    ]


def run_tests_in_directory(directory, model):
    for filename in os.listdir(directory):
        if filename.startswith('test') and filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            fp2 = os.path.join(directory, filename[5:])

            run_test_with_timeout(model, file_path, fp2)


def copy_folder(old_folder, new_folder):
    if os.path.exists(new_folder):
        os.remove(new_folder)

    os.makedirs(new_folder)

    for root, dirs, files in os.walk(old_folder):
        for file in files:
            if file.endswith('.py') or file == 'result.jsonl':
                old_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(old_file_path, start=old_folder)
                new_file_path = os.path.join(new_folder, relative_path)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.copy2(old_file_path, new_file_path)
                print(f"done: {old_file_path} -> {new_file_path}")


if __name__ == "__main__":
    args = parse_args()

    client = OpenAI(api_key=args.api_key, base_url=args.base_url)

    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    copy_folder('generated_tests', 'generated_tests_2')
    clear_env()
    run_tests_in_directory('generated_tests_2', args.model)
