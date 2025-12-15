import json
import re
import os
import subprocess
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
MAX_R = 1
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
            'packageName': method.get('packageName', ''),
            'returnType': method.get('returnType', ''),
        }
        method_info_list.append(info)
    return method_info_list


def generate_test_input(code, filename, previous_input=None, error_message=None):
    e_code1 = """
        public class MathUtils {
            public static int divide(int a, int b) {
                return a / b;
            }
        }
        """

    e_code2 = """
        public class TextUtils {
            public static Map<Character, Integer> countChars(String text) {
                Map<Character, Integer> freq = new HashMap<>();
                for (char c : text.toCharArray()) {
                    freq.put(c, freq.getOrDefault(c, 0) + 1);
                }
                return freq;
            }
        }
        """

    prompt = f"""
               Generate a minimal one-line function invocation example based on the given Java code.
               code:\n{code}\n\n
               The output must follow the two examples:
               The first one:
                    Generate a minimal one-line function invocation example based on the given Java code.
                    code:\n{e_code1}\n\n

                    output:
                    ```java
                    MathUtils.divide(10, 2);
                    ```
               The second one:
                    Generate a minimal one-line function invocation example based on the given Java code.
                    code:\n{e_code2}\n\n

                    output:
                    ```java
                    TextUtils.countChars("apple apple banana");
                    ```
               Note that the output must be exactly one single-line function invocation,
               because it will be used in this framework:\n""" + """
               ```java
               import ...
               
               public class Classifier {
                    public static void main(String[] args) {
                        try {
                            // the single line function invocation example here
                        } catch (Exception e) {
                            System.out.println(e.getMessage());
                            System.exit(1);
                        }
                    }
                }
               """

    if previous_input:
        prompt += f"\n\nThe previous generated function invocation:\n{previous_input}\n\n"
    if error_message:
        print(f"filename: {filename} \n {error_message}")
        prompt += f"\nThe previous input generation produced an error:\n{error_message}\n\n"

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

def create_classifier_file(method_info, single_line_invocation, license_text=LICENSE_TEXT):
    sub_project_name = method_info['sub_project_name']
    project_path = method_info['project_path']

    root_dir = PROJECTS_ROOT / sub_project_name
    classifier_dir = root_dir / "src/main/java/classifier"
    classifier_dir.mkdir(parents=True, exist_ok=True)

    # import 处理
    path_part = project_path.split("/src/main/java/")[-1].split("###")[0]
    path_part = os.path.splitext(path_part)[0]  # 去掉 .java
    import_statement = f"import {path_part.replace('/', '.')};\n"
    import_statement = import_statement + method_info['all_Import_statements'] + "\n"
    import_statement = import_statement + "import " + method_info['packageName'] + ".*;\n"

    classifier_code = f"""{license_text}
package classifier;

{import_statement}

public class Classifier {{
    public static void main(String[] args) {{
        try {{
            {single_line_invocation}
        }} catch (Exception e) {{
            System.out.println(e.getMessage());
            System.exit(1);
        }}
    }}
}}
"""
    file_path = classifier_dir / "Classifier.java"
    with file_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)

    tmp_dir = Path(method_info['sub_project_name']) / "classifier_code"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_filename = method_info["Class_name"] + "_" + method_info["Method_name"] + ".java"
    tmp_path = tmp_dir / tmp_filename
    with tmp_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)

    return root_dir


def run_maven_test(project_dir, vis):
    env = os.environ.copy()
    env['JAVA_HOME'] = JDK_PATH
    env['PATH'] = f"{JDK_PATH}\\bin;{env['PATH']}"
    env['MAVEN_OPTS'] = f"-Dmaven.repo.local={MAVEN_LOCAL_REPO}"

    maven_cmd = MAVEN_CMD
    if not os.path.exists(maven_cmd):
        print("can not find Maven")
        return False, "Maven not found"

    if vis:
        test_args = [maven_cmd, "clean", "compile", "exec:java", "-Dexec.mainClass=classifier.Classifier"]
    else:
        test_args = [maven_cmd, "compile", "exec:java", "-Dexec.mainClass=classifier.Classifier"]

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
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        success = True
        error_lines = []

        for line in process.stdout:
            print(line, end="")
            if "Exception" in line or "ERROR" in line:
                success = False
                error_lines.append(line.strip())

        process.wait()
        if process.returncode != 0:
            success = False

        error_message = "\n".join(error_lines) if error_lines else None
        return success, error_message

    except Exception as e:
        print(f"❌ Maven execution error: {e}")
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

def main():
    reload("boncey_Flickr4Java")
    reload("j256_ormlite-core")
    reload("ManfredTremmel_gwt-commons-lang3")
    reload("hutool-core")

    YES_FILE = Path("classified_results") / 'fixture-independent.txt'
    NO_FILE = Path("classified_results") / 'fixture-dependent.txt'
    os.makedirs(Path("classified_results"), exist_ok=True)

    global success
    json_path = "dataSet/merged.json"
    methods = extract_method_info(json_path)

    yes_list = []
    no_list = []

    for method in methods:
        method_name = method['Method_name']
        class_name = method['Class_name']
        code = method.copy()
        code.pop('all_Import_statements', None)

        retry_count = 0
        previous_input = None
        single_line = None
        error_message = None

        while retry_count < MAX_R:
            single_line = generate_test_input(
                code,
                method_name,
                previous_input=previous_input,
                error_message=error_message
            )
            project_dir = create_classifier_file(method, single_line)
            vis = 1 if (method['Method_body'] == methods[0]['Method_body'] and retry_count == 0) else 0

            print(f" executing Method: {method_name} (try {retry_count + 1}/{MAX_R})")
            success, error_message = run_maven_test(project_dir, vis)

            if success:
                print(f"Method {method_name} test success!")
                yes_list.append(class_name + "_" + method_name)
                break
            else:
                print(f" Method {method_name} failed, providing feedback to the LLM for regeneration...")
                previous_input = single_line
                retry_count += 1

        if retry_count >= MAX_R and not success:
            print(f"Method {method_name} ultimately failed")
            no_list.append(class_name + "_" + method_name)

    with open(YES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(yes_list))
    with open(NO_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(no_list))

    print(f"\nTest success method written: {YES_FILE}")
    print(f"Test FAIL method written: {NO_FILE}")


if __name__ == "__main__":
    main()
