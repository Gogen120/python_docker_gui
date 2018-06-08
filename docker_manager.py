import re
import subprocess
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QListWidget, QGridLayout
from docker_helpers import is_docker_installed, insert_docker_parameters


class DockerManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        if is_docker_installed():
            port = QLabel('Port')
            container_name = QLabel('Container name')
            volume_directory = QLabel('Volume directory')
            command_to_execute = QLabel('Command to execute')
            image = QLabel('Image')

            self.port_edit = QLineEdit()
            self.docker_port_edit = QLineEdit()
            self.name_edit = QLineEdit()
            self.volume_edit_from = QLineEdit()
            self.volume_edit_to = QLineEdit()
            self.command_edit = QLineEdit()
            self.image_edit = QLineEdit()

            grid.addWidget(port, 1, 0)
            grid.addWidget(self.port_edit, 1, 1)
            grid.addWidget(self.docker_port_edit, 1, 2)

            grid.addWidget(container_name, 2, 0)
            grid.addWidget(self.name_edit, 2, 1, 1, -1)

            grid.addWidget(volume_directory, 3, 0)
            grid.addWidget(self.volume_edit_from, 3, 1)
            grid.addWidget(self.volume_edit_to, 3, 2)

            grid.addWidget(command_to_execute, 4, 0)
            grid.addWidget(self.command_edit, 4, 1, 1, -1)

            grid.addWidget(image, 5, 0)
            grid.addWidget(self.image_edit, 5, 1, 1, -1)

            btn_run = QPushButton('Run Docker', self)
            btn_run.move(130, 290)
            btn_run.resize(120, 30)
            btn_run.clicked.connect(self.run_button)

            self.list_widget = QListWidget()

            self.list_widget.itemDoubleClicked.connect(self.choose_command)

        else:
            install_message = 'Docker is not installed. ' +\
                'Click the button to install'
            install_label = QLabel(install_message)

            grid.addWidget(install_label, 1, 0)

            btn_install = QPushButton('Install', self)
            btn_install.move(130, 180)

            btn_install.clicked.connect(self.install_button)

        self.setLayout(grid)

    def run_button(self):
        name = self.name_edit.text()
        volume_from = self.volume_edit_from.text()
        volume_to = self.volume_edit_to.text()
        local_port = self.port_edit.text()
        container_port = self.docker_port_edit.text()
        image = self.image_edit.text()
        command = self.command_edit.text()
        if all([name, volume_from, volume_to, local_port, container_port, image, command]):
            docker_command = insert_docker_parameters(name,
                                                      volume_from,
                                                      volume_to,
                                                      local_port,
                                                      container_port,
                                                      image,
                                                      command)
            subprocess.call(docker_command, shell=True)
        else:
            message = QMessageBox.question(self,
                                           'Message',
                                           'Some of the fields are empty',
                                           QMessageBox.Yes)

    def install_button(self):
        subprocess.call(['wget', '/tmp/docker.sh http://get.docker.com'])
        subprocess.call(['bash', '/tmp/docker.sh'])

    def choose_command(self, docker_command):
        command_string = docker_command.text()

        name_pattern = r'--name\s(\w+)\s'
        volume_pattern = r'-v\s([a-zA-Z0-9_\/.]+):([a-zA-Z0-9_\/.]+)\s'
        port_pattern = r'-p\s(\d+):(\d+)\s'
        image_command_pattern = r'\s([a-zA-Z_.-]+:?[a-zA-Z0-9_.-]*)\s(([a-zA-Z0-9_.-]+\s?)+)$'

        name = re.search(name_pattern, command_string).group(1)

        volume_from, volume_to = re.search(volume_pattern,
                                           command_string).group(1, 2)

        local_port, container_port = re.search(port_pattern,
                                               command_string).group(1, 2)

        image, command = re.search(image_command_pattern,
                                   command_string).group(1, 2)

        self.port_edit.setText(local_port)
        self.docker_port_edit.setText(container_port)
        self.name_edit.setText(name)
        self.volume_edit_from.setText(volume_from)
        self.volume_edit_to.setText(volume_to)
        self.command_edit.setText(command)
        self.image_edit.setText(image)
