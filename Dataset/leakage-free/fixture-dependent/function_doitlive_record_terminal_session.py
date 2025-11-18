import subprocess


def record_terminal_session(script_path: str):
    subprocess.run(["doitlive", "play", script_path])
    return True
