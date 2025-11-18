import json
import re
import os
import subprocess
from pathlib import Path
from openai import OpenAI
from threading import Thread
import queue

api_key = ''
client = OpenAI(api_key=api_key, base_url='')
PROJECTS_ROOT = Path("")
JDK_PATH = ""
MAVEN_SETTINGS = ""
MAVEN_LOCAL_REPO = ""
MAVEN_CMD = ""
MODEL = ""
MAX_R = 3

LICENSE_TEXT = ""

def extract_method_info(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    method_info_list = []
    for method in data:
        info = {
            'Method_name': method.get('Method_name', ''),
            'Class_name': method.get("Class_name"),
            'Method_signature': method.get('method_signature', ''),
            'Method_body': method.get('Method_body', ''),
            'sub_project_name': method.get('sub_project_name', ''),
            'project_path': method.get('project_path', ''),
            'all_Import_statements': method.get('all_Import_statements', ''),
            'constructors': method.get('constructors', ''),
            'returnType': method.get('returnType', ''),
        }
        method_info_list.append(info)
    return method_info_list


def generate_test_input(code, filename, previous_input=None, error_message=None):
    prompt = f"""
               Generate a correct function call example for the following Java function.
               Ensure the function is already provided before the call,so do not show or import the function code.
               The file package name is package classifier; the class name is public class Invocation. 
               The main function is written in the Invocation class.
               Function code:{code}
               Return result must be complete code only.
               """

    if previous_input and error_message:
        prompt += f"\n\nThe previous generated function invocation:\n{previous_input}\n\n"
        print(f"filename：{filename} \n {error_message}")
        prompt += f"\nThe previous input generation produced an error:\n{error_message}\n\n"
        prompt += f"\nReturn result must be complete code only.\n\n"
        prompt += f"""**If this error is caused by web link or services, database, or external dependencies, 
        then introduce the mock method in the next instance generation. If not, 
        there's no need for a mock.**"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=0
        )

        invocation1 = response.choices[0].message.content
        pattern = r"```(?:java|Java)?\n(.*?)\n```"
        matches = re.findall(pattern, invocation1, re.DOTALL)
        extracted_invocation = "\n\n".join(match.strip() for match in matches)

        return extracted_invocation

    except Exception as e:
        print(f"Error calling the LLM: {e}")
        return None


def create_invocation_file(method_info, generated_code_invocation, license_text=LICENSE_TEXT):
    sub_project_name = method_info['sub_project_name']

    root_dir = PROJECTS_ROOT / sub_project_name
    classifier_dir = root_dir / "src/main/java/classifier"
    classifier_dir.mkdir(parents=True, exist_ok=True)

    classifier_code = f"""{license_text}
{generated_code_invocation}
"""
    file_path = classifier_dir / "Invocation.java"
    with file_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)

    return root_dir


def save_copy(method_info, classifier_code):
    tmp_dir = Path(method_info['sub_project_name']) / "generated_invocations"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_filename = method_info["Class_name"] + "_" + method_info["Method_name"] + ".java"
    tmp_path = tmp_dir / tmp_filename
    with tmp_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)


def run_maven_test(project_dir, vis):
    env = os.environ.copy()
    env['JAVA_HOME'] = JDK_PATH
    env['PATH'] = f"{JDK_PATH}\\bin;{env['PATH']}"
    env['MAVEN_OPTS'] = f"-Dmaven.repo.local={MAVEN_LOCAL_REPO}"

    maven_cmd = MAVEN_CMD
    if not os.path.exists(maven_cmd):
        return False, "Maven not found"

    if vis:
        test_args = [maven_cmd, "clean", "compile", "exec:java", "-Dexec.mainClass=classifier.Invocation"]
    else:
        test_args = [maven_cmd, "compile", "exec:java", "-Dexec.mainClass=classifier.Invocation"]

    test_args.append("-Dgit-commit-id.skip=true")

    if os.path.exists(MAVEN_SETTINGS):
        test_args.extend(["-s", MAVEN_SETTINGS])

    print(test_args)

    try:
        process = subprocess.Popen(
            test_args,
            cwd=project_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        success = True
        error_lines = []


        def read_stream(stream, output_queue, is_stderr=False):
            for line in stream:
                print(line, end="")
                output_queue.put((line, is_stderr))

        output_queue = queue.Queue()

        stdout_thread = Thread(target=read_stream, args=(process.stdout, output_queue, False))
        stderr_thread = Thread(target=read_stream, args=(process.stderr, output_queue, True))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        has_stderr = False
        stderr_content = []

        while not output_queue.empty():
            line, is_stderr = output_queue.get()
            if is_stderr:
                has_stderr = True
                stderr_content.append(line.strip())
                success = False
            elif "Exception" in line or "ERROR" in line:
                success = False
                error_lines.append(line.strip())

        process.wait()
        if process.returncode != 0:
            success = False

        all_errors = []
        if stderr_content:
            all_errors.append("STDERR:")
            all_errors.extend(stderr_content)
        if error_lines:
            all_errors.append("errors in STDOUT :")
            all_errors.extend(error_lines)

        error_message = "\n".join(all_errors) if all_errors else None
        return success, error_message

    except Exception as e:
        return False, str(e)


def reload(project_name: str, license_text=LICENSE_TEXT):
    project_root = PROJECTS_ROOT / project_name
    classifier_dir = project_root / "src/main/java/classifier"
    classifier_dir.mkdir(parents=True, exist_ok=True)
    classifier_path = classifier_dir / "Classifier.java"
    invocation_path = classifier_dir / "Invocation.java"
    classifier_code = f"""{license_text}
    package classifier;

    public class Classifier {{
        public static void main(String[] args) {{
            try {{

            }} catch (Exception e) {{
                System.out.println(e.getMessage());
                System.exit(1);
            }}
        }}
    }}
    """
    invocation_code = f"""{license_text}
    package classifier;

    public class Invocation {{
        public static void main(String[] args) {{
            try {{

            }} catch (Exception e) {{
                System.out.println(e.getMessage());
                System.exit(1);
            }}
        }}
    }}
    """
    with classifier_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)
    with invocation_path.open("w", encoding="utf-8") as f:
        f.write(invocation_code)


def load_fixture_dependent(dependent_txt, dependent_json, independent_json):
    pairs = []
    with open(dependent_txt, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '_' in line:
                parts = line.split('_')
                class_name = '_'.join(parts[:-1])
                method_name = parts[-1]
                pairs.append((class_name, method_name))

    method_dict = {}

    for json_file in [dependent_json, independent_json]:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for method in data:
            class_name = method.get("Class_name", "")
            method_name = method.get("Method_name", "")
            if class_name and method_name:
                key = (class_name, method_name)
                method_dict[key] = method

    result_methods = []

    for class_name, method_name in pairs:
        try:
            key = (class_name, method_name)
            if key in method_dict:
                result_methods.append(method_dict[key])
            else:
                raise KeyError(f"Unable to find corresponding method{key}！")
        except KeyError:
            exit(1)

    with open("fixture-dependent.json", 'w', encoding='utf-8') as f:
        json.dump(result_methods, f, indent=2, ensure_ascii=False)


def main():
    reload("boncey_Flickr4Java")
    reload("j256_ormlite-core")
    reload("ManfredTremmel_gwt-commons-lang3")
    reload("hutool-core")

    global success
    load_fixture_dependent("classified_results/fixture-dependent.txt",
                           "classified_results/fixture-dependent.json",
                           "classified_results/fixture-independent.json")
    json_path = "fixture-dependent.json"
    methods = extract_method_info(json_path)


    for method in methods:
        method_name = method['Method_name']
        class_name = method['Class_name']
        code = method.copy()

        tmp_dir = Path(method['sub_project_name']) / "generated_invocations"
        tmp_filename = method["Class_name"] + "_" + method["Method_name"] + ".java"
        tmp_path = tmp_dir / tmp_filename
        if tmp_path.exists():
            print(f"There is already a feedback call example for {tmp_filename}, skip it")
            continue

        retry_count = 0
        previous_input = None
        generated_code = None
        error_message = None
        classifier_code = None

        while retry_count < MAX_R:
            generated_code = generate_test_input(
                code,
                method_name,
                previous_input=previous_input,
                error_message=error_message
            )
            project_dir = create_invocation_file(method, generated_code)
            vis = 1 if (method['Method_body'] == methods[0]['Method_body'] and retry_count == 0) else 0

            print(f"executing Method: {method_name} (try {retry_count + 1}/{MAX_R})")
            success, error_message = run_maven_test(project_dir, vis)

            if success:
                print(f"Method {method_name} test success!")
                save_copy(method, generated_code)
                break
            else:
                print(f" Method {method_name} failed, providing feedback to the LLM for regeneration...")
                previous_input = generated_code
                retry_count += 1

        if retry_count >= MAX_R and not success:
            print(f"Method {method_name} ultimately failed")


if __name__ == "__main__":
    main()
