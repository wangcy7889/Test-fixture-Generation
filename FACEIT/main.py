
import subprocess
import sys

API_KEY = ''
BASE_URL = ''
MODEL = ''

SCRIPTS = ["classification.py", "gene_call.py", "gene_test.py", "feedback.py"]

def run_script(script_name):
    cmd = [
        "python",
        script_name,
        f"--api_key={API_KEY}",
        f"--base_url={BASE_URL}",
        f"--model={MODEL}"
    ]

    print(f"\n>>> processing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    for script in SCRIPTS:
        ret = run_script(script)
        if ret != 0:
            print(f"!!! Error: {script} execution failed (return code: {ret})")
            sys.exit(1)

    print("\nAll script execution completed！")

if __name__ == "__main__":
    main()