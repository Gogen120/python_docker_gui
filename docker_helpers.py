import json
import subprocess


def save_json_file(filename, docker_commands):
    try:
        with open(filename, 'r') as json_file:
            command_list = json.load(json_file)
    except FileNotFoundError:
        command_list = []
    command_list.append(docker_commands)
    with open(filename, 'w') as json_file:
        json.dump(command_list, json_file)


def is_docker_installed():
    return subprocess.call('docker -v', shell=True) == 0


def insert_docker_parameters(name,
                             volume_from,
                             volume_to,
                             local_port,
                             container_port,
                             image,
                             command):
    docker_command_string = 'docker run -it --rm' +\
        ' --name {} -v {}:{} -p {}:{} {} {}'
    docker_command = docker_command_string.format(name,
                                                  volume_from,
                                                  volume_to,
                                                  local_port,
                                                  container_port,
                                                  image,
                                                  command)
    return docker_command
