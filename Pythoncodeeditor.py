from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QTabWidget, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog, QMessageBox, QPushButton, QToolBar
from PyQt5.QtCore import QProcess
import os

class MyIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('My PyCharm-Like IDE')
        self.setGeometry(100, 100, 1200, 800)

        # Menü çubuğu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        view_menu = menubar.addMenu('View')
        help_menu = menubar.addMenu('Help')

        # Dosya gezgini
        self.file_explorer = QTreeWidget()
        self.file_explorer.setHeaderLabel('Project')
        self.file_explorer.itemDoubleClicked.connect(self.open_file)

        file_explorer_dock = QDockWidget('File Explorer', self)
        file_explorer_dock.setWidget(self.file_explorer)
        file_explorer_dock.setFloating(False)
        self.addDockWidget(3, file_explorer_dock)

        # Kod düzenleyici
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        terminal_dock = QDockWidget('Terminal', self)
        terminal_dock.setWidget(self.terminal)
        self.addDockWidget(8, terminal_dock)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Araç çubuğu
        self.tool_bar = self.addToolBar('Tools')

        # Dosya oluşturma
        new_action = QAction('New File', self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        # Dosya kaydetme
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Dosya silme
        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_file)
        file_menu.addAction(delete_action)

        # Klasör açma
        open_folder_action = QAction('Open Folder', self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        # Kodu çalıştırma
        run_action = QAction('Run', self)
        run_action.triggered.connect(self.run_code)
        self.tool_bar.addAction(run_action)

        # Görsel düzenlemeler
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #a9b7c6;
            }
            QMenuBar {
                background-color: #3c3f41;
                color: #a9b7c6;
            }
            QMenu {
                background-color: #3c3f41;
                color: #a9b7c6;
            }
            QTreeWidget {
                background-color: #313335;
                color: #a9b7c6;
            }
            QTextEdit {
                background-color: #2b2b2b;
                color: #a9b7c6;
                font-family: Consolas;
            }
            QDockWidget {
                background-color: #3c3f41;
                color: #a9b7c6;
            }
            QStatusBar {
                background-color: #3c3f41;
                color: #a9b7c6;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #a9b7c6;
            }
        """)

        self.show()

    def new_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'New File')
        if file_name:
            with open(file_name, 'w') as f:
                f.write("")
            QTreeWidgetItem(self.file_explorer.topLevelItem(0), [os.path.basename(file_name)])

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.editor.toPlainText())

    def delete_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Delete File')
        if file_name:
            os.remove(file_name)
            root = self.file_explorer.topLevelItem(0)
            for i in range(root.childCount()):
                if root.child(i).text(0) == os.path.basename(file_name):
                    root.removeChild(root.child(i))
                    break

    def open_file(self, item, column):
        file_name = item.text(0)
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f:
                self.editor.setPlainText(f.read())

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if folder_path:
            self.file_explorer.clear()
            root_item = QTreeWidgetItem(self.file_explorer, [os.path.basename(folder_path)])
            self.add_files_and_folders(root_item, folder_path)

    def add_files_and_folders(self, parent_item, folder_path):
        for item_name in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item_name)
            if os.path.isdir(item_path):
                folder_item = QTreeWidgetItem(parent_item, [item_name])
                self.add_files_and_folders(folder_item, item_path)
            else:
                QTreeWidgetItem(parent_item, [item_name])

    def run_code(self):
        current_file = self.editor.toPlainText()
        if current_file:
            self.save_file()
            self.terminal.clear()
            process = QProcess(self)
            process.setProgram("python3")
            process.setArguments([current_file])
            process.setProcessChannelMode(QProcess.MergedChannels)
            process.start()
            process.readyRead.connect(lambda: self.terminal.append(process.readAll().data().decode()))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ide = MyIDE()
    sys.exit(app.exec_())