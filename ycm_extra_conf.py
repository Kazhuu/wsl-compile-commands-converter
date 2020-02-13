import subprocess
import re
import json
import os

"""
Works but is way too slow with big project/compile_commands.json file.
"""

COMPILE_COMMANDS_JSON_FILENAME = 'win_compile_commands.json'
SOURCE_EXTENSIONS = ['.cpp', '.cxx', '.cc', '.c', '.m', '.mm']

def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ['.h', '.hxx', '.hpp', '.hh']


def find_corresponding_source_file(filename):
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for extension in SOURCE_EXTENSIONS:
            replacement_file = basename + extension
            if os.path.exists(replacement_file):
                return replacement_file
    return filename


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
    filename = find_corresponding_source_file(filename)
    if filename in database:
        return {
            'flags': convert_paths(remove_compile_flags(database[filename])).split(' '),
            'override_filename': filename
        }
    print('no flags for {0}'.format(filename))
    return {}


database = read_compile_commands(COMPILE_COMMANDS_JSON_FILENAME)
print('done')

if __name__ == '__main__':
    Settings()
