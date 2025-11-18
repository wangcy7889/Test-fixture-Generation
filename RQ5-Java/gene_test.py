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
            'returnType': method.get('returnType', ''),
            'Junit_version': method.get('Junit_version', ''),

        }
        method_info_list.append(info)
    return method_info_list


def generate_test(code, invocation=None):
    prompt = f"""
               Based on the following code, please use **Junit 5** to generate a Java test suite that includes 5 test cases.
               Function code and context:
               {code}
               """
    if invocation:
        prompt += f"""
                   Here is its call example: 
                   ```java
                   {invocation}
                   ```\n
                   This can help you generate setUp and tearDown sections.
                   """
    else:
        prompt += f"**Ensure that the test class includes `setUp` and `tearDown` methods for setup and teardown operations. **"

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


def create_test_file(method_info, generated_test, license_text=LICENSE_TEXT):
    sub_project_name = method_info['sub_project_name']
    project_path = method_info['project_path']
    match = re.search(r'###(.+?)###', project_path)
    path = match.group(1)
    test_path = path.replace('.java', 'Test.java') if path.endswith('.java') else path + 'Test.java'
    test_path = re.sub(r'src/main/java', 'src/test/java', test_path)

    tmp_dir = Path(method_info['sub_project_name']) / "generated_tests"
    tmp_filename = method_info["Class_name"] + "_" + method_info["Method_name"] + ".java"
    tmp_path = tmp_dir / tmp_filename
    tmp_dir.mkdir(parents=True, exist_ok=True)


    classifier_code = \
        f"""
//{test_path}
{license_text}
{generated_test}
"""
    with tmp_path.open("w", encoding="utf-8") as f:
        f.write(classifier_code)


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

    json_path = "fixture-dependent.json"
    methods = extract_method_info(json_path)

    for method in methods:
        method_name = method['Method_name']
        class_name = method['Class_name']
        project_name = method['sub_project_name']
        junit_num = method['Junit_version']

        retry_count = 0
        previous_input = None
        generated_code = None
        error_message = None
        invocation = None

        tmp_dir = Path(method['sub_project_name']) / "generated_tests"
        tmp_filename = method["Class_name"] + "_" + method["Method_name"] + ".java"
        tmp_path = tmp_dir / tmp_filename
        if tmp_path.exists():
            print(f"There is already a feedback call example for {tmp_filename}, skip it")
            continue

        tmp_dir = Path(method['sub_project_name']) / "generated_invocations"
        tmp_filename = method["Class_name"] + "_" + method["Method_name"] + ".java"
        tmp_path = tmp_dir / tmp_filename
        if tmp_path.exists():
            with open(tmp_path, "r", encoding="utf-8") as f:
                invocation = f.read()

        while retry_count < MAX_R:
            generated_code = generate_test(
                method,
                invocation=invocation
            )
            create_test_file(method, generated_code)
            retry_count = retry_count + 1
            print(f"Project {project_name} Class {class_name} Method {method_name} successfully generated test")


if __name__ == "__main__":
    main()
