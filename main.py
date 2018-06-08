import json
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QAction
from docker_manager import DockerManager
from docker_helpers import save_json_file, is_docker_installed, insert_docker_parameters


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.docker_manager = DockerManager(self)
        self.setCentralWidget(self.docker_manager)

        if is_docker_installed():

            menu_bar = self.menuBar()

            file_menu = menu_bar.addMenu('File')
            volume_menu = menu_bar.addMenu('Volume')

            save_action = QAction('Save', self)
            load_action = QAction('Load', self)
            volume_dir_action = QAction('Choose Folder', self)
            volume_file_action = QAction('Choose File', self)

            save_action.triggered.connect(self.save_commands)
            load_action.triggered.connect(self.load_commands)
            volume_dir_action.triggered.connect(self.volume_dir_action)
            volume_file_action.triggered.connect(self.volume_file_action)

            file_menu.addAction(save_action)
            file_menu.addAction(load_action)
            volume_menu.addAction(volume_dir_action)
            volume_menu.addAction(volume_file_action)

        self.setGeometry(300, 300, 350, 320)
        self.setWindowTitle('Docker Manager')
        self.show()

    def volume_file_action(self):
        dialog = QFileDialog()
        options = dialog.Options()
        filename, _ = dialog.getOpenFileName(self,
                                             'Choose Volume File',
                                             '',
                                             'All Files (*)',
                                             options=options)
        if filename:
            self.docker_manager.volume_edit_from.setText(filename)

    def volume_dir_action(self):
        dialog = QFileDialog()
        options = dialog.Options()
        path = dialog.getExistingDirectory(self,
                                           'Choose Volume Directory',
                                           '',
                                           options=options)
        if path:
            self.docker_manager.volume_edit_from.setText(path)

    def save_commands(self):
        docker_commands_dict = {'image': self.docker_manager.image_edit.text(),
                                'name': self.docker_manager.name_edit.text(),
                                'local_port': self.docker_manager.port_edit.text(),
                                'container_port': self.docker_manager.docker_port_edit.text(),
                                'volume_from': self.docker_manager.volume_edit_from.text(),
                                'volume_to': self.docker_manager.volume_edit_to.text(),
                                'command': self.docker_manager.command_edit.text()}
        dialog = QFileDialog()
        options = dialog.Options()
        filename, _ = dialog.getSaveFileName(self,
                                             'Save Command',
                                             '',
                                             'JSON Files (*.json)',
                                             options=options)
        if filename:
            save_json_file(filename, docker_commands_dict)

    def load_commands(self):
        dialog = QFileDialog()
        options = dialog.Options()
        filename, _ = dialog.getOpenFileName(self,
                                             'Load Command',
                                             '',
                                             'JSON Files (*.json)',
                                             options=options)
        if filename:
            with open(filename, 'r') as json_file:
                self.docker_manager.list_widget.clear()
                docker_commands = json.load(json_file)
                for docker_command in docker_commands:
                    command = insert_docker_parameters(docker_command['name'],
                                                       docker_command['volume_from'],
                                                       docker_command['volume_to'],
                                                       docker_command['local_port'],
                                                       docker_command['container_port'],
                                                       docker_command['image'],
                                                       docker_command['command'])
                    self.docker_manager.list_widget.addItem(command)
                self.docker_manager.list_widget.show()
