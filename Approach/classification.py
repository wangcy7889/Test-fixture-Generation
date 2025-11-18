import json
import os
import re
import shutil
import subprocess
import time
import argparse

from openai import OpenAI

input_folder1 = 'dataSet/fixture-dependent'
input_folder2 = 'dataSet/fixture-independent'
success_folder = 'no'
fail_folder = 'yes'
temp_folder = 'temp'
temp_file = 'temp.py'

def parse_args():
    parser = argparse.ArgumentParser(description='Generate invocation examples using API.')
    parser.add_argument('--api_key', required=True, help='API key')
    parser.add_argument('--base_url', required=True, help='API base URL')
    parser.add_argument('--model', required=True, help='Model name to use for generation')
    return parser.parse_args()

CONFIG_FILE = "clear_env_config.json"

def initialize_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    all_items = os.listdir(script_dir)
    dirs = {item for item in all_items if os.path.isdir(os.path.join(script_dir, item))}
    files = {item for item in all_items if os.path.isfile(os.path.join(script_dir, item))}

    files.discard(os.path.basename(__file__))
    files.discard(CONFIG_FILE)

    # 保存配置
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

        elif os.path.isfile(item_path):
            if item not in keep_files:
                try:
                    os.remove(item_path)
                    print(f"folder deleted: {item}")
                except Exception as e:
                    print(f"Error deleting folder {item}: {e}")



def generate_test_input(code, filename, previous_input=None, error_message=None, model_name=None):
    if model_name is None:
        raise Exception("model_name cannot be None")
    e_code1 = """
    import numpy as np

    def test_divide(arr1, arr2=None, scalar=None):
        if arr2 is not None:
            return np.divide(arr1, arr2)
        elif scalar is not None:
            return np.divide(arr1, scalar)
    """
    e_code2 = """
    import nltk
    from nltk.probability import FreqDist, MLEProbDist

    def test_probability(text):
        fd = FreqDist(text)
        return MLEProbDist(fd)
       """
    prompt = f"""
           Generate a minimal one-line invocation example based on the given Python code.
           code:\n{code}\n\n
           The output must follow the two examples:
           The first one:
                Generate a minimal one-line invocation example based on the given Python code.
                code:\n{e_code1}\n\n

                output:
                ```python
                test_divide(np.array([1, 2, 3, 4]), np.array([2, 2, 2, 2]))
                ```
           The second one:
                Generate a minimal one-line invocation example based on the given Python code.
                code:\n{e_code2}\n\n

                output:
                ```python
                test_probability("apple apple banana".split())
                ```
           Note that the output must be exactly one single-line invocation, because it will be used in this framework:
           ```python
           if __name__ == "__main__":
                try:
                    #the single line invocation example here
                except Exception as e:
                    print(e)
                    exit(1)
           ```
           """

    if previous_input:
        prompt += f"\n\nThe previous generated invocation:\n{previous_input}\n\n"
    if error_message:
        print(f"filename :{filename} \n {error_message}")
        prompt += f"\nThe previous generation produced an error:\n{error_message}\n\n"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=0
        )

        call1 = response.choices[0].message.content
        pattern = r"```(?:python|py)?\n(.*?)\n```"
        matches = re.findall(pattern, call1, re.DOTALL)
        extracted_call = "\n\n".join(match.strip() for match in matches)

        return extracted_call

    except Exception as e:
        print(f"Error calling the LLM: {e}")
        return None


def create_temp_file(original_code, test_call, filename):
    temp_file_path = os.path.join(temp_folder, filename)

    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(original_code)
        f.write('\n\nif __name__ == "__main__":\n')
        f.write('    try:\n')
        f.write(f'        {test_call}\n')
        f.write('    except Exception as e:\n')
        f.write('        print(e)\n')
        f.write('        exit(1)\n')

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
        f.write('\n\nif __name__ == "__main__":\n')
        f.write('    try:\n')
        f.write(f'        {test_call}\n')
        f.write('    except Exception as e:\n')
        f.write('        print(e)\n')
        f.write('        exit(1)\n')


def run_temp_file():
    popen = subprocess.Popen(
        ['python', temp_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    try:
        stdout, stderr = popen.communicate(timeout=60)
        success = popen.returncode == 0
    except subprocess.TimeoutExpired:
        popen.kill()
        return "","Timed out after 60 seconds",False

    return stdout, stderr, success


def process_file(filename, model_name, folderx):
    filepath = os.path.join(folderx, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        original_code = f.read()

    previous_input = None
    error_message = None

    for attempt in range(1):
        print(f"Processing {filename}, attempt {attempt + 1}")
        clear_env()

        test_call = generate_test_input(original_code, filename, previous_input, error_message, model_name)
        if not test_call:
            print(f"Failed to generate test call for {filename}")
            return False

        previous_input = test_call

        create_temp_file(original_code, test_call, filename)

        output, error, success = run_temp_file()
        cks = (output or "") + (error or "")
        cks = cks.lower()

        error_keywords = ['warn', 'err', 'fail']
        has_error = any(keyword in cks for keyword in error_keywords)

        if not success or has_error:
            error_message = f"Stdout:\n{output}\nStderr:\n{error}"
            print(f"Attempt {attempt + 1} failed: {error_message}")
        else:
            # Success - save to success_folder
            success_path = os.path.join(success_folder, filename)
            with open(success_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            print(f"Successfully processed {filename}")
            return True

    # If all attempts failed, save to fail_folder
    fail_path = os.path.join(fail_folder, filename)
    with open(fail_path, 'w', encoding='utf-8') as f:
        f.write(original_code)
    print(f"Failed to process {filename} after 3 attempts")
    return False


def main():
    args = parse_args()

    global client
    client = OpenAI(api_key=args.api_key, base_url=args.base_url)

    os.makedirs(success_folder, exist_ok=True)
    os.makedirs(fail_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    # Process each file in input folder
    for filename in os.listdir(input_folder1):
        if filename.endswith('.py'):
            process_file(filename, args.model, input_folder1)

    for filename in os.listdir(input_folder2):
        if filename.endswith('.py'):
            process_file(filename, args.model, input_folder2)

    # Clean up the temporary execution file
    if os.path.exists(temp_file):
        os.remove(temp_file)

def classify_temp_files():
    temp_folder = 'temp'
    no_folder = 'no'
    yes_folder = 'yes'
    temp_no_folder = 'temp_no'
    temp_yes_folder = 'temp_yes'

    os.makedirs(temp_no_folder, exist_ok=True)
    os.makedirs(temp_yes_folder, exist_ok=True)

    temp_files = [f for f in os.listdir(temp_folder) if f.endswith('.py')]

    for temp_file in temp_files:
        temp_path = os.path.join(temp_folder, temp_file)

        no_path = os.path.join(no_folder, temp_file)
        yes_path = os.path.join(yes_folder, temp_file)

        if os.path.exists(no_path):
            shutil.copy2(temp_path, os.path.join(temp_no_folder, temp_file))
            print(f"Copied {temp_file} to temp_no (failed case)")
        elif os.path.exists(yes_path):
            shutil.copy2(temp_path, os.path.join(temp_yes_folder, temp_file))
            print(f"Copied {temp_file} to temp_yes (success case)")
        else:
            print(f"Warning: {temp_file} not found in either no or yes folders")
    folders = [temp_folder, no_folder, yes_folder, temp_no_folder, temp_yes_folder]
    headName = 'classified_results'
    for folder in folders:
        temp_folder = os.path.join(headName, folder)
        if os.path.exists(folder):
            shutil.move(folder, temp_folder)




if __name__ == "__main__":
    main()
    classify_temp_files()