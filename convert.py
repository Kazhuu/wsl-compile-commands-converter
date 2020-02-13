import subprocess
import re
import json
import argparse


def convert_paths(command):
    path_pattern = r'(?:(?<=[I| |"])|^)(\w+:?(?:[\\|\/]+[\w\.-]+)+)'
    return re.sub(path_pattern, replace_path, command)


def replace_path(path):
    return wsl_path(path.group(1))


def wsl_path(windows_path):
    completed_process = subprocess.run(['wslpath', '-a', windows_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return completed_process.stdout.decode('ascii').strip()


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
        command['directory'] = wsl_path(command['directory'])
        command['file'] = wsl_path(command['file'])
        print('{0}/{1}'.format(index + 1, length))
    with open('compile_commands.json', 'w') as output_file:
        json.dump(database, output_file, indent=2)


if __name__ == '__main__':
    main()
