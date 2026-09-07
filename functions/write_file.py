import os 

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abspath, file_path))

        valid_target_file = os.path.commonpath([working_directory_abspath, target_file_path]) == working_directory_abspath
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a file relative to the working directory, creating directories as needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}