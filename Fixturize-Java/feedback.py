import json
import os
import re
import subprocess
import sys
from pathlib import Path
from openai import OpenAI

api_key = ''
client = OpenAI(api_key=api_key, base_url='')
PROJECTS_ROOT = Path("")
JDK_PATH = ""
MAVEN_SETTINGS = ""
MAVEN_LOCAL_REPO = ""
MAVEN_CMD = ""
MODEL = ""
FIXTURE_JSON = "fixture-dependent.json"
LICENSE_TEXT = ""


def load_fixture_methods(fixture_path: str):
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    method_info_list = []
    for method in data:
        info = {
            "Method_name": method.get("Method_name", ""),
            "Class_name": method.get("Class_name", ""),
            "Method_signature": method.get("method_signature", ""),
            "Method_body": method.get("Method_body", ""),
            "sub_project_name": method.get("sub_project_name", ""),
            "project_path": method.get("project_path", ""),
            "constructors": method.get("constructors", ""),
            "returnType": method.get("returnType", "")
        }
        method_info_list.append(info)

    return method_info_list



def parse_test_filename(java_file: str):

    base = os.path.splitext(os.path.basename(java_file))[0]
    if base.endswith("Test"):
        base = base[:-4]

    parts = base.split("_")
    if len(parts) >= 2:
        class_name = parts[0]
        method_name = parts[1]
    else:
        raise ValueError(f"The file name: {java_file} does not comply with the rules")

    return class_name, method_name


def match_fixture_method(fixture_data, test_class_name, target_method_name):
    target_class = test_class_name
    if target_class.endswith("Test"):
        target_class = target_class[:-4]

    for method in fixture_data:
        if (method.get("Class_name", "") == target_class and
                method.get("Method_name", "") == target_method_name):
            return method

    return None


def run_maven_test(project_dir, test_class=None):
    env = os.environ.copy()
    env['JAVA_HOME'] = JDK_PATH
    env['PATH'] = f"{JDK_PATH}\\bin;{env['PATH']}"
    env['MAVEN_OPTS'] = f"-Dmaven.repo.local={MAVEN_LOCAL_REPO}"

    if not os.path.exists(MAVEN_CMD):
        print("can not find Maven")
        return False, "Maven not found", {}

    test_args = [MAVEN_CMD, "test"]
    if test_class:
        test_args.append(f"-Dtest={test_class}")
    test_args.extend(["-DfailIfNoTests=false", "-Dmaven.test.failure.ignore=true"])
    test_args.extend(["-Dfile.encoding=UTF-8"])
    if MAVEN_SETTINGS and os.path.exists(MAVEN_SETTINGS):
        test_args.extend(["-s", MAVEN_SETTINGS])

    print(f"executing command: {' '.join(test_args)}")
    print(f"Directory: {project_dir}")

    result_info = {
        "compilation_success": False,
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "tests_skipped": 0,
        "total_success": False
    }

    try:
        process = subprocess.Popen(
            test_args,
            cwd=project_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors='ignore'
        )

        output_lines = []
        while True:
            line = process.stdout.readline()
            if line:
                print(line, end='')
                output_lines.append(line)
            if line == '' and process.poll() is not None:
                break

        process.wait()
        output = ''.join(output_lines)

        result_info["compilation_success"] = "BUILD SUCCESS" in output or "Tests run:" in output

        if "Tests run:" in output:
            for line in output.split('\n'):
                if "Tests run:" in line:
                    parts = line.split(',')
                    for part in parts:
                        if "Tests run:" in part:
                            result_info["tests_run"] = int(part.split(':')[1].strip())
                        elif "Failures:" in part:
                            result_info["tests_failed"] = int(part.split(':')[1].strip())
                        elif "Errors:" in part:
                            result_info["tests_failed"] += int(part.split(':')[1].strip())
                        elif "Skipped:" in part:
                            result_info["tests_skipped"] = int(part.split(':')[1].strip())
                    result_info["tests_passed"] = (result_info["tests_run"] -
                                                   result_info["tests_failed"] -
                                                   result_info["tests_skipped"])
                    break

        result_info["total_success"] = (result_info["compilation_success"] and
                                        result_info["tests_failed"] == 0 and
                                        process.returncode == 0)

        error_message = None

        if "BUILD FAILURE" in output and not result_info["compilation_success"]:
            error_lines = []
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("[ERROR] /D:/Java_programs/projects/") or line.startswith("[ERROR] D:\\Java_programs\\projects"):
                    error_lines.append(line.strip())
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith("[INFO]"):
                            error_lines.append(next_line)
            if error_lines:
                error_message = "\n".join(error_lines)

        if error_message is None and result_info["tests_failed"] > 0:
            lines = output.split('\n')
            capture = False
            error_lines = []
            for line in lines:
                if "[INFO]  T E S T S" in line:
                    capture = True
                    continue
                if capture:
                    if "[INFO] BUILD SUCCESS" in line or "[INFO] BUILD FAILURE" in line:
                        break
                    if not line.strip().startswith("at "):
                        error_lines.append(line)
            if error_lines:
                error_message = "\n".join(error_lines).strip()

        return result_info["total_success"], error_message, result_info

    except Exception as e:
        print(f"Maven execution failed: {e}")
        return False, str(e), result_info

def extract_test_class_name(java_file_path):
    try:
        with open(java_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "public class" in content:
            class_line = [line for line in content.split('\n') if "public class" in line][0]
            class_name = class_line.split("public class")[1].split('{')[0].strip()
            return class_name
        elif "class" in content:
            class_line = [line for line in content.split('\n') if "class" in line and "{" in line][0]
            class_name = class_line.split("class")[1].split('{')[0].strip()
            return class_name
    except Exception as e:
        print(f" Extracting class name failed: {e}")
    return Path(java_file_path).stem


def get_package_name(test_file_stem, fixture_data):
    try:
        if "_" not in test_file_stem:
            return None
        class_name, method_name = test_file_stem.split("_", 1)
        for entry in fixture_data:
            if entry.get("Class_name") == class_name and entry.get("Method_name") == method_name:
                return entry.get("packageName")
    except Exception as e:
        print(f"Failed to retrieve package: {e}")
    return None


def generate_test_input(function_code, original_code, error_message=None):
    prompt = f"""
    The following Java test code failed to run. Please analyze the error and regenerate the correct test code.
    Please return the revised complete Java test code directly, only the code itself, without any explanation or  
    comments. Ensure that the code format is correct and can be run directly.
    
    Original function code:
    {function_code}

    Original test code:
    {original_code}

    error_message:
    {error_message}
    
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        pattern = r"```(?:java|Java)?\n(.*?)\n```"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0].strip()
        return content.strip()

    except Exception as e:
        print(f"Error calling API: {e}")
        return None


def process(dirA):
    generated_tests_dir = os.path.join(dirA, "generated_tests")
    generated_tests_dir2 = os.path.join(dirA, "generated_tests_2")
    result_file = os.path.join(dirA, "result_2.jsonl")

    os.makedirs(generated_tests_dir2, exist_ok=True)


    if not os.path.exists(dirA):
        print(f"Directory does not exist: {dirA}")
        sys.exit(1)
    if not os.path.exists(generated_tests_dir):
        print(f"The generated test directory does not exist: {generated_tests_dir}")
        sys.exit(1)

    java_files = [f for f in os.listdir(generated_tests_dir) if f.endswith('.java')]
    print(f"Find {len(java_files)} test files")

    fixture_path = FIXTURE_JSON
    with open(fixture_path, "r", encoding="utf-8") as f:
        fixture_data = json.load(f)

    for java_file in sorted(java_files):
        java_file_path = os.path.join(generated_tests_dir, java_file)
        test2_path = Path(generated_tests_dir2) / java_file
        if test2_path.exists():
            print(f"There is already a feedback call example for {java_file}, skip it")
            continue
        print(f"\n{'=' * 60}")
        print(f"Processing test file: {java_file}")

        try:
            with open(java_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            original_code = "".join(lines)
        except Exception as e:
            print(f"fail to read file: {e}")
            continue

        if len(lines) < 2:
            print(f"Insufficient file content: {java_file}")
            continue

        target_path_line = lines[1].strip()
        if "///" in target_path_line:
            target_path = target_path_line.split("///")[-1].strip()
        elif "//" in target_path_line:
            target_path = target_path_line.split("//")[-1].strip()
        else:
            target_path = target_path_line

        target_full_path = os.path.join(PROJECTS_ROOT, target_path)
        target_dir = os.path.dirname(target_full_path)
        os.makedirs(target_dir, exist_ok=True)

        test_file_stem = Path(java_file).stem
        has_package = any(line.strip().startswith("package ") for line in lines)
        if not has_package:
            package_name = get_package_name(test_file_stem, fixture_data)
            if package_name:
                lines[0] = f"package {package_name};\n"
                with open(java_file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

        try:
            with open(target_full_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Copy file failed: {e}")
            continue

        test_class_name = extract_test_class_name(java_file_path)
        if "<" in test_class_name:
            test_class_name = test_class_name.split("<")[0].strip()

        success, error_message, test_results = run_maven_test(PROJECTS_ROOT / dirA, test_class_name)

        final_record = None

        if success:
            new_test_path = os.path.join(generated_tests_dir2, java_file)
            with open(new_test_path, "w", encoding="utf-8") as f:
                f.write(original_code)
            print(f"Once passed, saved to: {new_test_path}")

            final_record = {
                "test_file": java_file,
                "target_path": target_path,
                "test_class": test_class_name,
                "success": success,
                "error_message": error_message,
                "test_results": test_results
            }
        else:
            print(f"Test failed, call LLM to generate a new test: {java_file}")

            target_class, target_method = parse_test_filename(java_file)

            fixture_data = load_fixture_methods(FIXTURE_JSON)
            matched_method = match_fixture_method(fixture_data, target_class, target_method)
            if matched_method:
                function_code = matched_method
            else:
                function_code = {}

            new_code = generate_test_input(function_code, original_code, error_message)
            if new_code:
                new_test_path = os.path.join(generated_tests_dir2, java_file)
                new_code = LICENSE_TEXT + "\n" + new_code
                with open(new_test_path, "w", encoding="utf-8") as f:
                    f.write(new_code)
                print(f"The new test has been saved to: {new_test_path}")

                try:
                    with open(target_full_path, "w", encoding="utf-8") as f:
                        f.write(new_code)

                    test_class_name2 = extract_test_class_name(new_test_path)
                    if "<" in test_class_name2:
                        test_class_name2 = test_class_name2.split("<")[0].strip()

                    success2, error_message2, test_results2 = run_maven_test(PROJECTS_ROOT / dirA, test_class_name2)

                    final_record = {
                        "test_file": java_file,
                        "target_path": target_path,
                        "test_class": test_class_name2,
                        "success": success2,
                        "error_message": error_message2,
                        "test_results": test_results2
                    }

                finally:
                    if os.path.exists(target_full_path):
                        os.remove(target_full_path)
                        print(f"Cleaned up new test file: {target_full_path}")

        if final_record:
            with open(result_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(final_record, ensure_ascii=False) + '\n')

        try:
            if os.path.exists(target_full_path):
                os.remove(target_full_path)
                print(f"Cleaned up new test file: {target_full_path}")
        except:
            pass

    print(f"All test processing completed! output: {result_file}")


if __name__ == "__main__":
    process("j256_ormlite-core")
    process("ManfredTremmel_gwt-commons-lang3")
    process("boncey_Flickr4Java")
    process("hutool-core")
