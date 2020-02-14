import subprocess
import re
import json
import argparse

"""
Script to convert already existing compile_commands.json compile database with
Windows paths to use WSL compatible paths instead. This allows Vim usage on WSL
side but project code to be compiled on Windows side with Windows tools.

Usage:
python convert.py win_compile_commands.json

This will convert paths in the given file and write output to
compile_commands.json file.
"""

path_cache = {}

def convert_paths(string):
    string = convert_slashes(string)
    return convert_drive_paths(string)


def convert_drive_paths(path):
    drive_path = r'(?:(?<=[I| |"])|^)(\w+:[\\\/]+)'
    return re.sub(drive_path, replace_path, path)


def convert_slashes(path):
    slash_pattern = r'(?<=\w)(\\+)(?=\w)'
    return re.sub(slash_pattern, '/', path)


def replace_path(path):
    return wsl_path(path.group(1))


def wsl_path(windows_path):
    wsl_path = path_cache.get(windows_path)
    if not wsl_path:
        completed_process = subprocess.run(['wslpath', '-a', windows_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        wsl_path = completed_process.stdout.decode('ascii').strip()
        path_cache[windows_path] = wsl_path
    return wsl_path


def main():
    parser = argparse.ArgumentParser(description='Convert given compile_commands.json with Windows paths to Windows Subsystem for Linux (WSL) compatible paths')
    parser.add_argument('compile_commands', help='compile_commands.json file with Windows paths')
    args = parser.parse_args()
    database = None
    with open(args.compile_commands, 'r') as input_file:
        database = json.load(input_file)
    length = len(database)
    for index, command in enumerate(database):
        command['command'] = convert_paths(command['command'])
        command['directory'] = convert_paths(command['directory'])
        command['file'] = convert_paths(command['file'])
        print('{0}/{1}: {2}'.format(index + 1, length, command['file']))
    with open('compile_commands.json', 'w') as output_file:
        json.dump(database, output_file, indent=2)


if __name__ == '__main__':
    main()
