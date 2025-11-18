import os
import PyInstaller.__main__
from typing import List, Optional


class PyinstallerPackager:
    def __init__(self, entry_script: str, output_dir: str = "dist"):

        self.entry_script = entry_script
        self.output_dir = output_dir

    def create_executable(self,
                          name: str,
                          one_file: bool = True,
                          hidden_imports: Optional[List[str]] = None,
                          additional_files: Optional[List[str]] = None) -> str:
        if not os.path.exists(self.entry_script):
            raise FileNotFoundError(f"Error: Entry script {self.entry_script} not existed")

        args = [
            self.entry_script,
            '--name', name,
            '--distpath', self.output_dir,
            '--clean'
        ]

        if one_file:
            args.append('--onefile')

        if hidden_imports:
            for imp in hidden_imports:
                args.extend(['--hidden-import', imp])

        if additional_files:
            for file in additional_files:
                args.extend(['--add-data', f'{file}{os.pathsep}.'])

        PyInstaller.__main__.run(args)


        ext = '.exe' if os.name == 'nt' else ''
        executable_path = os.path.join(self.output_dir, f"{name}{ext}")

        if not os.path.exists(executable_path):
            raise RuntimeError("Error: The packaging process failed and no executable file was generated")

        return executable_path