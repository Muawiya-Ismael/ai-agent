import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abspath, file_path))

        valid_target_file = os.path.commonpath([working_directory_abspath, target_file_path]) == working_directory_abspath
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_directory_abspath, capture_output=True, text=True, timeout=30,)

        output: str = ""

        result_code = result.returncode
        if result_code != 0:
            output += f'Process exited with code {result_code} \n'
        elif result.stdout and result.stderr is None:
            output += f'No output produced'
        else:
            output += f'STDOUT:{result.stdout}\n'
            output += f'STDERR:{result.stderr}.'
        
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with optional command-line arguments and returns stdout and stderr output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of string arguments to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}