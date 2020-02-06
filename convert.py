import subprocess
import re
import json



def convert_paths(command):
    path_pattern = r'((\w\:|\/)?[\/\\][^(\s|")]+)'
    return re.sub(path_pattern, replace_path, command)


def replace_path(path):
    return wsl_path(path.group(1))


def wsl_path(windows_path):
    completed_process = subprocess.run('wslpath -a {0}'.format(windows_path), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(windows_path)
    return completed_process.stdout.decode('ascii').strip()


def main():
    database = None
    with open('compile_commands.json', 'w') as output_file:
        with open('win_compile_commands.json', 'r') as input_file:
            for line in input_file:
                line = convert_paths(line.strip())
                print(line)
                output_file.write(convert_paths(line))


if __name__ == '__main__':
    main()
