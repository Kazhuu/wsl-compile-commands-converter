import subprocess
import re
import json


COMPILE_COMMANDS_JSON_FILENAME = 'compile_commands.json'


def read_compile_commands(filename):
    database = None
    with open(COMPILE_COMMANDS_JSON_FILENAME, 'r') as compile_commands:
        database = json.loads(compile_commands.read())
    result = {}
    for data in database:
        filename = wsl_path(data['file'])
        result[filename] = data['command']
    return result


def remove_compile_flags(command):
    o_pattern = r'-o\s*[\w\/\.]+'
    c_pattern = r'-c\s*[\w\/\.]+'
    command = re.sub(o_pattern, '', command)
    command = re.sub(c_pattern, '', command)
    return command


def replace_path(path):
    return wsl_path(path.group(1))


def convert_paths(command):
    path_pattern = r'((\w\:|)?[\/\\][^\s]+)'
    return re.sub(path_pattern, replace_path, command)


def wsl_path(windows_path):
    completed_process = subprocess.run(['wslpath', '-a', windows_path], check=True, stdout=subprocess.PIPE)
    return completed_process.stdout.decode('ascii').strip()


def Settings(**kwargs):
    filename = kwargs.get('filename', '')
    if filename in database:
        return {
            'flags': convert_paths(remove_compile_flags(database[filename])).split(' ')
        }
    return {}


database = read_compile_commands(COMPILE_COMMANDS_JSON_FILENAME)
print('done')

if __name__ == '__main__':
    Settings()
